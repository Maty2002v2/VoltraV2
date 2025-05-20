import { createWebHistory, createRouter } from "vue-router";

import PageHome from "@/pages/PageHome.vue";
import PageDocsLibrary from "@/pages/PageDocsLibrary.vue";
import PagePPE from "@/pages/PagePPE.vue";

const routes = [
  { path: "/", component: PageHome },

  //   { path: "/panel/customers", component: PageTwo },
  { path: "/panel/ppe", component: PageDocsLibrary },
  { path: "/panel/library", component: PagePPE },
  //   { path: "/panel/raports", component: PageTwo },
  //   { path: "/panel/notifications", component: PageTwo },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
