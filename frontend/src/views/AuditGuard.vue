<template>
  <div class="auditguard-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">🛡️ AuditGuard</h1>
      <p class="text-gray-300">Security & Compliance Warden</p>
    </div>

    <!-- Repository Audit Section -->
    <div class="glass-panel p-8 mb-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Repository Security Audit</h2>
      
      <!-- Repository Input -->
      <div class="mb-6">
        <label class="block text-sm font-medium mb-2">Repository URL</label>
        <div class="flex space-x-4">
          <input 
            v-model="repositoryUrl" 
            type="text" 
            placeholder="https://github.com/username/repository"
            class="flex-1 glass-panel p-3 rounded-lg border border-gray-600 focus:border-indigo-400 focus:outline-none"
          />
          <button 
            @click="runAudit" 
            :disabled="isAuditing || !repositoryUrl"
            class="glass-panel px-6 py-3 rounded-lg font-medium transition-all duration-300 disabled:opacity-50"
            :class="isAuditing ? 'animate-pulse' : 'hover:bg-indigo-600'"
          >
            <span v-if="!isAuditing">🔍 Run Audit</span>
            <span v-else>Auditing...</span>
          </button>
        </div>
      </div>

      <!-- Audit Results -->
      <div v-if="auditResults" class="space-y-6">
        <!-- Compliance Status -->
        <div class="compliance-status glass-panel p-6 rounded-lg">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-medium">Compliance Status</h3>
            <div class="flex items-center space-x-2">
              <div 
                class="w-4 h-4 rounded-full"
                :class="auditResults.compliance === 'compliant' ? 'bg-green-500' : 'bg-red-500'"
              ></div>
              <span class="font-medium" :class="auditResults.compliance === 'compliant' ? 'text-green-400' : 'text-red-400'">
                {{ auditResults.compliance === 'compliant' ? 'Compliant' : 'Non-Compliant' }}
              </span>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="text-center">
              <div class="text-2xl font-bold text-white mb-1">{{ auditResults.score }}/100</div>
              <div class="text-sm text-gray-400">Security Score</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-white mb-1">{{ auditResults.issues.length }}</div>
              <div class="text-sm text-gray-400">Issues Found</div>
            </div>
            <div class="text-center">
              <div class="text-2xl font-bold text-white mb-1">{{ auditResults.recommendations.length }}</div>
              <div class="text-sm text-gray-400">Recommendations</div>
            </div>
          </div>
        </div>

        <!-- Security Issues -->
        <div v-if="auditResults.issues.length > 0" class="glass-panel p-6 rounded-lg">
          <h3 class="text-xl font-medium mb-4">Security Issues</h3>
          <div class="space-y-3">
            <div 
              v-for="issue in auditResults.issues" 
              :key="issue.id"
              class="issue-item p-4 rounded-lg border-l-4"
              :class="{
                'border-red-500 bg-red-900/20': issue.severity === 'high',
                'border-yellow-500 bg-yellow-900/20': issue.severity === 'medium',
                'border-blue-500 bg-blue-900/20': issue.severity === 'low'
              }"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h4 class="font-medium mb-1">{{ issue.title }}</h4>
                  <p class="text-sm text-gray-300 mb-2">{{ issue.description }}</p>
                  <div class="flex items-center space-x-4 text-xs text-gray-400">
                    <span>Severity: {{ issue.severity }}</span>
                    <span>Category: {{ issue.category }}</span>
                    <span>File: {{ issue.file }}</span>
                  </div>
                </div>
                <div class="ml-4">
                  <span 
                    class="px-2 py-1 rounded text-xs font-medium"
                    :class="{
                      'bg-red-500 text-white': issue.severity === 'high',
                      'bg-yellow-500 text-black': issue.severity === 'medium',
                      'bg-blue-500 text-white': issue.severity === 'low'
                    }"
                  >
                    {{ issue.severity.toUpperCase() }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- GitOps Recommendations -->
        <div class="glass-panel p-6 rounded-lg">
          <h3 class="text-xl font-medium mb-4">GitOps Transformation Recommendations</h3>
          <div class="space-y-4">
            <div 
              v-for="rec in auditResults.recommendations" 
              :key="rec.id"
              class="recommendation-item p-4 rounded-lg border border-gray-600"
            >
              <div class="flex items-start space-x-3">
                <div class="text-2xl">{{ rec.icon }}</div>
                <div class="flex-1">
                  <h4 class="font-medium mb-1">{{ rec.title }}</h4>
                  <p class="text-sm text-gray-300 mb-2">{{ rec.description }}</p>
                  <div class="flex items-center space-x-2">
                    <span class="text-xs text-gray-400">Priority:</span>
                    <span 
                      class="px-2 py-1 rounded text-xs font-medium"
                      :class="{
                        'bg-red-500 text-white': rec.priority === 'high',
                        'bg-yellow-500 text-black': rec.priority === 'medium',
                        'bg-green-500 text-white': rec.priority === 'low'
                      }"
                    >
                      {{ rec.priority.toUpperCase() }}
                    </span>
                  </div>
                  <div v-if="rec.implementation" class="mt-3">
                    <details class="text-sm">
                      <summary class="cursor-pointer text-indigo-400 hover:text-indigo-300">
                        Implementation Steps
                      </summary>
                      <div class="mt-2 p-3 bg-gray-800 rounded">
                        <pre class="text-xs text-gray-300">{{ rec.implementation }}</pre>
                      </div>
                    </details>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Security Alerts -->
    <div class="glass-panel p-8 mb-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Security Alerts</h2>
      <div class="space-y-4">
        <div 
          v-for="alert in securityAlerts" 
          :key="alert.id"
          class="alert-item p-4 rounded-lg border-l-4"
          :class="{
            'border-red-500 bg-red-900/20': alert.level === 'critical',
            'border-yellow-500 bg-yellow-900/20': alert.level === 'warning',
            'border-blue-500 bg-blue-900/20': alert.level === 'info'
          }"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h4 class="font-medium mb-1">{{ alert.title }}</h4>
              <p class="text-sm text-gray-300">{{ alert.message }}</p>
              <div class="flex items-center space-x-4 mt-2 text-xs text-gray-400">
                <span>{{ alert.timestamp }}</span>
                <span>{{ alert.source }}</span>
              </div>
            </div>
            <div class="ml-4">
              <span 
                class="px-2 py-1 rounded text-xs font-medium"
                :class="{
                  'bg-red-500 text-white': alert.level === 'critical',
                  'bg-yellow-500 text-black': alert.level === 'warning',
                  'bg-blue-500 text-white': alert.level === 'info'
                }"
              >
                {{ alert.level.toUpperCase() }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Compliance Dashboard -->
    <div class="glass-panel p-8 mb-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Compliance Dashboard</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="text-center">
          <div class="text-3xl font-bold text-green-400 mb-2">85%</div>
          <div class="text-sm text-gray-300">SOC 2 Compliance</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-blue-400 mb-2">92%</div>
          <div class="text-sm text-gray-300">GDPR Compliance</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-yellow-400 mb-2">78%</div>
          <div class="text-sm text-gray-300">HIPAA Compliance</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-purple-400 mb-2">88%</div>
          <div class="text-sm text-gray-300">ISO 27001</div>
        </div>
      </div>
    </div>

    <!-- Audit Logs -->
    <div class="glass-panel p-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Audit Logs</h2>
      <div class="space-y-3 max-h-96 overflow-y-auto">
        <div 
          v-for="log in auditLogs" 
          :key="log.id"
          class="log-item p-3 rounded-lg border border-gray-600"
        >
          <div class="flex items-center justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-2">
                <span class="text-sm font-medium">{{ log.action }}</span>
                <span class="text-xs text-gray-400">by {{ log.user }}</span>
              </div>
              <p class="text-xs text-gray-300 mt-1">{{ log.description }}</p>
            </div>
            <div class="text-xs text-gray-400">{{ log.timestamp }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { auditguardService } from '@/services/api'

export default {
  name: 'AuditGuard',
  setup() {
    const repositoryUrl = ref('')
    const isAuditing = ref(false)
    const auditResults = ref(null)
    
    const securityAlerts = ref([
      {
        id: 1,
        title: 'Suspicious Login Attempt',
        message: 'Multiple failed login attempts detected from IP 192.168.1.100',
        level: 'warning',
        timestamp: '2 minutes ago',
        source: 'Authentication System'
      },
      {
        id: 2,
        title: 'Dependency Vulnerability',
        message: 'High severity vulnerability found in package lodash@4.17.15',
        level: 'critical',
        timestamp: '15 minutes ago',
        source: 'Dependency Scanner'
      },
      {
        id: 3,
        title: 'Configuration Drift',
        message: 'Infrastructure configuration has drifted from Git state',
        level: 'warning',
        timestamp: '1 hour ago',
        source: 'Infrastructure Monitor'
      }
    ])

    const auditLogs = ref([
      {
        id: 1,
        action: 'Repository Audit',
        user: 'system',
        description: 'Security audit completed for repository: github.com/example/repo',
        timestamp: '2 minutes ago'
      },
      {
        id: 2,
        action: 'Compliance Check',
        user: 'admin',
        description: 'SOC 2 compliance assessment initiated',
        timestamp: '1 hour ago'
      },
      {
        id: 3,
        action: 'Security Scan',
        user: 'system',
        description: 'Automated security scan completed - 3 issues found',
        timestamp: '3 hours ago'
      }
    ])

    const runAudit = async () => {
      if (!repositoryUrl.value) return
      
      isAuditing.value = true
      
      try {
        // Call AuditGuard API for repository scanning
        const response = await auditguardService.scanRepository(repositoryUrl.value)
        
        // Use the actual response from the API
        auditResults.value = response.data
        
        // Add to audit logs
        auditLogs.value.unshift({
          id: Date.now(),
          action: 'Repository Audit',
          user: 'system',
          description: `Security audit completed for repository: ${repositoryUrl.value}`,
          timestamp: 'Just now'
        })
        
      } catch (error) {
        console.error('Audit failed:', error)
        // Fallback to demo data if API fails
        auditResults.value = {
          compliance: 'non-compliant',
          score: 72,
          issues: [
            {
              id: 1,
              title: 'Exposed API Keys',
              description: 'API keys found in commit history',
              severity: 'high',
              category: 'Secrets Management',
              file: 'config/database.yml'
            },
            {
              id: 2,
              title: 'Weak Password Policy',
              description: 'No password complexity requirements enforced',
              severity: 'medium',
              category: 'Authentication',
              file: 'auth/policy.json'
            },
            {
              id: 3,
              title: 'Missing Security Headers',
              description: 'Security headers not configured in web server',
              severity: 'low',
              category: 'Web Security',
              file: 'nginx.conf'
            }
          ],
          recommendations: [
            {
              id: 1,
              title: 'Implement GitOps Workflow',
              description: 'Set up automated deployment pipeline with Git as source of truth',
              priority: 'high',
              icon: '🔄',
              implementation: `# Create GitHub Actions workflow
name: GitOps Deployment
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f k8s/
          kubectl rollout status deployment/app`
            },
            {
              id: 2,
              title: 'Add Security Scanning',
              description: 'Integrate automated security scanning in CI/CD pipeline',
              priority: 'high',
              icon: '🔍',
              implementation: `# Add to .github/workflows/security.yml
- name: Run Security Scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'fs'
    scan-ref: '.'
    format: 'sarif'
    output: 'trivy-results.sarif'`
            },
            {
              id: 3,
              title: 'Implement Infrastructure as Code',
              description: 'Convert manual infrastructure to Terraform/CloudFormation',
              priority: 'medium',
              icon: '🏗️',
              implementation: `# Example Terraform configuration
resource "aws_ecs_cluster" "main" {
  name = "production-cluster"
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}`
            }
          ]
        }
      } finally {
        isAuditing.value = false
      }
    }

    onMounted(async () => {
      // Load initial data
      try {
        const [logsResponse, alertsResponse] = await Promise.all([
          auditguardService.getAuditLogs(),
          auditguardService.getSecurityAlerts()
        ])
        
        if (logsResponse.data?.logs) {
          auditLogs.value = logsResponse.data.logs
        }
        
        if (alertsResponse.data?.alerts) {
          securityAlerts.value = alertsResponse.data.alerts
        }
      } catch (error) {
        console.error('Failed to load initial data:', error)
      }
    })

    return {
      repositoryUrl,
      isAuditing,
      auditResults,
      securityAlerts,
      auditLogs,
      runAudit
    }
  }
}
</script>

<style scoped>
.auditguard-container {
  max-width: 1400px;
  margin: 0 auto;
}

.issue-item, .recommendation-item, .alert-item, .log-item {
  transition: all 0.3s ease;
}

.issue-item:hover, .recommendation-item:hover, .alert-item:hover, .log-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.compliance-status {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  border: 1px solid rgba(99, 102, 241, 0.3);
}
</style>
