<template>
  <div class="holo-card">
    <div class="flex items-center gap-2 mb-2">
      <span class="font-bold text-holo-cyan">{{ rune.orb }}</span>
      <StatusBadge :status="rune.is_flagged ? 'pending' : 'approved'" />
    </div>
    <div class="text-xs text-holo-cyan/60 mb-1">Task: {{ rune.task_id }}</div>
    <pre class="bg-cyber-dark p-2 rounded text-holo-cyan/90 text-xs mb-2 whitespace-pre-wrap">{{ rune.script_content }}</pre>
    <div class="flex gap-2 text-xs text-holo-cyan/60">
      <span>Lang: {{ rune.language }}</span>
      <span>Ver: {{ rune.version }}</span>
      <span v-if="rune.created_at">• {{ formatTime(rune.created_at) }}</span>
    </div>
  </div>
</template>

<script setup>
import StatusBadge from './StatusBadge.vue'
const props = defineProps({
  rune: {
    type: Object,
    required: true
  }
})
const formatTime = (ts) => ts ? new Date(ts).toLocaleTimeString() : ''
</script> 