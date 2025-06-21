<template>
  <div class="p-4 space-y-6">
    <h1 class="text-xl font-bold">🧠 James Task Router</h1>

    <input v-model="taskText" placeholder="Enter your task..." class="border p-2 w-full" />
    <button @click="submitTask" class="btn mt-2">Submit Task</button>

    <div v-if="tasks.length" class="mt-6 space-y-4">
      <div v-for="task in tasks" :key="task.id" class="p-3 border rounded shadow">
        <p class="font-semibold">📝 {{ task.input_text }}</p>
        <ul>
          <li v-for="(score, agent) in task.rankings" :key="agent">
            {{ agent }}: {{ score }}%
          </li>
        </ul>
        <p v-if="task.assigned_to">✅ Sent to: {{ task.assigned_to }}</p>
        <div v-else class="space-x-2">
          <button v-for="agent in ['katie', 'igris', 'whis']" :key="agent"
            @click="dispatch(task.id, agent)" class="btn-sm">
            Send to {{ agent }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const taskText = ref('')
const tasks = ref([])

const submitTask = async () => {
  if (!taskText.value) return
  await axios.post('/api/tasks', { input_text: taskText.value })
  taskText.value = ''
  fetchTasks()
}

const dispatch = async (taskId, agent) => {
  await axios.post('/api/tasks/dispatch', { task_id: taskId, agent })
  fetchTasks()
}

const fetchTasks = async () => {
  const res = await axios.get('/api/tasks/ranked')
  tasks.value = res.data
}

onMounted(fetchTasks)
</script> 