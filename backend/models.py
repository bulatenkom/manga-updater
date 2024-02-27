from collections import deque
from dataclasses import dataclass
from datetime import datetime
from queue import Queue
from typing import Literal
from uuid import UUID

from msgspec import Struct
    

@dataclass
class DownloadedProgress:
    # queued: int
    downloaded: int
    total: int


@dataclass
class Image:
    source_url: str
    downloaded_url: str | None = None


@dataclass
class Chapter:
    uuid: UUID
    name: str
    images: list[Image]
    source_url: str
    added_on: datetime


@dataclass
class Manga:
    uuid: UUID
    title: str
    alt_title: str
    description: str
    poster: Image
    lastChapterDate: datetime | None
    nextChapterDateEst: datetime | None  # estimated date
    avgTimeOnChapter: float  # how long user reads one chapter (this metric is used to calculate required time to read all unread chapters)
    downloadedChaptersProgress: DownloadedProgress
    downloadedImagesProgress: DownloadedProgress
    downloadedImagesSize: int # in MB
    chapters: list[Chapter]
    source_url: str

    def get_last_chapter(self) -> Chapter:
        return self.chapters[len(self.chapters)-1]

@dataclass
class Task:
    action: Literal["monitor-manga", "download-chapter-images"]
    payload: object
    status: Literal["new", "done", "failed", "running"] = "new"
    created_on: datetime = datetime.now()
    failed_on: datetime | None = None
    done_on: datetime | None = None
    failed_reason: str | None = None


class AppState(Struct):
    manga_list: list[Manga] = []
    download_deque: deque[Chapter] = deque()
    monitoring_list: list[UUID] = []
    task_queue: Queue[Task] = Queue()