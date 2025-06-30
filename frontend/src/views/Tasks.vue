<template>
  <div class="tasks-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">Manager Input Console</h1>
      <p class="text-gray-300">Submit tasks to the LinkOps AI system</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Task Submission Form -->
      <div class="glass-panel p-6">
        <h2 class="futuristic-subtitle text-2xl mb-6">Submit New Task</h2>
        
        <form @submit.prevent="submitTask" class="space-y-6">
          <!-- Task Description -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Task Description
            </label>
            <textarea
              v-model="taskForm.description"
              rows="4"
              class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
              placeholder="Describe the task you want the AI to handle..."
              required
            ></textarea>
          </div>

          <!-- Priority -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Priority
            </label>
            <select
              v-model="taskForm.priority"
              class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="urgent">Urgent</option>
            </select>
          </div>

          <!-- Tags -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Tags
            </label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tag in taskForm.tags"
                :key="tag"
                class="glass-panel px-3 py-1 rounded-full text-sm flex items-center space-x-1"
              >
                <span>{{ tag }}</span>
                <button
                  @click="removeTag(tag)"
                  class="text-gray-400 hover:text-white"
                >
                  ×
                </button>
              </span>
            </div>
            <div class="flex space-x-2">
              <input
                v-model="newTag"
                @keyup.enter="addTag"
                type="text"
                class="flex-1 glass-panel p-2 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                placeholder="Add tag..."
              />
              <button
                @click="addTag"
                type="button"
                class="glass-panel px-4 py-2 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300"
              >
                Add
              </button>
            </div>
          </div>

          <!-- Task Type -->
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">
              Task Type
            </label>
            <div class="grid grid-cols-2 gap-4">
              <label class="glass-panel p-4 rounded-lg cursor-pointer hover:neon-border transition-all duration-300">
                <input
                  v-model="taskForm.type"
                  type="radio"
                  value="infrastructure"
                  class="sr-only"
                />
                <div class="text-center">
                  <div class="text-2xl mb-2">🏗️</div>
                  <div class="futuristic-subtitle">Infrastructure</div>
                  <div class="text-xs text-gray-300">Deploy, configure, manage</div>
                </div>
              </label>
              <label class="glass-panel p-4 rounded-lg cursor-pointer hover:neon-border transition-all duration-300">
                <input
                  v-model="taskForm.type"
                  type="radio"
                  value="monitoring"
                  class="sr-only"
                />
                <div class="text-center">
                  <div class="text-2xl mb-2">📊</div>
                  <div class="futuristic-subtitle">Monitoring</div>
                  <div class="text-xs text-gray-300">Alerts, metrics, logs</div>
                </div>
              </label>
              <label class="glass-panel p-4 rounded-lg cursor-pointer hover:neon-border transition-all duration-300">
                <input
                  v-model="taskForm.type"
                  type="radio"
                  value="security"
                  class="sr-only"
                />
                <div class="text-center">
                  <div class="text-2xl mb-2">🔒</div>
                  <div class="futuristic-subtitle">Security</div>
                  <div class="text-xs text-gray-300">Audit, compliance, threats</div>
                </div>
              </label>
              <label class="glass-panel p-4 rounded-lg cursor-pointer hover:neon-border transition-all duration-300">
                <input
                  v-model="taskForm.type"
                  type="radio"
                  value="automation"
                  class="sr-only"
                />
                <div class="text-center">
                  <div class="text-2xl mb-2">🤖</div>
                  <div class="futuristic-subtitle">Automation</div>
                  <div class="text-xs text-gray-300">Scripts, workflows, CI/CD</div>
                </div>
              </label>
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isSubmitting"
            class="w-full glass-panel py-4 rounded-lg futuristic-subtitle text-lg hover:neon-border transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="isSubmitting">🔄 Submitting...</span>
            <span v-else>🚀 Submit Task</span>
          </button>
        </form>
      </div>

      <!-- Task Preview & Feasibility -->
      <div class="space-y-6">
        <!-- Task Preview -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Task Preview</h3>
          <div v-if="taskForm.description" class="space-y-3">
            <div class="glass-panel p-4 rounded-lg">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium">Description</span>
                <span class="text-xs text-gray-400">{{ taskForm.type || 'Not selected' }}</span>
              </div>
              <p class="text-sm text-gray-300">{{ taskForm.description }}</p>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm">Priority:</span>
              <span class="text-sm font-medium" :class="priorityColor">{{ taskForm.priority }}</span>
            </div>
            
            <div v-if="taskForm.tags.length > 0">
              <span class="text-sm">Tags:</span>
              <div class="flex flex-wrap gap-1 mt-1">
                <span
                  v-for="tag in taskForm.tags"
                  :key="tag"
                  class="text-xs glass-panel px-2 py-1 rounded"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>
          <div v-else class="text-center text-gray-400 py-8">
            Start typing to see task preview...
          </div>
        </div>

        <!-- Feasibility Assessment -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">AI Feasibility Assessment</h3>
          <div v-if="feasibilityAssessment" class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-sm">Automation Level:</span>
              <span class="text-sm font-medium" :class="feasibilityColor">
                {{ feasibilityAssessment.level }}
              </span>
            </div>
            
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-xs">Confidence:</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 h-2 bg-gray-700 rounded">
                    <div 
                      class="h-full rounded transition-all duration-500"
                      :class="feasibilityBarColor"
                      :style="{ width: feasibilityAssessment.confidence + '%' }"
                    ></div>
                  </div>
                  <span class="text-xs">{{ feasibilityAssessment.confidence }}%</span>
                </div>
              </div>
            </div>
            
            <div class="glass-panel p-3 rounded-lg">
              <div class="text-xs text-gray-300 mb-2">Recommended Agent:</div>
              <div class="flex items-center space-x-2">
                <div class="status-indicator status-online"></div>
                <span class="font-medium">{{ feasibilityAssessment.recommendedAgent }}</span>
              </div>
            </div>
            
            <div class="text-xs text-gray-300">
              {{ feasibilityAssessment.reasoning }}
            </div>
          </div>
          <div v-else class="text-center text-gray-400 py-8">
            Submit a task to see feasibility assessment...
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Tasks -->
    <div class="mt-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Recent Tasks</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="task in recentTasks"
          :key="task.id"
          class="glass-panel p-4 rounded-lg"
          :class="`agent-${task.assignedAgent.toLowerCase()}`"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium">{{ task.type }}</span>
            <span class="text-xs" :class="statusColor(task.status)">{{ task.status }}</span>
          </div>
          <p class="text-sm text-gray-300 mb-3">{{ task.description }}</p>
          <div class="flex items-center justify-between text-xs">
            <span>{{ task.assignedAgent }}</span>
            <span class="text-gray-400">{{ task.timestamp }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import axios from 'axios'

export default {
  name: 'Tasks',
  setup() {
    const taskForm = ref({
      description: '',
      priority: 'medium',
      tags: [],
      type: ''
    })

    const newTag = ref('')
    const isSubmitting = ref(false)
    const feasibilityAssessment = ref(null)

    const recentTasks = ref([
      {
        id: 1,
        description: 'Deploy Prometheus monitoring stack to AKS cluster',
        type: 'infrastructure',
        priority: 'high',
        status: 'processing',
        assignedAgent: 'Katie',
        timestamp: '2h ago'
      },
      {
        id: 2,
        description: 'Audit security policies across all environments',
        type: 'security',
        priority: 'urgent',
        status: 'completed',
        assignedAgent: 'Igris',
        timestamp: '4h ago'
      },
      {
        id: 3,
        description: 'Optimize CI/CD pipeline performance',
        type: 'automation',
        priority: 'medium',
        status: 'queued',
        assignedAgent: 'Ficknury',
        timestamp: '6h ago'
      }
    ])

    const priorityColor = computed(() => {
      const colors = {
        low: 'text-green-400',
        medium: 'text-yellow-400',
        high: 'text-orange-400',
        urgent: 'text-red-400'
      }
      return colors[taskForm.value.priority] || 'text-gray-400'
    })

    const feasibilityColor = computed(() => {
      if (!feasibilityAssessment.value) return 'text-gray-400'
      const colors = {
        'Full Auto': 'text-green-400',
        'Semi Auto': 'text-yellow-400',
        'Manual': 'text-red-400'
      }
      return colors[feasibilityAssessment.value.level] || 'text-gray-400'
    })

    const feasibilityBarColor = computed(() => {
      if (!feasibilityAssessment.value) return 'bg-gray-500'
      const confidence = feasibilityAssessment.value.confidence
      if (confidence >= 80) return 'bg-green-500'
      if (confidence >= 60) return 'bg-yellow-500'
      return 'bg-red-500'
    })

    const statusColor = (status) => {
      const colors = {
        completed: 'text-green-400',
        processing: 'text-blue-400',
        queued: 'text-yellow-400',
        failed: 'text-red-400'
      }
      return colors[status] || 'text-gray-400'
    }

    const addTag = () => {
      if (newTag.value.trim() && !taskForm.value.tags.includes(newTag.value.trim())) {
        taskForm.value.tags.push(newTag.value.trim())
        newTag.value = ''
      }
    }

    const removeTag = (tag) => {
      taskForm.value.tags = taskForm.value.tags.filter(t => t !== tag)
    }

    const assessFeasibility = async () => {
      if (!taskForm.value.description) {
        feasibilityAssessment.value = null
        return
      }

      try {
        // Simulate API call to Ficknury evaluator
        const response = await axios.post('/api/evaluator/assess', {
          description: taskForm.value.description,
          type: taskForm.value.type,
          tags: taskForm.value.tags
        })
        
        feasibilityAssessment.value = response.data
      } catch (error) {
        // Fallback to mock assessment
        feasibilityAssessment.value = {
          level: 'Semi Auto',
          confidence: 75,
          recommendedAgent: 'Katie',
          reasoning: 'Task involves Kubernetes deployment which can be partially automated with human oversight.'
        }
      }
    }

    const submitTask = async () => {
      isSubmitting.value = true
      
      try {
        const payload = {
          raw_text: taskForm.value.description,
          source: 'manual_input',
          topic: taskForm.value.type,
          metadata: {
            priority: taskForm.value.priority,
            tags: taskForm.value.tags,
            submitted_by: 'manager'
          }
        }

        await axios.post('/api/input/manual', payload)
        
        // Reset form
        taskForm.value = {
          description: '',
          priority: 'medium',
          tags: [],
          type: ''
        }
        feasibilityAssessment.value = null
        
        // Add to recent tasks
        recentTasks.value.unshift({
          id: Date.now(),
          description: payload.raw_text,
          type: payload.topic,
          priority: payload.metadata.priority,
          status: 'queued',
          assignedAgent: 'Ficknury',
          timestamp: 'Just now'
        })
        
      } catch (error) {
        console.error('Error submitting task:', error)
      } finally {
        isSubmitting.value = false
      }
    }

    // Watch for changes to trigger feasibility assessment
    watch(() => taskForm.value.description, assessFeasibility, { debounce: 500 })

    return {
      taskForm,
      newTag,
      isSubmitting,
      feasibilityAssessment,
      recentTasks,
      priorityColor,
      feasibilityColor,
      feasibilityBarColor,
      statusColor,
      addTag,
      removeTag,
      submitTask
    }
  }
}
</script>

<style scoped>
.tasks-container {
  max-width: 1400px;
  margin: 0 auto;
}

/* Custom radio button styling */
input[type="radio"]:checked + div {
  border-color: var(--whis-primary);
  box-shadow: 0 0 15px rgba(99, 102, 241, 0.3);
}
</style> 