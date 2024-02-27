<template>
  <q-page padding>
    <h2 class="text-center">{{ chapter.name }}</h2>
    <q-img
      v-for="(img, idx) in chapter.images"
      :key="idx"
      :src="selectSource(img)"
      placeholder-src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWBAMAAADOL2zRAAAAG1BMVEXMzMyWlpaqqqq3t7fFxcW+vr6xsbGjo6OcnJyLKnDGAAAACXBIWXMAAA7EAAAOxAGVKw4bAAABAElEQVRoge3SMW+DMBiE4YsxJqMJtHOTITPeOsLQnaodGImEUMZEkZhRUqn92f0MaTubtfeMh/QGHANEREREREREREREtIJJ0xbH299kp8l8FaGtLdTQ19HjofxZlJ0m1+eBKZcikd9PWtXC5DoDotRO04B9YOvFIXmXLy2jEbiqE6Df7DTleA5socLqvEFVxtJyrpZFWz/pHM2CVte0lS8g2eDe6prOyqPglhzROL+Xye4tmT4WvRcQ2/m81p+/rdguOi8Hc5L/8Qk4vhZzy08DduGt9eVQyP2qoTM1zi0/uf4hvBWf5c77e69Gf798y08L7j0RERERERERERH9P99ZpSVRivB/rgAAAABJRU5ErkJggg=="
      @error="
        $q.notify({
          type: 'negative',
          message: `Failed to load ${selectSource(img)}`,
        })
      "
    />
  </q-page>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { getChapter } from 'src/shared/funcs';
import { customToolbarProps } from 'src/store/global-state';
import { store } from 'src/store/store';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';

const $q = useQuasar();

const route = useRoute();

const manga = store.mangaMap[route.params['manga_uuid']];
const chapter = getChapter(manga, route.params['chapter_uuid']);

onMounted(() => {
  console.log('ChapterPage component mounted');

  const { next, prev } = findAdjacentChapters(manga.chapters, chapter);
  let nextChapter, prevChapter;
  if (next) {
    nextChapter = `/manga-list/${manga.uuid}/chapters/${next.uuid}`;
  }
  if (prev) {
    prevChapter = `/manga-list/${manga.uuid}/chapters/${prev.uuid}`;
  }
  customToolbarProps.value = {
    toManga: store.routes[1].url,
    nextChapter,
    prevChapter,
  };
});

function selectSource(img) {
  if (img.downloaded_url) return img.downloaded_url;
  return img.source_url;
}

function findAdjacentChapters(chlist, ch) {
  let next = null,
    prev = null;
  if (chlist.length <= 1) return { next, prev };

  for (let i = 0; i < chlist.length; i++) {
    if (chlist[i].uuid === ch.uuid) {
      try {
        next = chlist[i + 1];
        prev = chlist[i - 1];
      } catch (e) {}
      break;
    }
  }

  return { next, prev };
}
</script>
