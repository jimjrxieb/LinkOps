<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="holo-card">
      <h2 class="text-2xl font-bold text-glow mb-2">🧠 Whis - AI Training & Learning</h2>
      <p class="text-holo-cyan/70">Neural network training, approval queue, and daily digest</p>
    </div>

    <!-- Training Queue Status -->
    <div class="holo-card">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">📊 Training Queue Status</h3>
        <button @click="refreshQueueStatus" class="holo-button" :disabled="loading">
          🔄 Refresh
        </button>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-cyber-gray/30 p-4 rounded border border-holo-cyan/20 text-center">
          <div class="text-2xl font-bold text-holo-cyan">{{ queueStatus.pending || 0 }}</div>
          <div class="text-sm text-holo-cyan/70">🕒 Pending</div>
        </div>
        <div class="bg-cyber-gray/30 p-4 rounded border border-holo-green/20 text-center">
          <div class="text-2xl font-bold text-holo-green">{{ queueStatus.trained || 0 }}</div>
          <div class="text-sm text-holo-green/70">✅ Trained</div>
        </div>
        <div class="bg-cyber-gray/30 p-4 rounded border border-holo-blue/20 text-center">
          <div class="text-2xl font-bold text-holo-blue">{{ queueStatus.matches || 0 }}</div>
          <div class="text-sm text-holo-blue/70">📎 Matches</div>
        </div>
        <div class="bg-cyber-gray/30 p-4 rounded border border-holo-yellow/20 text-center">
          <div class="text-2xl font-bold text-holo-yellow">{{ queueStatus.fallbacks || 0 }}</div>
          <div class="text-sm text-holo-yellow/70">🧩 Fallbacks</div>
        </div>
      </div>
    </div>

    <!-- Approval Queue -->
    <div class="holo-card">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">🧾 Approval Queue</h3>
        <span class="text-sm text-holo-cyan/70">{{ approvals.length }} pending</span>
      </div>
      
      <div v-if="approvals.length === 0" class="text-center py-8 text-holo-cyan/60">
        <div class="text-4xl mb-2">✅</div>
        <div>No pending approvals</div>
        <div class="text-sm">All runes have been reviewed</div>
      </div>
      
      <div v-else class="space-y-4 max-h-96 overflow-y-auto">
        <div 
          v-for="rune in approvals" 
          :key="rune.rune_id"
          class="bg-cyber-gray/30 p-4 rounded border border-holo-cyan/20"
        >
          <div class="flex justify-between items-start mb-3">
            <div>
              <h4 class="font-semibold text-holo-cyan">{{ rune.orb }}</h4>
              <div class="text-sm text-holo-cyan/70">{{ rune.task_id }}</div>
            </div>
            <button 
              @click="approveRune(rune.rune_id)"
              class="holo-button bg-holo-green/20 border-holo-green text-holo-green hover:bg-holo-green/30"
              :disabled="loading"
            >
              ✅ Approve
            </button>
          </div>
          
          <div class="bg-cyber-dark p-3 rounded border border-holo-cyan/10 mb-3">
            <pre class="text-sm text-holo-cyan/90 font-mono whitespace-pre-wrap">{{ rune.script_content }}</pre>
          </div>
          
          <div class="flex justify-between text-xs text-holo-cyan/60">
            <span>Language: {{ rune.language }}</span>
            <span>Version: {{ rune.version }}</span>
            <span>{{ formatTime(rune.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Daily Digest -->
    <div class="holo-card">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold">📅 Daily Digest</h3>
        <button @click="refreshDigest" class="holo-button" :disabled="loading">
          🔄 Refresh
        </button>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div class="bg-cyber-gray/30 p-4 rounded border border-holo-cyan/20 text-center">
          <div class="text-2xl font-bold text-holo-cyan">{{ digest.orbs_created || 0 }}</div>
          <div class="text-sm text-holo-cyan/70">🌀 Orbs Updated</div>
        </div>
        <div class="bg-cyber-gray/30 p-4 rounded border border-holo-green/20 text-center">
          <div class="text-2xl font-bold text-holo-green">{{ digest.runes_created || 0 }}</div>
          <div class="text-sm text-holo-green/70">📜 Runes Created</div>
        </div>
        <div class="bg-cyber-gray/30 p-4 rounded border border-holo-blue/20 text-center">
          <div class="text-2xl font-bold text-holo-blue">{{ digest.logs_processed || 0 }}</div>
          <div class="text-sm text-holo-blue/70">📚 Logs Processed</div>
        </div>
      </div>
      
      <div class="text-xs text-holo-cyan/60 text-center">
        Last updated: {{ digest.timestamp ? formatTime(digest.timestamp) : 'N/A' }}
      </div>
    </div>

    <!-- Night Training -->
    <div class="holo-card">
      <h3 class="text-lg font-semibold mb-4">🌙 Night Training</h3>
      <p class="text-holo-cyan/70 mb-4">Process all today's logs and create new runes for approval</p>
      
      <button 
        @click="triggerNightTraining"
        class="holo-button-primary w-full"
        :disabled="loading"
      >
        {{ loading ? '🔄 Training...' : '🚀 Trigger Night Training' }}
      </button>
      
      <div v-if="loading" class="mt-4 text-center text-holo-cyan/70">
        <div class="animate-pulse">Processing logs and creating runes...</div>
      </div>
    </div>

    <!-- Status Messages -->
    <div v-if="statusMessage" class="holo-card" :class="statusMessage.type === 'error' ? 'border-holo-red' : 'border-holo-green'">
      <div class="flex items-center space-x-2">
        <span v-if="statusMessage.type === 'error'">❌</span>
        <span v-else>✅</span>
        <span>{{ statusMessage.text }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// State
const loading = ref(false)
const queueStatus = ref({})
const approvals = ref([])
const digest = ref({})
const statusMessage = ref(null)

// Methods
const refreshQueueStatus = async () => {
  try {
    const response = await axios.get('/api/whis/queue')
    queueStatus.value = response.data
  } catch (error) {
    console.error('Error loading queue status:', error)
    showStatus('Failed to load queue status', 'error')
  }
}

const refreshApprovals = async () => {
  try {
    const response = await axios.get('/api/whis/approvals')
    approvals.value = response.data
  } catch (error) {
    console.error('Error loading approvals:', error)
    showStatus('Failed to load approvals', 'error')
  }
}

const refreshDigest = async () => {
  try {
    const response = await axios.get('/api/whis/digest')
    digest.value = response.data
  } catch (error) {
    console.error('Error loading digest:', error)
    showStatus('Failed to load digest', 'error')
  }
}

const approveRune = async (runeId) => {
  loading.value = true
  statusMessage.value = null
  
  try {
    await axios.post('/api/whis/approve-rune', { rune_id: runeId })
    showStatus('Rune approved successfully!', 'success')
    await Promise.all([refreshApprovals(), refreshDigest()])
  } catch (error) {
    console.error('Error approving rune:', error)
    showStatus(`Error: ${error.response?.data?.detail || error.message}`, 'error')
  } finally {
    loading.value = false
  }
}

const triggerNightTraining = async () => {
  loading.value = true
  statusMessage.value = null
  
  try {
    const response = await axios.post('/api/whis/train-nightly')
    showStatus('Night training completed successfully!', 'success')
    await Promise.all([refreshQueueStatus(), refreshApprovals(), refreshDigest()])
  } catch (error) {
    console.error('Error triggering night training:', error)
    showStatus(`Error: ${error.response?.data?.detail || error.message}`, 'error')
  } finally {
    loading.value = false
  }
}

const showStatus = (text, type = 'success') => {
  statusMessage.value = { text, type }
  setTimeout(() => {
    statusMessage.value = null
  }, 5000)
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

// Lifecycle
onMounted(async () => {
  await Promise.all([
    refreshQueueStatus(),
    refreshApprovals(),
    refreshDigest()
  ])
})
</script> 