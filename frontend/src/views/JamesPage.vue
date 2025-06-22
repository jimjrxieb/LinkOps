<template>
  <div class="james-page">
    <h1>👑 James Task Router</h1>
    <form @submit.prevent="submitTask">
      <input v-model="taskInput" placeholder="Enter your task..." />
      <button>Submit Task</button>
    </form>
    <div v-if="result">
      <h2>🧠 AI Response</h2>
      <pre>{{ result }}</pre>
    </div>

    <section class="qa-input">
      <h2>📘 Q&A Training</h2>
      <form @submit.prevent="submitQA">
        <input v-model="taskId" placeholder="Task ID" />
        <input v-model="question" placeholder="Question" />
        <textarea v-model="answer" placeholder="Correct Answer"></textarea>
        <button>Submit</button>
      </form>
    </section>

    <section class="info-dump">
      <h2>🗃️ Info Dump</h2>
      <textarea v-model="dump" placeholder="Paste blog post or article..."></textarea>
      <button @click="submitDump">Submit</button>
    </section>

    <section class="image-extractor">
      <h2>🖼️ Image Extractor</h2>
      <input type="file" @change="handleImage" />
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const taskInput = ref('')
const result = ref(null)
const taskId = ref('')
const question = ref('')
const answer = ref('')
const dump = ref('')

const submitTask = async () => {
  const res = await fetch('/api/tasks', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task_input: taskInput.value, origin: 'manager' })
  })
  result.value = await res.json()
}

const submitQA = async () => {
  await fetch('/api/qa', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task_id: taskId.value, question: question.value, answer: answer.value })
  })
}

const submitDump = async () => {
  await fetch('/api/info-dump', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: dump.value })
  })
}

const handleImage = async (event) => {
  const file = event.target.files[0]
  const formData = new FormData()
  formData.append('image', file)
  await fetch('/api/image-extraction', {
    method: 'POST',
    body: formData
  })
}
</script>

<style scoped>
.james-page {
  padding: 2rem;
  max-width: 900px;
  margin: auto;
}

input, textarea {
  width: 100%;
  padding: 0.8rem;
  margin-bottom: 1rem;
  background: #222;
  border: 1px solid #444;
  color: #fff;
  border-radius: 4px;
  font-size: 14px;
}

input::placeholder, textarea::placeholder {
  color: #888;
}

textarea {
  min-height: 120px;
  resize: vertical;
  font-family: inherit;
}

button {
  padding: 0.8rem 1.5rem;
  font-weight: bold;
  background: #0ff;
  color: #000;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 1rem;
}

button:hover {
  background: #0dd;
}

pre {
  background: #111;
  padding: 1rem;
  border-radius: 10px;
  color: #0f0;
  white-space: pre-wrap;
  overflow-x: auto;
  font-size: 12px;
  line-height: 1.4;
}

section {
  margin-top: 3rem;
  padding: 2rem;
  background: #1a1a1a;
  border-radius: 8px;
  border: 3px solid #ff0000;
  box-shadow: 0 0 20px #ff0000;
}

section h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #0ff;
  font-size: 1.5rem;
}

h1 {
  color: #0ff;
  margin-bottom: 2rem;
  font-size: 2rem;
}

input[type="file"] {
  background: #333;
  border: 2px dashed #555;
  padding: 1rem;
  text-align: center;
  color: #ccc;
}

input[type="file"]:hover {
  border-color: #0ff;
}
