# ARCHITECHTURE 

┌─────────────────────────────────────────────────┐
│                  FRONTEND                        │
│  Nuxt 4 + NuxtUI (Web) + WebSocket client       │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│              NUXT SERVER (API)                   │
│  • Routes API REST                               │
│  • WebSocket server (real-time)                  │
│  • LangChain orchestration                       │
└─┬────────┬────────┬────────┬─────────┬──────────┘
  │        │        │        │         │
  ▼        ▼        ▼        ▼         ▼
┌────┐  ┌────┐  ┌──────┐  ┌─────┐  ┌──────┐
│Supa│  │Qdrant│ │Redis │  │LLM  │  │Tools │
│base│  │Vector│ │Cache │  │API  │  │Agents│
└────┘  └──────┘ └──────┘  └─────┘  └──────┘
                                        │
                    ┌───────────────────┴────────────┐
                    ▼                                ▼
              ┌──────────┐                    ┌──────────┐
              │ Météo API│                    │Home APIs │
              │ Agent    │                    │(Temp,etc)│
              └──────────┘                    └──────────┘

┌─────────────────────────────────────────────────┐
│              IoT DEVICE                          │
│  • Microphone + Speaker                          │
│  • WebSocket client → Nuxt Server                │
│  • Local STT (Whisper tiny) ou cloud             │
│  • TTS (Piper local ou cloud)                    │
└──────────────────────────────────────────────────┘


# Structure 
mon-assistant/
├── front/          # Frontend + API
├── docker/            # Docker configs
│   ├── qdrant/
│   ├── redis/
│   └── docker-compose.yml
├── agents/            # Logique agents séparée
│   ├── rag/
│   ├── weather/
│   └── home-control/
└── iot/               # Code pour ton device IoT