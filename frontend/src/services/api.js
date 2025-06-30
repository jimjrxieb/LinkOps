import axios from 'axios'

// Create axios instance with default config
const api = axios.create({
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Environment-based API URLs
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const WHIS_URL = import.meta.env.VITE_WHIS_URL || 'http://localhost:8001'
const JAMES_URL = import.meta.env.VITE_JAMES_URL || 'http://localhost:8002'
const SANITIZER_URL = import.meta.env.VITE_SANITIZER_URL || 'http://localhost:8003'
const DATA_COLLECTOR_URL = import.meta.env.VITE_DATA_COLLECTOR_URL || 'http://localhost:8004'
const IGRIS_URL = import.meta.env.VITE_IGRIS_URL || 'http://localhost:8005'
const KATIE_URL = import.meta.env.VITE_KATIE_URL || 'http://localhost:8006'
const FICKNURY_URL = import.meta.env.VITE_FICKNURY_URL || 'http://localhost:8007'
const AUDITGUARD_URL = import.meta.env.VITE_AUDITGUARD_URL || 'http://localhost:8008'
const WEBSCRAPER_URL = import.meta.env.VITE_WEBSCRAPER_URL || 'http://localhost:8009'

// API Services
export const backendAPI = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

export const whisAPI = axios.create({
  baseURL: WHIS_URL,
  timeout: 15000,
})

export const jamesAPI = axios.create({
  baseURL: JAMES_URL,
  timeout: 30000,
})

export const sanitizerAPI = axios.create({
  baseURL: SANITIZER_URL,
  timeout: 10000,
})

export const dataCollectorAPI = axios.create({
  baseURL: DATA_COLLECTOR_URL,
  timeout: 10000,
})

export const igrisAPI = axios.create({
  baseURL: IGRIS_URL,
  timeout: 20000,
})

export const katieAPI = axios.create({
  baseURL: KATIE_URL,
  timeout: 15000,
})

export const ficknuryAPI = axios.create({
  baseURL: FICKNURY_URL,
  timeout: 15000,
})

export const auditguardAPI = axios.create({
  baseURL: AUDITGUARD_URL,
  timeout: 10000,
})

export const webscraperAPI = axios.create({
  baseURL: WEBSCRAPER_URL,
  timeout: 20000,
})

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message)
    
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Handle unauthorized
      console.log('Unauthorized access, redirecting to login')
    } else if (error.response?.status === 503) {
      // Handle service unavailable
      console.log('Service temporarily unavailable')
    }
    
    return Promise.reject(error)
  }
)

// Health check functions
export const healthChecks = {
  backend: () => backendAPI.get('/health'),
  whis: () => whisAPI.get('/health'),
  james: () => jamesAPI.get('/health'),
  sanitizer: () => sanitizerAPI.get('/health'),
  dataCollector: () => dataCollectorAPI.get('/health'),
  igris: () => igrisAPI.get('/health'),
  katie: () => katieAPI.get('/health'),
  ficknury: () => ficknuryAPI.get('/health'),
  auditguard: () => auditguardAPI.get('/health'),
  webscraper: () => webscraperAPI.get('/health'),
}

// James API functions
export const jamesService = {
  activateShadowArmy: () => jamesAPI.post('/api/james/activate'),
  submitTask: (taskData) => jamesAPI.post('/api/james/task', taskData),
  askQuestion: (question) => jamesAPI.post('/api/james/qa', { question }),
  submitInfoDump: (data) => jamesAPI.post('/api/james/info-dump', data),
  extractFromImage: (imageData) => jamesAPI.post('/api/james/image-extract', imageData),
  generateSolution: (problemData) => jamesAPI.post('/api/james/solution', problemData),
  voiceInteraction: (audioData) => jamesAPI.post('/api/james/voice', audioData),
  describeImage: (imageData) => jamesAPI.post('/api/james/describe-image', imageData),
}

// Whis API functions
export const whisService = {
  getTrainingQueue: () => whisAPI.get('/api/whis/training-queue'),
  getDigest: (date) => whisAPI.get(`/api/whis/digest?date=${date}`),
  getApprovalQueue: () => whisAPI.get('/api/whis/approval-queue'),
  approveItem: (type, id) => whisAPI.post(`/api/whis/approve/${type}/${id}`),
  rejectItem: (type, id) => whisAPI.post(`/api/whis/reject/${type}/${id}`),
  getAnalytics: () => whisAPI.get('/api/whis/analytics'),
  generateOrbs: (data) => whisAPI.post('/api/whis/generate-orbs', data),
  generateRunes: (data) => whisAPI.post('/api/whis/generate-runes', data),
  getSmithingLog: () => whisAPI.get('/api/whis/smithing-log'),
}

// Igris API functions
export const igrisService = {
  getInfrastructureStatus: () => igrisAPI.get('/api/igris/infrastructure'),
  analyzeCosts: () => igrisAPI.get('/api/igris/cost-analysis'),
  getSecurityAudit: () => igrisAPI.get('/api/igris/security-audit'),
  deployInfrastructure: (config) => igrisAPI.post('/api/igris/deploy', config),
  getCapabilities: () => igrisAPI.get('/api/igris/capabilities'),
  getEnhancedRunes: () => igrisAPI.get('/api/igris/enhanced-runes'),
  runSimulation: (params) => igrisAPI.post('/api/igris/simulation', params),
  getAgentStats: () => igrisAPI.get('/api/igris/agent-stats'),
}

// Katie API functions
export const katieService = {
  getKubernetesStatus: () => katieAPI.get('/api/katie/kubernetes'),
  getTasksHandled: () => katieAPI.get('/api/katie/tasks'),
  getYAMLVisualizer: () => katieAPI.get('/api/katie/yaml-visualizer'),
  getAgentLogicTree: () => katieAPI.get('/api/katie/agent-logic'),
  getHelmCharts: () => katieAPI.get('/api/katie/helm-charts'),
  getTroubleshootingLog: () => katieAPI.get('/api/katie/troubleshooting'),
  scaleDeployment: (params) => katieAPI.post('/api/katie/scale', params),
  describeResource: (params) => katieAPI.post('/api/katie/describe', params),
  getLogs: (params) => katieAPI.get('/api/katie/logs', { params }),
  patchResource: (params) => katieAPI.post('/api/katie/patch', params),
}

// Ficknury API functions
export const ficknuryService = {
  getIncomingTasks: () => ficknuryAPI.get('/api/ficknury/incoming-tasks'),
  getFeasibilityRanking: () => ficknuryAPI.get('/api/ficknury/feasibility'),
  getAgentAssignmentStats: () => ficknuryAPI.get('/api/ficknury/agent-stats'),
  getDecisionMatrix: () => ficknuryAPI.get('/api/ficknury/decision-matrix'),
  getProcessingQueue: () => ficknuryAPI.get('/api/ficknury/processing-queue'),
  getFallbackAnalysis: () => ficknuryAPI.get('/api/ficknury/fallback-analysis'),
  evaluateTask: (taskData) => ficknuryAPI.post('/api/ficknury/evaluate', taskData),
  routeTask: (taskData) => ficknuryAPI.post('/api/ficknury/route', taskData),
}

// Data Collector API functions
export const dataCollectorService = {
  collectData: (data) => dataCollectorAPI.post('/api/collect', data),
  getCollectionStats: () => dataCollectorAPI.get('/api/stats'),
  submitYouTubeData: (url) => dataCollectorAPI.post('/api/youtube', { url }),
  submitManualTask: (taskData) => dataCollectorAPI.post('/api/manual-task', taskData),
}

// Sanitizer API functions
export const sanitizerService = {
  sanitizeData: (data) => sanitizerAPI.post('/api/sanitize', data),
  getSanitizationStats: () => sanitizerAPI.get('/api/stats'),
  getDataLake: () => sanitizerAPI.get('/api/data-lake'),
  getSanitizedInputs: () => sanitizerAPI.get('/api/sanitized-inputs'),
}

// AuditGuard API functions
export const auditguardService = {
  getAuditLogs: () => auditguardAPI.get('/api/audit/logs'),
  getComplianceStatus: () => auditguardAPI.get('/api/audit/compliance'),
  getSecurityAlerts: () => auditguardAPI.get('/api/audit/security'),
  runSecurityScan: () => auditguardAPI.post('/api/audit/security-scan'),
}

// WebScraper API functions
export const webscraperService = {
  scrapeWebsite: (url) => webscraperAPI.post('/api/scrape', { url }),
  getScrapingAgents: () => webscraperAPI.get('/api/agents'),
  getOrbsRunes: () => webscraperAPI.get('/api/orbs-runes'),
  getScrapingLogs: () => webscraperAPI.get('/api/logs'),
  reloopScraping: (params) => webscraperAPI.post('/api/reloop', params),
}

// Backend API functions
export const backendService = {
  getSystemStatus: () => backendAPI.get('/api/status'),
  getDashboardData: () => backendAPI.get('/api/dashboard'),
  getLogs: (params) => backendAPI.get('/api/logs', { params }),
  getAgentStatus: () => backendAPI.get('/api/agents/status'),
  getSystemMetrics: () => backendAPI.get('/api/metrics'),
  getLearningEvents: () => backendAPI.get('/api/learning-events'),
  getDataFlowMap: () => backendAPI.get('/api/data-flow'),
}

// Utility functions
export const apiUtils = {
  // Check if all services are healthy
  checkAllServices: async () => {
    const checks = await Promise.allSettled([
      healthChecks.backend(),
      healthChecks.whis(),
      healthChecks.james(),
      healthChecks.sanitizer(),
      healthChecks.dataCollector(),
      healthChecks.igris(),
      healthChecks.katie(),
      healthChecks.ficknury(),
      healthChecks.auditguard(),
      healthChecks.webscraper(),
    ])
    
    return {
      backend: checks[0].status === 'fulfilled',
      whis: checks[1].status === 'fulfilled',
      james: checks[2].status === 'fulfilled',
      sanitizer: checks[3].status === 'fulfilled',
      dataCollector: checks[4].status === 'fulfilled',
      igris: checks[5].status === 'fulfilled',
      katie: checks[6].status === 'fulfilled',
      ficknury: checks[7].status === 'fulfilled',
      auditguard: checks[8].status === 'fulfilled',
      webscraper: checks[9].status === 'fulfilled',
    }
  },
  
  // Retry function for failed requests
  retry: async (fn, retries = 3, delay = 1000) => {
    try {
      return await fn()
    } catch (error) {
      if (retries > 0) {
        await new Promise(resolve => setTimeout(resolve, delay))
        return apiUtils.retry(fn, retries - 1, delay * 2)
      }
      throw error
    }
  },
}

export default api 