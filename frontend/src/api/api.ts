import { useFetch } from '@vueuse/core';
import { stringify } from 'querystring';

const PROXY = 'http://localhost:7777';
const BACKEND = 'http://localhost:8000';
const BASE_URL = `${PROXY}/${BACKEND}`;

export async function getMangaList() {
  const { data: mangaList } = await useFetch<unknown[]>(
    `${BASE_URL}/manga-list`,
  )
    .get()
    .json();
  return mangaList;
}

export async function addManga(url: string) {
  if (!url) {
    throw Error('URL is required');
  }

  const response = await fetch(`${BASE_URL}/parse-manga?url=${url}`, {
    method: 'POST',
  });

  // const { data, statusCode, error, response, text, json } =
  //   await useFetch<unknown>(`${BASE_URL}/parse-manga?url=${url}`).post().json();

  if (response.status != 200) {
    throw new Error(`${await response.text()}`);
  }
  return await response.json();
}

export async function downloadChapterImages(
  manga_uuid: string,
  chapters_uuids: string[],
) {
  if (!manga_uuid || !chapters_uuids) {
    throw Error('URL is required');
  }
  await (
    await fetch(
      `${BASE_URL}/download-chapter-images?manga_uuid=${manga_uuid}`,
      {
        method: 'POST',
        body: JSON.stringify(chapters_uuids),
        headers: { 'Content-Type': 'application/json' },
      },
    )
  ).json();
}
