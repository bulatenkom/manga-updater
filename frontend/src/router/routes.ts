import { RouteRecordRaw } from 'vue-router';

// Seems Vue Router has no option to render childs without parent
// There is discussion about workarounds https://github.com/vuejs/vue-router/issues/2105
// None of solution is straight in my opinion.
// So, let's write a boilerplate, then...
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: () => import('layouts/RootLayout.vue'),
    redirect: '/manga-list',
    children: [
      {
        path: 'manga-list',
        component: () => import('pages/MangaListPage.vue'),
      },
      {
        path: 'manga-list/:manga_uuid',
        component: () => import('pages/MangaPage.vue'),
        meta: { uuidName: 'manga_uuid' },
        children: [
          {
            path: 'chapters/:chapter_uuid',
            component: () => import('pages/ChapterPage.vue'),
            meta: {
              uuidName: 'chapter_uuid',
              customToolbar: () => import('pages/ChapterPageToolbar.vue'),
            },
          },
        ],
      },
    ],
  },
  // {
  //   path: '/',
  //   component: () => import('layouts/RootLayout.vue'),
  //   redirect: '/manga-list',
  //   children: [
  //     {
  //       path: 'manga-list',
  //       component: () => import('pages/MangaListPage.vue'),
  //     },
  //     {
  //       path: 'manga-list/:manga_uuid',
  //       component: () => import('pages/MangaPage.vue'),
  //       meta: { uuidName: 'manga_uuid' },
  //     },
  //     {
  //       path: 'manga-list/:manga_uuid/chapters/:chapter_uuid',
  //       component: () => import('pages/ChapterPage.vue'),
  //       meta: {
  //         uuidName: 'chapter_uuid',
  //         customToolbar: () => import('pages/ChapterPageToolbar.vue'),
  //       },
  //     },
  //   ],
  // },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
