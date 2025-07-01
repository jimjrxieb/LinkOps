<template>
  <div class="igris-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">Igris Platform Engineering</h1>
      <p class="text-gray-300">Infrastructure automation and platform management</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Current Capabilities -->
      <div class="lg:col-span-2">
        <div class="glass-panel p-6">
          <h2 class="futuristic-subtitle text-2xl mb-6">Current Capabilities</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="capability in capabilities"
              :key="capability.id"
              class="glass-panel p-4 rounded-lg agent-igris"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="text-lg">{{ capability.icon }}</span>
                <span class="text-xs" :class="statusColor(capability.status)">
                  {{ capability.status }}
                </span>
              </div>
              <h3 class="font-medium mb-1">{{ capability.name }}</h3>
              <p class="text-sm text-gray-300 mb-2">{{ capability.description }}</p>
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-400">Confidence: {{ capability.confidence }}%</span>
                <div class="iq-bar w-16" :style="{ width: capability.confidence + '%' }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Enhanced Runes Timeline -->
        <div class="glass-panel p-6 mt-6">
          <h2 class="futuristic-subtitle text-2xl mb-6">Enhanced Runes Over Time</h2>
          <div class="space-y-4">
            <div
              v-for="rune in enhancedRunes"
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
                <span class="text-gray-400">Domain: {{ rune.domain }}</span>
                <span class="text-gray-400">Efficiency: {{ rune.efficiency }}%</span>
              </div>
              <div class="mt-2 flex items-center space-x-2">
                <span class="text-xs">Before:</span>
                <div class="iq-bar w-16" :style="{ width: rune.beforeEfficiency + '%' }"></div>
                <span class="text-xs">{{ rune.beforeEfficiency }}%</span>
                <span class="text-xs">→</span>
                <div class="iq-bar w-16" :style="{ width: rune.efficiency + '%' }"></div>
                <span class="text-xs">{{ rune.efficiency }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Simulation Panel -->
      <div class="space-y-6">
        <!-- Run Simulation -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Run Simulation</h3>
          <form @submit.prevent="runSimulation" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Simulation Type
              </label>
              <select
                v-model="simulationForm.type"
                class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
              >
                <option value="terraform-plan">Terraform Plan</option>
                <option value="infrastructure-audit">Infrastructure Audit</option>
                <option value="cost-optimization">Cost Optimization</option>
                <option value="security-scan">Security Scan</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Environment
              </label>
              <select
                v-model="simulationForm.environment"
                class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
              >
                <option value="dev">Development</option>
                <option value="staging">Staging</option>
                <option value="production">Production</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">
                Parameters (JSON)
              </label>
              <textarea
                v-model="simulationForm.parameters"
                rows="4"
                class="w-full glass-panel p-3 rounded-lg border border-gray-600 bg-transparent text-white placeholder-gray-400 focus:border-slate-500 focus:ring-1 focus:ring-slate-500"
                placeholder='{"region": "us-west-2", "instance_type": "t3.medium"}'
              ></textarea>
            </div>
            <button
              type="submit"
              :disabled="isRunningSimulation"
              class="w-full glass-panel py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300 disabled:opacity-50 agent-igris"
            >
              <span v-if="isRunningSimulation">🔄 Running...</span>
              <span v-else>🚀 Run Simulation</span>
            </button>
          </form>
        </div>

        <!-- Simulation Results -->
        <div v-if="simulationResults" class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Simulation Results</h3>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm">Status:</span>
              <span class="text-sm font-medium" :class="statusColor(simulationResults.status)">
                {{ simulationResults.status }}
              </span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm">Duration:</span>
              <span class="text-sm text-gray-300">{{ simulationResults.duration }}s</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm">Confidence:</span>
              <div class="flex items-center space-x-2">
                <div class="w-20 h-2 bg-gray-700 rounded">
                  <div 
                    class="h-full bg-slate-500 rounded" 
                    :style="{ width: simulationResults.confidence + '%' }"
                  ></div>
                </div>
                <span class="text-xs">{{ simulationResults.confidence }}%</span>
              </div>
            </div>
            <div class="glass-panel p-3 rounded-lg">
              <div class="text-sm text-gray-300">{{ simulationResults.summary }}</div>
            </div>
          </div>
        </div>

        <!-- Agent Stats -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Agent Statistics</h3>
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-sm">Total Simulations:</span>
              <span class="text-sm font-medium">{{ agentStats.totalSimulations }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm">Success Rate:</span>
              <span class="text-sm font-medium text-green-400">{{ agentStats.successRate }}%</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm">Avg Response Time:</span>
              <span class="text-sm text-gray-300">{{ agentStats.avgResponseTime }}s</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm">Active Runes:</span>
              <span class="text-sm font-medium">{{ agentStats.activeRunes }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activities -->
    <div class="mt-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Recent Activities</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="activity in recentActivities"
          :key="activity.id"
          class="glass-panel p-4 rounded-lg"
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center space-x-2">
              <span class="text-lg">{{ activity.icon }}</span>
              <span class="font-medium">{{ activity.type }}</span>
            </div>
            <span class="text-xs text-gray-400">{{ activity.timestamp }}</span>
          </div>
          <p class="text-sm text-gray-300 mb-2">{{ activity.description }}</p>
          <div class="flex items-center justify-between text-xs">
            <span class="text-gray-400">{{ activity.environment }}</span>
            <span :class="statusColor(activity.status)">{{ activity.status }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'Igris',
  setup() {
    const simulationForm = ref({
      type: 'terraform-plan',
      environment: 'dev',
      parameters: ''
    })

    const isRunningSimulation = ref(false)
    const simulationResults = ref(null)

    const capabilities = ref([
      {
        id: 1,
        name: 'Terraform Automation',
        description: 'Infrastructure as Code deployment and management',
        icon: '🏗️',
        status: 'active',
        confidence: 95
      },
      {
        id: 2,
        name: 'Cost Optimization',
        description: 'Resource usage analysis and cost reduction',
        icon: '💰',
        status: 'active',
        confidence: 88
      },
      {
        id: 3,
        name: 'Security Scanning',
        description: 'Infrastructure security assessment and compliance',
        icon: '🔒',
        status: 'active',
        confidence: 92
      },
      {
        id: 4,
        name: 'Performance Monitoring',
        description: 'System performance analysis and optimization',
        icon: '📊',
        status: 'learning',
        confidence: 75
      }
    ])

    const enhancedRunes = ref([
      {
        id: 1,
        name: 'TerraformOptimizer',
        description: 'Enhanced Terraform plan analysis with cost prediction',
        domain: 'Infrastructure',
        efficiency: 95,
        beforeEfficiency: 78,
        timestamp: '1d ago'
      },
      {
        id: 2,
        name: 'SecurityAuditor',
        description: 'Automated security policy validation and enforcement',
        domain: 'Security',
        efficiency: 92,
        beforeEfficiency: 65,
        timestamp: '3d ago'
      },
      {
        id: 3,
        name: 'CostAnalyzer',
        description: 'Intelligent cost optimization recommendations',
        domain: 'Finance',
        efficiency: 88,
        beforeEfficiency: 72,
        timestamp: '5d ago'
      }
    ])

    const agentStats = ref({
      totalSimulations: 1247,
      successRate: 96.8,
      avgResponseTime: 2.3,
      activeRunes: 23
    })

    const recentActivities = ref([
      {
        id: 1,
        type: 'Terraform Plan',
        icon: '🏗️',
        description: 'Deployed new VPC configuration to production',
        environment: 'Production',
        status: 'completed',
        timestamp: '2h ago'
      },
      {
        id: 2,
        type: 'Security Scan',
        icon: '🔒',
        description: 'Identified 3 security vulnerabilities in staging',
        environment: 'Staging',
        status: 'completed',
        timestamp: '4h ago'
      },
      {
        id: 3,
        type: 'Cost Analysis',
        icon: '💰',
        description: 'Optimized EC2 instance types for 15% cost reduction',
        environment: 'Development',
        status: 'processing',
        timestamp: '6h ago'
      }
    ])

    const runSimulation = async () => {
      isRunningSimulation.value = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        simulationResults.value = {
          status: 'completed',
          duration: 2.3,
          confidence: 94,
          summary: 'Terraform plan completed successfully. 3 resources will be created, 2 modified, 0 destroyed. Estimated cost: $45.20/month.'
        }
      } catch (error) {
        console.error('Error running simulation:', error)
        simulationResults.value = {
          status: 'failed',
          duration: 0,
          confidence: 0,
          summary: 'Simulation failed due to configuration error.'
        }
      } finally {
        isRunningSimulation.value = false
      }
    }

    const statusColor = (status) => {
      const colors = {
        active: 'text-green-400',
        learning: 'text-yellow-400',
        completed: 'text-green-400',
        processing: 'text-blue-400',
        failed: 'text-red-400'
      }
      return colors[status] || 'text-gray-400'
    }

    return {
      simulationForm,
      isRunningSimulation,
      simulationResults,
      capabilities,
      enhancedRunes,
      agentStats,
      recentActivities,
      runSimulation,
      statusColor
    }
  }
}
</script>

<style scoped>
.igris-container {
  max-width: 1400px;
  margin: 0 auto;
}
</style> 