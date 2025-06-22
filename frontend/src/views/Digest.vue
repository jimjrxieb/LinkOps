<template>
  <div class="p-6 text-white">
    <h1 class="text-2xl font-bold mb-4">📒 Daily Digest</h1>

    <div class="bg-gray-900 p-4 rounded-xl shadow space-y-3 border border-gray-700">
      <p><strong>Logs Processed:</strong> {{ digest.log_count }}</p>
      <p><strong>Total Runes:</strong> {{ digest.runes_total }}</p>
      <p><strong>Approved:</strong> ✅ {{ digest.runes_approved }}</p>
      <p><strong>Pending:</strong> ⏳ {{ digest.runes_pending }}</p>

      <div>
        <strong>Agents Affected:</strong>
        <ul class="pl-4 list-disc text-sm">
          <li v-for="(count, agent) in digest.agents_affected" :key="agent">
            {{ agent }} → {{ count }} runes
          </li>
        </ul>
      </div>

      <div v-if="digest.preview?.length">
        <strong>Preview of Runes:</strong>
        <div v-for="(entry, index) in digest.preview" :key="index" class="bg-gray-800 mt-2 p-2 rounded text-xs">
          <pre>{{ JSON.stringify(entry, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const digest = ref({})

const fetchDigest = async () => {
  const res = await fetch('/api/whis/digest')
  digest.value = await res.json()
}

onMounted(fetchDigest)
</script>
