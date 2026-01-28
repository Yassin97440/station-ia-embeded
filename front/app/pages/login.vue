<script setup lang="ts">
definePageMeta({
  layout: false
})

const supabase = useSupabaseClient()
const redirectInfo = useSupabaseCookieRedirect()

// Form state
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref<string | null>(null)

// Sign in with email/password
const signIn = async () => {
  if (!email.value || !password.value) {
    error.value = 'Veuillez remplir tous les champs'
    return
  }

  loading.value = true
  error.value = null

  const { error: signInError } = await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value
  })

  if (signInError) {
    error.value = signInError.message === 'Invalid login credentials'
      ? 'Email ou mot de passe incorrect'
      : signInError.message
    loading.value = false
    return
  }

  // Redirect to saved path or home
  const path = redirectInfo.pluck()
  await navigateTo(path || '/')
}

// Sign in with OAuth (Google)
const signInWithGoogle = async () => {
  loading.value = true
  error.value = null

  const { error: oauthError } = await supabase.auth.signInWithOAuth({
    provider: 'google',
    options: {
      redirectTo: `${window.location.origin}/confirm`
    }
  })

  if (oauthError) {
    error.value = oauthError.message
    loading.value = false
  }
}

// Sign in with OAuth (GitHub)
const signInWithGitHub = async () => {
  loading.value = true
  error.value = null

  const { error: oauthError } = await supabase.auth.signInWithOAuth({
    provider: 'github',
    options: {
      redirectTo: `${window.location.origin}/confirm`
    }
  })

  if (oauthError) {
    error.value = oauthError.message
    loading.value = false
  }
}
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-tropical p-4">
    <!-- Background effect -->
    <div class="fixed inset-0 z-0">
      <div class="absolute inset-0 bg-linear-to-br from-emerald-950/50 via-transparent to-emerald-900/30" />
    </div>

    <!-- Login card -->
    <UCard
      class="relative z-10 w-full max-w-md"
      :ui="{
        root: 'bg-[#111916]/90 backdrop-blur-xl border-emerald-900/50',
        body: 'p-8'
      }"
    >
      <!-- Header -->
      <div class="mb-8 text-center">
        <div
          class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-linear-to-br from-emerald-500 to-emerald-700"
        >
          <UIcon
            name="i-lucide-leaf"
            class="h-8 w-8 text-white"
          />
        </div>
        <h1 class="text-2xl font-bold text-gradient-emerald">
          Connexion
        </h1>
        <p class="mt-2 text-sm text-emerald-300/60">
          Accédez à votre assistant vocal intelligent
        </p>
      </div>

      <!-- Error message -->
      <UAlert
        v-if="error"
        color="error"
        variant="subtle"
        class="mb-6"
        :close-button="{ icon: 'i-lucide-x', color: 'error', variant: 'link' }"
        @close="error = null"
      >
        <template #icon>
          <UIcon name="i-lucide-alert-circle" />
        </template>
        {{ error }}
      </UAlert>

      <!-- Form -->
      <UForm
        class="space-y-5"
        @submit.prevent="signIn"
      >
        <UFormField label="Email">
          <UInput
            v-model="email"
            type="email"
            placeholder="votre@email.com"
            icon="i-lucide-mail"
            size="lg"
            :disabled="loading"
            autocomplete="email"
          />
        </UFormField>

        <UFormField label="Mot de passe">
          <UInput
            v-model="password"
            type="password"
            placeholder="••••••••"
            icon="i-lucide-lock"
            size="lg"
            :disabled="loading"
            autocomplete="current-password"
          />
        </UFormField>

        <div class="flex items-center justify-between text-sm">
          <UCheckbox
            label="Se souvenir de moi"
            color="primary"
          />
          <NuxtLink
            to="/forgot-password"
            class="text-emerald-400 hover:text-emerald-300"
          >
            Mot de passe oublié ?
          </NuxtLink>
        </div>

        <UButton
          type="submit"
          block
          size="lg"
          :loading="loading"
          :disabled="loading"
        >
          <UIcon
            name="i-lucide-log-in"
            class="mr-2 h-5 w-5"
          />
          Se connecter
        </UButton>
      </UForm>

      <!-- Divider -->
      <div class="my-6 flex items-center gap-4">
        <USeparator class="flex-1" />
        <span class="text-xs text-emerald-300/40">ou continuer avec</span>
        <USeparator class="flex-1" />
      </div>

      <!-- OAuth buttons -->
      <div class="grid grid-cols-2 gap-3">
        <UButton
          color="neutral"
          variant="outline"
          size="lg"
          :disabled="loading"
          @click="signInWithGoogle"
        >
          <UIcon
            name="i-simple-icons-google"
            class="mr-2 h-5 w-5"
          />
          Google
        </UButton>
        <UButton
          color="neutral"
          variant="outline"
          size="lg"
          :disabled="loading"
          @click="signInWithGitHub"
        >
          <UIcon
            name="i-simple-icons-github"
            class="mr-2 h-5 w-5"
          />
          GitHub
        </UButton>
      </div>

      <!-- Register link -->
      <p class="mt-8 text-center text-sm text-emerald-300/60">
        Pas encore de compte ?
        <NuxtLink
          to="/register"
          class="font-medium text-emerald-400 hover:text-emerald-300"
        >
          Créer un compte
        </NuxtLink>
      </p>
    </UCard>
  </div>
</template>
