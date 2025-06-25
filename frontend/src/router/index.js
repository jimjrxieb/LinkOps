import { createRouter, createWebHistory } from 'vue-router'

// Import all views
import Dashboard from '@/views/Dashboard.vue'
import James from '@/views/James.vue'
import Whis from '@/views/Whis.vue'
import Agents from '@/views/Agents.vue'
import Login from '@/views/Login.vue'
import About from '@/views/About.vue'
import DataCollection from '@/views/DataCollection.vue'
import Digest from '@/views/Digest.vue'
import AuditDashboard from '@/components/PwCDashboard.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard },
  { path: '/james', component: James },
  { path: '/whis', component: Whis },
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