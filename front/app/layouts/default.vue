<template>
  <div class="min-h-screen bg-tropical text-white">
    <!-- Particles background -->
    <div class="particles">
      <div
        v-for="i in 15"
        :key="i"
        class="particle"
        :style="{
          left: `${Math.random() * 100}%`,
          animationDelay: `${Math.random() * 15}s`,
          animationDuration: `${15 + Math.random() * 10}s`
        }"
      />
    </div>

    <!-- Header -->
    <header class="relative z-10 border-b border-emerald-900/50 bg-[#0a0f0d]/80 backdrop-blur-sm">
      <div class="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <!-- Logo -->
        <NuxtLink to="/" class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500 to-emerald-900 text-lg glow-emerald">
            🌿
          </div>
          <span class="text-xl font-bold text-gradient-emerald">RIVO-IA</span>
        </NuxtLink>

        <!-- Nav -->
        <nav class="hidden items-center gap-6 md:flex">
          <NuxtLink to="/" class="text-sm text-emerald-300/70 transition hover:text-emerald-300">
            Dashboard
          </NuxtLink>
          <NuxtLink to="/chat" class="text-sm text-emerald-300/70 transition hover:text-emerald-300">
            Chat
          </NuxtLink>
        </nav>

        <!-- User menu -->
        <div class="flex items-center gap-3">
          <UDropdownMenu
            :items="[
              [{ label: 'Profil', icon: 'i-lucide-user' }],
              [{ label: 'Paramètres', icon: 'i-lucide-settings' }],
              [{ label: 'Déconnexion', icon: 'i-lucide-log-out', color: 'error' }]
            ]"
          >
            <UButton
              color="neutral"
              variant="ghost"
              class="gap-2"
            >
              <UAvatar
                src="https://api.dicebear.com/7.x/avataaars/svg?seed=Felix"
                size="sm"
              />
              <span class="hidden text-sm text-emerald-100 md:block">Yassin</span>
              <UIcon name="i-lucide-chevron-down" class="h-4 w-4 text-emerald-400" />
            </UButton>
          </UDropdownMenu>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="relative z-10 mx-auto max-w-6xl px-4 py-8">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="relative z-10 border-t border-emerald-900/50 bg-[#0a0f0d]/80 backdrop-blur-sm">
      <div class="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-4 py-6 md:flex-row">
        <div class="flex items-center gap-2 text-sm text-emerald-300/50">
          <span>🌿</span>
          <span>RIVO-IA v0.1</span>
          <span class="text-emerald-700">•</span>
          <span>Assistant Vocal Intelligent</span>
        </div>
        <div class="flex items-center gap-4 text-xs text-emerald-300/40">
          <span>© {{ new Date().getFullYear() }} Station IA</span>
          <span class="text-emerald-700">•</span>
          <a href="#" class="transition hover:text-emerald-300">Confidentialité</a>
          <span class="text-emerald-700">•</span>
          <a href="#" class="transition hover:text-emerald-300">Conditions</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>
