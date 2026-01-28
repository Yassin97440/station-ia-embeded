<script setup lang="ts">
// Types
interface Stat {
  label: string
  value: string
  icon: string
  trend?: number
  description?: string
}

interface Conversation {
  id: number
  title: string
  preview: string
  date: string
  messages: number
  mode: 'voice' | 'text'
}

// Stats data (à remplacer par de vraies données)
const stats = ref<Stat[]>([
  {
    label: 'Conversations',
    value: '24',
    icon: 'i-lucide-message-square',
    trend: 12,
    description: 'Total de conversations'
  },
  {
    label: 'Messages',
    value: '156',
    icon: 'i-lucide-messages-square',
    trend: 8,
    description: 'Messages échangés'
  },
  {
    label: 'Temps de réponse',
    value: '2.3s',
    icon: 'i-lucide-timer',
    trend: -15,
    description: 'Temps moyen'
  },
  {
    label: 'Actions exécutées',
    value: '42',
    icon: 'i-lucide-zap',
    trend: 25,
    description: 'Actions automatisées'
  }
])

// Recent conversations (mock data)
const recentConversations = ref<Conversation[]>([
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

// Quick action cards
const quickActions = [
  {
    to: '/chat?mode=voice',
    icon: 'i-lucide-mic',
    title: 'Mode Vocal',
    description: 'Parlez directement à l\'assistant',
    gradient: 'from-emerald-500 to-emerald-700'
  },
  {
    to: '/chat?mode=text',
    icon: 'i-lucide-message-square',
    title: 'Mode Texte',
    description: 'Écrivez votre message',
    gradient: 'from-emerald-600 to-emerald-800'
  }
]
</script>

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
      <UCard
        v-for="stat in stats"
        :key="stat.label"
        :ui="{
          root: 'bg-[#111916] border-emerald-900/50 hover:border-emerald-700 transition-colors',
          body: 'p-5'
        }"
      >
        <div class="flex items-center gap-3">
          <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-emerald-900/50">
            <UIcon
              :name="stat.icon"
              class="h-5 w-5 text-emerald-400"
            />
          </div>
          <div class="min-w-0">
            <p class="text-2xl font-bold text-white">
              {{ stat.value }}
            </p>
            <p class="truncate text-xs text-emerald-300/50">
              {{ stat.label }}
            </p>
          </div>
        </div>

        <div
          v-if="stat.trend"
          class="mt-3 flex items-center gap-1.5"
        >
          <UBadge
            :color="stat.trend > 0 ? 'success' : 'error'"
            variant="subtle"
            size="xs"
          >
            <UIcon
              :name="stat.trend > 0 ? 'i-lucide-trending-up' : 'i-lucide-trending-down'"
              class="mr-1 h-3 w-3"
            />
            {{ Math.abs(stat.trend) }}%
          </UBadge>
          <span class="text-xs text-emerald-300/40">
            vs semaine dernière
          </span>
        </div>
      </UCard>
    </section>

    <!-- Quick actions -->
    <UCard
      :ui="{
        root: 'bg-[#111916] border-emerald-900/50',
        body: 'p-6'
      }"
    >
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon
            name="i-lucide-sparkles"
            class="h-5 w-5 text-emerald-400"
          />
          <h2 class="font-semibold text-white">
            Démarrer une conversation
          </h2>
        </div>
      </template>

      <div class="grid gap-4 md:grid-cols-2">
        <NuxtLink
          v-for="action in quickActions"
          :key="action.to"
          :to="action.to"
          class="group flex items-center gap-4 rounded-xl border border-emerald-800 bg-emerald-900/20 p-5 transition hover:border-emerald-600 hover:bg-emerald-900/40"
        >
          <div
            :class="[
              'flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-linear-to-br transition group-hover:glow-emerald',
              action.gradient
            ]"
          >
            <UIcon
              :name="action.icon"
              class="h-7 w-7 text-white"
            />
          </div>
          <div class="min-w-0 flex-1">
            <h3 class="font-medium text-white">
              {{ action.title }}
            </h3>
            <p class="text-sm text-emerald-300/50">
              {{ action.description }}
            </p>
          </div>
          <UIcon
            name="i-lucide-arrow-right"
            class="h-5 w-5 shrink-0 text-emerald-600 transition group-hover:translate-x-1 group-hover:text-emerald-400"
          />
        </NuxtLink>
      </div>
    </UCard>

    <!-- Recent conversations -->
    <UCard
      :ui="{
        root: 'bg-[#111916] border-emerald-900/50',
        body: 'p-6'
      }"
    >
      <template #header>
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <UIcon
              name="i-lucide-history"
              class="h-5 w-5 text-emerald-400"
            />
            <h2 class="font-semibold text-white">
              Conversations récentes
            </h2>
          </div>
          <UButton
            variant="ghost"
            size="sm"
            color="neutral"
            trailing-icon="i-lucide-chevron-right"
          >
            Voir tout
          </UButton>
        </div>
      </template>

      <!-- Liste des conversations -->
      <div
        v-if="recentConversations.length > 0"
        class="space-y-2"
      >
        <div
          v-for="conv in recentConversations"
          :key="conv.id"
          class="group flex cursor-pointer items-center gap-4 rounded-lg border border-transparent p-3 transition hover:border-emerald-800 hover:bg-emerald-900/20"
        >
          <UAvatar
            :icon="conv.mode === 'voice' ? 'i-lucide-mic' : 'i-lucide-message-square'"
            size="md"
            :ui="{
              root: 'bg-emerald-900/50',
              icon: 'text-emerald-400'
            }"
          />
          <div class="min-w-0 flex-1">
            <p class="truncate font-medium text-white">
              {{ conv.title }}
            </p>
            <p class="truncate text-xs text-emerald-300/50">
              {{ conv.preview }}
            </p>
          </div>
          <div class="shrink-0 text-right">
            <p class="text-xs text-emerald-300/40">
              {{ conv.date }}
            </p>
            <UBadge
              color="primary"
              variant="subtle"
              size="xs"
            >
              {{ conv.messages }} msg
            </UBadge>
          </div>
          <UIcon
            name="i-lucide-chevron-right"
            class="h-4 w-4 shrink-0 text-emerald-700 opacity-0 transition group-hover:opacity-100"
          />
        </div>
      </div>

      <!-- Empty state -->
      <div
        v-else
        class="py-12 text-center"
      >
        <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-900/30">
          <UIcon
            name="i-lucide-message-circle"
            class="h-8 w-8 text-emerald-400/50"
          />
        </div>
        <p class="font-medium text-emerald-300/60">
          Aucune conversation pour le moment
        </p>
        <p class="mt-1 text-sm text-emerald-300/40">
          Démarrez votre première conversation ci-dessus
        </p>
        <UButton
          class="mt-4"
          to="/chat"
          trailing-icon="i-lucide-arrow-right"
        >
          Nouvelle conversation
        </UButton>
      </div>
    </UCard>
  </div>
</template>
