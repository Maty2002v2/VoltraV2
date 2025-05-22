import { createWebHistory, createRouter } from "vue-router";

import PageDashboard from "@/pages/PageDashboard.vue";
import PageDocsLibrary from "@/pages/PageDocsLibrary.vue";
import PagePPE from "@/pages/PagePPE.vue";

const routes = [
  { path: "/", component: PageDashboard },

  //   { path: "/panel/customers", component: PageTwo },
  { path: "/panel/ppe", component: PageDashboard },
  { path: "/panel/library", component: PageDocsLibrary },
  //   { path: "/panel/raports", component: PageTwo },
  //   { path: "/panel/notifications", component: PageTwo },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
