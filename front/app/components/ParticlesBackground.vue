<script setup lang="ts">
defineProps<{
  count?: number
}>()

// Générer les positions une seule fois côté client
const particles = ref<{ left: string; delay: string; duration: string }[]>([])

onMounted(() => {
  const count = 15
  particles.value = Array.from({ length: count }, () => ({
    left: `${Math.random() * 100}%`,
    delay: `${Math.random() * 15}s`,
    duration: `${15 + Math.random() * 10}s`
  }))
})
</script>

<template>
  <div class="particles">
    <div
      v-for="(particle, i) in particles"
      :key="i"
      class="particle"
      :style="{
        left: particle.left,
        animationDelay: particle.delay,
        animationDuration: particle.duration
      }"
    />
  </div>
</template>
