<template>
  <q-page padding>
    <div class="q-pa-md row">
      <q-space></q-space>
      <q-btn icon="add_circle_outline" color="accent" @click="prompt = true"
        >Add manga</q-btn
      >
    </div>

    <q-dialog v-model="prompt" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">Manga url</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input
            hint="E.g. https://manga18fx.com/manga/academys-genius-swordsman"
            dense
            v-model="mangaUrl"
            autofocus
            @keyup.enter="prompt = false"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn
            flat
            label="Add"
            @click="addManga"
            :loading="addMangaLoading"
          ></q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>

    <div class="q-gutter-md row items-start justify-start content-start">
      <q-card
        class="hovering-card pointer"
        v-for="manga in mangaList"
        :key="manga.uuid"
        style="max-width: 250px"
        @click="$router.push(`${$route.path}/${manga.uuid}`)"
      >
        <q-img
          height="325px"
          width="250px"
          :src="manga.poster.downloaded_url ?? manga.poster.source_url"
        ></q-img>
        <!-- <img /> -->
        <q-card-section>
          <p class="ellipsis no-margin text-h6">{{ manga.title }}</p>
        </q-card-section>
        <q-btn color="grey-3" text-color="grey-8" class="fit">Read</q-btn>
      </q-card>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { getMangaList, addManga as addMangaEndpoint } from 'src/api/api';
import { store } from 'src/store/store';
import { toObject } from 'src/util/util';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const $q = useQuasar();

const mangaList = await getMangaList();
store.mangaMap = toObject(mangaList.value);

const prompt = ref(false);
const mangaUrl = ref(null);
const addMangaLoading = ref(false);

async function addManga() {
  addMangaLoading.value = true;
  try {
    await addMangaEndpoint(mangaUrl.value);
  } catch (e) {
    $q.notify({ type: 'negative', message: e.toString() });
  } finally {
    addMangaLoading.value = false;
  }
}

onMounted(() => {
  console.log('MangaListPage component mounted');
});
</script>

<style scoped>
.hovering-card:hover {
  transition: filter 125ms ease;
  filter: drop-shadow(0 -1px 2px #3a3a3a);
}
.pointer {
  cursor: pointer;
}
</style>
