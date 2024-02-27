<template>
  <q-page class="row">
    <q-card v-for="manga in mangaList" :key="manga.uuid">
      <img :src="manga.poster.source_url" />
      <q-card-section>
        <p class="text-h6">{{ manga.title }}</p>
      </q-card-section>
    </q-card>

    <pre class="">
      {{ mangaList }}
    </pre>
  </q-page>
</template>

<script setup lang="ts">
import { useFetch } from '@vueuse/core';

const PROXY = 'http://localhost:7777';
const BACKEND = 'http://localhost:8000';
const BASE_URL = `${PROXY}/${BACKEND}`;
const { data: mangaList } = await useFetch(`${BASE_URL}/manga-list`)
  .get()
  .json();
</script>
