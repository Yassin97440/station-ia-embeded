import { MistralService } from '../services/MistralService'

const llm = new MistralService(process.env.MISTRAL_API_KEY || '',
  'mistral-small-latest',
  'You are a helpful assistant. Respond in French.'
)
export default defineEventHandler(async (event) => {
  console.log('Simple Message')
  const body = await readBody(event)
  // Le threadId peut venir du client pour identifier la conversation
  const threadId = body.threadId || 'default-thread'
  const response = await llm.chat(body.message, threadId)

  return {
    response: {
      content: response?.content,
      role: 'assistant'
    }
  }
})
