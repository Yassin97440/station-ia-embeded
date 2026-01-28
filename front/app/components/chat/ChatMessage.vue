<script setup lang="ts">
interface Action {
  name: string
  status: 'success' | 'pending' | 'error'
}

interface Props {
  role: 'user' | 'assistant'
  content: string
  time: string
  audio?: string
  actions?: Action[]
}

defineProps<Props>()
</script>

<template>
  <div
    :class="[
      'flex gap-3',
      role === 'user' ? 'flex-row-reverse' : ''
    ]"
  >
    <!-- Avatar -->
    <UAvatar
      :icon="role === 'user' ? 'i-lucide-user' : 'i-lucide-bot'"
      size="sm"
      :ui="{
        root: role === 'user' ? 'bg-emerald-600' : 'bg-emerald-900/50',
        icon: 'text-white'
      }"
    />

    <!-- Message bubble -->
    <div
      :class="[
        'max-w-[80%] rounded-2xl px-4 py-3',
        role === 'user'
          ? 'bg-emerald-600 text-white'
          : 'bg-emerald-900/30 text-emerald-100 border border-emerald-800'
      ]"
    >
      <p class="text-sm leading-relaxed whitespace-pre-wrap">
        {{ content }}
      </p>

      <!-- Audio player for voice responses -->
      <div
        v-if="audio"
        class="mt-3 border-t border-emerald-700/50 pt-3"
      >
        <audio
          :src="audio"
          controls
          class="h-8 w-full"
        />
      </div>

      <!-- Actions executed -->
      <div
        v-if="actions?.length"
        class="mt-3 space-y-2 border-t border-emerald-700/50 pt-3"
      >
        <div
          v-for="action in actions"
          :key="action.name"
          class="flex items-center gap-2 rounded-lg bg-emerald-950/50 px-3 py-2"
        >
          <UIcon
            name="i-lucide-zap"
            class="h-3 w-3 text-emerald-400"
          />
          <span class="flex-1 text-xs text-emerald-300">
            {{ action.name }}
          </span>
          <UBadge
            :color="action.status === 'success' ? 'success' : action.status === 'error' ? 'error' : 'warning'"
            variant="subtle"
            size="xs"
          >
            {{ action.status === 'success' ? 'Terminé' : action.status === 'error' ? 'Erreur' : 'En cours' }}
          </UBadge>
        </div>
      </div>

      <p class="mt-2 text-xs opacity-50">
        {{ time }}
      </p>
    </div>
  </div>
</template>
