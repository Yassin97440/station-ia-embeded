<script setup lang="ts">
</script>

<template>
  <div class="flex gap-3">
    <UAvatar
      icon="i-lucide-bot"
      size="sm"
      :ui="{
        root: 'bg-emerald-900/50',
        icon: 'text-white'
      }"
    />
    <div class="flex items-center gap-2 rounded-2xl border border-emerald-800 bg-emerald-900/30 px-4 py-3">
      <div class="flex gap-1">
        <span
          v-for="i in 3"
          :key="i"
          class="h-2 w-2 animate-bounce rounded-full bg-emerald-400"
          :style="{ animationDelay: `${(i - 1) * 150}ms` }"
        />
      </div>
    </div>
  </div>
</template>
