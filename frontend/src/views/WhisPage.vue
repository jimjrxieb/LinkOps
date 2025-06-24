<template>
  <div class="p-6 space-y-6">

    <!-- 🔹 Data Collection Input -->
    <div class="bg-white shadow rounded-2xl p-4">
      <h2 class="text-xl font-bold mb-2">🧠 Data Collection</h2>
      <form @submit.prevent="submitData">
        <input v-model="task" placeholder="Enter task/question..." class="w-full p-2 border rounded mb-2" />
        <input v-model="answer" placeholder="Enter correct answer..." class="w-full p-2 border rounded mb-2" />
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Submit</button>
      </form>
    </div>

    <!-- 🔸 Log Preview -->
    <div v-if="logPreview" class="bg-gray-100 p-4 rounded">
      <h3 class="font-semibold">Sanitized Preview:</h3>
      <pre>{{ logPreview }}</pre>
    </div>

    <!-- 🔍 Approval Queue -->
    <div class="bg-white shadow rounded-2xl p-4">
      <h2 class="text-lg font-bold mb-2">⚖️ Rune Approval Queue</h2>
      <div v-for="entry in approvalQueue" :key="entry.task_id" class="border-b py-2">
        <div class="text-sm">{{ entry.result.question }}</div>
        <button @click="approveRune(entry.task_id)" class="mt-1 text-green-700">✅ Approve</button>
      </div>
    </div>

    <!-- 🌙 Digest Section -->
    <div class="bg-white shadow rounded-2xl p-4">
      <h2 class="text-lg font-bold mb-2">🌙 Whis Training Digest</h2>
      <div v-if="digest">
        <pre>{{ digest }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const task = ref('')
const answer = ref('')
const logPreview = ref(null)
const approvalQueue = ref([])
const digest = ref(null)

async function submitData() {
  const payload = {
    task_id: Date.now().toString(),
    question: task.value,
    correct_answer: answer.value
  }
  
  try {
    const res = await axios.post('http://localhost:8001/api/collect/qna', payload)
    logPreview.value = res.data || payload
    console.log('Data queued:', res.data)
    
    // Clear form
    task.value = ''
    answer.value = ''
  } catch (error) {
    console.error('Error submitting data:', error)
    logPreview.value = { error: 'Failed to submit data' }
  }
}

async function approveRune(taskId) {
  try {
    await axios.post('/api/whis/approve-rune', { task_id: taskId })
    loadQueue()
  } catch (error) {
    console.error('Error approving rune:', error)
  }
}

async function loadQueue() {
  try {
    const res = await axios.get('/api/whis/approvals')
    approvalQueue.value = res.data || []
  } catch (error) {
    console.error('Error loading queue:', error)
  }
}

async function loadDigest() {
  try {
    const res = await axios.get('/api/whis/digest')
    digest.value = res.data || {}
  } catch (error) {
    console.error('Error loading digest:', error)
  }
}

onMounted(() => {
  loadQueue()
  loadDigest()
})
</script>

<style scoped>
pre {
  background-color: #f7fafc;
  padding: 1rem;
  border-radius: 0.5rem;
  white-space: pre-wrap;
  word-break: break-word;
}
</style> 