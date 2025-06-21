import { createRouter, createWebHistory } from 'vue-router'
import JamesTab from './agents/JamesTab.vue'
import WhisTab from './agents/WhisTab.vue'
import MemoryTab from './agents/MemoryTab.vue'

const routes = [
  { path: '/', redirect: '/james' },
  { path: '/james', component: JamesTab },
  { path: '/whis', component: WhisTab },
  { path: '/memory', component: MemoryTab },
  // You'll add Katie and Igris later
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 