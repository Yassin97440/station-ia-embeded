<script setup lang="ts">
definePageMeta({
  layout: false
})

const user = useSupabaseUser()
const redirectInfo = useSupabaseCookieRedirect()

// Watch for user authentication
watch(user, () => {
  if (user.value) {
    // Get saved redirect path or fallback to home
    const path = redirectInfo.pluck()
    return navigateTo(path || '/')
  }
}, { immediate: true })
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-tropical p-4">
    <!-- Background effect -->
    <div class="fixed inset-0 z-0">
      <div class="absolute inset-0 bg-linear-to-br from-emerald-950/50 via-transparent to-emerald-900/30" />
    </div>

    <!-- Loading card -->
    <UCard
      class="relative z-10 w-full max-w-md"
      :ui="{
        root: 'bg-[#111916]/90 backdrop-blur-xl border-emerald-900/50',
        body: 'p-8'
      }"
    >
      <div class="text-center">
        <!-- Animated loader -->
        <div class="mx-auto mb-6 flex h-20 w-20 items-center justify-center">
          <div class="relative">
            <div class="absolute inset-0 animate-ping rounded-full bg-emerald-500/30" />
            <div class="relative flex h-16 w-16 items-center justify-center rounded-full bg-linear-to-br from-emerald-500 to-emerald-700">
              <UIcon
                name="i-lucide-leaf"
                class="h-8 w-8 animate-pulse text-white"
              />
            </div>
          </div>
        </div>

        <h2 class="text-xl font-bold text-white">
          Connexion en cours...
        </h2>
        <p class="mt-3 text-sm text-emerald-300/60">
          Veuillez patienter pendant que nous vérifions votre authentification.
        </p>

        <!-- Progress dots -->
        <div class="mt-6 flex justify-center gap-2">
          <span
            v-for="i in 3"
            :key="i"
            class="h-2 w-2 animate-bounce rounded-full bg-emerald-500"
            :style="{ animationDelay: `${i * 0.15}s` }"
          />
        </div>
      </div>
    </UCard>
  </div>
</template>
