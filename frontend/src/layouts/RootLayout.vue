<template>
  <q-layout view="hHh Lpr fFf">
    <q-header reveal elevated>
      <q-toolbar>
        <q-btn flat round dense icon="menu" @click="leftDrawer = !leftDrawer" />
        <q-toolbar-title> {{ useRoute().fullPath }}</q-toolbar-title>
        <div v-if="$route.meta.customToolbar">
          <component :is="customToolbarViewer" :props="customToolbarProps" />
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawer"
      side="left"
      bordered
      content-class="bg-grey-2"
    >
      <q-scroll-area class="fit q-pa-sm"> </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <app-breadcrumbs />
      <suspense>
        <router-view />
        <template #fallback> Loading... </template>
      </suspense>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import AppBreadcrumbs from 'components/AppBreadcrumbs.vue';
import { getMangaList } from 'src/api/api';
import { customToolbarProps } from 'src/store/global-state';
import { store } from 'src/store/store';
import { toObject } from 'src/util/util';
import { onMounted, ref, shallowRef, watch } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const leftDrawer = ref(false);
const customToolbarViewer = shallowRef();

const mangaList = await getMangaList();
store.mangaMap = toObject(mangaList.value);

watch(
  () => route.path,
  (newVal, oldVal) => {
    initCustomToolbar();
  },
);

function initCustomToolbar() {
  if (route.meta.customToolbar) {
    route.meta
      .customToolbar()
      .then((mod) => (customToolbarViewer.value = mod.default));
  } else {
    customToolbarViewer.value = null;
  }
}

onMounted(() => {
  console.log('RootLayout component mounted');
  initCustomToolbar();
});
</script>
