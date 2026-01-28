interface Action {
  name: string
  status: 'success' | 'pending' | 'error'
}

interface Message {
  id: number
  role: 'user' | 'assistant'
  content: string
  time: string
  audio?: string
  actions?: Action[]
}

export type { Action, Message }
