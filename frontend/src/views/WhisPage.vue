<template>
  <div class="p-6 text-white">
    <h1 class="text-2xl font-bold mb-6">🧠 Whis Training Queue</h1>

    <!-- Whis Data Lake trigger -->
    <div class="mb-6 p-4 bg-blue-950 rounded-xl border border-blue-600 shadow">
      <h2 class="text-lg font-bold text-blue-300">🧠 Whis Data Lake</h2>
      <p class="text-sm mb-2 text-blue-200">Trigger nightly learning from all sanitized logs.</p>
      <button
        @click="trainWhis"
        class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white font-medium"
      >
        🔄 Start Night Training
      </button>
    </div>

    <div v-if="runes.length === 0" class="text-green-400">
      ✅ No pending runes. Whis is fully trained.
    </div>

    <div v-for="rune in runes" :key="rune.id" class="bg-gray-900 p-4 rounded-xl mb-4 shadow border border-gray-700">
      <p class="text-sm text-gray-400 mb-2">
        <strong>Agent:</strong> {{ rune.agent }} | 
        <strong>Origin:</strong> {{ rune.origin }} | 
        <strong>ID:</strong> #{{ rune.id }}
      </p>
      <pre class="bg-gray-800 p-2 rounded text-sm max-h-64 overflow-y-auto">
{{ JSON.stringify(rune.content, null, 2) }}
      </pre>
      <button
        class="mt-2 bg-green-600 hover:bg-green-700 px-4 py-2 rounded text-white"
        @click="approve(rune.id)"
      >
        ✅ Approve Rune
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const runes = ref([])

const fetchRunes = async () => {
  const res = await fetch('/api/whis/approvals')
  const data = await res.json()
  runes.value = data
}

const trainWhis = async () => {
  const res = await fetch('/api/whis/train-nightly', { method: 'POST' })
  const data = await res.json()
  alert(`Whis trained on ${data.count} logs.`)
  fetchRunes()  // refresh approval queue
}

const approve = async (id) => {
  await fetch(`/api/whis/approve-rune/${id}`, {
    method: 'POST'
  })
  runes.value = runes.value.filter(r => r.id !== id)
}

onMounted(fetchRunes)
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