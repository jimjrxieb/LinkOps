import { createRouter, createWebHistory } from 'vue-router'
import JamesPage from '@/views/JamesPage.vue'
import WhisPage from '@/views/WhisPage.vue'
import AgentsPage from '@/views/AgentsPage.vue'
import Dashboard from '@/views/Dashboard.vue'

const routes = [
  { path: '/', redirect: '/james' },
  { path: '/james', component: JamesPage },
  { path: '/whis', component: WhisPage },
  { path: '/agents', component: AgentsPage },
  { path: '/dashboard', component: Dashboard }
]

export default createRouter({
  history: createWebHistory(),
  routes
}) 