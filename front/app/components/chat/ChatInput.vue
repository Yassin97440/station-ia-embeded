<script setup lang="ts">
const props = defineProps<{
  mode: 'voice' | 'text'
  isRecording?: boolean
  disabled?: boolean
}>()

const emit = defineEmits<{
  send: [content: string]
  toggleRecording: []
}>()

const textInput = ref('')

function handleSend() {
  if (!textInput.value.trim()) return
  emit('send', textInput.value)
  textInput.value = ''
}

function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSend()
  }
}
</script>

<template>
  <div class="mt-4">
    <!-- Voice mode -->
    <div
      v-if="mode === 'voice'"
      class="flex flex-col items-center gap-4"
    >
      <button
        :disabled="disabled"
        class="flex h-20 w-20 items-center justify-center rounded-full transition disabled:opacity-50"
        :class="[
          isRecording
            ? 'bg-red-500 animate-pulse-glow'
            : 'bg-linear-to-br from-emerald-500 to-emerald-700 glow-emerald hover:glow-emerald-lg'
        ]"
        @click="emit('toggleRecording')"
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
      <UTextarea
        v-model="textInput"
        placeholder="Écrivez votre message..."
        :rows="1"
        autoresize
        :maxrows="4"
        :disabled="disabled"
        class="flex-1"
        :ui="{
          root: 'w-full',
          base: 'bg-emerald-900/30 border-emerald-800 focus:border-emerald-600 text-white placeholder:text-emerald-300/40 resize-none'
        }"
        @keydown="handleKeydown"
      />
      <UButton
        size="lg"
        :disabled="!textInput.trim() || disabled"
        icon="i-lucide-send"
        @click="handleSend"
      />
    </div>
  </div>
</template>
