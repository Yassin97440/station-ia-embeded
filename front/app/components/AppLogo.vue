<script setup lang="ts">
defineProps<{
  size?: 'sm' | 'md' | 'lg'
}>()
</script>

<template>
  <div class="flex items-center gap-2">
    <div
      :class="[
        'flex items-center justify-center rounded-xl bg-linear-to-br from-emerald-500 to-emerald-900 glow-emerald',
        size === 'sm' ? 'h-8 w-8 text-base' : size === 'lg' ? 'h-12 w-12 text-xl' : 'h-10 w-10 text-lg'
      ]"
    >
      🌿
    </div>
    <span
      :class="[
        'font-bold text-gradient-emerald',
        size === 'sm' ? 'text-lg' : size === 'lg' ? 'text-2xl' : 'text-xl'
      ]"
    >
      RIVO-IA
    </span>
  </div>
</template>
