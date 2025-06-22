<template>
  <div class="dashboard-page">
    <h1>📊 Agent Dashboard</h1>
    <div class="grid">
      <div class="agent-card" v-for="agent in agents" :key="agent.name">
        <h2>{{ agent.icon }} {{ agent.name }}</h2>
        <p><strong>Purpose:</strong> {{ agent.purpose }}</p>
        <p><strong>Orbs:</strong> {{ agent.orbs }}</p>
        <p><strong>Runes:</strong> {{ agent.runes }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const agents = ref([])

const fetchDashboardData = async () => {
  try {
    const res = await fetch('/api/gui/dashboard')
    const data = await res.json()
    agents.value = data.agents || []
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    // Fallback to static data if API fails
    agents.value = [
      { name: 'James', icon: '👑', purpose: 'General logic and task coordination', orbs: 3, runes: 5 },
      { name: 'Whis', icon: '🧠', purpose: 'AI/ML model training and Orbs/Rune generation', orbs: 4, runes: 6 },
      { name: 'Katie', icon: '☸️', purpose: 'Kubernetes Ops and CKA/CKS logic (Coming Soon)', orbs: 0, runes: 0 },
      { name: 'Igris', icon: '🛡️', purpose: 'Platform and DevSecOps task execution (Coming Soon)', orbs: 0, runes: 0 }
    ]
  }
}

onMounted(fetchDashboardData)
</script>

<style scoped>
.dashboard-page {
  padding: 2rem;
  max-width: 1200px;
  margin: auto;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}
.agent-card {
  background: #222;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 0 0 8px #0ff4;
  transition: all 0.3s ease;
}
.agent-card:hover {
  box-shadow: 0 0 16px #0ff6;
  transform: translateY(-2px);
}
.agent-card h2 {
  margin-top: 0;
  color: #0ff;
}
.agent-card p {
  margin: 0.5rem 0;
}
</style> 