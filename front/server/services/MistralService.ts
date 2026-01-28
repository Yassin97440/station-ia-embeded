import { ChatMistralAI } from '@langchain/mistralai'

export class MistralService {
  private readonly apiKey: string
  private readonly llm: ChatMistralAI
  private readonly model: string
  private readonly system_prompt: string
  constructor(apiKey: string, model: string = 'mistral-medium-latest', system_prompt: string = 'You are a helpful assistant.') {
    this.apiKey = apiKey
    this.model = model
    this.system_prompt = system_prompt
    this.llm = new ChatMistralAI({
      model: this.model,
      temperature: 0,
      maxRetries: 2
    // other params...
    })
  }

  async chat(message: string) {
    const response = await this.llm.invoke(message)
    return response
  }
}
