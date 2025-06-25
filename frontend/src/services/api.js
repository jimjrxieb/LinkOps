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
}

// James API functions
export const jamesService = {
  submitTask: (taskData) => jamesAPI.post('/api/james/task', taskData),
  askQuestion: (question) => jamesAPI.post('/api/james/qa', { question }),
  submitInfoDump: (data) => jamesAPI.post('/api/james/info-dump', data),
  extractFromImage: (imageData) => jamesAPI.post('/api/james/image-extract', imageData),
  generateSolution: (problemData) => jamesAPI.post('/api/james/solution', problemData),
}

// Whis API functions
export const whisService = {
  getTrainingQueue: () => whisAPI.get('/api/whis/training-queue'),
  getDigest: (date) => whisAPI.get(`/api/whis/digest?date=${date}`),
  getApprovalQueue: () => whisAPI.get('/api/whis/approval-queue'),
  approveItem: (type, id) => whisAPI.post(`/api/whis/approve/${type}/${id}`),
  rejectItem: (type, id) => whisAPI.post(`/api/whis/reject/${type}/${id}`),
  getAnalytics: () => whisAPI.get('/api/whis/analytics'),
}

// Data Collector API functions
export const dataCollectorService = {
  collectData: (data) => dataCollectorAPI.post('/api/collect', data),
  getCollectionStats: () => dataCollectorAPI.get('/api/stats'),
}

// Sanitizer API functions
export const sanitizerService = {
  sanitizeData: (data) => sanitizerAPI.post('/api/sanitize', data),
  getSanitizationStats: () => sanitizerAPI.get('/api/stats'),
}

// Backend API functions
export const backendService = {
  getSystemStatus: () => backendAPI.get('/api/status'),
  getDashboardData: () => backendAPI.get('/api/dashboard'),
  getLogs: (params) => backendAPI.get('/api/logs', { params }),
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
    ])
    
    return {
      backend: checks[0].status === 'fulfilled',
      whis: checks[1].status === 'fulfilled',
      james: checks[2].status === 'fulfilled',
      sanitizer: checks[3].status === 'fulfilled',
      dataCollector: checks[4].status === 'fulfilled',
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