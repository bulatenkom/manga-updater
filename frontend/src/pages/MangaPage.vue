<template>
  <q-page padding v-if="isMangaPage()">
    <div class="flex-center row">
      <div style="max-width: 900px">
        <q-card>
          <q-card-section class="row" horizontal>
            <q-img
              :src="manga.poster.downloaded_url ?? manga.poster.source_url"
              fit="none"
            />
            <div class="col-9">
              <h4>
                {{ manga.title
                }}<q-btn
                  class="float-right q-mr-md"
                  round
                  icon="settings"
                  @click="settingsDialog = true"
                />
              </h4>

              <table>
                <tr>
                  <td>Alt title:</td>
                  <td>{{ manga.alt_title }}</td>
                </tr>
                <tr>
                  <td>Description:</td>
                  <td>{{ manga.description }}</td>
                </tr>
                <tr>
                  <td>Last chapter date:</td>
                  <td>{{ manga.lastChapterDate }}</td>
                </tr>
                <tr>
                  <td>Next chapter date estimation:</td>
                  <td>{{ manga.nextChapterDateEst }}</td>
                </tr>
                <tr>
                  <td>Average time on chapter:</td>
                  <td>{{ manga.avgTimeOnChapter }}</td>
                </tr>
                <tr>
                  <td>Downloaded chapters progress:</td>
                  <td>{{ manga.downloadedChaptersProgress }}</td>
                </tr>
                <tr>
                  <td>Downloaded images progress:</td>
                  <td>{{ manga.downloadedImagesProgress }}</td>
                </tr>
                <tr>
                  <td>Downloaded images size:</td>
                  <td>{{ manga.downloadedImagesSize }}</td>
                </tr>
                <tr>
                  <td>Source url:</td>
                  <td>
                    <a :href="manga.source_url">{{ manga.source_url }}</a>
                  </td>
                </tr>
              </table>
            </div>
          </q-card-section>
          <q-separator />
          <q-card-section>
            <q-list separator>
              <q-item
                v-for="ch in manga.chapters.toReversed()"
                :key="ch.uuid"
                :to="`${$route.path}/chapters/${ch.uuid}`"
              >
                <q-item-section>
                  <q-item-label>{{ ch.name }} </q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-item-label
                    ><q-badge
                      outline
                      color="secondary"
                      label="cached"
                      v-if="isChapterCached(ch)"
                    />
                    {{ ch.added_on }}</q-item-label
                  >
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>

  <router-view :key="$route.fullPath"></router-view>

  <q-dialog v-model="settingsDialog">
    <q-card style="min-width: 550px">
      <q-card-section>
        <div class="text-h6">Settings</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <q-card-section>
          <p class="text-h5 text-blue-6">Cache</p>
          <q-list separator>
            <q-item v-for="ch in manga.chapters.toReversed()" :key="ch.uuid">
              <q-item-section avatar>
                <q-checkbox v-model="cacheSelection" :val="ch" color="teal" />
              </q-item-section>
              <q-item-section>
                <q-item-label>{{ ch.name }} </q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-item-label
                  ><q-badge
                    outline
                    color="secondary"
                    label="cached"
                    v-if="isChapterCached(ch)"
                  />
                  {{ ch.added_on }}</q-item-label
                >
              </q-item-section>
            </q-item>
          </q-list>
        </q-card-section>
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="Cancel" v-close-popup />
        <q-btn flat label="Save" @click="saveSettings" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { useQuasar } from 'quasar';
import { downloadChapterImages } from 'src/api/api';
import { getChapter } from 'src/shared/funcs';
import { store } from 'src/store/store';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const $q = useQuasar();

const route = useRoute();

const manga = store.mangaMap[route.params['manga_uuid']];

const settingsDialog = ref(false);
const saveSettingsLoading = ref(false);
const cacheSelection = ref(getCachedChaptersCopy());

function getCachedChaptersCopy() {
  return manga.chapters.filter((ch) => isChapterCached(ch)).slice();
}

function isMangaPage() {
  return route.meta.uuidName === 'manga_uuid';
}

function isChapterCached(ch) {
  for (let img of ch.images) {
    if (!img.downloaded_url) return false;
  }
  return true;
}

async function saveSettings() {
  saveSettingsLoading.value = true;
  try {
    let selected = cacheSelection.value.map((ch) => ch.uuid);
    let selectedNew = selectNew(
      getCachedChaptersCopy().map((ch) => ch.uuid),
      selected,
    );
    await downloadChapterImages(manga.uuid, selectedNew);
  } catch (e) {
    $q.notify({ type: 'negative', message: e.toString() });
  } finally {
    saveSettingsLoading.value = false;
  }
}

function selectNew(cached, selection) {
  let res = [];
  for (let uuid of selection) {
    if (!cached.includes(uuid)) res.push(uuid);
  }
  return res;
}
</script>
