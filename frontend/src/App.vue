<template>
  <div id="app" class="animated-bg min-h-screen">
    <!-- Futuristic Navigation Bar -->
    <nav class="glass-panel fixed top-0 left-0 right-0 z-50 mx-4 mt-4 p-4">
      <div class="flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center space-x-4">
          <div class="futuristic-title text-2xl text-white">
            LINKOPS
          </div>
          <div class="text-sm text-gray-300">
            AI Command Center
          </div>
        </div>

        <!-- Agent Navigation -->
        <div class="flex items-center space-x-2">
          <router-link 
            v-for="agent in agents" 
            :key="agent.name"
            :to="agent.route"
            class="agent-nav-item glass-panel p-3 rounded-lg transition-all duration-300"
            :class="[
              `agent-${agent.name.toLowerCase()}`,
              { 'neon-border': $route.path === agent.route }
            ]"
          >
            <div class="flex items-center space-x-2">
              <div 
                class="status-indicator"
                :class="agent.status === 'online' ? 'status-online' : 
                       agent.status === 'processing' ? 'status-processing' : 'status-offline'"
              ></div>
              <span class="futuristic-subtitle text-sm">{{ agent.displayName }}</span>
            </div>
          </router-link>
          
          <!-- About Link -->
          <router-link 
            to="/about"
            class="agent-nav-item glass-panel p-3 rounded-lg transition-all duration-300"
            :class="{ 'neon-border': $route.path === '/about' }"
          >
            <div class="flex items-center space-x-2">
              <div class="status-indicator status-online"></div>
              <span class="futuristic-subtitle text-sm">About</span>
      </div>
          </router-link>
        </div>

        <!-- System Status -->
        <div class="flex items-center space-x-4">
          <div class="text-sm text-gray-300">
            <span class="status-indicator status-online"></span>
            System Online
          </div>
          <div class="text-xs text-gray-400">
            {{ currentTime }}
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="pt-24 px-4 pb-8">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- Orb Stream Sidebar -->
    <div class="fixed right-4 top-24 bottom-4 w-80 glass-panel p-4 overflow-hidden">
      <h3 class="futuristic-subtitle text-lg mb-4">Orb Stream</h3>
      <div class="space-y-3 max-h-full overflow-y-auto">
        <div 
          v-for="orb in orbStream" 
          :key="orb.id"
          class="orb-item glass-panel p-3 rounded-lg"
          :class="`agent-${orb.agent.toLowerCase()}`"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium">{{ orb.agent }}</span>
            <span class="text-xs text-gray-400">{{ orb.timestamp }}</span>
          </div>
          <p class="text-xs text-gray-300">{{ orb.description }}</p>
          <div class="iq-bar mt-2" :style="{ width: orb.iq + '%' }"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'App',
  setup() {
    const currentTime = ref('')
    const orbStream = ref([
      {
        id: 1,
        agent: 'Whis',
        description: 'Enhanced transcript processing logic',
        timestamp: '2m ago',
        iq: 85
      },
      {
        id: 2,
        agent: 'Katie',
        description: 'New Kubernetes deployment pattern',
        timestamp: '5m ago',
        iq: 78
      },
      {
        id: 3,
        agent: 'Igris',
        description: 'Terraform module optimization',
        timestamp: '8m ago',
        iq: 92
      },
      {
        id: 4,
        agent: 'Ficknury',
        description: 'Task routing algorithm update',
        timestamp: '12m ago',
        iq: 88
      }
    ])

    const agents = ref([
      { name: 'dashboard', displayName: 'Dashboard', route: '/dashboard', status: 'online' },
      { name: 'tasks', displayName: 'Tasks', route: '/tasks', status: 'online' },
      { name: 'whis', displayName: 'Whis', route: '/whis', status: 'processing' },
      { name: 'igris', displayName: 'Igris', route: '/igris', status: 'online' },
      { name: 'katie', displayName: 'Katie', route: '/katie', status: 'online' },
      { name: 'ficknury', displayName: 'Ficknury', route: '/ficknury', status: 'online' },
      { name: 'agents', displayName: 'Agents', route: '/agents', status: 'online' }
    ])

    let timeInterval

    const updateTime = () => {
      const now = new Date()
      currentTime.value = now.toLocaleTimeString('en-US', { 
        hour12: false,
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }

    onMounted(() => {
      updateTime()
      timeInterval = setInterval(updateTime, 1000)
    })

    onUnmounted(() => {
      if (timeInterval) {
        clearInterval(timeInterval)
      }
    })

    return {
      currentTime,
      agents,
      orbStream
    }
  }
}
</script>

<style>
@import './assets/futuristic.css';

/* Page transitions */
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Agent navigation hover effects */
.agent-nav-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

.agent-nav-item.agent-whis:hover {
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

.agent-nav-item.agent-katie:hover {
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.agent-nav-item.agent-igris:hover {
  box-shadow: 0 8px 25px rgba(100, 116, 139, 0.3);
}

.agent-nav-item.agent-ficknury:hover {
  box-shadow: 0 8px 25px rgba(251, 191, 36, 0.3);
}

/* Orb stream animations */
.orb-item {
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style> 