import { createRouter, createWebHistory } from 'vue-router'

// NEW PAGES
import Dashboard from '@/views/Dashboard.vue'
import DataCollection from '@/views/DataCollection.vue'
import WhisPage from '@/views/WhisPage.vue'
import AgentsPage from '@/views/AgentsPage.vue'
import Digest from '@/views/Digest.vue'
import AuditDashboard from '@/components/PwCDashboard.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard },
  { path: '/audit-dashboard', component: AuditDashboard },
  { path: '/data-collection', component: DataCollection },
  { path: '/whis', component: WhisPage },
  { path: '/agents', component: AgentsPage },
  { path: '/digest', component: Digest },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 