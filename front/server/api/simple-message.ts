import { MistralService } from '../services/MistralService'

export default defineEventHandler(async (event) => {
  console.log('Simple Message')
  const body = await readBody(event)
  console.log('Body:', body)
  const llm = new MistralService(process.env.MISTRAL_API_KEY || '', 'mistral-small-latest', 'You are a helpful assistant. Respond in French.')
  const response = await llm.chat(body.message)
  console.log('Response:', response)

  return {
    response: {
      content: response.content,
      role: 'assistant'
    }
  }
})
