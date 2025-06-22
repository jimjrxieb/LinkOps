<template>
  <div class="p-6 space-y-8 text-white">
    <h1 class="text-3xl font-bold mb-6">📥 Data Collection</h1>

    <!-- TASK INPUT -->
    <section class="bg-gray-900 p-4 rounded-xl shadow">
      <h2 class="text-xl font-semibold text-blue-400 mb-2">📝 Task Input</h2>
      <textarea v-model="taskInput" class="w-full h-24 bg-gray-800 rounded p-2" placeholder="Describe a task..." />
      <button @click="submit('task', taskInput)" class="mt-2 bg-blue-500 px-4 py-2 rounded hover:bg-blue-600">
        Submit Task
      </button>
    </section>

    <!-- Q&A INPUT -->
    <section class="bg-gray-900 p-4 rounded-xl shadow">
      <h2 class="text-xl font-semibold text-yellow-400 mb-2">🎓 Q&A Input</h2>
      <input v-model="qnaQuestion" placeholder="Question" class="w-full mb-2 bg-gray-800 p-2 rounded" />
      <input v-model="qnaAnswer" placeholder="Answer" class="w-full bg-gray-800 p-2 rounded" />
      <button @click="submit('qna', { question: qnaQuestion, answer: qnaAnswer })" class="mt-2 bg-yellow-500 px-4 py-2 rounded hover:bg-yellow-600">
        Submit Q&A
      </button>
    </section>

    <!-- INFO DUMP -->
    <section class="bg-gray-900 p-4 rounded-xl shadow">
      <h2 class="text-xl font-semibold text-purple-400 mb-2">📚 Info Dump</h2>
      <textarea v-model="infoDump" class="w-full h-32 bg-gray-800 p-2 rounded" placeholder="Paste an article or log..." />
      <button @click="submit('dump', infoDump)" class="mt-2 bg-purple-500 px-4 py-2 rounded hover:bg-purple-600">
        Submit Info Dump
      </button>
    </section>

    <!-- IMAGE EXTRACTOR -->
    <section class="bg-gray-900 p-4 rounded-xl shadow">
      <h2 class="text-xl font-semibold text-pink-400 mb-2">🖼️ Image Extractor</h2>
      <input type="file" @change="handleImageUpload" class="block text-white" />
      <div v-if="imageText" class="mt-2 p-2 bg-gray-800 rounded">
        <p class="text-sm text-green-300">🧠 Extracted:</p>
        <pre class="text-xs">{{ imageText }}</pre>
      </div>
      <button v-if="imageText" @click="submit('image', imageText)" class="mt-2 bg-pink-500 px-4 py-2 rounded hover:bg-pink-600">
        Submit Extracted Text
      </button>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const taskInput = ref('')
const qnaQuestion = ref('')
const qnaAnswer = ref('')
const infoDump = ref('')
const imageText = ref('')

const submit = async (type, content) => {
  const payload = { type, content }
  try {
    const res = await fetch('/api/data-collect/sanitize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await res.json()
    alert(`✅ Submitted & sanitized: ${data.status || 'ok'}`)
  } catch (err) {
    alert('❌ Submission failed.')
  }
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  const res = await fetch('/api/data-collect/image-text', {
    method: 'POST',
    body: formData,
  })
  const data = await res.json()
  imageText.value = data.text || 'No text found.'
}
</script>
