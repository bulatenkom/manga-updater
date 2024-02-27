from datetime import datetime, timedelta
import math
from statistics import mean
from uuid import uuid4
from bs4 import BeautifulSoup
from models import Chapter, DownloadedProgress, Image, Manga


def parseManga18fx(body) -> Manga:
    soup = BeautifulSoup(body, 'html.parser')

    chapters: list[Chapter] = []
    for atag in soup.select('#chapterlist > ul > li > a'):
        ch_url = atag['href']

        ch_name = atag.get_text(strip=True) # type: ignore

        ch_added_on_tag = atag.find_next()
        if ch_added_on_tag is not None:
            if ch_added_on_tag.name == 'span' and 'chapter-time' in ch_added_on_tag.get('class', []):
                ch_added_on = atag.find_next().string.strip() # type: ignore
                ch_added_on = datetime.strptime(ch_added_on, '%d %b %y')
            else:
                ch_added_on = datetime.now()

        chapters.append(Chapter(
            uuid=uuid4(),
            name=ch_name,
            images=[],
            source_url=ch_url, # type: ignore
            added_on=ch_added_on # type: ignore
        ))
    chapters = list(reversed(chapters))

    return Manga(
        uuid=uuid4(),
        title=soup.select_one('body > div.manga-content > div.profile-manga > div > div.post-title > h1').get_text(strip=True), # type: ignore
        alt_title=soup.select_one('body > div.manga-content > div.profile-manga > div > div.tab-summary > div.summary_content_wrap > div > div.post-content > div:nth-child(2) > div.summary-content').get_text(strip=True), # type: ignore
        description=soup.select_one('body > div.manga-content > div.centernav > div > div.content-manga-left > div.panel-story-description > div').get_text(strip=True), # type: ignore
        poster=Image(source_url=soup.select_one('body > div.manga-content > div.profile-manga > div > div.tab-summary > div.summary_image > a > img')['src']), # type: ignore
        lastChapterDate=None,
        nextChapterDateEst=None,
        avgTimeOnChapter=0.0, # TODO: 
        downloadedChaptersProgress=DownloadedProgress(0, len(chapters)), # TODO
        downloadedImagesProgress=DownloadedProgress(0,0), # TODO
        downloadedImagesSize=0, # TODO
        chapters=chapters,
        source_url=""
    )

def parseManga18fxChapterImages(body) -> list[Image]:
    soup = BeautifulSoup(body, 'html.parser')
    images = []
    for imgtag in soup.select('body > div.manga-content > div > div > div > div > div.read-content > div > img'):
        images.append(
            Image(source_url=imgtag['src']) # type: ignore
        )
    return images

def mockHtmlForManga18fx():
    with open('body-bind-page.html', 'r') as f:
        return f.read()


def mockChapterHtmlForManga18fx():
    with open('body-bind-ch37-page.html', 'r') as f:
        return f.read()


def mockedParseManga18fx(body) -> Manga:
    return parseManga18fx(mockHtmlForManga18fx())


def mockedParseManga18fxChapterImages(body) -> list[Image]:
    return parseManga18fxChapterImages(mockChapterHtmlForManga18fx())