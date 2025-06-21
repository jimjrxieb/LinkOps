<template>
  <div class="holo-card flex flex-col gap-2">
    <div class="flex items-center gap-2">
      <span class="font-bold text-holo-cyan text-lg">{{ task.task_id }}</span>
      <StatusBadge :status="task.status" />
    </div>
    <div class="text-holo-cyan/80 text-sm">{{ task.task_description }}</div>
    <div class="flex gap-2 text-xs text-holo-cyan/60">
      <span>Agent: {{ task.agent }}</span>
      <span v-if="task.created_at">• {{ formatTime(task.created_at) }}</span>
    </div>
  </div>
</template>

<script setup>
import StatusBadge from './StatusBadge.vue'
const props = defineProps({
  task: {
    type: Object,
    required: true
  }
})
const formatTime = (ts) => ts ? new Date(ts).toLocaleTimeString() : ''
</script> 