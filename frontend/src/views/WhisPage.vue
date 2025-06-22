<template>
  <div class="whis-page">
    <h1>🧠 Whis Training Pipeline</h1>

    <section>
      <h2>📥 Data in Queue</h2>
      <ul>
        <li v-for="item in queue" :key="item.id">{{ item.summary }}</li>
      </ul>
    </section>

    <section>
      <h2>✅ Approvals Needed</h2>
      <ul>
        <li v-for="approval in approvals" :key="approval.id">{{ approval.description }}</li>
      </ul>
    </section>

    <section>
      <h2>📦 Whis-Generated Orbs</h2>
      <ul>
        <li v-for="orb in orbs" :key="orb.id">{{ orb.name }}</li>
      </ul>
    </section>

    <section>
      <h2>📜 Runes Created</h2>
      <ul>
        <li v-for="rune in runes" :key="rune.id">{{ rune.title }}</li>
      </ul>
    </section>

    <section>
      <h2>📡 Agent Capabilities</h2>
      <ul>
        <li v-for="agent in capabilities" :key="agent.name">
          {{ agent.name }} → {{ agent.abilities.join(', ') }}
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const queue = ref([])
const approvals = ref([])
const orbs = ref([])
const runes = ref([])
const capabilities = ref([])

onMounted(async () => {
  try {
    const res = await fetch('/api/gui/whis')
    const data = await res.json()
    queue.value = data.queue || []
    approvals.value = data.approvals || []
    orbs.value = data.orbs || []
    runes.value = data.runes || []
    capabilities.value = data.capabilities || []
  } catch (error) {
    console.error('Failed to fetch Whis data:', error)
    // Fallback to empty arrays if API fails
  }
})
</script>

<style scoped>
.whis-page {
  max-width: 1000px;
  margin: auto;
  padding: 2rem;
}
section {
  margin-bottom: 2rem;
}
ul {
  background: #222;
  padding: 1rem;
  border-radius: 10px;
  list-style: none;
}
li {
  margin-bottom: 0.5rem;
}
</style> 