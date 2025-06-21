<template>
  <div class="p-4">
    <h2 class="text-lg font-bold">🧠 Core Memory Orb</h2>

    <section>
      <h3 class="font-semibold mt-4">📦 Orbs</h3>
      <ul>
        <li v-for="orb in memory.orbs" :key="orb.name">
          {{ orb.name }} — {{ orb.cat }}<br />
          <small>{{ orb.desc }}</small>
        </li>
      </ul>
    </section>

    <section>
      <h3 class="font-semibold mt-4">📜 Runes</h3>
      <ul>
        <li v-for="rune in memory.runes" :key="rune.path">
          {{ rune.lang }}: {{ rune.path }}
        </li>
      </ul>
    </section>

    <section>
      <h3 class="font-semibold mt-4">✅ Completed Tasks</h3>
      <ul>
        <li v-for="task in memory.tasks" :key="task.text">
          {{ task.text }} → {{ task.agent }}
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const memory = ref({ orbs: [], runes: [], tasks: [] })

const fetchMemory = async () => {
  memory.value = (await axios.get('/api/core-memory')).data
}

onMounted(fetchMemory)
</script> 