<template>
  <div class="fixed bottom-4 right-4 w-96 p-4 bg-gray-900 rounded-2xl shadow-xl border border-gray-700 z-50">
    <h2 class="text-xl font-semibold mb-2 text-blue-400">🤖 James Assistant</h2>
    <textarea
      v-model="input"
      placeholder="Ask James something..."
      class="w-full h-24 p-2 rounded bg-gray-800 text-white resize-none"
    />
    <button
      @click="sendMessage"
      class="mt-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded"
    >
      Send
    </button>

    <div v-if="response" class="mt-4 text-sm text-green-300">
      {{ response }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const input = ref('')
const response = ref('')

const sendMessage = async () => {
  if (!input.value.trim()) return

  try {
    const res = await fetch('/api/james/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input.value }),
    })
    const data = await res.json()
    response.value = data.response || 'James has no response.'
  } catch (err) {
    response.value = 'Error reaching James.'
  }

  input.value = ''
}
</script> 