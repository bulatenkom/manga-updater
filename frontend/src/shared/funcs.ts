export function getChapter(manga, chapterUuid) {
  for (const ch of manga.chapters) {
    if (ch.uuid === chapterUuid) return ch;
  }
}
