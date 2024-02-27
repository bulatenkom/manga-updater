import asyncio
import datetime
import os
import pathlib
from statistics import mean
from contextlib import asynccontextmanager
from datetime import timedelta
from urllib.parse import urlsplit
from uuid import UUID, uuid4
from fastapi.staticfiles import StaticFiles
import httpx

import msgspec
import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import parsers
from msgspec_hooks import dec_hook, enc_hook
from db import app_state
from exceptions import AppEx
from models import AppState, Chapter, Manga, Task
from utils import build_url

structlog.configure(
    processors=[
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.THREAD_NAME,
            ]
        ),
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%b-%d %H:%M:%S.%f", utc=False),
        structlog.dev.ConsoleRenderer(),
    ]
)
log: structlog.stdlib.BoundLogger = structlog.get_logger()

client = httpx.AsyncClient()


# dispatches incoming tasks to appropriate processor queues
async def dispatcher():
    log.info("[dispatcher] started...")
    while True:
        if not app_state.task_queue.empty():
            task = app_state.task_queue.get_nowait()
            match task.action:
                case "monitor-manga":
                    app_state.monitoring_list.append(task.payload)
                case "download-chapter-images":
                    app_state.download_deque.append(task.payload)
                case _:
                    log.error(f"[dispatcher] unsupported task action '{task.action}'.")
        await asyncio.sleep(7)  # throttle 60s



# downloads chapter images
async def downloader():
    log.info("[downloader] started...")
    while True:
        if len(app_state.download_deque) != 0:
            try:
                log.info("[downloader] downloading chapter....")
                ch = app_state.download_deque.pop()
                for img in ch.images:
                    resp = await client.get(img.source_url)
                    content = await resp.aread()
                    gen_uuid = uuid4()
                    file_ext = pathlib.Path(img.source_url).suffix
                    fname = f'ch_uuid-{ch.uuid}-gen_uuid-{gen_uuid}{file_ext}'
                    with open("static/" + fname, "wb") as f:
                        f.write(content)
                    img.downloaded_url = f'/static/{fname}'
            except BaseException as ex:
                log.error(f'[downloader] error: {str(ex)}') 
        await asyncio.sleep(7)  # throttle 60s


# monitors recent manga updates
async def monitor():
    log.info("[monitor] started...")
    while True:
        if len(app_state.monitoring_list) != 0:
            log.info("[monitor] checking for manga updates...")
            try:
                for uuid in app_state.monitoring_list:
                    manga = next((m for m in app_state.manga_list if m.uuid == uuid), None)
                    if manga:
                            # determine parser
                            parse_manga_f, parse_images_f = determineParseFuncs(manga.source_url)
                            resp = await client.get(manga.source_url)
                            if resp.status_code != 200:
                                raise AppEx(
                                    f"Could not download manga's html page by url={manga.source_url} status={resp.status_code} message={resp.text}"
                                )
                            # parse manga / detect new chapters
                            recent_manga = parse_manga_f(resp.text)
                            cur_last_ch = manga.get_last_chapter()
                            new_chapters = []
                            reached_last_ch = False
                            for ch in recent_manga.chapters:
                                if ch.name == cur_last_ch.name:
                                    reached_last_ch = True
                                    continue
                                if reached_last_ch:
                                    new_chapters.append(ch)
                            if len(new_chapters) > 0:
                                log.info(f'[monitor] Spotted {len(new_chapters)} new chapters for {manga.title}')
                            # get source image urls for chapters
                            for ch in new_chapters:
                                await update_source_image_urls_for_chapter(manga.source_url, parse_images_f, ch)
                                await asyncio.sleep(0.5) # TODO increase throttle 10s
                            manga.chapters.extend(new_chapters)
                            update_stats(manga)
            except BaseException as ex:
                log.error(f'[monitor] error: {str(ex)}')
        await asyncio.sleep(300)  # throttle 60s


# syncs app's state against FS every 30 min
async def app_state_fs_syncer():
    log.info("[app_state_fs_syncer] started...")
    while True:
        await asyncio.sleep(30 * 60)  # throttle 30 min
        if len(app_state.monitoring_list) != 0:
            try:    
                log.info("[app_state_fs_syncer] syncing app's state into FS (app-state.json)")
                with open("app-state.json", "wb") as f:
                    json = msgspec.json.encode(app_state, enc_hook=enc_hook)
                    f.write(json)
            except BaseException as ex:
                log.error(f"[app_state_fs_syncer] could not sync app's state into FS (app-state.json) due to '{str(ex)}'.")



# according to asyncio docs, to prevent GCing tasks, they have to be stored as a strong-ref
# rel - https://docs.python.org/3/library/asyncio-task.html#creating-tasks
background_tasks = set()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # load app's state
    if os.path.exists("app-state.json"):
        with open("app-state.json", "rb") as f:
            global app_state
            import json
            app_state = msgspec.json.decode(f.read(), type=AppState, dec_hook=dec_hook)
    else:
        with open("app-state.json", "wb") as f:
            json = msgspec.json.encode(AppState(), enc_hook=enc_hook)
            f.write(json)

    # start background tasks
    asyncio_create_task(dispatcher())
    asyncio_create_task(monitor())
    asyncio_create_task(downloader())
    asyncio_create_task(app_state_fs_syncer())

    yield

    # persist app's state
    with open("app-state.json", "wb") as f:
        try:
            json = msgspec.json.encode(app_state, enc_hook=enc_hook)
            f.write(json)
        except BaseException as ex:
            log.error(str(ex))


def asyncio_create_task(coroutine):
    task = asyncio.create_task(coroutine)
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)


app = FastAPI(lifespan=lifespan)
pathlib.Path('static').mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(AppEx)
async def exception_handler(request: Request, ex: AppEx):
    return JSONResponse(status_code=ex.http_status, content={"message": str(ex)})


@app.get("/manga-list")
async def manga_list():
    return app_state.manga_list


def determineParseFuncs(url):
    if url == "mock":
        return (parsers.mockedParseManga18fx, parsers.mockedParseManga18fxChapterImages)

    hostname = urlsplit(url).netloc
    match hostname:
        case "manga18fx.com":
            return (parsers.parseManga18fx, parsers.parseManga18fxChapterImages)
        case "" | " " | None as v:
            raise AppEx(f"url parsed incorrectly, got {v}.")
        case _:
            raise AppEx("unsupported manga provider.")


@app.post("/parse-manga", name="Parses manga meta/data")
async def parse_manga(url):
    # check duplicate
    if url in [manga.source_url for manga in app_state.manga_list]:
        raise AppEx(f"Cannot parse already parsed manga {url}", http_status=409)
    # determine parser
    parse_manga_f, parse_images_f = determineParseFuncs(url)
    resp = await client.get(url)
    if resp.status_code != 200:
        raise AppEx(
            f"Could not download manga's html page by url={url} status={resp.status_code} message={resp.text}"
        )
    # parse manga info
    manga = parse_manga_f(resp.text)

    update_stats(manga)
    manga.source_url = url
    # get source image urls for chapters
    for ch in manga.chapters:
        await update_source_image_urls_for_chapter(url, parse_images_f, ch)
        await asyncio.sleep(0.03) # TODO increase throttle 10s
    # save manga into DB
    app_state.manga_list.append(manga)
    # add download task to queue
    app_state.task_queue.put_nowait(Task(action="monitor-manga", payload=manga.uuid))
    return manga

def update_stats(manga: Manga):
    manga.lastChapterDate = manga.get_last_chapter().added_on if len(manga.chapters) > 0 else None
    manga.nextChapterDateEst = calculateNextChapterDate(manga.chapters) if len(manga.chapters) > 1 else None

# calculates approximate next chapter date based on previous dates
def calculateNextChapterDate(chapters: list[Chapter]) -> datetime.datetime:
    timestamps = [ch.added_on.timestamp() for ch in chapters]
    if len(timestamps) > 10:
        deltas = [timestamps[i] - timestamps[i-1] for i in range(1 + len(timestamps) - 10, len(timestamps))]    
    else:
        deltas = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
    mean_delta = round(mean(deltas))
    est_date = chapters[0].added_on + timedelta(seconds=mean_delta)
    return est_date

async def update_source_image_urls_for_chapter(url, parse_images_f, ch):
    # repair source urls
    scheme, hostname, *_ = urlsplit(url)
    ch.source_url = build_url(f"{scheme}://{hostname}", ch.source_url)
    resp = await client.get(ch.source_url)
    if resp.status_code != 200:
        raise AppEx(
                f"Could not download chapter's html page by url={url} status={resp.status_code} message={resp.text}"
            )
    for img in parse_images_f(resp.text):
        ch.images.append(img)


@app.post("/download-chapter-images", name="Downloads chapter's images")
async def download_chapters(manga_uuid: UUID, chapters: set[UUID]):
    matching_manga = next((m for m in app_state.manga_list if m.uuid == manga_uuid), None)

    if matching_manga:
        chapters_to_download = [
            ch for ch in matching_manga.chapters if ch.uuid in chapters
        ]
        for ch in chapters_to_download:
            app_state.task_queue.put_nowait(Task(action="download-chapter-images", payload=ch))
    else:
        raise AppEx(f'Could not found manga with UUID={manga_uuid}', http_status=400)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
