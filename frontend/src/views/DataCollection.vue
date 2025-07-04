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

    <!-- YOUTUBE TRANSCRIPT DOWNLOAD -->
    <section class="bg-gray-900 p-4 rounded-xl shadow">
      <h2 class="text-xl font-semibold text-red-400 mb-2">📺 YouTube Transcript Download</h2>
      <input 
        v-model="youtubeUrl" 
        placeholder="Enter YouTube URL (e.g., https://www.youtube.com/watch?v=...)" 
        class="w-full mb-2 bg-gray-800 p-2 rounded" 
      />
      <input 
        v-model="youtubeTopic" 
        placeholder="Topic/Category (e.g., AI, Programming, Science)" 
        class="w-full mb-2 bg-gray-800 p-2 rounded" 
      />
      <button 
        @click="downloadYouTubeTranscript" 
        :disabled="isDownloading || !youtubeUrl"
        class="mt-2 bg-red-500 px-4 py-2 rounded hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="!isDownloading">📥 Download Transcript</span>
        <span v-else>⏳ Downloading...</span>
      </button>
      <div v-if="youtubeTranscript" class="mt-4 p-3 bg-gray-800 rounded">
        <p class="text-sm text-green-300 mb-2">📝 Transcript Preview:</p>
        <div class="max-h-40 overflow-y-auto">
          <pre class="text-xs text-gray-300">{{ youtubeTranscript.substring(0, 500) }}{{ youtubeTranscript.length > 500 ? '...' : '' }}</pre>
        </div>
        <button @click="submit('youtube', youtubeTranscript)" class="mt-2 bg-green-500 px-4 py-2 rounded hover:bg-green-600">
          ✅ Submit Transcript
        </button>
      </div>
      <div v-if="youtubeError" class="mt-2 p-2 bg-red-900/50 border border-red-500 rounded">
        <p class="text-sm text-red-300">❌ {{ youtubeError }}</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { dataCollectorService } from '@/services/api'

const taskInput = ref('')
const qnaQuestion = ref('')
const qnaAnswer = ref('')
const infoDump = ref('')
const imageText = ref('')
const youtubeUrl = ref('')
const youtubeTopic = ref('')
const isDownloading = ref(false)
const youtubeTranscript = ref('')
const youtubeError = ref('')

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

const downloadYouTubeTranscript = async () => {
  if (!youtubeUrl.value) return

  isDownloading.value = true
  youtubeError.value = ''
  youtubeTranscript.value = ''

  try {
    const response = await dataCollectorService.downloadYouTubeTranscript({
      url: youtubeUrl.value,
      topic: youtubeTopic.value || 'General'
    })
    
    if (response.data.status === 'queued') {
      youtubeTranscript.value = 'Transcript downloaded and queued for processing!'
    } else if (response.data.transcript) {
      youtubeTranscript.value = response.data.transcript
    } else {
      youtubeTranscript.value = 'Transcript downloaded successfully!'
    }
  } catch (err) {
    youtubeError.value = err.response?.data?.detail || err.message || 'Failed to download transcript. Make sure the video has captions enabled.'
  } finally {
    isDownloading.value = false
  }
}
</script>
