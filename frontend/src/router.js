import { createRouter, createWebHashHistory } from "vue-router";
import HelloWorld from "./components/HelloWorld.vue";
import GridGenerator from "./components/GridGenerator.vue";

const routes = [
  { path: "/", redirect: "/grid" }, // Default landing page
  { path: "/grid", component: GridGenerator },
  { path: "/hello", component: HelloWorld },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
