import { createRouter, createWebHistory } from 'vue-router';
import HomeView from './components/HomeView.vue';
import AnalyticsView from './components/AnalyticsView.vue';
import AddNoteView from './components/AddNoteView.vue';
import EditNoteView from './components/EditNoteView.vue';

const routes = [
  { path: '/', component: HomeView },
  { path: '/analytics', component: AnalyticsView },
  { path: '/add_note', component: AddNoteView },
  { path: '/edit_note/:id', component: EditNoteView },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
