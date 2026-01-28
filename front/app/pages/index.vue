<template>
  <div class="space-y-8">
    <!-- Welcome section -->
    <section class="text-center">
      <h1 class="text-3xl font-bold text-gradient-emerald md:text-4xl">
        Bonjour, Yassin 👋
      </h1>
      <p class="mt-2 text-emerald-300/60">
        Bienvenue sur votre assistant vocal intelligent
      </p>
    </section>

    <!-- Stats section -->
    <section class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="card-forest p-5 transition hover:border-emerald-700"
      >
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-900/50 text-emerald-400">
            <UIcon
              :name="stat.icon"
              class="h-5 w-5"
            />
          </div>
          <div>
            <p class="text-2xl font-bold text-white">
              {{ stat.value }}
            </p>
            <p class="text-xs text-emerald-300/50">
              {{ stat.label }}
            </p>
          </div>
        </div>
        <div
          v-if="stat.trend"
          class="mt-3 flex items-center gap-1 text-xs"
        >
          <UIcon
            :name="stat.trend > 0 ? 'i-lucide-trending-up' : 'i-lucide-trending-down'"
            :class="stat.trend > 0 ? 'text-emerald-400' : 'text-red-400'"
            class="h-3 w-3"
          />
          <span :class="stat.trend > 0 ? 'text-emerald-400' : 'text-red-400'">
            {{ Math.abs(stat.trend) }}%
          </span>
          <span class="text-emerald-300/40">vs semaine dernière</span>
        </div>
      </div>
    </section>

    <!-- Quick actions -->
    <section class="card-forest p-6">
      <h2 class="mb-4 text-lg font-semibold text-white">
        Démarrer une conversation
      </h2>
      <div class="grid gap-4 md:grid-cols-2">
        <!-- Voice chat -->
        <NuxtLink
          to="/chat?mode=voice"
          class="group flex items-center gap-4 rounded-xl border border-emerald-800 bg-emerald-900/20 p-5 transition hover:border-emerald-600 hover:bg-emerald-900/40"
        >
          <div class="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-emerald-500 to-emerald-700 transition group-hover:glow-emerald">
            <UIcon
              name="i-lucide-mic"
              class="h-7 w-7 text-white"
            />
          </div>
          <div>
            <h3 class="font-medium text-white">Mode Vocal</h3>
            <p class="text-sm text-emerald-300/50">
              Parlez directement à l'assistant
            </p>
          </div>
          <UIcon
            name="i-lucide-arrow-right"
            class="ml-auto h-5 w-5 text-emerald-600 transition group-hover:translate-x-1 group-hover:text-emerald-400"
          />
        </NuxtLink>

        <!-- Text chat -->
        <NuxtLink
          to="/chat?mode=text"
          class="group flex items-center gap-4 rounded-xl border border-emerald-800 bg-emerald-900/20 p-5 transition hover:border-emerald-600 hover:bg-emerald-900/40"
        >
          <div class="flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-emerald-600 to-emerald-800 transition group-hover:glow-emerald">
            <UIcon
              name="i-lucide-message-square"
              class="h-7 w-7 text-white"
            />
          </div>
          <div>
            <h3 class="font-medium text-white">Mode Texte</h3>
            <p class="text-sm text-emerald-300/50">
              Écrivez votre message
            </p>
          </div>
          <UIcon
            name="i-lucide-arrow-right"
            class="ml-auto h-5 w-5 text-emerald-600 transition group-hover:translate-x-1 group-hover:text-emerald-400"
          />
        </NuxtLink>
      </div>
    </section>

    <!-- Recent conversations -->
    <section class="card-forest p-6">
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-white">
          Conversations récentes
        </h2>
        <UButton
          variant="ghost"
          size="sm"
          color="neutral"
        >
          Voir tout
          <template #trailing>
            <UIcon
              name="i-lucide-chevron-right"
              class="h-4 w-4"
            />
          </template>
        </UButton>
      </div>

      <div class="space-y-3">
        <div
          v-for="conv in recentConversations"
          :key="conv.id"
          class="flex items-center gap-4 rounded-lg border border-transparent p-3 transition hover:border-emerald-800 hover:bg-emerald-900/20 cursor-pointer"
        >
          <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-900/50">
            <UIcon
              :name="conv.mode === 'voice' ? 'i-lucide-mic' : 'i-lucide-message-square'"
              class="h-5 w-5 text-emerald-400"
            />
          </div>
          <div class="flex-1 overflow-hidden">
            <p class="truncate font-medium text-white">
              {{ conv.title }}
            </p>
            <p class="truncate text-xs text-emerald-300/50">
              {{ conv.preview }}
            </p>
          </div>
          <div class="text-right">
            <p class="text-xs text-emerald-300/40">
              {{ conv.date }}
            </p>
            <p class="text-xs text-emerald-400">
              {{ conv.messages }} msg
            </p>
          </div>
        </div>
      </div>

      <div
        v-if="recentConversations.length === 0"
        class="py-8 text-center text-emerald-300/40"
      >
        <UIcon
          name="i-lucide-message-circle"
          class="mx-auto mb-2 h-12 w-12 opacity-50"
        />
        <p>Aucune conversation pour le moment</p>
        <p class="text-sm">
          Démarrez votre première conversation ci-dessus
        </p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// Stats data (à remplacer par de vraies données)
const stats = ref([
  {
    label: 'Conversations',
    value: '24',
    icon: 'i-lucide-message-square',
    trend: 12
  },
  {
    label: 'Messages',
    value: '156',
    icon: 'i-lucide-messages-square',
    trend: 8
  },
  {
    label: 'Temps de réponse',
    value: '2.3s',
    icon: 'i-lucide-timer',
    trend: -15
  },
  {
    label: 'Actions exécutées',
    value: '42',
    icon: 'i-lucide-zap',
    trend: 25
  }
])

// Recent conversations (mock data)
const recentConversations = ref([
  {
    id: 1,
    title: 'Météo de demain',
    preview: 'Demain il fera beau avec quelques nuages...',
    date: 'Aujourd\'hui',
    messages: 4,
    mode: 'voice'
  },
  {
    id: 2,
    title: 'Rappel réunion',
    preview: 'J\'ai créé un rappel pour votre réunion de 14h...',
    date: 'Hier',
    messages: 6,
    mode: 'text'
  },
  {
    id: 3,
    title: 'Recherche documentation',
    preview: 'Voici les ressources sur FastAPI que j\'ai trouvées...',
    date: '23 Jan',
    messages: 8,
    mode: 'voice'
  }
])
</script>
