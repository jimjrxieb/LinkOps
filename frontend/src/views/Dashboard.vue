<template>
  <div class="dashboard-container">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="futuristic-title text-4xl mb-2">Command Overview</h1>
      <p class="text-gray-300">System state and learning analytics</p>
    </div>

    <!-- System State Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div class="glass-panel p-6 agent-whis">
        <div class="flex items-center justify-between mb-4">
          <h3 class="futuristic-subtitle text-lg">Active Tasks</h3>
          <div class="status-indicator status-processing"></div>
        </div>
        <div class="text-3xl font-bold text-white mb-2">{{ systemState.activeTasks }}</div>
        <div class="text-sm text-gray-300">In processing queue</div>
        <div class="iq-bar mt-3" :style="{ width: systemState.taskProgress + '%' }"></div>
      </div>

      <div class="glass-panel p-6 agent-katie">
        <div class="flex items-center justify-between mb-4">
          <h3 class="futuristic-subtitle text-lg">Sanitized Inputs</h3>
          <div class="status-indicator status-online"></div>
        </div>
        <div class="text-3xl font-bold text-white mb-2">{{ systemState.sanitizedInputs }}</div>
        <div class="text-sm text-gray-300">Ready for processing</div>
        <div class="iq-bar mt-3" :style="{ width: systemState.sanitizationProgress + '%' }"></div>
      </div>

      <div class="glass-panel p-6 agent-igris">
        <div class="flex items-center justify-between mb-4">
          <h3 class="futuristic-subtitle text-lg">Queued Orbs</h3>
          <div class="status-indicator status-online"></div>
        </div>
        <div class="text-3xl font-bold text-white mb-2">{{ systemState.queuedOrbs }}</div>
        <div class="text-sm text-gray-300">Awaiting smithing</div>
        <div class="iq-bar mt-3" :style="{ width: systemState.orbProgress + '%' }"></div>
      </div>

      <div class="glass-panel p-6 agent-ficknury">
        <div class="flex items-center justify-between mb-4">
          <h3 class="futuristic-subtitle text-lg">Nightly Runs</h3>
          <div class="status-indicator status-online"></div>
        </div>
        <div class="text-3xl font-bold text-white mb-2">{{ systemState.nightlyRuns }}</div>
        <div class="text-sm text-gray-300">Last 24 hours</div>
        <div class="iq-bar mt-3" :style="{ width: systemState.nightlyProgress + '%' }"></div>
      </div>
    </div>

    <!-- Charts and Analytics -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Learning Events Chart -->
      <div class="glass-panel p-6">
        <h3 class="futuristic-subtitle text-xl mb-4">Learning Events (24h)</h3>
        <div class="h-64 flex items-center justify-center">
          <div class="text-center">
            <div class="text-4xl text-white mb-2">{{ learningEvents.total }}</div>
            <div class="text-sm text-gray-300">Total learning events</div>
            <div class="mt-4 space-y-2">
              <div class="flex items-center justify-between">
                <span class="text-sm">Whis</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 h-2 bg-gray-700 rounded">
                    <div class="h-full bg-indigo-500 rounded" :style="{ width: learningEvents.whis + '%' }"></div>
                  </div>
                  <span class="text-xs">{{ learningEvents.whis }}%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm">Katie</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 h-2 bg-gray-700 rounded">
                    <div class="h-full bg-blue-500 rounded" :style="{ width: learningEvents.katie + '%' }"></div>
                  </div>
                  <span class="text-xs">{{ learningEvents.katie }}%</span>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm">Igris</span>
                <div class="flex items-center space-x-2">
                  <div class="w-20 h-2 bg-gray-700 rounded">
                    <div class="h-full bg-slate-500 rounded" :style="{ width: learningEvents.igris + '%' }"></div>
                  </div>
                  <span class="text-xs">{{ learningEvents.igris }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Agent Enhancements -->
      <div class="glass-panel p-6">
        <h3 class="futuristic-subtitle text-xl mb-4">Agent Enhancements</h3>
        <div class="space-y-4">
          <div 
            v-for="enhancement in agentEnhancements" 
            :key="enhancement.id"
            class="enhancement-item glass-panel p-4 rounded-lg"
            :class="`agent-${enhancement.agent.toLowerCase()}`"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="font-medium">{{ enhancement.agent }}</span>
              <span class="text-xs text-gray-400">{{ enhancement.timestamp }}</span>
            </div>
            <p class="text-sm text-gray-300 mb-2">{{ enhancement.description }}</p>
            <div class="flex items-center space-x-2">
              <span class="text-xs">IQ:</span>
              <div class="iq-bar flex-1" :style="{ width: enhancement.iq + '%' }"></div>
              <span class="text-xs">{{ enhancement.iq }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Data Flow Map -->
    <div class="glass-panel p-6">
      <h3 class="futuristic-subtitle text-xl mb-6">Data Flow Map</h3>
      <div class="data-flow-map relative h-48 bg-gray-900 rounded-lg p-4">
        <!-- Data Flow Visualization -->
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="grid grid-cols-5 gap-4 w-full max-w-4xl">
            <div class="text-center">
              <div class="data-node glass-panel p-3 rounded-full w-16 h-16 mx-auto mb-2 flex items-center justify-center">
                <span class="text-xs">Input</span>
              </div>
              <div class="text-xs text-gray-300">Data Input</div>
            </div>
            <div class="flex items-center justify-center">
              <div class="data-flow-line"></div>
            </div>
            <div class="text-center">
              <div class="data-node glass-panel p-3 rounded-full w-16 h-16 mx-auto mb-2 flex items-center justify-center agent-whis">
                <span class="text-xs">Whis</span>
              </div>
              <div class="text-xs text-gray-300">Sanitize</div>
            </div>
            <div class="flex items-center justify-center">
              <div class="data-flow-line"></div>
            </div>
            <div class="text-center">
              <div class="data-node glass-panel p-3 rounded-full w-16 h-16 mx-auto mb-2 flex items-center justify-center agent-ficknury">
                <span class="text-xs">Route</span>
              </div>
              <div class="text-xs text-gray-300">Route</div>
            </div>
          </div>
        </div>
        
        <!-- Animated data particles -->
        <div 
          v-for="particle in dataParticles" 
          :key="particle.id"
          class="data-particle"
          :style="{ 
            left: particle.x + '%', 
            top: particle.y + '%',
            animationDelay: particle.delay + 's'
          }"
        ></div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mt-8 flex space-x-4">
      <button 
        @click="simulateLearning"
        class="glass-panel px-6 py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300"
      >
        🧠 Simulate Learning
      </button>
      <button 
        @click="viewLogicInjection"
        class="glass-panel px-6 py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300"
      >
        🔧 View Logic Injection
      </button>
      <button 
        @click="runNightlyTraining"
        class="glass-panel px-6 py-3 rounded-lg futuristic-subtitle hover:neon-border transition-all duration-300"
      >
        🌙 Run Nightly Training
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'Dashboard',
  setup() {
    const systemState = ref({
      activeTasks: 12,
      taskProgress: 75,
      sanitizedInputs: 45,
      sanitizationProgress: 90,
      queuedOrbs: 8,
      orbProgress: 60,
      nightlyRuns: 3,
      nightlyProgress: 100
    })

    const learningEvents = ref({
      total: 156,
      whis: 45,
      katie: 32,
      igris: 23
    })

    const agentEnhancements = ref([
      {
        id: 1,
        agent: 'Whis',
        description: 'Enhanced transcript processing with 15% accuracy improvement',
        timestamp: '2h ago',
        iq: 85
      },
      {
        id: 2,
        agent: 'Katie',
        description: 'New Kubernetes deployment pattern learned',
        timestamp: '4h ago',
        iq: 78
      },
      {
        id: 3,
        agent: 'Igris',
        description: 'Terraform module optimization completed',
        timestamp: '6h ago',
        iq: 92
      }
    ])

    const dataParticles = ref([
      { id: 1, x: 10, y: 50, delay: 0 },
      { id: 2, x: 30, y: 30, delay: 1 },
      { id: 3, x: 50, y: 70, delay: 2 },
      { id: 4, x: 70, y: 40, delay: 3 },
      { id: 5, x: 90, y: 60, delay: 4 }
    ])

    const simulateLearning = () => {
      console.log('Simulating learning event...')
      // Add animation and API call logic here
    }

    const viewLogicInjection = () => {
      console.log('Viewing logic injection...')
      // Navigate to agents view or show modal
    }

    const runNightlyTraining = () => {
      console.log('Running nightly training...')
      // Trigger nightly training API call
    }

    onMounted(() => {
      // Initialize any dashboard-specific logic
    })

    return {
      systemState,
      learningEvents,
      agentEnhancements,
      dataParticles,
      simulateLearning,
      viewLogicInjection,
      runNightlyTraining
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 0 auto;
}

.data-flow-line {
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, var(--agent-primary), var(--agent-secondary));
  position: relative;
  overflow: hidden;
}

.data-flow-line::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
  animation: flow-sweep 2s infinite;
}

@keyframes flow-sweep {
  0% { left: -100%; }
  100% { left: 100%; }
}

.data-node {
  transition: all 0.3s ease;
}

.data-node:hover {
  transform: scale(1.1);
  box-shadow: 0 0 20px rgba(99, 102, 241, 0.5);
}

.enhancement-item {
  transition: all 0.3s ease;
}

.enhancement-item:hover {
  transform: translateX(5px);
}
</style> 