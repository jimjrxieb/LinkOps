<template>
  <span :class="badgeClass">
    <slot>{{ label }}</slot>
  </span>
</template>

<script setup>
const props = defineProps({
  status: String,
  label: String
})
const badgeClass = {
  'status-badge': true,
  'success': props.status === 'approved' || props.status === 'done',
  'warning': props.status === 'pending',
  'error': props.status === 'error' || props.status === 'failed',
  'info': props.status === 'info' || props.status === 'dispatched'
}
</script>

<style scoped>
.status-badge {
  @apply px-2 py-1 rounded text-xs font-bold bg-cyber-gray/40 border border-holo-cyan/30;
}
.status-badge.success {
  @apply bg-holo-green/20 text-holo-green border-holo-green/50;
}
.status-badge.warning {
  @apply bg-holo-yellow/20 text-holo-yellow border-holo-yellow/50;
}
.status-badge.error {
  @apply bg-holo-red/20 text-holo-red border-holo-red/50;
}
.status-badge.info {
  @apply bg-holo-blue/20 text-holo-blue border-holo-blue/50;
}
</style> 