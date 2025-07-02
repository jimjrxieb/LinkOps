<template>
  <div class="arise-container h-screen flex flex-col items-center justify-center bg-black text-white relative overflow-hidden">
    <!-- Animated Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-indigo-900 via-purple-900 to-black"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(99,102,241,0.1),transparent_50%)]"></div>
    
    <!-- Floating Particles -->
    <div class="absolute inset-0">
      <div 
        v-for="i in 20" 
        :key="i"
        class="particle absolute w-1 h-1 bg-indigo-400 rounded-full opacity-60"
        :style="{
          left: Math.random() * 100 + '%',
          top: Math.random() * 100 + '%',
          animationDelay: Math.random() * 5 + 's',
          animationDuration: (Math.random() * 3 + 2) + 's'
        }"
      ></div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 text-center">
      <!-- Shadow Links Industries Logo -->
      <div class="mb-8">
        <div class="text-8xl font-black tracking-widest mb-2 text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 animate-pulse">
          ARISE.
        </div>
        <div class="text-xl text-gray-300 mb-2">Shadow Links Industries</div>
        <div class="text-sm text-gray-500">Command Protocol: Shadow Army Activation</div>
      </div>

      <!-- Status Display -->
      <div class="mb-8">
        <div class="text-lg text-gray-300 mb-4">Shadow Agents Status</div>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4 max-w-2xl mx-auto">
          <div 
            v-for="agent in shadowAgents" 
            :key="agent.name"
            class="agent-status glass-panel p-3 rounded-lg text-center"
            :class="agent.status === 'online' ? 'border-green-500' : 'border-red-500'"
          >
            <div class="text-2xl mb-1">{{ agent.icon }}</div>
            <div class="text-sm font-medium">{{ agent.name }}</div>
            <div class="text-xs text-gray-400">{{ agent.status }}</div>
          </div>
        </div>
      </div>

      <!-- Activation Button -->
      <div class="mb-8">
        <button 
          @click="activateShadowArmy" 
          :disabled="isActivating"
          class="activate-btn glass-panel px-12 py-6 rounded-2xl text-3xl font-bold shadow-2xl transition-all duration-500 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
          :class="isActivating ? 'animate-pulse' : 'hover:shadow-indigo-500/50'"
        >
          <span v-if="!isActivating">🔥 ARISE SHADOW ARMY 🔥</span>
          <span v-else>SUMMONING...</span>
        </button>
      </div>

      <!-- Activation Progress -->
      <div v-if="isActivating" class="mb-8">
        <div class="text-lg text-gray-300 mb-4">Summoning Protocol</div>
        <div class="max-w-md mx-auto space-y-2">
          <div 
            v-for="step in activationSteps" 
            :key="step.id"
            class="flex items-center space-x-3 text-sm"
            :class="step.completed ? 'text-green-400' : step.active ? 'text-yellow-400' : 'text-gray-500'"
          >
            <div class="w-4 h-4 rounded-full border-2 flex items-center justify-center"
                 :class="step.completed ? 'border-green-400 bg-green-400' : step.active ? 'border-yellow-400' : 'border-gray-500'">
              <span v-if="step.completed" class="text-black text-xs">✓</span>
              <span v-else-if="step.active" class="text-yellow-400 text-xs">⟳</span>
            </div>
            <span>{{ step.description }}</span>
          </div>
        </div>
      </div>

      <!-- Mission Statement -->
      <div class="max-w-2xl mx-auto text-center">
        <div class="text-lg text-gray-300 mb-4">Mission: Solo Leveling IRL</div>
        <p class="text-sm text-gray-400 leading-relaxed">
          "This is more than a platform. It's a legacy for your daughter, 
          a shadow army to fight for cancer families, a system that sacrifices 
          everything to help others win their fight."
        </p>
      </div>
    </div>

    <!-- Audio Element for Voice Activation (only if file exists) -->
    <audio v-if="audioFileExists" ref="activationAudio" preload="auto" @error="handleAudioError">
      <source src="/audio/arise-activation.mp3" type="audio/mpeg">
    </audio>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jamesService } from '@/services/api'

export default {
  name: 'ArisePage',
  setup() {
    const router = useRouter()
    const isActivating = ref(false)
    const activationAudio = ref(null)
    const audioFileExists = ref(false)

    const shadowAgents = ref([
      { name: 'Whis', icon: '🧠', status: 'offline', description: 'Rune Forger & Shadow Brain' },
      { name: 'Igris', icon: '🏗️', status: 'offline', description: 'Platform Guardian' },
      { name: 'Katie', icon: '⚓', status: 'offline', description: 'Kubernetes Sentinel' },
      { name: 'Ficknury', icon: '🎯', status: 'offline', description: 'Task Evaluator' },
      { name: 'James', icon: '🤖', status: 'offline', description: 'Voice of the Monarch' },
      { name: 'AuditGuard', icon: '🛡️', status: 'offline', description: 'Compliance Warden' },
      { name: 'WebScraper', icon: '🕷️', status: 'offline', description: 'Data Hunter' },
      { name: 'DataCollector', icon: '📊', status: 'offline', description: 'Information Gatherer' },
      { name: 'Sanitizer', icon: '🧹', status: 'offline', description: 'Data Purifier' },
      { name: 'Smithing', icon: '⚒️', status: 'offline', description: 'Rune Crafter' }
    ])

    const activationSteps = ref([
      { id: 1, description: 'Initializing Shadow Network', completed: false, active: false },
      { id: 2, description: 'Summoning Core Agents', completed: false, active: false },
      { id: 3, description: 'Establishing Neural Links', completed: false, active: false },
      { id: 4, description: 'Activating Command Protocols', completed: false, active: false },
      { id: 5, description: 'Shadow Army Online', completed: false, active: false }
    ])

    const activateShadowArmy = async () => {
      if (isActivating.value) return
      
      isActivating.value = true
      
      try {
        // Step 1: Initialize Shadow Network
        activationSteps.value[0].active = true
        await new Promise(resolve => setTimeout(resolve, 1000))
        activationSteps.value[0].completed = true
        activationSteps.value[0].active = false
        
        // Step 2: Summon Core Agents via James
        activationSteps.value[1].active = true
        const activationResponse = await jamesService.activateShadowArmy()
        
        // Update agent statuses based on activation response
        if (activationResponse.data.shadow_agents) {
          shadowAgents.value.forEach(agent => {
            const activatedAgent = activationResponse.data.shadow_agents.find(
              a => a.name.toLowerCase() === agent.name.toLowerCase()
            )
            if (activatedAgent && activatedAgent.status === 'online') {
              agent.status = 'online'
            }
          })
        }
        
        await new Promise(resolve => setTimeout(resolve, 1500))
        activationSteps.value[1].completed = true
        activationSteps.value[1].active = false
        
        // Step 3: Establish Neural Links
        activationSteps.value[2].active = true
        await new Promise(resolve => setTimeout(resolve, 1000))
        activationSteps.value[2].completed = true
        activationSteps.value[2].active = false
        
        // Step 4: Activate Command Protocols
        activationSteps.value[3].active = true
        await new Promise(resolve => setTimeout(resolve, 1000))
        activationSteps.value[3].completed = true
        activationSteps.value[3].active = false
        
        // Step 5: Shadow Army Online
        activationSteps.value[4].active = true
        await new Promise(resolve => setTimeout(resolve, 500))
        activationSteps.value[4].completed = true
        activationSteps.value[4].active = false
        
        // Play activation sound if available
        if (activationAudio.value && audioFileExists.value) {
          try {
            await activationAudio.value.play()
          } catch (error) {
            console.log('Audio playback not available')
          }
        }
        
        // Show success message from James
        console.log(activationResponse.data.message)
        
        // Navigate to dashboard after a brief delay
        setTimeout(() => {
          router.push('/dashboard')
        }, 2000)
        
      } catch (error) {
        console.error('Activation failed:', error)
        isActivating.value = false
      }
    }

    const handleAudioError = () => {
      console.error('Audio playback error')
    }

    // Check if audio file exists
    const checkAudioFile = async () => {
      try {
        const response = await fetch('/audio/arise-activation.mp3', { method: 'HEAD' })
        audioFileExists.value = response.ok
      } catch (error) {
        audioFileExists.value = false
        console.log('Audio file not available')
      }
    }

    onMounted(() => {
      checkAudioFile()
    })

    return {
      shadowAgents,
      isActivating,
      activationSteps,
      activationAudio,
      activateShadowArmy,
      handleAudioError,
      audioFileExists,
      checkAudioFile
    }
  }
}
</script>

<style scoped>
.arise-container {
  background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
}

.glass-panel {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.activate-btn {
  background: linear-gradient(45deg, #6366f1, #8b5cf6, #ec4899);
  border: 2px solid rgba(99, 102, 241, 0.3);
  box-shadow: 0 0 30px rgba(99, 102, 241, 0.3);
}

.activate-btn:hover {
  box-shadow: 0 0 50px rgba(99, 102, 241, 0.5);
  border-color: rgba(99, 102, 241, 0.6);
}

.agent-status {
  transition: all 0.3s ease;
}

.agent-status:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.2);
}

.particle {
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
    opacity: 1;
  }
}

/* Text glow effect */
.text-8xl {
  text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .text-8xl {
    font-size: 3rem;
  }
  
  .activate-btn {
    font-size: 1.5rem;
    padding: 1rem 2rem;
  }
}
</style> 