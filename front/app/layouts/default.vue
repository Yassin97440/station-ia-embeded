<script setup lang="ts">
import type { NavigationMenuItem, DropdownMenuItem } from '@nuxt/ui'

const route = useRoute()
const supabase = useSupabaseClient()
const user = useSupabaseUser()

// Navigation items
const navItems = computed<NavigationMenuItem[]>(() => [
  {
    label: 'Dashboard',
    icon: 'i-lucide-layout-dashboard',
    to: '/',
    active: route.path === '/'
  },
  {
    label: 'Chat',
    icon: 'i-lucide-message-square',
    to: '/chat',
    active: route.path.startsWith('/chat')
  }
])

// Logout function
const logout = async () => {
  await supabase.auth.signOut()
  await navigateTo('/login')
}

// User dropdown items
const userMenuItems = computed<DropdownMenuItem[][]>(() => [
  [
    {
      label: 'Profil',
      icon: 'i-lucide-user'
    },
    {
      label: 'Paramètres',
      icon: 'i-lucide-settings'
    }
  ],
  [
    {
      label: 'Déconnexion',
      icon: 'i-lucide-log-out',
      color: 'error' as const,
      onSelect: logout
    }
  ]
])

// User display name
const displayName = computed(() => {
  if (!user.value) return 'Utilisateur'

  // Try to get full_name from user metadata
  const metadata = user.value.user_metadata
  if (metadata?.full_name) return metadata.full_name

  // Fallback to email
  const email = user.value.email
  if (email) return email.split('@')[0]

  return 'Utilisateur'
})

// User avatar URL
const avatarUrl = computed(() => {
  if (!user.value) return ''

  // Check for OAuth avatar
  const metadata = user.value.user_metadata
  if (metadata?.avatar_url) return metadata.avatar_url
  if (metadata?.picture) return metadata.picture

  // Generate from email
  const seed = user.value.email || user.value.id
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}`
})

// Footer links
const footerLinks = [
  { label: 'Confidentialité', to: '/privacy' },
  { label: 'Conditions', to: '/terms' }
]
</script>

<template>
  <div class="min-h-screen bg-tropical text-white">
    <!-- Particles background -->
    <ParticlesBackground />

    <!-- Header -->
    <UHeader
      :ui="{
        root: 'bg-[#0a0f0d]/80 backdrop-blur-sm border-b border-emerald-900/50'
      }"
    >
      <template #title>
        <AppLogo size="sm" />
      </template>

      <!-- Navigation centrale -->
      <UNavigationMenu
        :items="navItems"
        :ui="{
          link: 'text-emerald-300/70 hover:text-emerald-300 data-[active]:text-emerald-400'
        }"
      />

      <template #right>
        <!-- User menu -->
        <UDropdownMenu :items="userMenuItems">
          <UButton
            color="neutral"
            variant="ghost"
            class="gap-2"
          >
            <UAvatar
              :src="avatarUrl"
              size="xs"
            />
            <span class="hidden text-sm text-emerald-100 md:block">
              {{ displayName }}
            </span>
            <UIcon
              name="i-lucide-chevron-down"
              class="h-4 w-4 text-emerald-400"
            />
          </UButton>
        </UDropdownMenu>
      </template>

      <!-- Mobile menu body -->
      <template #body>
        <UNavigationMenu
          :items="navItems"
          orientation="vertical"
          class="-mx-2.5"
        />
      </template>
    </UHeader>

    <!-- Main content -->
    <UMain class="relative z-10 mx-auto max-w-6xl px-4 py-8">
      <slot />
    </UMain>

    <!-- Footer -->
    <UFooter
      :ui="{
        root: 'bg-[#0a0f0d]/80 backdrop-blur-sm border-t border-emerald-900/50'
      }"
    >
      <template #left>
        <div class="flex items-center gap-2 text-sm text-emerald-300/50">
          <span>🌿</span>
          <span>RIVO-IA v0.1</span>
          <USeparator
            orientation="vertical"
            class="h-4"
          />
          <span>Assistant Vocal Intelligent</span>
        </div>
      </template>

      <template #right>
        <div class="flex items-center gap-4 text-xs text-emerald-300/40">
          <span>© {{ new Date().getFullYear() }} Station IA</span>
          <template
            v-for="(link, index) in footerLinks"
            :key="link.label"
          >
            <USeparator
              v-if="index > 0"
              orientation="vertical"
              class="h-3"
            />
            <NuxtLink
              :to="link.to"
              class="transition hover:text-emerald-300"
            >
              {{ link.label }}
            </NuxtLink>
          </template>
        </div>
      </template>
    </UFooter>
  </div>
</template>
