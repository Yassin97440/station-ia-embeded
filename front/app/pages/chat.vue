<script setup lang="ts">
// Route
const route = useRoute()

// State
const mode = ref<'voice' | 'text'>(route.query.mode === 'voice' ? 'voice' : 'text')
const isRecording = ref(false)
const isLoading = ref(false)
const messages = ref<Message[]>([])
const messagesContainer = ref<HTMLElement>()

// Suggestions
const suggestions = [
  { label: 'Quelle heure est-il ?', icon: 'i-lucide-clock' },
  { label: 'Rappelle-moi dans 10 min', icon: 'i-lucide-bell' },
  { label: 'Quel temps fait-il ?', icon: 'i-lucide-cloud-sun' },
  { label: 'Crée une note', icon: 'i-lucide-file-plus' }
]

// Mode toggle items
const modeItems = [
  { value: 'voice', icon: 'i-lucide-mic', label: 'Vocal' },
  { value: 'text', icon: 'i-lucide-keyboard', label: 'Texte' }
]

// Scroll to bottom when new message
function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// Get current time formatted
function getCurrentTime() {
  return new Date().toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

// Send message
async function sendMessage(content: string) {
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content,
    time: getCurrentTime()
  })

  scrollToBottom()

  // Simulate AI response
  isLoading.value = true
  const response = await $fetch('/api/simple-message', {
    method: 'POST',
    body: {
      message: content
    }
  })
  console.log('Response:', response)
  messages.value.push({
    id: Date.now() + 1,
    role: 'assistant',
    content: response.response.content as string,
    time: getCurrentTime()
  })
  scrollToBottom()
  isLoading.value = false
}

// Toggle recording
function toggleRecording() {
  isRecording.value = !isRecording.value

  if (!isRecording.value) {
    // Simulate sending voice message
    sendMessage('🎤 Message vocal envoyé')
  }
}

// Watch mode changes
watch(mode, () => {
  // Reset recording when switching modes
  isRecording.value = false
})
</script>

<template>
  <div class="flex h-[calc(100vh-12rem)] flex-col">
    <!-- Chat header -->
    <div class="mb-4 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <UButton to="/" color="neutral" variant="ghost" icon="i-lucide-arrow-left" size="sm" />
        <div>
          <h1 class="font-semibold text-white">
            Nouvelle conversation
          </h1>
          <p class="text-xs text-emerald-300/50">
            Mode {{ mode === 'voice' ? 'vocal' : 'texte' }} activé
          </p>
        </div>
      </div>

      <!-- Mode toggle -->
      <UButtonGroup size="sm">
        <UButton v-for="item in modeItems" :key="item.value" :icon="item.icon"
          :variant="mode === item.value ? 'solid' : 'ghost'" :color="mode === item.value ? 'primary' : 'neutral'"
          @click="mode = item.value as 'voice' | 'text'">
          <span class="hidden sm:inline">
            {{ item.label }}
          </span>
        </UButton>
      </UButtonGroup>
    </div>

    <!-- Messages area -->
    <UCard :ui="{
      root: 'flex-1 flex flex-col overflow-hidden bg-[#111916] border-emerald-900/50',
      body: 'flex-1 overflow-y-auto p-4'
    }">
      <div ref="messagesContainer" class="h-full overflow-y-auto">
        <!-- Empty state -->
        <div v-if="messages.length === 0" class="flex h-full flex-col items-center justify-center text-center">
          <div class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-900/50">
            <UIcon name="i-lucide-bot" class="h-8 w-8 text-emerald-400" />
          </div>
          <h2 class="text-lg font-medium text-white">
            Comment puis-je vous aider ?
          </h2>
          <p class="mt-1 max-w-sm text-sm text-emerald-300/50">
            Posez une question, demandez une action ou discutez simplement avec moi.
          </p>

          <!-- Suggestions -->
          <div class="mt-6 flex flex-wrap justify-center gap-2">
            <UButton v-for="suggestion in suggestions" :key="suggestion.label" variant="outline" size="sm"
              color="neutral" :icon="suggestion.icon" class="text-emerald-300/70"
              @click="sendMessage(suggestion.label)">
              {{ suggestion.label }}
            </UButton>
          </div>
        </div>

        <!-- Messages list -->
        <div v-else class="space-y-4">
          <ChatMessage v-for="msg in messages" :key="msg.id" :role="msg.role" :content="msg.content" :time="msg.time"
            :audio="msg.audio" :actions="msg.actions" />

          <!-- Typing indicator -->
          <ChatTypingIndicator v-if="isLoading" />
        </div>
      </div>
    </UCard>

    <!-- Input area -->
    <ChatInput :mode="mode" :is-recording="isRecording" :disabled="isLoading" @send="sendMessage"
      @toggle-recording="toggleRecording" />
  </div>
</template>
