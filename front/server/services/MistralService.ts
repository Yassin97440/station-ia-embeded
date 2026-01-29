import { ChatMistralAI } from '@langchain/mistralai'
import {
  START,
  END,
  MessagesAnnotation,
  StateGraph,
  MemorySaver
} from '@langchain/langgraph'

export class MistralService {
  private readonly llm: ChatMistralAI
  private readonly app: ReturnType<typeof this.createGraph>
  private readonly memory: MemorySaver
  private readonly systemPrompt: string

  constructor(
    apiKey: string,
    model: string = 'mistral-medium-latest',
    systemPrompt: string = 'You are a helpful assistant.'
  ) {
    this.systemPrompt = systemPrompt
    this.llm = new ChatMistralAI({
      apiKey,
      model,
      temperature: 0,
      maxRetries: 2
    })

    // Créer le checkpointer pour la persistance
    this.memory = new MemorySaver()
    this.app = this.createGraph()
  }

  private createGraph() {
    const llm = this.llm
    const systemPrompt = this.systemPrompt

    // Fonction qui appelle le modèle avec le contexte
    const callModel = async (state: typeof MessagesAnnotation.State) => {
      const messages = [
        { role: 'system', content: systemPrompt },
        ...state.messages
      ]
      const response = await llm.invoke(messages)
      return { messages: response }
    }

    // Créer le workflow
    const workflow = new StateGraph(MessagesAnnotation)
      .addNode('model', callModel)
      .addEdge(START, 'model')
      .addEdge('model', END)

    // Compiler avec le checkpointer
    return workflow.compile({ checkpointer: this.memory })
  }

  // Chat avec persistance - utilise un thread_id pour identifier la conversation
  async chat(message: string, threadId: string) {
    const config = { configurable: { thread_id: threadId } }

    const result = await this.app.invoke(
      { messages: [{ role: 'user', content: message }] },
      config
    )

    // Retourne le dernier message (la réponse de l'assistant)
    return result.messages[result.messages.length - 1]
  }
}
