<template>
  <div class="flex h-[calc(100vh-12rem)] flex-col">
    <!-- Chat header -->
    <div class="mb-4 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <NuxtLink
          to="/"
          class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-900/50 text-emerald-400 transition hover:bg-emerald-800/50"
        >
          <UIcon
            name="i-lucide-arrow-left"
            class="h-4 w-4"
          />
        </NuxtLink>
        <div>
          <h1 class="font-semibold text-white">
            Nouvelle conversation
          </h1>
          <p class="text-xs text-emerald-300/50">
            Mode {{ mode === 'voice' ? 'vocal' : 'texte' }} activé
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <UButton
          :variant="mode === 'voice' ? 'solid' : 'ghost'"
          size="sm"
          @click="mode = 'voice'"
        >
          <UIcon
            name="i-lucide-mic"
            class="h-4 w-4"
          />
        </UButton>
        <UButton
          :variant="mode === 'text' ? 'solid' : 'ghost'"
          size="sm"
          @click="mode = 'text'"
        >
          <UIcon
            name="i-lucide-keyboard"
            class="h-4 w-4"
          />
        </UButton>
      </div>
    </div>

    <!-- Messages area -->
    <div class="card-forest flex-1 overflow-y-auto p-4">
      <div
        v-if="messages.length === 0"
        class="flex h-full flex-col items-center justify-center text-center"
      >
        <div class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-900/50">
          <UIcon
            name="i-lucide-bot"
            class="h-8 w-8 text-emerald-400"
          />
        </div>
        <h2 class="text-lg font-medium text-white">
          Comment puis-je vous aider ?
        </h2>
        <p class="mt-1 max-w-sm text-sm text-emerald-300/50">
          Posez une question, demandez une action ou discutez simplement avec moi.
        </p>
        <div class="mt-6 flex flex-wrap justify-center gap-2">
          <UButton
            v-for="suggestion in suggestions"
            :key="suggestion"
            variant="outline"
            size="sm"
            color="neutral"
            class="text-emerald-300/70"
            @click="sendMessage(suggestion)"
          >
            {{ suggestion }}
          </UButton>
        </div>
      </div>

      <div
        v-else
        class="space-y-4"
      >
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="[
            'flex gap-3',
            msg.role === 'user' ? 'flex-row-reverse' : ''
          ]"
        >
          <!-- Avatar -->
          <div
            :class="[
              'flex h-8 w-8 shrink-0 items-center justify-center rounded-full',
              msg.role === 'user' ? 'bg-emerald-600' : 'bg-emerald-900/50'
            ]"
          >
            <UIcon
              :name="msg.role === 'user' ? 'i-lucide-user' : 'i-lucide-bot'"
              class="h-4 w-4 text-white"
            />
          </div>

          <!-- Message bubble -->
          <div
            :class="[
              'max-w-[80%] rounded-2xl px-4 py-3',
              msg.role === 'user'
                ? 'bg-emerald-600 text-white'
                : 'bg-emerald-900/30 text-emerald-100 border border-emerald-800'
            ]"
          >
            <p class="text-sm leading-relaxed">
              {{ msg.content }}
            </p>

            <!-- Audio player for voice responses -->
            <div
              v-if="msg.audio"
              class="mt-3 pt-3 border-t border-emerald-700/50"
            >
              <audio
                :src="msg.audio"
                controls
                class="h-8 w-full"
              />
            </div>

            <!-- Actions executed -->
            <div
              v-if="msg.actions?.length"
              class="mt-3 space-y-2 pt-3 border-t border-emerald-700/50"
            >
              <div
                v-for="action in msg.actions"
                :key="action.name"
                class="flex items-center gap-2 rounded-lg bg-emerald-950/50 px-3 py-2 text-xs"
              >
                <UIcon
                  name="i-lucide-zap"
                  class="h-3 w-3 text-emerald-400"
                />
                <span class="text-emerald-300">{{ action.name }}</span>
                <UBadge
                  :color="action.status === 'success' ? 'success' : 'warning'"
                  size="xs"
                >
                  {{ action.status }}
                </UBadge>
              </div>
            </div>

            <p class="mt-2 text-xs opacity-50">
              {{ msg.time }}
            </p>
          </div>
        </div>

        <!-- Loading indicator -->
        <div
          v-if="isLoading"
          class="flex gap-3"
        >
          <div class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-900/50">
            <UIcon
              name="i-lucide-bot"
              class="h-4 w-4 text-white"
            />
          </div>
          <div class="flex items-center gap-2 rounded-2xl border border-emerald-800 bg-emerald-900/30 px-4 py-3">
            <div class="flex gap-1">
              <span
                class="h-2 w-2 animate-bounce rounded-full bg-emerald-400"
                style="animation-delay: 0ms"
              />
              <span
                class="h-2 w-2 animate-bounce rounded-full bg-emerald-400"
                style="animation-delay: 150ms"
              />
              <span
                class="h-2 w-2 animate-bounce rounded-full bg-emerald-400"
                style="animation-delay: 300ms"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input area -->
    <div class="mt-4">
      <!-- Voice mode -->
      <div
        v-if="mode === 'voice'"
        class="flex flex-col items-center gap-4"
      >
        <button
          class="flex h-20 w-20 items-center justify-center rounded-full transition"
          :class="[
            isRecording
              ? 'bg-red-500 animate-pulse-glow'
              : 'bg-gradient-to-br from-emerald-500 to-emerald-700 glow-emerald hover:glow-emerald-lg'
          ]"
          @click="toggleRecording"
        >
          <UIcon
            :name="isRecording ? 'i-lucide-square' : 'i-lucide-mic'"
            class="h-8 w-8 text-white"
          />
        </button>
        <p class="text-sm text-emerald-300/50">
          {{ isRecording ? 'Cliquez pour arrêter' : 'Cliquez pour parler' }}
        </p>
      </div>

      <!-- Text mode -->
      <div
        v-else
        class="flex gap-3"
      >
        <UInput
          v-model="textInput"
          placeholder="Écrivez votre message..."
          size="lg"
          class="flex-1"
          :ui="{
            base: 'bg-emerald-900/30 border-emerald-800 focus:border-emerald-600 text-white placeholder:text-emerald-300/40'
          }"
          @keyup.enter="sendTextMessage"
        />
        <UButton
          size="lg"
          :disabled="!textInput.trim()"
          @click="sendTextMessage"
        >
          <UIcon
            name="i-lucide-send"
            class="h-5 w-5"
          />
        </UButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()

// Mode (voice or text)
const mode = ref(route.query.mode === 'voice' ? 'voice' : 'text')

// State
const textInput = ref('')
const isRecording = ref(false)
const isLoading = ref(false)

// Messages
interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  time: string
  audio?: string
  actions?: { name: string, status: string }[]
}

const messages = ref<Message[]>([])

// Suggestions
const suggestions = [
  'Quelle heure est-il ?',
  'Rappelle-moi dans 10 min',
  'Quel temps fait-il ?',
  'Crée une note'
]

// Send message
function sendMessage(content: string) {
  const now = new Date()
  const time = now.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })

  messages.value.push({
    id: Date.now(),
    role: 'user',
    content,
    time
  })

  // Simulate AI response
  isLoading.value = true
  setTimeout(() => {
    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: 'Voici ma réponse à votre question. Je suis là pour vous aider !',
      time: new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }),
      actions: [
        { name: 'Recherche effectuée', status: 'success' }
      ]
    })
    isLoading.value = false
  }, 1500)
}

function sendTextMessage() {
  if (!textInput.value.trim()) return
  sendMessage(textInput.value)
  textInput.value = ''
}

function toggleRecording() {
  isRecording.value = !isRecording.value

  if (!isRecording.value) {
    // Simulate sending voice message
    sendMessage('[Message vocal]')
  }
}
</script>
