<template>
  <div class="katie-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">Katie Kubernetes Agent</h1>
      <p class="text-gray-300">Kubernetes orchestration and cluster management</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Tasks Handled -->
      <div class="glass-panel p-6">
        <h2 class="futuristic-subtitle text-2xl mb-6">Tasks Handled</h2>
        <div class="space-y-4">
          <div
            v-for="task in handledTasks"
            :key="task.id"
            class="glass-panel p-4 rounded-lg agent-katie"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-lg">{{ task.icon }}</span>
                <span class="font-medium">{{ task.type }}</span>
              </div>
              <span class="text-xs" :class="statusColor(task.status)">
                {{ task.status }}
              </span>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ task.description }}</p>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-400">Cluster: {{ task.cluster }}</span>
              <span class="text-gray-400">{{ task.timestamp }}</span>
            </div>
            <div class="mt-2 flex items-center space-x-2">
              <span class="text-xs">Success Rate:</span>
              <div class="iq-bar w-16" :style="{ width: task.successRate + '%' }"></div>
              <span class="text-xs">{{ task.successRate }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- K8s YAML Visualizer -->
      <div class="glass-panel p-6">
        <h2 class="futuristic-subtitle text-2xl mb-6">K8s YAML Visualizer</h2>
        <div class="space-y-4">
          <div class="flex space-x-2 mb-4">
            <button
              v-for="resource in k8sResources"
              :key="resource.type"
              @click="selectedResource = resource.type"
              class="glass-panel px-4 py-2 rounded-lg text-sm transition-all duration-300"
              :class="selectedResource === resource.type ? 'neon-border agent-katie' : 'hover:neon-border'"
            >
              {{ resource.type }}
            </button>
          </div>
          
          <div v-if="selectedResource" class="glass-panel p-4 rounded-lg">
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium">{{ selectedResource }}</span>
              <span class="text-xs text-gray-400">{{ getResourceCount(selectedResource) }} instances</span>
            </div>
            <div class="space-y-2">
              <div
                v-for="resource in getResourcesByType(selectedResource)"
                :key="resource.name"
                class="glass-panel p-3 rounded-lg"
              >
                <div class="flex items-center justify-between">
                  <span class="text-sm font-medium">{{ resource.name }}</span>
                  <span class="text-xs" :class="statusColor(resource.status)">
                    {{ resource.status }}
                  </span>
                </div>
                <div class="text-xs text-gray-300 mt-1">
                  Namespace: {{ resource.namespace }} | Age: {{ resource.age }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Agent Logic Tree -->
    <div class="mt-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Agent Logic Tree</h2>
      <div class="glass-panel p-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="text-3xl mb-2">📄</div>
            <h3 class="futuristic-subtitle text-lg mb-2">YAML Input</h3>
            <p class="text-sm text-gray-300 mb-4">Parse and validate Kubernetes manifests</p>
            <div class="iq-bar mx-auto w-24" :style="{ width: logicTree.yaml + '%' }"></div>
            <div class="text-xs text-gray-400 mt-1">{{ logicTree.yaml }}% accuracy</div>
          </div>
          
          <div class="text-center">
            <div class="text-3xl mb-2">⚡</div>
            <h3 class="futuristic-subtitle text-lg mb-2">Action Decision</h3>
            <p class="text-sm text-gray-300 mb-4">Determine optimal deployment strategy</p>
            <div class="iq-bar mx-auto w-24" :style="{ width: logicTree.action + '%' }"></div>
            <div class="text-xs text-gray-400 mt-1">{{ logicTree.action }}% confidence</div>
          </div>
          
          <div class="text-center">
            <div class="text-3xl mb-2">✅</div>
            <h3 class="futuristic-subtitle text-lg mb-2">Result Validation</h3>
            <p class="text-sm text-gray-300 mb-4">Verify deployment success and health</p>
            <div class="iq-bar mx-auto w-24" :style="{ width: logicTree.result + '%' }"></div>
            <div class="text-xs text-gray-400 mt-1">{{ logicTree.result }}% success rate</div>
          </div>
        </div>
        
        <!-- Logic Flow Visualization -->
        <div class="mt-8 relative">
          <div class="flex items-center justify-center space-x-8">
            <div class="text-center">
              <div class="glass-panel p-4 rounded-full w-16 h-16 mx-auto mb-2 flex items-center justify-center">
                <span class="text-lg">📄</span>
              </div>
              <div class="text-xs">Input</div>
            </div>
            <div class="flex-1 h-1 bg-gradient-to-r from-blue-500 to-cyan-500 rounded"></div>
            <div class="text-center">
              <div class="glass-panel p-4 rounded-full w-16 h-16 mx-auto mb-2 flex items-center justify-center">
                <span class="text-lg">⚡</span>
              </div>
              <div class="text-xs">Process</div>
            </div>
            <div class="flex-1 h-1 bg-gradient-to-r from-cyan-500 to-green-500 rounded"></div>
            <div class="text-center">
              <div class="glass-panel p-4 rounded-full w-16 h-16 mx-auto mb-2 flex items-center justify-center">
                <span class="text-lg">✅</span>
              </div>
              <div class="text-xs">Output</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Helm Chart Viewer -->
    <div class="mt-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">Helm Chart Viewer</h2>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Chart List -->
        <div class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">Available Charts</h3>
          <div class="space-y-3">
            <div
              v-for="chart in helmCharts"
              :key="chart.name"
              @click="selectedChart = chart"
              class="glass-panel p-4 rounded-lg cursor-pointer hover:neon-border transition-all duration-300"
              :class="selectedChart?.name === chart.name ? 'neon-border agent-katie' : ''"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium">{{ chart.name }}</span>
                <span class="text-xs text-gray-400">v{{ chart.version }}</span>
              </div>
              <p class="text-sm text-gray-300 mb-2">{{ chart.description }}</p>
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-400">{{ chart.repository }}</span>
                <span class="text-gray-400">{{ chart.lastUpdated }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Chart Details -->
        <div v-if="selectedChart" class="glass-panel p-6">
          <h3 class="futuristic-subtitle text-xl mb-4">{{ selectedChart.name }} Details</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Chart Information</label>
              <div class="glass-panel p-4 rounded-lg space-y-2">
                <div class="flex justify-between">
                  <span class="text-sm">Version:</span>
                  <span class="text-sm font-medium">{{ selectedChart.version }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm">Repository:</span>
                  <span class="text-sm text-gray-300">{{ selectedChart.repository }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm">Last Updated:</span>
                  <span class="text-sm text-gray-300">{{ selectedChart.lastUpdated }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-sm">Downloads:</span>
                  <span class="text-sm text-gray-300">{{ selectedChart.downloads }}</span>
                </div>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-300 mb-2">Values Preview</label>
              <div class="glass-panel p-4 rounded-lg">
                <pre class="text-xs text-gray-300 overflow-x-auto">{{ selectedChart.valuesPreview }}</pre>
              </div>
            </div>

            <div class="flex space-x-4">
              <button class="flex-1 glass-panel py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300 agent-katie">
                📊 View Values
              </button>
              <button class="flex-1 glass-panel py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300 agent-katie">
                🚀 Deploy Chart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- K8s Troubleshooting Log -->
    <div class="mt-8">
      <h2 class="futuristic-subtitle text-2xl mb-6">K8s Troubleshooting Log</h2>
      <div class="glass-panel p-6">
        <div class="space-y-4">
          <div
            v-for="log in troubleshootingLogs"
            :key="log.id"
            class="glass-panel p-4 rounded-lg"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center space-x-2">
                <span class="text-lg">{{ log.icon }}</span>
                <span class="font-medium">{{ log.type }}</span>
              </div>
              <span class="text-xs text-gray-400">{{ log.timestamp }}</span>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ log.description }}</p>
            <div class="flex items-center justify-between text-xs">
              <span class="text-gray-400">Namespace: {{ log.namespace }}</span>
              <span :class="severityColor(log.severity)">{{ log.severity }}</span>
            </div>
            <div v-if="log.solution" class="mt-2 glass-panel p-3 rounded-lg">
              <div class="text-xs text-gray-400 mb-1">Solution:</div>
              <div class="text-sm text-gray-300">{{ log.solution }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'Katie',
  setup() {
    const selectedResource = ref('')
    const selectedChart = ref(null)

    const handledTasks = ref([
      {
        id: 1,
        type: 'Deployment',
        icon: '🚀',
        description: 'Deployed Prometheus monitoring stack to production cluster',
        cluster: 'prod-cluster-1',
        status: 'completed',
        successRate: 95,
        timestamp: '2h ago'
      },
      {
        id: 2,
        type: 'Scaling',
        icon: '📈',
        description: 'Scaled frontend deployment from 3 to 5 replicas',
        cluster: 'staging-cluster',
        status: 'completed',
        successRate: 100,
        timestamp: '4h ago'
      },
      {
        id: 3,
        type: 'Rollback',
        icon: '🔄',
        description: 'Rolled back failed deployment to previous version',
        cluster: 'prod-cluster-2',
        status: 'completed',
        successRate: 88,
        timestamp: '6h ago'
      }
    ])

    const k8sResources = ref([
      { type: 'Pods', count: 156 },
      { type: 'Deployments', count: 23 },
      { type: 'Services', count: 18 },
      { type: 'ConfigMaps', count: 12 },
      { type: 'Secrets', count: 8 }
    ])

    const resourceInstances = ref({
      'Pods': [
        { name: 'frontend-abc123', namespace: 'default', status: 'Running', age: '2h' },
        { name: 'backend-def456', namespace: 'default', status: 'Running', age: '4h' },
        { name: 'monitoring-ghi789', namespace: 'monitoring', status: 'Running', age: '1d' }
      ],
      'Deployments': [
        { name: 'frontend', namespace: 'default', status: 'Available', age: '2h' },
        { name: 'backend', namespace: 'default', status: 'Available', age: '4h' },
        { name: 'prometheus', namespace: 'monitoring', status: 'Available', age: '1d' }
      ],
      'Services': [
        { name: 'frontend-service', namespace: 'default', status: 'Active', age: '2h' },
        { name: 'backend-service', namespace: 'default', status: 'Active', age: '4h' }
      ]
    })

    const logicTree = ref({
      yaml: 98,
      action: 92,
      result: 96
    })

    const helmCharts = ref([
      {
        name: 'prometheus',
        version: '25.8.0',
        description: 'Prometheus monitoring and alerting system',
        repository: 'prometheus-community',
        lastUpdated: '2024-01-15',
        downloads: '1.2M',
        valuesPreview: `replicaCount: 1
image:
  repository: prom/prometheus
  tag: v2.45.0
service:
  type: ClusterIP
  port: 9090`
      },
      {
        name: 'nginx-ingress',
        version: '9.7.0',
        description: 'NGINX Ingress Controller for Kubernetes',
        repository: 'ingress-nginx',
        lastUpdated: '2024-01-10',
        downloads: '2.1M',
        valuesPreview: `controller:
  replicaCount: 2
  service:
    type: LoadBalancer
  resources:
    requests:
      cpu: 100m
      memory: 128Mi`
      }
    ])

    const troubleshootingLogs = ref([
      {
        id: 1,
        type: 'Pod Crash',
        icon: '💥',
        description: 'Frontend pod crashed due to memory limit exceeded',
        namespace: 'default',
        severity: 'high',
        timestamp: '1h ago',
        solution: 'Increased memory limits from 512Mi to 1Gi and added resource requests'
      },
      {
        id: 2,
        type: 'Service Unreachable',
        icon: '🔌',
        description: 'Backend service not responding on port 8080',
        namespace: 'default',
        severity: 'medium',
        timestamp: '3h ago',
        solution: 'Fixed port configuration in service definition'
      },
      {
        id: 3,
        type: 'Image Pull Error',
        icon: '📦',
        description: 'Failed to pull image due to authentication issues',
        namespace: 'monitoring',
        severity: 'low',
        timestamp: '5h ago',
        solution: 'Updated image pull secret with correct credentials'
      }
    ])

    const getResourceCount = (type) => {
      const resource = k8sResources.value.find(r => r.type === type)
      return resource ? resource.count : 0
    }

    const getResourcesByType = (type) => {
      return resourceInstances.value[type] || []
    }

    const statusColor = (status) => {
      const colors = {
        completed: 'text-green-400',
        running: 'text-blue-400',
        available: 'text-green-400',
        active: 'text-green-400',
        failed: 'text-red-400',
        pending: 'text-yellow-400'
      }
      return colors[status] || 'text-gray-400'
    }

    const severityColor = (severity) => {
      const colors = {
        high: 'text-red-400',
        medium: 'text-yellow-400',
        low: 'text-blue-400'
      }
      return colors[severity] || 'text-gray-400'
    }

    return {
      selectedResource,
      selectedChart,
      handledTasks,
      k8sResources,
      resourceInstances,
      logicTree,
      helmCharts,
      troubleshootingLogs,
      getResourceCount,
      getResourcesByType,
      statusColor,
      severityColor
    }
  }
}
</script>

<style scoped>
.katie-container {
  max-width: 1400px;
  margin: 0 auto;
}
</style> 