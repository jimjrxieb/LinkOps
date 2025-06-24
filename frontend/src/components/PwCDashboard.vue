<template>
  <div class="p-6 bg-gray-900 min-h-screen holo-bg">
    <div class="max-w-7xl mx-auto">
      <!-- Header with Cyberpunk Effects -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white mb-2 neon-text glitch" data-text="AI Audit Platform">AI Audit Platform</h1>
        <p class="text-gray-400 typewriter">Compliance-driven AI agent orchestration and audit logging</p>
      </div>

      <!-- Compliance Overview Cards with Holographic Effects -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-gray-800 p-6 rounded-xl border border-blue-600 holo-hover pulse-cyber">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Total Audit Logs</p>
              <p class="text-2xl font-bold text-blue-400 neon-text">{{ stats.totalAuditLogs }}</p>
            </div>
            <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center status-indicator">
              <span class="text-xl">📊</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl border border-green-600 holo-hover pulse-cyber">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Approved Actions</p>
              <p class="text-2xl font-bold text-green-400 neon-text">{{ stats.approvedActions }}</p>
            </div>
            <div class="w-12 h-12 bg-green-600 rounded-full flex items-center justify-center status-indicator">
              <span class="text-xl">✅</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl border border-red-600 holo-hover pulse-cyber">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Security Findings</p>
              <p class="text-2xl font-bold text-red-400 neon-text">{{ stats.securityFindings }}</p>
            </div>
            <div class="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center status-indicator">
              <span class="text-xl">🛡️</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl border border-purple-600 holo-hover pulse-cyber">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-400">Active Agents</p>
              <p class="text-2xl font-bold text-purple-400 neon-text">{{ stats.activeAgents }}</p>
            </div>
            <div class="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center status-indicator">
              <span class="text-xl">🤖</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Compliance Tag Breakdown with Holographic Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div class="bg-gray-800 p-6 rounded-xl holo-card-3d">
          <h2 class="text-xl font-bold text-white mb-4 neon-text">Compliance Framework Coverage</h2>
          <div class="space-y-4">
            <div v-for="(count, tag) in stats.complianceTags" :key="tag" class="flex items-center justify-between holo-hover">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full mr-3" :class="getComplianceColor(tag)"></div>
                <span class="text-gray-300">{{ tag }}</span>
              </div>
              <span class="text-white font-semibold neon-text">{{ count }}</span>
            </div>
          </div>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl holo-card-3d">
          <h2 class="text-xl font-bold text-white mb-4 neon-text">Agent Activity</h2>
          <div class="space-y-4">
            <div v-for="(count, agent) in stats.agentActivity" :key="agent" class="flex items-center justify-between holo-hover">
              <div class="flex items-center">
                <div class="w-8 h-8 rounded-full mr-3 flex items-center justify-center text-sm font-bold status-indicator" :class="getAgentBgColor(agent)">
                  {{ getAgentInitial(agent) }}
                </div>
                <span class="text-gray-300 capitalize">{{ agent }}</span>
              </div>
              <span class="text-white font-semibold neon-text">{{ count }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Audit Logs with Cyberpunk Styling -->
      <div class="bg-gray-800 p-6 rounded-xl mb-8 holo-card-3d">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-white neon-text">Recent Audit Logs</h2>
          <div class="flex space-x-2">
            <select v-model="selectedAgent" class="bg-gray-700 text-white px-3 py-1 rounded text-sm border border-cyan-500 focus:border-cyan-300 focus:outline-none">
              <option value="">All Agents</option>
              <option value="auditguard">AuditGuard</option>
              <option value="ficknury">FickNury</option>
              <option value="whis">Whis</option>
              <option value="katie">Katie</option>
              <option value="igris">Igris</option>
              <option value="james">James</option>
            </select>
            <select v-model="selectedCompliance" class="bg-gray-700 text-white px-3 py-1 rounded text-sm border border-cyan-500 focus:border-cyan-300 focus:outline-none">
              <option value="">All Compliance</option>
              <option value="SOC2">SOC2</option>
              <option value="GDPR">GDPR</option>
              <option value="ISO27001">ISO27001</option>
              <option value="NIST">NIST</option>
            </select>
          </div>
        </div>

        <div class="space-y-4">
          <div v-for="log in filteredLogs" :key="log.id" class="bg-gray-700 p-4 rounded-lg border-l-4 holo-hover" :class="getLogBorderColor(log)">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="flex items-center mb-2">
                  <span class="text-sm font-semibold neon-text" :class="getAgentColor(log.agent)">{{ log.agent }}</span>
                  <span class="text-xs text-gray-400 ml-2">{{ formatDate(log.created_at) }}</span>
                  <div v-if="log.approved" class="ml-2 px-2 py-1 bg-green-600 text-white text-xs rounded pulse-cyber">Approved</div>
                  <div v-else-if="log.auto_approved" class="ml-2 px-2 py-1 bg-blue-600 text-white text-xs rounded pulse-cyber">Auto-Approved</div>
                </div>
                <p class="text-white font-medium mb-1">{{ log.action }}</p>
                <p class="text-gray-300 text-sm mb-2 terminal-text">{{ log.result }}</p>
                <div v-if="log.solution_path" class="text-green-300 text-sm">
                  <strong>Solution:</strong> {{ log.solution_path }}
                </div>
                <div v-if="log.compliance_tags" class="flex flex-wrap gap-1 mt-2">
                  <span v-for="tag in parseComplianceTags(log.compliance_tags)" :key="tag" 
                        class="px-2 py-1 bg-gray-600 text-white text-xs rounded border border-cyan-500">
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredLogs.length === 0" class="text-center py-8 text-gray-400">
          <div class="cyber-spinner mx-auto mb-4"></div>
          No audit logs found matching the selected filters.
        </div>
      </div>

      <!-- Quick Actions with Cyberpunk Buttons -->
      <div class="bg-gray-800 p-6 rounded-xl holo-card-3d">
        <h2 class="text-xl font-bold text-white mb-4 neon-text">Quick Actions</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button @click="runSecurityScan" class="cyber-button bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg transition-colors">
            🔍 Run Security Scan
          </button>
          <button @click="proposeNewAgent" class="cyber-button bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition-colors">
            🤖 Propose New Agent
          </button>
          <button @click="viewComplianceReport" class="cyber-button bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
            📋 Compliance Report
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const stats = ref({
  totalAuditLogs: 0,
  approvedActions: 0,
  securityFindings: 0,
  activeAgents: 0,
  complianceTags: {},
  agentActivity: {}
})

const auditLogs = ref([])
const selectedAgent = ref('')
const selectedCompliance = ref('')

const filteredLogs = computed(() => {
  let logs = auditLogs.value

  if (selectedAgent.value) {
    logs = logs.filter(log => log.agent === selectedAgent.value)
  }

  if (selectedCompliance.value) {
    logs = logs.filter(log => {
      if (!log.compliance_tags) return false
      const tags = parseComplianceTags(log.compliance_tags)
      return tags.includes(selectedCompliance.value)
    })
  }

  return logs.slice(0, 10) // Show last 10
})

const getComplianceColor = (tag) => {
  const colors = {
    'SOC2': 'bg-blue-500',
    'GDPR': 'bg-green-500',
    'ISO27001': 'bg-purple-500',
    'NIST': 'bg-yellow-500'
  }
  return colors[tag] || 'bg-gray-500'
}

const getAgentBgColor = (agent) => {
  const colors = {
    'auditguard': 'bg-red-600',
    'ficknury': 'bg-purple-600',
    'whis': 'bg-blue-600',
    'katie': 'bg-green-600',
    'igris': 'bg-purple-600',
    'james': 'bg-yellow-600'
  }
  return colors[agent] || 'bg-gray-600'
}

const getAgentColor = (agent) => {
  const colors = {
    'auditguard': 'text-red-400',
    'ficknury': 'text-purple-400',
    'whis': 'text-blue-400',
    'katie': 'text-green-400',
    'igris': 'text-purple-400',
    'james': 'text-yellow-400'
  }
  return colors[agent] || 'text-gray-400'
}

const getAgentInitial = (agent) => {
  return agent.charAt(0).toUpperCase()
}

const getLogBorderColor = (log) => {
  if (log.error_outcome) return 'border-red-500'
  if (log.approved || log.auto_approved) return 'border-green-500'
  return 'border-gray-500'
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString()
}

const parseComplianceTags = (tagsString) => {
  try {
    return JSON.parse(tagsString)
  } catch {
    return []
  }
}

const fetchStats = async () => {
  try {
    const [complianceRes, auditLogsRes] = await Promise.all([
      fetch('/api/compliance/stats'),
      fetch('/api/audit-logs?limit=100')
    ])

    const complianceData = await complianceRes.json()
    const auditLogsData = await auditLogsRes.json()

    stats.value = {
      totalAuditLogs: complianceData.total_approved_logs,
      approvedActions: complianceData.total_approved_logs,
      securityFindings: auditLogsData.logs.filter(log => log.agent === 'auditguard').length,
      activeAgents: Object.keys(complianceData.agent_breakdown).length,
      complianceTags: complianceData.compliance_tag_breakdown,
      agentActivity: complianceData.agent_breakdown
    }

    auditLogs.value = auditLogsData.logs
  } catch (error) {
    console.error('Failed to fetch PwC dashboard data:', error)
  }
}

const runSecurityScan = async () => {
  try {
    const response = await fetch('/api/auditguard/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scan_type: 'trivy',
        target: '/app',
        compliance_scope: ['SOC2', 'GDPR'],
        auto_approve: false
      })
    })
    
    if (response.ok) {
      await fetchStats() // Refresh stats
      alert('Security scan initiated successfully')
    }
  } catch (error) {
    console.error('Failed to run security scan:', error)
    alert('Failed to run security scan')
  }
}

const proposeNewAgent = async () => {
  try {
    const response = await fetch('/api/ficknury/propose-agent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        agent_name: 'new-security-agent',
        agent_type: 'new',
        intelligence_source: 'whis',
        reasoning: 'Repeated security scan patterns detected',
        capabilities: ['security', 'compliance', 'automation'],
        deployment_target: 'kubernetes',
        priority: 'high'
      })
    })
    
    if (response.ok) {
      await fetchStats() // Refresh stats
      alert('Agent proposal submitted successfully')
    }
  } catch (error) {
    console.error('Failed to propose agent:', error)
    alert('Failed to propose agent')
  }
}

const viewComplianceReport = () => {
  // This would open a detailed compliance report
  alert('Compliance report feature coming soon')
}

onMounted(() => {
  fetchStats()
})
</script> 