<template>
  <div class="ficknury-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">Ficknury Task Router</h1>
      <p class="text-gray-300">Intelligent task evaluation and agent assignment</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Task Timeline -->
      <div class="lg:col-span-2">
        <div class="glass-panel p-6">
          <h2 class="futuristic-subtitle text-2xl mb-6">Incoming Tasks Timeline</h2>
          <div class="space-y-4">
            <div
              v-for="task in incomingTasks"
              :key="task.id"
              class="glass-panel p-4 rounded-lg agent-ficknury"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-2">
                  <span class="text-lg">{{ task.icon }}</span>
                  <span class="font-medium">{{ task.title }}</span>
                </div>
                <span class="text-xs text-gray-400">{{ task.timestamp }}</span>
              </div>
              <p class="text-sm text-gray-300 mb-3">{{ task.description }}</p>
              
              <!-- Feasibility Assessment -->
              <div class="flex items-center justify-between mb-3">
                <span class="text-sm">Feasibility:</span>
                <div class="flex items-center space-x-2">
                  <span class="text-sm font-medium" :class="feasibilityColor(task.feasibility.level)">
                    {{ task.feasibility.level }}
                  </span>
                  <div class="w-20 h-2 bg-gray-700 rounded">
                    <div 
                      class="h-full rounded transition-all duration-500"
                      :class="feasibilityBarColor(task.feasibility.confidence)"
                      :style="{ width: task.feasibility.confidence + '%' }"
                    ></div>
                  </div>
                  <span class="text-xs">{{ task.feasibility.confidence }}%</span>
                </div>
              </div>

              <!-- Decision Logic -->
              <div class="glass-panel p-3 rounded-lg mb-3">
                <div class="text-xs text-gray-400 mb-1">Decision Logic:</div>
                <div class="text-sm text-gray-300">{{ task.feasibility.reasoning }}</div>
              </div>

              <!-- Agent Assignment -->
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="text-xs text-gray-400">Assigned to:</span>
                  <div class="flex items-center space-x-1">
                    <div class="status-indicator status-online"></div>
                    <span class="text-sm font-medium">{{ task.assignedAgent }}</span>
                  </div>
                </div>
                <span class="text-xs" :class="statusColor(task.status)">
                  {{ task.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Evaluation Panel -->
      <div class="space-y-6">
        <!-- AI Feasibility Ranking -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">AI Feasibility Ranking</h3>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm">Full Auto:</span>
              <div class="flex items-center space-x-2">
                <div class="w-16 h-2 bg-gray-700 rounded">
                  <div class="h-full bg-green-500 rounded" :style="{ width: feasibilityStats.fullAuto + '%' }"></div>
                </div>
                <span class="text-xs">{{ feasibilityStats.fullAuto }}%</span>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm">Semi Auto:</span>
              <div class="flex items-center space-x-2">
                <div class="w-16 h-2 bg-gray-700 rounded">
                  <div class="h-full bg-yellow-500 rounded" :style="{ width: feasibilityStats.semiAuto + '%' }"></div>
                </div>
                <span class="text-xs">{{ feasibilityStats.semiAuto }}%</span>
              </div>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm">Manual:</span>
              <div class="flex items-center space-x-2">
                <div class="w-16 h-2 bg-gray-700 rounded">
                  <div class="h-full bg-red-500 rounded" :style="{ width: feasibilityStats.manual + '%' }"></div>
                </div>
                <span class="text-xs">{{ feasibilityStats.manual }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Agent Assignment Stats -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Agent Assignment Stats</h3>
          <div class="space-y-3">
            <div
              v-for="agent in agentStats"
              :key="agent.name"
              class="flex items-center justify-between"
            >
              <div class="flex items-center space-x-2">
                <div class="status-indicator" :class="agent.status === 'online' ? 'status-online' : 'status-offline'"></div>
                <span class="text-sm">{{ agent.name }}</span>
              </div>
              <div class="flex items-center space-x-2">
                <span class="text-xs text-gray-400">{{ agent.tasks }}</span>
                <div class="iq-bar w-12" :style="{ width: agent.load + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Decision Matrix -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Decision Matrix</h3>
          <div class="space-y-3">
            <div
              v-for="factor in decisionFactors"
              :key="factor.name"
              class="glass-panel p-3 rounded-lg"
            >
              <div class="flex items-center justify-between mb-1">
                <span class="text-sm font-medium">{{ factor.name }}</span>
                <span class="text-xs" :class="factorColor(factor.weight)">
                  {{ factor.weight }}
                </span>
              </div>
              <div class="text-xs text-gray-300">{{ factor.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Task Processing Queue -->
    <div class="mt-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Task Processing Queue</h2>
      <div class="glass-panel p-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div class="text-center">
            <div class="text-2xl font-bold text-white mb-1">{{ queueStats.pending }}</div>
            <div class="text-sm text-gray-300">Pending</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-blue-400 mb-1">{{ queueStats.processing }}</div>
            <div class="text-sm text-gray-300">Processing</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-green-400 mb-1">{{ queueStats.completed }}</div>
            <div class="text-sm text-gray-300">Completed</div>
          </div>
          <div class="text-center">
            <div class="text-2xl font-bold text-red-400 mb-1">{{ queueStats.failed }}</div>
            <div class="text-sm text-gray-300">Failed</div>
          </div>
        </div>

        <div class="space-y-3">
          <div
            v-for="task in processingQueue"
            :key="task.id"
            class="glass-panel p-4 rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-lg">{{ task.icon }}</span>
                <span class="font-medium">{{ task.title }}</span>
              </div>
              <span class="text-xs text-gray-400">{{ task.timestamp }}</span>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ task.description }}</p>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-400">Assigned: {{ task.assignedAgent }}</span>
              <span :class="statusColor(task.status)">{{ task.status }}</span>
            </div>
            <div v-if="task.progress" class="mt-2">
              <div class="flex items-center justify-between text-xs mb-1">
                <span>Progress:</span>
                <span>{{ task.progress }}%</span>
              </div>
              <div class="w-full h-2 bg-gray-700 rounded">
                <div 
                  class="h-full rounded transition-all duration-500"
                  :class="progressColor(task.progress)"
                  :style="{ width: task.progress + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Fallback Analysis -->
    <div class="mt-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Fallback Analysis</h2>
      <div class="glass-panel p-6">
        <div class="space-y-4">
          <div
            v-for="fallback in fallbackAnalysis"
            :key="fallback.id"
            class="glass-panel p-4 rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-lg">⚠️</span>
                <span class="font-medium">{{ fallback.reason }}</span>
              </div>
              <span class="text-xs text-gray-400">{{ fallback.timestamp }}</span>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ fallback.description }}</p>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-400">Original Agent: {{ fallback.originalAgent }}</span>
              <span class="text-gray-400">Fallback: {{ fallback.fallbackAction }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Ficknury',
  setup() {
    const incomingTasks = ref([
      {
        id: 1,
        title: 'Deploy Monitoring Stack',
        icon: '📊',
        description: 'Deploy Prometheus and Grafana to production cluster',
        timestamp: '2h ago',
        feasibility: {
          level: 'Full Auto',
          confidence: 95,
          reasoning: 'Standard monitoring deployment with well-defined patterns'
        },
        assignedAgent: 'Katie',
        status: 'assigned'
      },
      {
        id: 2,
        title: 'Security Audit',
        icon: '🔒',
        description: 'Comprehensive security audit of infrastructure',
        timestamp: '4h ago',
        feasibility: {
          level: 'Semi Auto',
          confidence: 78,
          reasoning: 'Complex security requirements need human oversight'
        },
        assignedAgent: 'Igris',
        status: 'processing'
      },
      {
        id: 3,
        title: 'Cost Optimization',
        icon: '💰',
        description: 'Analyze and optimize cloud costs',
        timestamp: '6h ago',
        feasibility: {
          level: 'Full Auto',
          confidence: 88,
          reasoning: 'Automated cost analysis with predefined optimization rules'
        },
        assignedAgent: 'Igris',
        status: 'completed'
      }
    ])

    const feasibilityStats = ref({
      fullAuto: 65,
      semiAuto: 25,
      manual: 10
    })

    const agentStats = ref([
      { name: 'Katie', tasks: 12, load: 75, status: 'online' },
      { name: 'Igris', tasks: 8, load: 60, status: 'online' },
      { name: 'Whis', tasks: 15, load: 90, status: 'processing' }
    ])

    const decisionFactors = ref([
      {
        name: 'Task Complexity',
        weight: 'High',
        description: 'Analyzes task complexity and required expertise'
      },
      {
        name: 'Agent Availability',
        weight: 'Medium',
        description: 'Checks agent workload and availability'
      },
      {
        name: 'Historical Success',
        weight: 'High',
        description: 'Considers past success rates for similar tasks'
      },
      {
        name: 'Resource Requirements',
        weight: 'Medium',
        description: 'Evaluates required resources and permissions'
      }
    ])

    const queueStats = ref({
      pending: 8,
      processing: 5,
      completed: 1247,
      failed: 3
    })

    const processingQueue = ref([
      {
        id: 1,
        title: 'Database Migration',
        icon: '🗄️',
        description: 'Migrate PostgreSQL database to new version',
        assignedAgent: 'Igris',
        status: 'processing',
        progress: 75,
        timestamp: '1h ago'
      },
      {
        id: 2,
        title: 'Load Balancer Config',
        icon: '⚖️',
        description: 'Update load balancer configuration for new services',
        assignedAgent: 'Katie',
        status: 'processing',
        progress: 45,
        timestamp: '2h ago'
      }
    ])

    const fallbackAnalysis = ref([
      {
        id: 1,
        reason: 'Agent Overload',
        description: 'Katie was overloaded, task reassigned to Igris',
        originalAgent: 'Katie',
        fallbackAction: 'Manual Review',
        timestamp: '3h ago'
      },
      {
        id: 2,
        reason: 'Permission Denied',
        description: 'Insufficient permissions for automated deployment',
        originalAgent: 'Igris',
        fallbackAction: 'Manual Deployment',
        timestamp: '5h ago'
      }
    ])

    const feasibilityColor = (level) => {
      const colors = {
        'Full Auto': 'text-green-400',
        'Semi Auto': 'text-yellow-400',
        'Manual': 'text-red-400'
      }
      return colors[level] || 'text-gray-400'
    }

    const feasibilityBarColor = (confidence) => {
      if (confidence >= 80) return 'bg-green-500'
      if (confidence >= 60) return 'bg-yellow-500'
      return 'bg-red-500'
    }

    const statusColor = (status) => {
      const colors = {
        assigned: 'text-blue-400',
        processing: 'text-yellow-400',
        completed: 'text-green-400',
        failed: 'text-red-400'
      }
      return colors[status] || 'text-gray-400'
    }

    const factorColor = (weight) => {
      const colors = {
        'High': 'text-red-400',
        'Medium': 'text-yellow-400',
        'Low': 'text-green-400'
      }
      return colors[weight] || 'text-gray-400'
    }

    const progressColor = (progress) => {
      if (progress >= 80) return 'bg-green-500'
      if (progress >= 50) return 'bg-yellow-500'
      return 'bg-blue-500'
    }

    return {
      incomingTasks,
      feasibilityStats,
      agentStats,
      decisionFactors,
      queueStats,
      processingQueue,
      fallbackAnalysis,
      feasibilityColor,
      feasibilityBarColor,
      statusColor,
      factorColor,
      progressColor
    }
  }
}
</script>

<style scoped>
.ficknury-container {
  max-width: 1400px;
  margin: 0 auto;
}
</style> 