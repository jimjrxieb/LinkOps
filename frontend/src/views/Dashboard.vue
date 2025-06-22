<template>
  <div class="p-6 text-white">
    <h1 class="text-2xl font-bold mb-4">📊 LinkOps Dashboard</h1>

    <p>Welcome to mission control. Here you'll see today's activity, agent summaries, digest, and approval queues.</p>

    <!-- James Assistant Widget -->
    <JamesAssistant />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import JamesAssistant from '@/components/JamesAssistant.vue'

const james = ref({
  orbs: { current: 0, desired: 0 },
  runes: { current: 0, desired: 0 },
  autonomy: 0,
  suggestions: []
})

const whis = ref({
  last_sync: '',
  updated_orbs: 0,
  created_runes: 0,
  unmapped: []
})

const agents = ref([])

onMounted(async () => {
  try {
    const res = await fetch('/api/gui/dashboard')
    const data = await res.json()
    james.value = data.james || james.value
    whis.value = data.whis || whis.value
    agents.value = data.agents || []
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    // Fallback to static data if API fails
    james.value = {
      orbs: { current: 3, desired: 10 },
      runes: { current: 5, desired: 15 },
      autonomy: 45,
      suggestions: [
        'Add more Kubernetes orbs for better container orchestration',
        'Create runes for security scanning and compliance',
        'Increase autonomy by training on more edge cases'
      ]
    }
    whis.value = {
      last_sync: '2024-01-15 14:30:00',
      updated_orbs: 2,
      created_runes: 3,
      unmapped: [
        'Advanced network policies',
        'Service mesh configuration',
        'Multi-cluster management'
      ]
    }
    agents.value = [
      { name: 'James', capabilities: ['Task routing', 'Solution generation', 'Agent coordination'] },
      { name: 'Whis', capabilities: ['ML training', 'Orb generation', 'Rune creation'] },
      { name: 'Katie', capabilities: ['Kubernetes ops', 'CKA/CKS logic', 'Container orchestration'] },
      { name: 'Igris', capabilities: ['Platform ops', 'DevSecOps', 'Infrastructure automation'] }
    ]
  }
})
</script>

<style scoped>
.dashboard-page {
  max-width: 1200px;
  margin: auto;
  padding: 2rem;
}

section {
  margin-bottom: 2.5rem;
  background: #1c1c1c;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  border: 1px solid #333;
  box-shadow: 0 4px 8px rgba(0, 255, 255, 0.1);
}

section h2 {
  color: #0ff;
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin-bottom: 0.4rem;
  color: #eee;
}

ul ul {
  margin-left: 1.5rem;
  margin-top: 0.5rem;
}

ul ul li {
  color: #ccc;
  font-size: 0.9rem;
}

.dashboard-page h1 {
  color: #0ff;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}
</style> 