<script setup lang="ts">
definePageMeta({
  layout: false
})

const supabase = useSupabaseClient()

// Form state
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const fullName = ref('')
const loading = ref(false)
const error = ref<string | null>(null)
const success = ref(false)

// Password validation
const passwordStrength = computed(() => {
  const pwd = password.value
  let strength = 0

  if (pwd.length >= 8) strength++
  if (/[a-z]/.test(pwd) && /[A-Z]/.test(pwd)) strength++
  if (/\d/.test(pwd)) strength++
  if (/[^a-zA-Z\d]/.test(pwd)) strength++

  return strength
})

const passwordStrengthColor = computed(() => {
  switch (passwordStrength.value) {
    case 0:
    case 1:
      return 'error'
    case 2:
      return 'warning'
    case 3:
    case 4:
      return 'success'
    default:
      return 'neutral'
  }
})

const passwordStrengthText = computed(() => {
  switch (passwordStrength.value) {
    case 0:
    case 1:
      return 'Faible'
    case 2:
      return 'Moyen'
    case 3:
    case 4:
      return 'Fort'
    default:
      return ''
  }
})

// Sign up
const signUp = async () => {
  // Validation
  if (!email.value || !password.value || !confirmPassword.value || !fullName.value) {
    error.value = 'Veuillez remplir tous les champs'
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Les mots de passe ne correspondent pas'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Le mot de passe doit contenir au moins 8 caractères'
    return
  }

  loading.value = true
  error.value = null

  const { error: signUpError } = await supabase.auth.signUp({
    email: email.value,
    password: password.value,
    options: {
      data: {
        full_name: fullName.value
      },
      emailRedirectTo: `${window.location.origin}/confirm`
    }
  })

  if (signUpError) {
    if (signUpError.message.includes('already registered')) {
      error.value = 'Un compte existe déjà avec cet email'
    } else {
      error.value = signUpError.message
    }
    loading.value = false
    return
  }

  success.value = true
  loading.value = false
}

// Sign up with OAuth (Google)
const signUpWithGoogle = async () => {
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

// Sign up with OAuth (GitHub)
const signUpWithGitHub = async () => {
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

    <!-- Register card -->
    <UCard
      class="relative z-10 w-full max-w-md"
      :ui="{
        root: 'bg-[#111916]/90 backdrop-blur-xl border-emerald-900/50',
        body: 'p-8'
      }"
    >
      <!-- Success state -->
      <div
        v-if="success"
        class="text-center"
      >
        <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/20">
          <UIcon
            name="i-lucide-mail-check"
            class="h-8 w-8 text-emerald-400"
          />
        </div>
        <h2 class="text-xl font-bold text-white">
          Vérifiez votre email
        </h2>
        <p class="mt-3 text-sm text-emerald-300/60">
          Un email de confirmation a été envoyé à
          <span class="font-medium text-emerald-400">{{ email }}</span>.
          Cliquez sur le lien pour activer votre compte.
        </p>
        <UButton
          class="mt-6"
          to="/login"
          variant="outline"
        >
          Retour à la connexion
        </UButton>
      </div>

      <!-- Register form -->
      <template v-else>
        <!-- Header -->
        <div class="mb-8 text-center">
          <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-linear-to-br from-emerald-500 to-emerald-700">
            <UIcon
              name="i-lucide-user-plus"
              class="h-8 w-8 text-white"
            />
          </div>
          <h1 class="text-2xl font-bold text-gradient-emerald">
            Créer un compte
          </h1>
          <p class="mt-2 text-sm text-emerald-300/60">
            Rejoignez RIVO-IA et accédez à votre assistant vocal
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
        <form
          class="space-y-5"
          @submit.prevent="signUp"
        >
          <UFormField label="Nom complet">
            <UInput
              v-model="fullName"
              type="text"
              placeholder="Jean Dupont"
              icon="i-lucide-user"
              size="lg"
              :disabled="loading"
              autocomplete="name"
            />
          </UFormField>

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
              autocomplete="new-password"
            />
            <!-- Password strength indicator -->
            <div
              v-if="password"
              class="mt-2 flex items-center gap-2"
            >
              <div class="flex flex-1 gap-1">
                <div
                  v-for="i in 4"
                  :key="i"
                  class="h-1 flex-1 rounded-full transition-colors"
                  :class="i <= passwordStrength ? `bg-${passwordStrengthColor}-500` : 'bg-emerald-900/50'"
                />
              </div>
              <span
                class="text-xs"
                :class="`text-${passwordStrengthColor}-400`"
              >
                {{ passwordStrengthText }}
              </span>
            </div>
          </UFormField>

          <UFormField label="Confirmer le mot de passe">
            <UInput
              v-model="confirmPassword"
              type="password"
              placeholder="••••••••"
              icon="i-lucide-lock"
              size="lg"
              :disabled="loading"
              autocomplete="new-password"
            />
          </UFormField>

          <UButton
            type="submit"
            block
            size="lg"
            :loading="loading"
            :disabled="loading"
          >
            <UIcon
              name="i-lucide-user-plus"
              class="mr-2 h-5 w-5"
            />
            Créer mon compte
          </UButton>
        </form>

        <!-- Divider -->
        <div class="my-6 flex items-center gap-4">
          <USeparator class="flex-1" />
          <span class="text-xs text-emerald-300/40">ou s'inscrire avec</span>
          <USeparator class="flex-1" />
        </div>

        <!-- OAuth buttons -->
        <div class="grid grid-cols-2 gap-3">
          <UButton
            color="neutral"
            variant="outline"
            size="lg"
            :disabled="loading"
            @click="signUpWithGoogle"
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
            @click="signUpWithGitHub"
          >
            <UIcon
              name="i-simple-icons-github"
              class="mr-2 h-5 w-5"
            />
            GitHub
          </UButton>
        </div>

        <!-- Login link -->
        <p class="mt-8 text-center text-sm text-emerald-300/60">
          Déjà un compte ?
          <NuxtLink
            to="/login"
            class="font-medium text-emerald-400 hover:text-emerald-300"
          >
            Se connecter
          </NuxtLink>
        </p>
      </template>
    </UCard>
  </div>
</template>
