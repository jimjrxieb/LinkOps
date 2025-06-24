<template>
  <div class="p-6 text-white">
    <h1 class="text-2xl font-bold mb-6">🤖 Agent Intelligence Hub</h1>

    <!-- Agent Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      
      <!-- WHIS Agent -->
      <div class="bg-gray-900 p-4 rounded-xl shadow border border-blue-600">
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-2xl">🧠</div>
          <div class="ml-3">
            <h2 class="text-xl font-bold text-blue-400">Whis</h2>
            <p class="text-sm text-gray-400">AI Training & Learning</p>
          </div>
        </div>
        
        <div class="space-y-3">
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-blue-300 mb-2">🎯 Logic</h3>
            <ul class="text-xs text-gray-300 space-y-1">
              <li>• Processes sanitized data for training</li>
              <li>• Generates rune candidates</li>
              <li>• Manages approval workflow</li>
              <li>• Maintains knowledge base</li>
            </ul>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-blue-300 mb-2">💎 Orbs</h3>
            <div class="text-xs text-gray-300">
              <p>• Training Data: {{ whisStats.trainingData || 0 }}</p>
              <p>• Approved Runes: {{ whisStats.approvedRunes || 0 }}</p>
              <p>• Pending Review: {{ whisStats.pendingRunes || 0 }}</p>
            </div>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-blue-300 mb-2">⚡ Status</h3>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              <span class="text-xs text-green-400">Active</span>
            </div>
          </div>
        </div>
      </div>

      <!-- KATIE Agent -->
      <div class="bg-gray-900 p-4 rounded-xl shadow border border-green-600">
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center text-2xl">⚙️</div>
          <div class="ml-3">
            <h2 class="text-xl font-bold text-green-400">Katie</h2>
            <p class="text-sm text-gray-400">Kubernetes & DevOps</p>
          </div>
        </div>
        
        <div class="space-y-3">
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-green-300 mb-2">🎯 Logic</h3>
            <ul class="text-xs text-gray-300 space-y-1">
              <li>• Kubernetes cluster management</li>
              <li>• Deployment automation</li>
              <li>• Infrastructure scaling</li>
              <li>• Monitoring & alerting</li>
            </ul>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-green-300 mb-2">💎 Orbs</h3>
            <div class="text-xs text-gray-300">
              <p>• Clusters Managed: {{ katieStats.clusters || 0 }}</p>
              <p>• Deployments: {{ katieStats.deployments || 0 }}</p>
              <p>• Services Running: {{ katieStats.services || 0 }}</p>
            </div>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-green-300 mb-2">⚡ Status</h3>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              <span class="text-xs text-green-400">Active</span>
            </div>
          </div>
        </div>
      </div>

      <!-- IGRIS Agent -->
      <div class="bg-gray-900 p-4 rounded-xl shadow border border-purple-600">
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center text-2xl">🏗️</div>
          <div class="ml-3">
            <h2 class="text-xl font-bold text-purple-400">Igris</h2>
            <p class="text-sm text-gray-400">Infrastructure & Terraform</p>
          </div>
        </div>
        
        <div class="space-y-3">
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-purple-300 mb-2">🎯 Logic</h3>
            <ul class="text-xs text-gray-300 space-y-1">
              <li>• Infrastructure provisioning</li>
              <li>• Terraform state management</li>
              <li>• Cloud resource orchestration</li>
              <li>• Cost optimization</li>
            </ul>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-purple-300 mb-2">💎 Orbs</h3>
            <div class="text-xs text-gray-300">
              <p>• Environments: {{ igrisStats.environments || 0 }}</p>
              <p>• Resources Managed: {{ igrisStats.resources || 0 }}</p>
              <p>• Terraform States: {{ igrisStats.states || 0 }}</p>
            </div>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-purple-300 mb-2">⚡ Status</h3>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
              <span class="text-xs text-green-400">Active</span>
            </div>
          </div>
        </div>
      </div>

      <!-- AUDITGUARD Agent -->
      <div class="bg-gray-900 p-4 rounded-xl shadow border border-red-600">
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center text-2xl">🛡️</div>
          <div class="ml-3">
            <h2 class="text-xl font-bold text-red-400">AuditGuard</h2>
            <p class="text-sm text-gray-400">Security & Compliance</p>
          </div>
        </div>
        
        <div class="space-y-3">
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-red-300 mb-2">🎯 Logic</h3>
            <ul class="text-xs text-gray-300 space-y-1">
              <li>• Trivy vulnerability scanning</li>
              <li>• Bandit security linting</li>
              <li>• Checkov infrastructure scanning</li>
              <li>• Repository security audits</li>
            </ul>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-red-300 mb-2">💎 Compliance</h3>
            <div class="text-xs text-gray-300">
              <p>• SOC2: {{ auditGuardStats.soc2 || 0 }} scans</p>
              <p>• GDPR: {{ auditGuardStats.gdpr || 0 }} checks</p>
              <p>• ISO27001: {{ auditGuardStats.iso27001 || 0 }} audits</p>
            </div>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-red-300 mb-2">⚡ Status</h3>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
              <span class="text-xs text-red-400">Active</span>
            </div>
          </div>
        </div>
      </div>

      <!-- FICKNURY Agent -->
      <div class="bg-gray-900 p-4 rounded-xl shadow border border-purple-600">
        <div class="flex items-center mb-4">
          <div class="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center text-2xl">🎭</div>
          <div class="ml-3">
            <h2 class="text-xl font-bold text-purple-400">FickNury</h2>
            <p class="text-sm text-gray-400">Agent Orchestration</p>
          </div>
        </div>
        
        <div class="space-y-3">
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-purple-300 mb-2">🎯 Logic</h3>
            <ul class="text-xs text-gray-300 space-y-1">
              <li>• Agent creation & deployment</li>
              <li>• Intelligence-driven decisions</li>
              <li>• Multi-environment orchestration</li>
              <li>• Version management</li>
            </ul>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-purple-300 mb-2">💎 Deployments</h3>
            <div class="text-xs text-gray-300">
              <p>• Docker: {{ fickNuryStats.docker || 0 }} agents</p>
              <p>• Kubernetes: {{ fickNuryStats.kubernetes || 0 }} agents</p>
              <p>• Local: {{ fickNuryStats.local || 0 }} agents</p>
            </div>
          </div>
          
          <div class="bg-gray-800 p-3 rounded">
            <h3 class="text-sm font-semibold text-purple-300 mb-2">⚡ Status</h3>
            <div class="flex items-center">
              <div class="w-2 h-2 bg-purple-500 rounded-full mr-2"></div>
              <span class="text-xs text-purple-400">Active</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Runes Section -->
    <div class="mt-8">
      <h2 class="text-xl font-bold mb-4">📜 Recent Runes</h2>
      <div v-if="recentRunes.length === 0" class="text-gray-400 text-center py-8">
        No runes generated yet. Submit data to start training!
      </div>
      <div v-else class="space-y-4">
        <div v-for="rune in recentRunes" :key="rune.id" class="bg-gray-900 p-4 rounded-xl border border-gray-700">
          <div class="flex justify-between items-start mb-2">
            <div>
              <span class="text-sm font-semibold" :class="getAgentColor(rune.agent)">{{ rune.agent }}</span>
              <span class="text-xs text-gray-400 ml-2">{{ rune.origin }}</span>
            </div>
            <span class="text-xs text-gray-500">#{{ rune.id }}</span>
          </div>
          <pre class="text-xs bg-gray-800 p-2 rounded max-h-32 overflow-y-auto">{{ JSON.stringify(rune.content, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const whisStats = ref({})
const katieStats = ref({})
const igrisStats = ref({})
const auditGuardStats = ref({})
const fickNuryStats = ref({})
const recentRunes = ref([])

const getAgentColor = (agent) => {
  const colors = {
    'whis': 'text-blue-400',
    'katie': 'text-green-400', 
    'igris': 'text-purple-400',
    'james': 'text-yellow-400',
    'auditguard': 'text-red-400',
    'ficknury': 'text-purple-400'
  }
  return colors[agent] || 'text-gray-400'
}

const fetchAgentStats = async () => {
  try {
    // Fetch Whis stats from digest
    const digestRes = await fetch('/api/whis/digest')
    const digestData = await digestRes.json()
    
    whisStats.value = {
      trainingData: digestData.log_count,
      approvedRunes: digestData.runes_approved,
      pendingRunes: digestData.runes_pending
    }
    
    // Fetch compliance stats for AuditGuard
    const complianceRes = await fetch('/api/compliance/stats')
    const complianceData = await complianceRes.json()
    
    auditGuardStats.value = {
      soc2: complianceData.compliance_tag_breakdown?.SOC2 || 0,
      gdpr: complianceData.compliance_tag_breakdown?.GDPR || 0,
      iso27001: complianceData.compliance_tag_breakdown?.ISO27001 || 0
    }
    
    // Fetch agent status for FickNury
    const agentStatusRes = await fetch('/api/agents/status')
    const agentStatusData = await agentStatusRes.json()
    
    fickNuryStats.value = {
      docker: agentStatusData.docker_agents?.length || 0,
      kubernetes: agentStatusData.kubernetes_agents?.length || 0,
      local: agentStatusData.local_agents?.length || 0
    }
    
    // Fetch recent runes
    const runesRes = await fetch('/api/whis/approvals')
    const runesData = await runesRes.json()
    recentRunes.value = runesData.slice(0, 5) // Show last 5
    
  } catch (error) {
    console.error('Failed to fetch agent stats:', error)
  }
}

onMounted(fetchAgentStats)
</script>

<style scoped>
.agents-page {
  max-width: 1200px;
  margin: auto;
}
</style> 