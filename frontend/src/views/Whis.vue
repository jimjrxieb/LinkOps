<template>
  <div class="whis-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">Whis AI Brain</h1>
      <p class="text-gray-300">Intelligent data processing and learning system</p>
    </div>

    <!-- Subtabs Navigation -->
    <div class="glass-panel p-2 rounded-lg mb-8">
      <div class="flex space-x-2">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex-1 glass-panel p-4 rounded-lg futuristic-subtitle transition-all duration-300"
          :class="[
            activeTab === tab.id ? 'neon-border agent-whis' : 'hover:neon-border'
          ]"
        >
          <div class="flex items-center justify-center space-x-2">
            <span class="text-xl">{{ tab.icon }}</span>
            <span>{{ tab.name }}</span>
          </div>
        </button>
      </div>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Input Console Tab -->
      <div v-if="activeTab === 'input'" class="space-y-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- YouTube Input -->
          <div class="glass-panel p-6">
            <h3 class="futuristic-subtitle text-xl mb-4">YouTube Transcript Input</h3>
            <form @submit.prevent="submitYouTube" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  YouTube URL
                </label>
                <input
                  v-model="youtubeForm.url"
                  type="url"
                  class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                  placeholder="https://www.youtube.com/watch?v=..."
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Topic
                </label>
                <input
                  v-model="youtubeForm.topic"
                  type="text"
                  class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                  placeholder="e.g., Kubernetes, CI/CD, Security"
                  required
                />
              </div>
              <button
                type="submit"
                :disabled="isSubmittingYouTube"
                class="w-full glass-panel py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300 disabled:opacity-50"
              >
                <span v-if="isSubmittingYouTube">🔄 Processing...</span>
                <span v-else>📹 Submit YouTube Video</span>
              </button>
            </form>
          </div>

          <!-- Manual Task Input -->
          <div class="glass-panel p-6">
            <h3 class="futuristic-subtitle text-xl mb-4">Manual Task Input</h3>
            <form @submit.prevent="submitManualTask" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Task Description
                </label>
                <textarea
                  v-model="manualForm.description"
                  rows="4"
                  class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                  placeholder="Describe the task or error to process..."
                  required
                ></textarea>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-300 mb-2">
                  Topic
                </label>
                <input
                  v-model="manualForm.topic"
                  type="text"
                  class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                  placeholder="e.g., Error Fix, Task Processing"
                  required
                />
              </div>
              <button
                type="submit"
                :disabled="isSubmittingManual"
                class="w-full glass-panel py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300 disabled:opacity-50"
              >
                <span v-if="isSubmittingManual">🔄 Processing...</span>
                <span v-else>📝 Submit Manual Task</span>
              </button>
            </form>
          </div>
        </div>

        <!-- Recent Inputs -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Recent Inputs</h3>
          <div class="space-y-3">
            <div
              v-for="input in recentInputs"
              :key="input.id"
              class="glass-panel p-4 rounded-lg"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-2">
                  <span class="text-lg">{{ input.icon }}</span>
                  <span class="font-medium">{{ input.type }}</span>
                </div>
                <span class="text-xs text-gray-400">{{ input.timestamp }}</span>
              </div>
              <p class="text-sm text-gray-300 mb-2">{{ input.description }}</p>
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-400">Topic: {{ input.topic }}</span>
                <span :class="statusColor(input.status)">{{ input.status }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sanitizer View Tab -->
      <div v-if="activeTab === 'sanitizer'" class="space-y-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Raw Input -->
          <div class="glass-panel p-6">
            <h3 class="futuristic-subtitle text-xl mb-4">Raw Input</h3>
            <div class="space-y-4">
              <div
                v-for="item in sanitizerData.raw"
                :key="item.id"
                class="glass-panel p-4 rounded-lg"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium">{{ item.source }}</span>
                  <span class="text-xs text-gray-400">{{ item.timestamp }}</span>
                </div>
                <div class="text-sm text-gray-300 max-h-32 overflow-y-auto">
                  {{ item.content }}
                </div>
              </div>
            </div>
          </div>

          <!-- Sanitized Output -->
          <div class="glass-panel p-6">
            <h3 class="futuristic-subtitle text-xl mb-4">Sanitized Output</h3>
            <div class="space-y-4">
              <div
                v-for="item in sanitizerData.sanitized"
                :key="item.id"
                class="glass-panel p-4 rounded-lg agent-whis"
              >
                <div class="flex items-center justify-between mb-2">
                  <span class="text-sm font-medium">Sanitized</span>
                  <span class="text-xs text-gray-400">{{ item.timestamp }}</span>
                </div>
                <div class="text-sm text-gray-300 max-h-32 overflow-y-auto">
                  {{ item.content }}
                </div>
                <div class="mt-2 flex items-center justify-between text-xs">
                  <span>Confidence: {{ item.confidence }}%</span>
                  <span>Processing Time: {{ item.processingTime }}ms</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sanitization Stats -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Sanitization Statistics</h3>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-white mb-1">{{ sanitizerStats.totalProcessed }}</div>
              <div class="text-sm text-gray-300">Total Processed</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-green-400 mb-1">{{ sanitizerStats.successRate }}%</div>
              <div class="text-sm text-gray-300">Success Rate</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-400 mb-1">{{ sanitizerStats.avgProcessingTime }}ms</div>
              <div class="text-sm text-gray-300">Avg Processing Time</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-purple-400 mb-1">{{ sanitizerStats.activeQueue }}</div>
              <div class="text-sm text-gray-300">Active Queue</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Data Lake Viewer Tab -->
      <div v-if="activeTab === 'datalake'" class="space-y-6">
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Data Lake Contents</h3>
          <div class="space-y-4">
            <div
              v-for="item in dataLakeItems"
              :key="item.id"
              class="glass-panel p-4 rounded-lg"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-2">
                  <span class="text-lg">{{ item.icon }}</span>
                  <span class="font-medium">{{ item.type }}</span>
                </div>
                <span class="text-xs text-gray-400">{{ item.timestamp }}</span>
              </div>
              <p class="text-sm text-gray-300 mb-2">{{ item.description }}</p>
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-400">Size: {{ item.size }}</span>
                <span class="text-gray-400">Tags: {{ item.tags.join(', ') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Smithing Log Tab -->
      <div v-if="activeTab === 'smithing'" class="space-y-6">
        <!-- Orb Generation -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Orb Generation</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="orb in smithingData.orbs"
              :key="orb.id"
              class="glass-panel p-4 rounded-lg text-center agent-whis"
            >
              <div class="text-3xl mb-2">🔮</div>
              <div class="font-medium mb-1">{{ orb.name }}</div>
              <div class="text-sm text-gray-300 mb-2">{{ orb.description }}</div>
              <div class="iq-bar mx-auto" :style="{ width: orb.power + '%' }"></div>
              <div class="text-xs text-gray-400 mt-1">Power: {{ orb.power }}%</div>
            </div>
          </div>
        </div>

        <!-- Rune Generation -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Rune Generation</h3>
          <div class="space-y-3">
            <div
              v-for="rune in smithingData.runes"
              :key="rune.id"
              class="glass-panel p-4 rounded-lg"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-2">
                  <span class="text-lg">⚡</span>
                  <span class="font-medium">{{ rune.name }}</span>
                </div>
                <span class="text-xs text-gray-400">{{ rune.timestamp }}</span>
              </div>
              <p class="text-sm text-gray-300 mb-2">{{ rune.description }}</p>
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-400">Target Agent: {{ rune.targetAgent }}</span>
                <span class="text-gray-400">Efficiency: {{ rune.efficiency }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Smithing Statistics -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Smithing Statistics</h3>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-white mb-1">{{ smithingStats.totalOrbs }}</div>
              <div class="text-sm text-gray-300">Total Orbs Created</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-white mb-1">{{ smithingStats.totalRunes }}</div>
              <div class="text-sm text-gray-300">Total Runes Forged</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-white mb-1">{{ smithingStats.successRate }}%</div>
              <div class="text-sm text-gray-300">Success Rate</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'Whis',
  setup() {
    const activeTab = ref('input')
    
    const tabs = [
      { id: 'input', name: 'Input Console', icon: '📥' },
      { id: 'sanitizer', name: 'Sanitizer View', icon: '🧹' },
      { id: 'datalake', name: 'Data Lake', icon: '🌊' },
      { id: 'smithing', name: 'Smithing Log', icon: '⚒️' }
    ]

    // Form data
    const youtubeForm = ref({
      url: '',
      topic: ''
    })

    const manualForm = ref({
      description: '',
      topic: ''
    })

    const isSubmittingYouTube = ref(false)
    const isSubmittingManual = ref(false)

    // Mock data
    const recentInputs = ref([
      {
        id: 1,
        type: 'YouTube Video',
        icon: '📹',
        description: 'Kubernetes deployment tutorial',
        topic: 'Kubernetes',
        status: 'processed',
        timestamp: '2h ago'
      },
      {
        id: 2,
        type: 'Manual Task',
        icon: '📝',
        description: 'Fix authentication error in production',
        topic: 'Error Fix',
        status: 'processing',
        timestamp: '4h ago'
      }
    ])

    const sanitizerData = ref({
      raw: [
        {
          id: 1,
          source: 'YouTube Transcript',
          content: 'In this tutorial, we will learn how to deploy applications to Kubernetes...',
          timestamp: '2h ago'
        }
      ],
      sanitized: [
        {
          id: 1,
          content: 'Kubernetes deployment tutorial: Deploy applications to Kubernetes clusters',
          confidence: 95,
          processingTime: 120,
          timestamp: '2h ago'
        }
      ]
    })

    const sanitizerStats = ref({
      totalProcessed: 1247,
      successRate: 98.5,
      avgProcessingTime: 145,
      activeQueue: 3
    })

    const dataLakeItems = ref([
      {
        id: 1,
        type: 'Transcript',
        icon: '📹',
        description: 'Kubernetes deployment tutorial transcript',
        size: '2.3KB',
        tags: ['kubernetes', 'deployment', 'tutorial'],
        timestamp: '2h ago'
      },
      {
        id: 2,
        type: 'Error Log',
        icon: '🐛',
        description: 'Authentication error in production environment',
        size: '1.1KB',
        tags: ['error', 'authentication', 'production'],
        timestamp: '4h ago'
      }
    ])

    const smithingData = ref({
      orbs: [
        {
          id: 1,
          name: 'Deployment Orb',
          description: 'Enhanced Kubernetes deployment logic',
          power: 85
        },
        {
          id: 2,
          name: 'Security Orb',
          description: 'Authentication and authorization patterns',
          power: 92
        }
      ],
      runes: [
        {
          id: 1,
          name: 'DeployRune',
          description: 'Automated deployment pattern for Kubernetes',
          targetAgent: 'Katie',
          efficiency: 88,
          timestamp: '2h ago'
        },
        {
          id: 2,
          name: 'AuthRune',
          description: 'Authentication error resolution pattern',
          targetAgent: 'Igris',
          efficiency: 95,
          timestamp: '4h ago'
        }
      ]
    })

    const smithingStats = ref({
      totalOrbs: 47,
      totalRunes: 156,
      successRate: 94.2
    })

    // Methods
    const submitYouTube = async () => {
      isSubmittingYouTube.value = true
      try {
        await axios.post('/api/input/youtube-transcript', youtubeForm.value)
        youtubeForm.value = { url: '', topic: '' }
        // Add to recent inputs
        recentInputs.value.unshift({
          id: Date.now(),
          type: 'YouTube Video',
          icon: '📹',
          description: youtubeForm.value.url,
          topic: youtubeForm.value.topic,
          status: 'queued',
          timestamp: 'Just now'
        })
      } catch (error) {
        console.error('Error submitting YouTube video:', error)
      } finally {
        isSubmittingYouTube.value = false
      }
    }

    const submitManualTask = async () => {
      isSubmittingManual.value = true
      try {
        const payload = {
          raw_text: manualForm.value.description,
          source: 'manual_input',
          topic: manualForm.value.topic
        }
        await axios.post('/api/input/manual', payload)
        manualForm.value = { description: '', topic: '' }
        // Add to recent inputs
        recentInputs.value.unshift({
          id: Date.now(),
          type: 'Manual Task',
          icon: '📝',
          description: payload.raw_text,
          topic: payload.topic,
          status: 'queued',
          timestamp: 'Just now'
        })
      } catch (error) {
        console.error('Error submitting manual task:', error)
      } finally {
        isSubmittingManual.value = false
      }
    }

    const statusColor = (status) => {
      const colors = {
        processed: 'text-green-400',
        processing: 'text-blue-400',
        queued: 'text-yellow-400',
        failed: 'text-red-400'
      }
      return colors[status] || 'text-gray-400'
    }

    return {
      activeTab,
      tabs,
      youtubeForm,
      manualForm,
      isSubmittingYouTube,
      isSubmittingManual,
      recentInputs,
      sanitizerData,
      sanitizerStats,
      dataLakeItems,
      smithingData,
      smithingStats,
      submitYouTube,
      submitManualTask,
      statusColor
    }
  }
}
</script>

<style scoped>
.whis-container {
  max-width: 1400px;
  margin: 0 auto;
}

.tab-content {
  min-height: 600px;
}
</style> 