<template>
  <div class="agents-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">Agent Evolution Matrix</h1>
      <p class="text-gray-300">Track agent evolution and AI confidence across domains</p>
    </div>

    <!-- Agent Overview Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div
        v-for="agent in agents"
        :key="agent.name"
        class="glass-panel p-6"
        :class="`agent-${agent.name.toLowerCase()}`"
      >
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-2">
            <span class="text-2xl">{{ agent.icon }}</span>
            <div>
              <h3 class="futuristic-subtitle text-lg">{{ agent.name }}</h3>
              <p class="text-xs text-gray-300">{{ agent.role }}</p>
            </div>
          </div>
          <div class="status-indicator" :class="agent.status === 'online' ? 'status-online' : 'status-offline'"></div>
        </div>
        
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm">IQ Level:</span>
            <span class="text-lg font-bold">{{ agent.iq }}</span>
          </div>
          <div class="iq-bar" :style="{ width: agent.iq + '%' }"></div>
          
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-400">Active Runes:</span>
            <span>{{ agent.activeRunes }}</span>
          </div>
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-400">Tasks Completed:</span>
            <span>{{ agent.tasksCompleted }}</span>
          </div>
        </div>

        <div class="mt-4 flex space-x-2">
          <button
            @click="upgradeAgent(agent.name)"
            class="flex-1 glass-panel py-2 rounded-lg text-xs futuristic-subtitle hover:neon-border transition-all duration-300"
          >
            ⬆️ Upgrade
          </button>
          <button
            @click="reviewRuneTrail(agent.name)"
            class="flex-1 glass-panel py-2 rounded-lg text-xs futuristic-subtitle hover:neon-border transition-all duration-300"
          >
            🔍 Review
          </button>
        </div>
      </div>
    </div>

    <!-- AI Confidence Per Domain -->
    <div class="mb-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">AI Confidence Per Domain</h2>
      <div class="glass-panel p-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Confidence Matrix -->
          <div>
            <h3 class="futuristic-subtitle text-xl mb-4">Confidence Matrix</h3>
            <div class="space-y-4">
              <div
                v-for="domain in domains"
                :key="domain.name"
                class="glass-panel p-4 rounded-lg"
              >
                <div class="flex items-center justify-between mb-3">
                  <span class="font-medium">{{ domain.name }}</span>
                  <span class="text-sm text-gray-400">{{ domain.description }}</span>
                </div>
                <div class="space-y-2">
                  <div
                    v-for="agent in agents"
                    :key="agent.name"
                    class="flex items-center justify-between"
                  >
                    <span class="text-sm">{{ agent.name }}:</span>
                    <div class="flex items-center space-x-2">
                      <div class="w-20 h-2 bg-gray-700 rounded">
                        <div 
                          class="h-full rounded transition-all duration-500"
                          :class="`agent-${agent.name.toLowerCase()}`"
                          :style="{ width: getDomainConfidence(agent.name, domain.name) + '%' }"
                        ></div>
                      </div>
                      <span class="text-xs">{{ getDomainConfidence(agent.name, domain.name) }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Evolution Timeline -->
          <div>
            <h3 class="futuristic-subtitle text-xl mb-4">Evolution Timeline</h3>
            <div class="space-y-4">
              <div
                v-for="event in evolutionEvents"
                :key="event.id"
                class="glass-panel p-4 rounded-lg"
                :class="`agent-${event.agent.toLowerCase()}`"
              >
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center space-x-2">
                    <span class="text-lg">{{ event.icon }}</span>
                    <span class="font-medium">{{ event.agent }}</span>
                  </div>
                  <span class="text-xs text-gray-400">{{ event.timestamp }}</span>
                </div>
                <p class="text-sm text-gray-300 mb-2">{{ event.description }}</p>
                <div class="flex items-center justify-between text-xs">
                  <span class="text-gray-400">IQ Change: {{ event.iqChange }}</span>
                  <span class="text-gray-400">Runes Added: {{ event.runesAdded }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Agent Analysis -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Rune Injection History -->
      <div class="glass-panel p-6">
        <h2 class="futuristic-subtitle text-2xl mb-6">Rune Injection History</h2>
        <div class="space-y-4">
          <div
            v-for="injection in runeInjections"
            :key="injection.id"
            class="glass-panel p-4 rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-lg">⚡</span>
                <span class="font-medium">{{ injection.runeName }}</span>
              </div>
              <span class="text-xs text-gray-400">{{ injection.timestamp }}</span>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ injection.description }}</p>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-400">Target: {{ injection.targetAgent }}</span>
              <span class="text-gray-400">Efficiency: {{ injection.efficiency }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Fallback Usage Analysis -->
      <div class="glass-panel p-6">
        <h2 class="futuristic-subtitle text-2xl mb-6">Fallback Usage Analysis</h2>
        <div class="space-y-4">
          <div
            v-for="fallback in fallbackUsage"
            :key="fallback.id"
            class="glass-panel p-4 rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-lg">⚠️</span>
                <span class="font-medium">{{ fallback.agent }}</span>
              </div>
              <span class="text-xs text-gray-400">{{ fallback.timestamp }}</span>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ fallback.reason }}</p>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-400">Fallback Type: {{ fallback.type }}</span>
              <span class="text-gray-400">Resolution: {{ fallback.resolution }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Performance Metrics -->
    <div class="mb-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Performance Metrics</h2>
      <div class="glass-panel p-6">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="text-center">
            <div class="text-3xl font-bold text-white mb-2">{{ performanceMetrics.totalTasks }}</div>
            <div class="text-sm text-gray-300">Total Tasks</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-green-400 mb-2">{{ performanceMetrics.successRate }}%</div>
            <div class="text-sm text-gray-300">Success Rate</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-blue-400 mb-2">{{ performanceMetrics.avgResponseTime }}s</div>
            <div class="text-sm text-gray-300">Avg Response Time</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-purple-400 mb-2">{{ performanceMetrics.totalRunes }}</div>
            <div class="text-sm text-gray-300">Total Runes</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Agent Comparison -->
    <div>
      <h2 class="futuristic-subtitle text-2xl mb-6">Agent Comparison</h2>
      <div class="glass-panel p-6">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-700">
                <th class="text-left p-3 text-sm font-medium">Agent</th>
                <th class="text-left p-3 text-sm font-medium">IQ</th>
                <th class="text-left p-3 text-sm font-medium">Tasks</th>
                <th class="text-left p-3 text-sm font-medium">Success Rate</th>
                <th class="text-left p-3 text-sm font-medium">Runes</th>
                <th class="text-left p-3 text-sm font-medium">Fallbacks</th>
                <th class="text-left p-3 text-sm font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="agent in agents"
                :key="agent.name"
                class="border-b border-gray-800"
              >
                <td class="p-3">
                  <div class="flex items-center space-x-2">
                    <span class="text-lg">{{ agent.icon }}</span>
                    <span class="font-medium">{{ agent.name }}</span>
                  </div>
                </td>
                <td class="p-3">
                  <div class="flex items-center space-x-2">
                    <span class="font-medium">{{ agent.iq }}</span>
                    <div class="iq-bar w-16" :style="{ width: agent.iq + '%' }"></div>
                  </div>
                </td>
                <td class="p-3">{{ agent.tasksCompleted }}</td>
                <td class="p-3">
                  <span class="text-green-400">{{ agent.successRate }}%</span>
                </td>
                <td class="p-3">{{ agent.activeRunes }}</td>
                <td class="p-3">
                  <span class="text-yellow-400">{{ agent.fallbacks }}</span>
                </td>
                <td class="p-3">
                  <div class="flex space-x-2">
                    <button
                      @click="upgradeAgent(agent.name)"
                      class="glass-panel px-3 py-1 rounded text-xs hover:neon-border transition-all duration-300"
                    >
                      Upgrade
                    </button>
                    <button
                      @click="reviewRuneTrail(agent.name)"
                      class="glass-panel px-3 py-1 rounded text-xs hover:neon-border transition-all duration-300"
                    >
                      Review
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Agents',
  setup() {
    const agents = ref([
      {
        name: 'Whis',
        icon: '🧠',
        role: 'AI Brain',
        status: 'online',
        iq: 85,
        activeRunes: 23,
        tasksCompleted: 1247,
        successRate: 96.8,
        fallbacks: 3
      },
      {
        name: 'Katie',
        icon: '⚓',
        role: 'Kubernetes',
        status: 'online',
        iq: 78,
        activeRunes: 18,
        tasksCompleted: 892,
        successRate: 94.2,
        fallbacks: 5
      },
      {
        name: 'Igris',
        icon: '🏗️',
        role: 'Platform Engineering',
        status: 'online',
        iq: 92,
        activeRunes: 31,
        tasksCompleted: 1567,
        successRate: 98.1,
        fallbacks: 2
      },
      {
        name: 'Ficknury',
        icon: '🎯',
        role: 'Task Router',
        status: 'online',
        iq: 88,
        activeRunes: 15,
        tasksCompleted: 2103,
        successRate: 97.5,
        fallbacks: 4
      }
    ])

    const domains = ref([
      {
        name: 'Infrastructure',
        description: 'Deployment and configuration'
      },
      {
        name: 'Security',
        description: 'Audit and compliance'
      },
      {
        name: 'Monitoring',
        description: 'Observability and alerts'
      },
      {
        name: 'Automation',
        description: 'CI/CD and workflows'
      }
    ])

    const evolutionEvents = ref([
      {
        id: 1,
        agent: 'Whis',
        icon: '🧠',
        description: 'Enhanced transcript processing with 15% accuracy improvement',
        iqChange: '+5',
        runesAdded: 3,
        timestamp: '2h ago'
      },
      {
        id: 2,
        agent: 'Katie',
        icon: '⚓',
        description: 'New Kubernetes deployment pattern learned',
        iqChange: '+3',
        runesAdded: 2,
        timestamp: '4h ago'
      },
      {
        id: 3,
        agent: 'Igris',
        icon: '🏗️',
        description: 'Terraform module optimization completed',
        iqChange: '+7',
        runesAdded: 4,
        timestamp: '6h ago'
      }
    ])

    const runeInjections = ref([
      {
        id: 1,
        runeName: 'DeployRune',
        description: 'Automated deployment pattern for Kubernetes',
        targetAgent: 'Katie',
        efficiency: 88,
        timestamp: '2h ago'
      },
      {
        id: 2,
        runeName: 'SecurityAuditor',
        description: 'Automated security policy validation',
        targetAgent: 'Igris',
        efficiency: 95,
        timestamp: '4h ago'
      },
      {
        id: 3,
        runeName: 'TranscriptProcessor',
        description: 'Enhanced text processing and analysis',
        targetAgent: 'Whis',
        efficiency: 92,
        timestamp: '6h ago'
      }
    ])

    const fallbackUsage = ref([
      {
        id: 1,
        agent: 'Katie',
        reason: 'Insufficient permissions for cluster modification',
        type: 'Manual Review',
        resolution: 'Admin approval granted',
        timestamp: '3h ago'
      },
      {
        id: 2,
        agent: 'Igris',
        reason: 'Complex infrastructure change requiring human oversight',
        type: 'Semi-Auto',
        resolution: 'Human validation completed',
        timestamp: '5h ago'
      }
    ])

    const performanceMetrics = ref({
      totalTasks: 5809,
      successRate: 96.7,
      avgResponseTime: 2.3,
      totalRunes: 87
    })

    const getDomainConfidence = (agentName, domainName) => {
      // Mock confidence data - in real app this would come from API
      const confidenceMap = {
        'Whis': { 'Infrastructure': 75, 'Security': 85, 'Monitoring': 90, 'Automation': 80 },
        'Katie': { 'Infrastructure': 95, 'Security': 70, 'Monitoring': 85, 'Automation': 75 },
        'Igris': { 'Infrastructure': 98, 'Security': 92, 'Monitoring': 88, 'Automation': 90 },
        'Ficknury': { 'Infrastructure': 85, 'Security': 80, 'Monitoring': 75, 'Automation': 95 }
      }
      return confidenceMap[agentName]?.[domainName] || 0
    }

    const upgradeAgent = (agentName) => {
      console.log(`Upgrading agent: ${agentName}`)
      // Implement upgrade logic
    }

    const reviewRuneTrail = (agentName) => {
      console.log(`Reviewing rune trail for: ${agentName}`)
      // Implement review logic
    }

    return {
      agents,
      domains,
      evolutionEvents,
      runeInjections,
      fallbackUsage,
      performanceMetrics,
      getDomainConfidence,
      upgradeAgent,
      reviewRuneTrail
    }
  }
}
</script>

<style scoped>
.agents-container {
  max-width: 1400px;
  margin: 0 auto;
}

/* Table styling */
table {
  border-collapse: separate;
  border-spacing: 0;
}

th {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

td, th {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

tr:hover {
  background: rgba(255, 255, 255, 0.02);
}
</style> 