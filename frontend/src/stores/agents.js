import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAgentsStore = defineStore('agents', () => {
  // State
  const tasks = ref([])
  const logs = ref([])
  const queueStatus = ref({})
  const approvals = ref([])
  const digest = ref({})
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const recentTasks = computed(() => tasks.value.slice(0, 10))
  const pendingApprovals = computed(() => approvals.value.filter(a => a.is_flagged))
  const systemHealth = computed(() => {
    const hasErrors = error.value !== null
    const hasPending = pendingApprovals.value.length > 0
    return {
      status: hasErrors ? 'error' : hasPending ? 'warning' : 'healthy',
      message: hasErrors ? 'System errors detected' : hasPending ? 'Pending approvals' : 'All systems operational'
    }
  })

  // Actions
  const submitTask = async (taskData) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/james/evaluate', taskData)
      tasks.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const completeWithJames = async (taskId) => {
    try {
      const response = await axios.post('/api/tasks/complete-with-james', { task_id: taskId })
      await loadLogs()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    }
  }

  const sendToAgent = async (taskId, agent) => {
    try {
      const response = await axios.post('/api/tasks/send-to-agent', null, {
        params: { task_id: taskId, agent }
      })
      await loadLogs()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    }
  }

  const loadQueueStatus = async () => {
    try {
      const response = await axios.get('/api/whis/queue')
      queueStatus.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    }
  }

  const loadApprovals = async () => {
    try {
      const response = await axios.get('/api/whis/approvals')
      approvals.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    }
  }

  const approveRune = async (runeId) => {
    try {
      await axios.post('/api/whis/approve-rune', { rune_id: runeId })
      await Promise.all([loadApprovals(), loadDigest()])
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    }
  }

  const triggerNightTraining = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await axios.post('/api/whis/train-nightly')
      await Promise.all([loadQueueStatus(), loadApprovals(), loadDigest(), loadLogs()])
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const loadDigest = async () => {
    try {
      const response = await axios.get('/api/whis/digest')
      digest.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    }
  }

  const loadLogs = async () => {
    try {
      const response = await axios.get('/api/logs')
      logs.value = response.data
    } catch (err) {
      error.value = err.response?.data?.detail || err.message
    }
  }

  const clearError = () => {
    error.value = null
  }

  const refreshAll = async () => {
    await Promise.all([
      loadQueueStatus(),
      loadApprovals(),
      loadDigest(),
      loadLogs()
    ])
  }

  return {
    // State
    tasks,
    logs,
    queueStatus,
    approvals,
    digest,
    loading,
    error,
    
    // Getters
    recentTasks,
    pendingApprovals,
    systemHealth,
    
    // Actions
    submitTask,
    completeWithJames,
    sendToAgent,
    loadQueueStatus,
    loadApprovals,
    approveRune,
    triggerNightTraining,
    loadDigest,
    loadLogs,
    clearError,
    refreshAll
  }
}) 