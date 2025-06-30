import { createRouter, createWebHistory } from 'vue-router'

// Import all views
import Dashboard from '@/views/Dashboard.vue'
import Tasks from '@/views/Tasks.vue'
import Whis from '@/views/Whis.vue'
import Igris from '@/views/Igris.vue'
import Katie from '@/views/Katie.vue'
import Ficknury from '@/views/Ficknury.vue'
import Agents from '@/views/Agents.vue'
import Login from '@/views/Login.vue'
import About from '@/views/About.vue'
import ArisePage from '@/views/ArisePage.vue'
import DataCollection from '@/views/DataCollection.vue'
import Digest from '@/views/Digest.vue'
import AuditDashboard from '@/components/PwCDashboard.vue'

const routes = [
  { path: '/', redirect: '/arise' },
  { path: '/arise', component: ArisePage },
  { path: '/dashboard', component: Dashboard },
  { path: '/tasks', component: Tasks },
  { path: '/whis', component: Whis },
  { path: '/igris', component: Igris },
  { path: '/katie', component: Katie },
  { path: '/ficknury', component: Ficknury },
  { path: '/agents', component: Agents },
  { path: '/login', component: Login },
  { path: '/about', component: About },
  { path: '/audit-dashboard', component: AuditDashboard },
  { path: '/data-collection', component: DataCollection },
  { path: '/digest', component: Digest },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 