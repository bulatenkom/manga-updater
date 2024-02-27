<template>
  <div class="q-pa-md q-gutter-sm">
    <q-breadcrumbs>
      <q-breadcrumbs-el
        v-for="(r, idx) in routes"
        :key="r.url"
        :label="selectLabel(r.label)"
        :to="r.url"
        :icon="selectIcon(r.label)"
        :disable="idx == routes.length - 1"
      />
    </q-breadcrumbs>
  </div>
</template>

<script setup lang="ts">
import { store } from 'src/store/store';
import { ref, watchEffect } from 'vue';
import { RouteLocationNormalizedLoaded, useRoute } from 'vue-router';
import { getChapter } from 'src/shared/funcs';

const route = useRoute();

let routes = ref<string[]>([]);
store.routes = routes;

watchEffect(() => {
  routes.value = normalize(route);
});

function selectIcon(route: string) {
  if (isHome(route)) return 'home';
}

function selectLabel(route: string) {
  if (isHome(route)) return 'Home';
  return route;
}

function isHome(route: string) {
  return route == '/' || route == '/manga-list';
}

function normalize(route: RouteLocationNormalizedLoaded) {
  let normalized = route.matched.map((rt) => {
    let resolvedUrl = resolveUrl(rt, route);
    try {
      if (rt.meta?.uuidName) {
        switch (rt.meta.uuidName) {
          case 'manga_uuid':
            return {
              label: store.mangaMap[route.params['manga_uuid']].title,
              url: resolvedUrl,
            };
          case 'chapter_uuid':
            return {
              label: getChapter(
                store.mangaMap[route.params['manga_uuid']],
                route.params['chapter_uuid'],
              ).name,
              url: resolvedUrl,
            };
        }
      }
    } catch (ex) {
      console.error(ex);
    }
    return {
      label: rt.path,
      url: resolvedUrl,
    };
  });

  if (isHome(normalized[0].url) && isHome(normalized[1].url)) {
    return normalized.slice(1);
  }
  return normalized;
}

function resolveUrl(rt, route) {
  let rawUrl: string = rt.path;

  if (route.params === null || route.params === undefined) return rawUrl;

  for (let [k, v] of Object.entries(route.params)) {
    rawUrl = rawUrl.replace(`:${k}`, v);
  }
  return rawUrl;
}
</script>
