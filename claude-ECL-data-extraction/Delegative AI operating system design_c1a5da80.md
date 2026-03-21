# Delegative AI operating system design

## Overview
- **Title:** Delegative AI operating system design
- **Url:** [https://claude.ai/chat/c1a5da80-2065-4945-80ba-ad871230a72a](https://claude.ai/chat/c1a5da80-2065-4945-80ba-ad871230a72a)
- **ID:** c1a5da80-2065-4945-80ba-ad871230a72a
- **Created:** 10/12/2025, 11:17:03 AM
- **Last Updated:** 10/12/2025, 11:50:27 AM
- **Total Messages:** 10

## Conversation
👉 - Indicates the current conversation path

<i>[10/12/2025, 11:17:05 AM]</i> 👉 <b>👤 User</b>: <br>
<i>[10/12/2025, 11:17:23 AM]</i> 👉 <b>🤖 Assistant</b>: 

The user has uploaded a PDF document that appears to be a critique/analysis of something called "AI Studio Chat" - a concept for a "Delegative Operating System for AI Interaction." The document is written as feedback to someone named Phoenix about their concept.

Let me read through this document to understand what it's about:

Key concepts from the document:
1. It's about a paradigm shift from "conversation interface" to "delegative operating system"
2. The system has a four-layer hierarchical structure: Executive → Department Head → Chief of Staff → Workers
3. It's designed to reduce cognitive load and chaos in AI interactions
4. Features include an "Enrichment Chain" and "Institutional Memory System"
5. The document provides both praise and suggestions for improvement
6. Areas to strengthen include: Governance & Policy, Language of Authority, Interoperability, Visual Layer, and Narrative Branding
7. Proposes next steps including MVP development starting with Chief of Staff AI

The user hasn't asked me a specific question yet - they've just uploaded the document. I should acknowledge receipt and ask what they'd like me to help them with regarding this document. I could:
- Summarize it
- Analyze it
- Help develop the concepts further
- Create the deliverables suggested in the document
- Discuss specific aspects

Let me provide a helpful, open-ended response that shows I've understood the document and am ready to help.I've read through this fascinating document - it's a comprehensive critique and enhancement proposal for a **Delegative Operating System for AI interaction**. This is a compelling vision that reimagines AI as a hierarchical cognitive workforce rather than a simple chat interface.

The core innovation here is architectural: treating AI interaction as an **organizational management problem** rather than a conversational UI problem. The four-layer structure (Executive → Department Head → Chief of Staff → Workers) is elegant and maps naturally to how complex work actually gets done.

Some particularly strong insights:
- **"The cost is in the chaos, not the compute"** - brilliant reframing of AI efficiency
- The **Enrichment Chain** as a bidirectional meaning refinement system
- **Institutional Memory** that turns ephemeral chats into persistent, queryable knowledge
- The focus on **bounded agency** through Task Charters

The critique also identifies smart areas for enhancement - governance layers, interoperability protocols, and the suggestion to build the Chief of Staff AI as the MVP entry point.

## What would you like to explore?

I can help you:
1. **Develop the System Architecture Blueprint** mentioned at the end
2. **Draft the Delegation Protocol / Task Charter schema**
3. **Design the technical implementation** (database schemas, API structure, etc.)
4. **Create UI/UX mockups** for the "Executive Suite" interface
5. **Refine the strategic positioning** and brand narrative
6. **Something else** related to this concept

What aspect would be most valuable to work on right now?<br>

<i>[10/12/2025, 11:21:07 AM]</i> 👉 <b>👤 User</b>: 

System Blueprint (MVP Scope)
* Start with the Chief of Staff AI as your first real subsystem.
* Build: conversation listener → task extractor → brief generator → OpenRouter dispatcher.<br>

<i>[10/12/2025, 11:22:39 AM]</i> 👉 <b>🤖 Assistant</b>: 

The user wants me to develop the System Blueprint for the MVP scope, specifically focusing on the Chief of Staff AI subsystem with the components:
1. Conversation listener
2. Task extractor
3. Brief generator
4. OpenRouter dispatcher

This is a technical architecture document. I should create a comprehensive blueprint that includes:
- System architecture overview
- Component specifications
- Data flows
- API designs
- Database schemas
- Implementation roadmap

Let me create a detailed, professional system blueprint that can serve as an actual implementation guide.# System Blueprint: Chief of Staff AI (MVP)

## Executive Summary

Building a **Chief of Staff AI** that sits between human conversation and AI worker execution. It listens to ongoing dialogue, extracts actionable tasks, generates structured briefs, and dispatches work to specialized AI workers via OpenRouter.

**Core Value Proposition:** Turn natural conversation into managed delegation without interrupting flow.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     CONVERSATION LAYER                       │
│  (User ←→ Executive AI Chat Interface)                      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               CHIEF OF STAFF AI SUBSYSTEM                    │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Conversation │→ │    Task      │→ │    Brief     │     │
│  │   Listener   │  │  Extractor   │  │  Generator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                              │               │
│                                              ▼               │
│                                    ┌──────────────┐         │
│                                    │  OpenRouter  │         │
│                                    │  Dispatcher  │         │
│                                    └──────────────┘         │
└─────────────────────────────────────────┬───────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    WORKER EXECUTION LAYER                    │
│  (Specialized AI Models via OpenRouter)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. **Conversation Listener**

**Purpose:** Passive monitoring of user-executive dialogue to detect delegation opportunities.

**Responsibilities:**
- Stream incoming conversation messages
- Maintain rolling context window (last N messages)
- Detect delegation triggers (keywords, patterns, explicit commands)
- Buffer context for task extraction

**Technical Specs:**
```typescript
interface ConversationListener {
  // Core methods
  attachToConversation(conversationId: string): void;
  onNewMessage(callback: MessageHandler): void;
  getRecentContext(messageCount: number): Message[];
  
  // Trigger detection
  detectDelegationSignals(message: Message): DelegationSignal[];
  
  // State management
  contextWindow: Message[];
  triggerPatterns: TriggerPattern[];
}

interface DelegationSignal {
  type: 'explicit' | 'implicit' | 'question' | 'request';
  confidence: number; // 0-1
  triggerPhrase: string;
  contextSnippet: string;
  suggestedAction: string;
}
```

**Trigger Patterns:**
```yaml
explicit_commands:
  - "delegate this to"
  - "have someone work on"
  - "spin up a task for"
  - "create a worker for"
  - "background process this"

implicit_patterns:
  - "I need [X] by [time]"
  - "Can we get [outcome]"
  - "Someone should [action]"
  - "We should analyze [topic]"
  - "Let's explore [concept]"

question_patterns:
  - "What if we [scenario]?"
  - "How would [approach] work?"
  - "Could we [action]?"
```

**Database Schema:**
```sql
CREATE TABLE conversation_contexts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,
    message_history JSONB NOT NULL,
    delegation_signals JSONB[],
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_conversation_contexts_conv_id 
ON conversation_contexts(conversation_id);
```

---

### 2. **Task Extractor**

**Purpose:** Parse conversation context and extract structured task definitions.

**Responsibilities:**
- Analyze delegation signals + surrounding context
- Identify: objective, scope, constraints, deliverables
- Classify task type and complexity
- Estimate resource requirements
- Generate task metadata

**Technical Specs:**
```typescript
interface TaskExtractor {
  extractTask(
    signal: DelegationSignal,
    context: Message[]
  ): ExtractedTask;
  
  classifyComplexity(task: ExtractedTask): ComplexityRating;
  estimateResources(task: ExtractedTask): ResourceEstimate;
}

interface ExtractedTask {
  id: string;
  conversationId: string;
  
  // Core task definition
  objective: string;
  scope: string[];
  constraints: string[];
  deliverables: Deliverable[];
  
  // Metadata
  taskType: TaskType;
  complexity: ComplexityRating;
  estimatedTokens: number;
  estimatedDuration: number; // minutes
  
  // Context
  sourceSignal: DelegationSignal;
  relevantContext: string;
  
  // Governance
  approvalRequired: boolean;
  costCeiling: number; // USD
  
  timestamp: Date;
}

enum TaskType {
  RESEARCH = 'research',
  ANALYSIS = 'analysis',
  GENERATION = 'generation',
  TRANSFORMATION = 'transformation',
  SYNTHESIS = 'synthesis',
  MONITORING = 'monitoring'
}

enum ComplexityRating {
  SIMPLE = 'simple',      // < 5 min, single-step
  MODERATE = 'moderate',  // 5-20 min, multi-step
  COMPLEX = 'complex',    // 20-60 min, requires planning
  EPIC = 'epic'          // > 60 min, needs decomposition
}

interface ResourceEstimate {
  modelRequired: string; // 'gpt-4', 'claude-3-opus', etc.
  estimatedTokens: number;
  estimatedCost: number;
  confidenceLevel: number; // 0-1
}
```

**AI Prompt Template for Extraction:**
```typescript
const EXTRACTION_PROMPT = `
You are a Chief of Staff AI analyzing a conversation to extract actionable tasks.

CONVERSATION CONTEXT:
{context}

DELEGATION SIGNAL:
{signal}

Extract a structured task definition:
1. OBJECTIVE: What needs to be accomplished? (1-2 sentences)
2. SCOPE: What's included/excluded? (bullet points)
3. CONSTRAINTS: Time, resources, quality requirements
4. DELIVERABLES: Specific outputs expected
5. TASK TYPE: {research|analysis|generation|transformation|synthesis|monitoring}
6. COMPLEXITY: {simple|moderate|complex|epic}

Respond in JSON format matching the ExtractedTask schema.
Be conservative with complexity estimates.
Flag if approval should be required (high cost/risk/ambiguity).
`;
```

**Database Schema:**
```sql
CREATE TABLE extracted_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,
    
    -- Core definition
    objective TEXT NOT NULL,
    scope JSONB NOT NULL,
    constraints JSONB NOT NULL,
    deliverables JSONB NOT NULL,
    
    -- Classification
    task_type VARCHAR(50) NOT NULL,
    complexity VARCHAR(20) NOT NULL,
    
    -- Estimates
    estimated_tokens INTEGER,
    estimated_duration INTEGER,
    estimated_cost DECIMAL(10,4),
    
    -- Context
    source_signal JSONB NOT NULL,
    relevant_context TEXT,
    
    -- Governance
    approval_required BOOLEAN DEFAULT FALSE,
    cost_ceiling DECIMAL(10,2),
    
    -- Lifecycle
    status VARCHAR(20) DEFAULT 'extracted',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    FOREIGN KEY (conversation_id) 
        REFERENCES conversation_contexts(conversation_id)
);

CREATE INDEX idx_extracted_tasks_status ON extracted_tasks(status);
CREATE INDEX idx_extracted_tasks_conv_id ON extracted_tasks(conversation_id);
```

---

### 3. **Brief Generator**

**Purpose:** Convert extracted tasks into executable worker briefs (prompts + instructions).

**Responsibilities:**
- Transform task definition into worker prompt
- Add context enrichment
- Include formatting/output specifications
- Attach relevant memory/documents
- Generate success criteria

**Technical Specs:**
```typescript
interface BriefGenerator {
  generateBrief(
    task: ExtractedTask,
    memory: MemoryContext
  ): WorkerBrief;
  
  enrichWithContext(
    brief: WorkerBrief,
    sources: ContextSource[]
  ): WorkerBrief;
  
  validateBrief(brief: WorkerBrief): ValidationResult;
}

interface WorkerBrief {
  id: string;
  taskId: string;
  
  // Core prompt
  systemPrompt: string;
  userPrompt: string;
  
  // Enrichment
  contextDocuments: Document[];
  relevantMemory: MemoryEntry[];
  examples: Example[];
  
  // Specifications
  outputFormat: OutputFormat;
  successCriteria: string[];
  qualityThresholds: QualityThreshold[];
  
  // Execution config
  modelConfig: ModelConfig;
  maxTokens: number;
  temperature: number;
  stopSequences: string[];
  
  // Governance
  costLimit: number;
  timeLimit: number; // seconds
  retryPolicy: RetryPolicy;
  
  timestamp: Date;
}

interface ModelConfig {
  provider: 'openai' | 'anthropic' | 'google' | 'meta';
  model: string;
  fallbackModels: string[];
}

interface OutputFormat {
  type: 'text' | 'json' | 'markdown' | 'code' | 'structured';
  schema?: object; // JSON schema if structured
  template?: string;
  validationRules: ValidationRule[];
}

interface QualityThreshold {
  metric: string; // 'completeness', 'accuracy', 'coherence'
  minScore: number; // 0-1
  evaluationMethod: string;
}
```

**Brief Generation Template:**
```typescript
const BRIEF_TEMPLATE = `
ROLE: You are a specialized AI worker executing a delegated task.

TASK OBJECTIVE:
{task.objective}

SCOPE:
{task.scope.map(s => `- ${s}`).join('\n')}

CONSTRAINTS:
{task.constraints.map(c => `- ${c}`).join('\n')}

CONTEXT:
{task.relevantContext}

DELIVERABLES REQUIRED:
{task.deliverables.map(d => `
- ${d.name}: ${d.description}
  Format: ${d.format}
  Quality bar: ${d.qualityRequirements}
`).join('\n')}

OUTPUT FORMAT:
{outputFormat}

SUCCESS CRITERIA:
{successCriteria.map(c => `- ${c}`).join('\n')}

INSTRUCTIONS:
1. Read and understand the full task brief
2. Gather necessary information from provided context
3. Execute the task systematically
4. Validate output against success criteria
5. Return structured deliverable

Begin your work:
`;
```

**Database Schema:**
```sql
CREATE TABLE worker_briefs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL,
    
    -- Prompts
    system_prompt TEXT NOT NULL,
    user_prompt TEXT NOT NULL,
    
    -- Context
    context_documents JSONB,
    relevant_memory JSONB,
    examples JSONB,
    
    -- Specifications
    output_format JSONB NOT NULL,
    success_criteria JSONB NOT NULL,
    quality_thresholds JSONB,
    
    -- Execution config
    model_config JSONB NOT NULL,
    max_tokens INTEGER,
    temperature DECIMAL(3,2),
    stop_sequences TEXT[],
    
    -- Governance
    cost_limit DECIMAL(10,4),
    time_limit INTEGER,
    retry_policy JSONB,
    
    -- Lifecycle
    status VARCHAR(20) DEFAULT 'generated',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    FOREIGN KEY (task_id) REFERENCES extracted_tasks(id)
);

CREATE INDEX idx_worker_briefs_task_id ON worker_briefs(task_id);
CREATE INDEX idx_worker_briefs_status ON worker_briefs(status);
```

---

### 4. **OpenRouter Dispatcher**

**Purpose:** Execute worker briefs via OpenRouter API and manage response handling.

**Responsibilities:**
- Route briefs to appropriate models
- Handle API calls + retries
- Stream responses back
- Log execution metrics
- Handle errors + fallbacks

**Technical Specs:**
```typescript
interface OpenRouterDispatcher {
  dispatch(brief: WorkerBrief): Promise<WorkerExecution>;
  
  streamResponse(
    execution: WorkerExecution,
    onChunk: (chunk: string) => void
  ): Promise<void>;
  
  handleFailure(
    execution: WorkerExecution,
    error: Error
  ): Promise<WorkerExecution>;
  
  getExecutionStatus(executionId: string): ExecutionStatus;
}

interface WorkerExecution {
  id: string;
  briefId: string;
  
  // Request
  modelUsed: string;
  requestPayload: object;
  requestTimestamp: Date;
  
  // Response
  responseContent: string;
  responseMetadata: ResponseMetadata;
  responseTimestamp: Date;
  
  // Metrics
  tokensUsed: TokenUsage;
  latencyMs: number;
  costUSD: number;
  
  // Status
  status: ExecutionStatus;
  error?: ExecutionError;
  retryCount: number;
  
  // Quality
  qualityScore?: number;
  meetsSuccessCriteria: boolean;
  validationResults: ValidationResult[];
}

interface TokenUsage {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
}

interface ResponseMetadata {
  finishReason: string;
  modelVersion: string;
  provider: string;
  requestId: string;
}

enum ExecutionStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
  RETRYING = 'retrying',
  CANCELLED = 'cancelled'
}
```

**OpenRouter Integration:**
```typescript
class OpenRouterClient {
  private apiKey: string;
  private baseUrl: string = 'https://openrouter.ai/api/v1';
  
  async createCompletion(brief: WorkerBrief): Promise<WorkerExecution> {
    const payload = {
      model: brief.modelConfig.model,
      messages: [
        {
          role: 'system',
          content: brief.systemPrompt
        },
        {
          role: 'user',
          content: brief.userPrompt
        }
      ],
      max_tokens: brief.maxTokens,
      temperature: brief.temperature,
      stop: brief.stopSequences,
      
      // OpenRouter specific
      route: 'fallback', // Use fallback models if primary fails
      models: brief.modelConfig.fallbackModels,
      provider: {
        order: ['OpenAI', 'Anthropic', 'Google']
      }
    };
    
    const response = await fetch(`${this.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'HTTP-Referer': 'https://delegativeos.ai',
        'X-Title': 'Chief of Staff AI',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });
    
    return this.parseResponse(response, brief);
  }
  
  async streamCompletion(
    brief: WorkerBrief,
    onChunk: (chunk: string) => void
  ): Promise<WorkerExecution> {
    // Streaming implementation
    // Similar to above but with stream: true
  }
}
```

**Database Schema:**
```sql
CREATE TABLE worker_executions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    brief_id UUID NOT NULL,
    
    -- Request
    model_used VARCHAR(100) NOT NULL,
    request_payload JSONB NOT NULL,
    request_timestamp TIMESTAMPTZ DEFAULT NOW(),
    
    -- Response
    response_content TEXT,
    response_metadata JSONB,
    response_timestamp TIMESTAMPTZ,
    
    -- Metrics
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    total_tokens INTEGER,
    latency_ms INTEGER,
    cost_usd DECIMAL(10,6),
    
    -- Status
    status VARCHAR(20) NOT NULL,
    error JSONB,
    retry_count INTEGER DEFAULT 0,
    
    -- Quality
    quality_score DECIMAL(3,2),
    meets_success_criteria BOOLEAN,
    validation_results JSONB,
    
    FOREIGN KEY (brief_id) REFERENCES worker_briefs(id)
);

CREATE INDEX idx_worker_executions_brief_id 
ON worker_executions(brief_id);

CREATE INDEX idx_worker_executions_status 
ON worker_executions(status);

CREATE INDEX idx_worker_executions_timestamp 
ON worker_executions(request_timestamp DESC);
```

---

## Data Flow Diagram

```
[User Message] 
    ↓
[Conversation Listener]
    ↓ (detects delegation signal)
[Task Extractor] ← (conversation context)
    ↓ (ExtractedTask)
[Brief Generator] ← (memory, documents)
    ↓ (WorkerBrief)
[OpenRouter Dispatcher]
    ↓ (API call)
[OpenRouter API] → [AI Model]
    ↓ (response)
[Worker Execution Result]
    ↓
[Chief of Staff AI] (synthesizes)
    ↓
[Executive AI] (presents to user)
```

---

## API Endpoints

### REST API
```typescript
// Task Management
POST   /api/v1/tasks/extract
GET    /api/v1/tasks/:id
PUT    /api/v1/tasks/:id/approve
DELETE /api/v1/tasks/:id/cancel

// Brief Management
POST   /api/v1/briefs/generate
GET    /api/v1/briefs/:id
PUT    /api/v1/briefs/:id/validate

// Execution Management
POST   /api/v1/executions/dispatch
GET    /api/v1/executions/:id
GET    /api/v1/executions/:id/stream
POST   /api/v1/executions/:id/retry

// Monitoring
GET    /api/v1/analytics/costs
GET    /api/v1/analytics/performance
GET    /api/v1/analytics/quality
```

### WebSocket API
```typescript
// Real-time updates
ws://api/v1/ws/conversations/:id
  → message: ConversationMessage
  → delegation_signal: DelegationSignal
  → task_extracted: ExtractedTask
  → execution_started: WorkerExecution
  → execution_chunk: StreamChunk
  → execution_completed: WorkerExecution
```

---

## Implementation Roadmap

### **Phase 1: Foundation (Week 1-2)**
- [ ] Database schema implementation
- [ ] Basic REST API scaffolding (Next.js API routes)
- [ ] OpenRouter client integration
- [ ] Simple conversation listener (keyword-based)

### **Phase 2: Core Pipeline (Week 3-4)**
- [ ] Task extractor with GPT-4 integration
- [ ] Brief generator with template system
- [ ] OpenRouter dispatcher with retry logic
- [ ] Basic execution tracking

### **Phase 3: Intelligence Layer (Week 5-6)**
- [ ] Advanced delegation signal detection (ML-based)
- [ ] Context enrichment system
- [ ] Quality validation system
- [ ] Cost/resource estimation

### **Phase 4: UI & Experience (Week 7-8)**
- [ ] Real-time execution dashboard
- [ ] Task approval workflow
- [ ] Execution history viewer
- [ ] Analytics dashboard

---

## Tech Stack Recommendation

```yaml
Backend:
  - Runtime: Node.js 20+ / Bun
  - Framework: Next.js 14 (App Router)
  - Database: PostgreSQL 16 + pgvector
  - ORM: Prisma
  - Queue: BullMQ + Redis
  - API: tRPC for type-safety

AI Integration:
  - Primary: OpenRouter API
  - Fallback: Direct OpenAI/Anthropic APIs
  - Embeddings: OpenAI text-embedding-3-large

Frontend:
  - Framework: Next.js 14 + React 18
  - Styling: Tailwind CSS
  - Components: shadcn/ui
  - State: Zustand
  - Real-time: WebSocket (Socket.io)

Infrastructure:
  - Hosting: Vercel (Next.js) + Railway (Postgres)
  - Cache: Upstash Redis
  - Monitoring: Sentry + PostHog
  - Logs: Axiom
```

---

## Configuration Example

```typescript
// config/chief-of-staff.config.ts
export const config = {
  conversationListener: {
    contextWindowSize: 20, // messages
    pollIntervalMs: 500,
    triggerConfidenceThreshold: 0.7
  },
  
  taskExtractor: {
    model: 'gpt-4-turbo-preview',
    temperature: 0.3,
    maxTokens: 2000,
    complexityThresholds: {
      simple: { tokens: 1000, duration: 5 },
      moderate: { tokens: 5000, duration: 20 },
      complex: { tokens: 15000, duration: 60 }
    }
  },
  
  briefGenerator: {
    includeExamples: true,
    maxContextDocuments: 5,
    enrichWithMemory: true
  },
  
  openRouterDispatcher: {
    apiKey: process.env.OPENROUTER_API_KEY,
    defaultModel: 'anthropic/claude-3-opus',
    fallbackModels: [
      'openai/gpt-4-turbo-preview',
      'google/gemini-pro-1.5'
    ],
    retryAttempts: 3,
    retryDelayMs: 1000,
    timeoutMs: 120000
  },
  
  governance: {
    requireApprovalOver: 1.00, // USD
    maxCostPerTask: 10.00, // USD
    dailyCostLimit: 100.00 // USD
  }
};
```

---

## Success Metrics

**MVP Success Criteria:**
- ✅ Extract tasks from conversation with 80%+ accuracy
- ✅ Generate executable briefs in < 2 seconds
- ✅ Dispatch to OpenRouter with 99%+ success rate
- ✅ Complete simple tasks in < 30 seconds end-to-end
- ✅ Stay under $0.50 average cost per task

**Quality Metrics:**
- Task extraction precision/recall
- Brief clarity score (LLM-as-judge)
- Execution success rate
- User approval rate
- Cost per successful task

---

## Next Steps

Would you like me to:

1. **Create the Prisma schema** with full database models?
2. **Write the API endpoint implementations** (Next.js API routes)?
3. **Build the OpenRouter client** with streaming support?
4. **Design the UI components** for the task dashboard?
5. **Create example prompts** for each component?

Let me know which piece to tackle next! 🚀<br>

<i>[10/12/2025, 11:23:41 AM]</i> 👉 <b>👤 User</b>: Create the Prisma schema with full database models?<br>
<i>[10/12/2025, 11:25:13 AM]</i> 👉 <b>🤖 Assistant</b>: 

The user wants me to create a comprehensive Prisma schema for the Chief of Staff AI system. I need to translate all the database schemas I outlined in the blueprint into a proper Prisma schema with:

1. All the models from the components:
   - Conversation contexts
   - Extracted tasks
   - Worker briefs
   - Worker executions

2. Proper relationships between models
3. Indexes for performance
4. Enums for type safety
5. Additional supporting models for:
   - Users/accounts
   - Memory/context
   - Analytics
   - Governance/approval workflows

Let me create a comprehensive, production-ready Prisma schema that covers the entire Chief of Staff AI MVP scope.# Prisma Schema: Chief of Staff AI (MVP)

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
  previewFeatures = ["postgresqlExtensions"]
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  extensions = [pgvector(map: "vector")]
}

// ============================================================================
// USER & ORGANIZATION MODELS
// ============================================================================

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  avatarUrl String?
  
  // Auth
  clerkId   String?  @unique
  
  // Organization
  organizationId String?
  organization   Organization? @relation(fields: [organizationId], references: [id])
  
  // Relations
  conversations      Conversation[]
  approvedTasks      ExtractedTask[]  @relation("TaskApprover")
  executionFeedback  ExecutionFeedback[]
  
  // Metadata
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@index([organizationId])
  @@map("users")
}

model Organization {
  id          String   @id @default(cuid())
  name        String
  slug        String   @unique
  
  // Configuration
  settings    Json     @default("{}")
  
  // Relations
  users       User[]
  
  // Governance
  dailyCostLimit    Decimal @default(100.00) @db.Decimal(10, 2)
  taskApprovalLimit Decimal @default(1.00) @db.Decimal(10, 2)
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@map("organizations")
}

// ============================================================================
// CONVERSATION MODELS
// ============================================================================

model Conversation {
  id          String   @id @default(cuid())
  userId      String
  user        User     @relation(fields: [userId], references: [id], onDelete: Cascade)
  
  // Conversation metadata
  title       String?
  summary     String?
  
  // Relations
  messages    Message[]
  contexts    ConversationContext[]
  tasks       ExtractedTask[]
  
  // Status
  isActive    Boolean  @default(true)
  archivedAt  DateTime?
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@index([userId])
  @@index([createdAt])
  @@map("conversations")
}

model Message {
  id             String       @id @default(cuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  // Message content
  role           MessageRole
  content        String       @db.Text
  
  // Metadata
  tokenCount     Int?
  modelUsed      String?
  
  // Relations
  delegationSignals DelegationSignal[]
  
  createdAt      DateTime     @default(now())
  
  @@index([conversationId])
  @@index([createdAt])
  @@map("messages")
}

enum MessageRole {
  USER
  ASSISTANT
  SYSTEM
  
  @@map("message_role")
}

model ConversationContext {
  id             String       @id @default(cuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  // Context window
  messageHistory Json         // Array of recent messages
  
  // Detected signals
  delegationSignals DelegationSignal[]
  
  // Vector embedding for semantic search
  embedding      Unsupported("vector(1536)")?
  
  createdAt      DateTime     @default(now())
  updatedAt      DateTime     @updatedAt
  
  @@index([conversationId])
  @@map("conversation_contexts")
}

// ============================================================================
// DELEGATION SIGNAL MODELS
// ============================================================================

model DelegationSignal {
  id         String   @id @default(cuid())
  
  // Relations
  messageId  String
  message    Message  @relation(fields: [messageId], references: [id], onDelete: Cascade)
  
  contextId  String?
  context    ConversationContext? @relation(fields: [contextId], references: [id])
  
  // Signal details
  type            SignalType
  confidence      Decimal    @db.Decimal(3, 2) // 0.00 - 1.00
  triggerPhrase   String
  contextSnippet  String     @db.Text
  suggestedAction String?
  
  // Processing
  processed       Boolean    @default(false)
  processedAt     DateTime?
  
  // Relations
  extractedTask   ExtractedTask?
  
  createdAt       DateTime   @default(now())
  
  @@index([messageId])
  @@index([processed])
  @@index([confidence])
  @@map("delegation_signals")
}

enum SignalType {
  EXPLICIT    // "delegate this to"
  IMPLICIT    // "I need X by Y"
  QUESTION    // "What if we..."
  REQUEST     // "Can we get..."
  
  @@map("signal_type")
}

// ============================================================================
// TASK MODELS
// ============================================================================

model ExtractedTask {
  id             String       @id @default(cuid())
  conversationId String
  conversation   Conversation @relation(fields: [conversationId], references: [id], onDelete: Cascade)
  
  // Source
  signalId       String       @unique
  signal         DelegationSignal @relation(fields: [signalId], references: [id])
  
  // Core task definition
  objective      String       @db.Text
  scope          Json         // Array of scope items
  constraints    Json         // Array of constraints
  deliverables   Json         // Array of deliverable specs
  
  // Classification
  taskType       TaskType
  complexity     ComplexityRating
  
  // Estimates
  estimatedTokens   Int?
  estimatedDuration Int?      // minutes
  estimatedCost     Decimal?  @db.Decimal(10, 4)
  
  // Context
  relevantContext   String?   @db.Text
  
  // Governance
  approvalRequired  Boolean   @default(false)
  costCeiling       Decimal?  @db.Decimal(10, 2)
  
  approvedBy        String?
  approver          User?     @relation("TaskApprover", fields: [approvedBy], references: [id])
  approvedAt        DateTime?
  
  rejectionReason   String?   @db.Text
  
  // Lifecycle
  status            TaskStatus @default(EXTRACTED)
  
  // Relations
  briefs            WorkerBrief[]
  
  createdAt         DateTime   @default(now())
  updatedAt         DateTime   @updatedAt
  
  @@index([conversationId])
  @@index([status])
  @@index([taskType])
  @@index([complexity])
  @@index([createdAt])
  @@map("extracted_tasks")
}

enum TaskType {
  RESEARCH        // Gather information
  ANALYSIS        // Analyze data/patterns
  GENERATION      // Create new content
  TRANSFORMATION  // Convert/modify content
  SYNTHESIS       // Combine multiple sources
  MONITORING      // Track ongoing events
  
  @@map("task_type")
}

enum ComplexityRating {
  SIMPLE    // < 5 min, single-step
  MODERATE  // 5-20 min, multi-step
  COMPLEX   // 20-60 min, requires planning
  EPIC      // > 60 min, needs decomposition
  
  @@map("complexity_rating")
}

enum TaskStatus {
  EXTRACTED         // Task identified
  PENDING_APPROVAL  // Awaiting human approval
  APPROVED          // Approved for execution
  REJECTED          // Rejected by human
  BRIEF_GENERATED   // Brief created
  EXECUTING         // Worker running
  COMPLETED         // Successfully finished
  FAILED            // Execution failed
  CANCELLED         // Cancelled by user
  
  @@map("task_status")
}

// ============================================================================
// BRIEF MODELS
// ============================================================================

model WorkerBrief {
  id         String        @id @default(cuid())
  taskId     String
  task       ExtractedTask @relation(fields: [taskId], references: [id], onDelete: Cascade)
  
  // Prompts
  systemPrompt String       @db.Text
  userPrompt   String       @db.Text
  
  // Context enrichment
  contextDocuments Json?     // Array of document references
  relevantMemory   Json?     // Array of memory entries
  examples         Json?     // Array of example inputs/outputs
  
  // Specifications
  outputFormat      Json      // OutputFormat spec
  successCriteria   Json      // Array of criteria strings
  qualityThresholds Json?     // Array of QualityThreshold specs
  
  // Execution config
  modelConfig   Json         // ModelConfig spec
  maxTokens     Int
  temperature   Decimal      @db.Decimal(3, 2)
  stopSequences String[]
  
  // Governance
  costLimit     Decimal?     @db.Decimal(10, 4)
  timeLimit     Int?         // seconds
  retryPolicy   Json?        // RetryPolicy spec
  
  // Lifecycle
  status        BriefStatus  @default(GENERATED)
  
  // Relations
  executions    WorkerExecution[]
  
  createdAt     DateTime     @default(now())
  updatedAt     DateTime     @updatedAt
  
  @@index([taskId])
  @@index([status])
  @@map("worker_briefs")
}

enum BriefStatus {
  GENERATED   // Brief created
  VALIDATED   // Passed validation
  DISPATCHED  // Sent to worker
  EXECUTING   // Worker running
  COMPLETED   // Execution finished
  FAILED      // Execution failed
  
  @@map("brief_status")
}

// ============================================================================
// EXECUTION MODELS
// ============================================================================

model WorkerExecution {
  id              String      @id @default(cuid())
  briefId         String
  brief           WorkerBrief @relation(fields: [briefId], references: [id], onDelete: Cascade)
  
  // Request
  modelUsed       String
  requestPayload  Json
  requestTimestamp DateTime   @default(now())
  
  // Response
  responseContent  String?    @db.Text
  responseMetadata Json?
  responseTimestamp DateTime?
  
  // Metrics
  promptTokens     Int?
  completionTokens Int?
  totalTokens      Int?
  latencyMs        Int?
  costUsd          Decimal?   @db.Decimal(10, 6)
  
  // Status
  status           ExecutionStatus @default(PENDING)
  error            Json?
  retryCount       Int        @default(0)
  
  // Quality assessment
  qualityScore          Decimal?   @db.Decimal(3, 2)
  meetsSuccessCriteria  Boolean?
  validationResults     Json?
  
  // Relations
  feedback         ExecutionFeedback[]
  
  createdAt        DateTime   @default(now())
  completedAt      DateTime?
  
  @@index([briefId])
  @@index([status])
  @@index([requestTimestamp])
  @@index([costUsd])
  @@map("worker_executions")
}

enum ExecutionStatus {
  PENDING     // Queued
  RUNNING     // In progress
  COMPLETED   // Finished successfully
  FAILED      // Failed
  RETRYING    // Retrying after failure
  CANCELLED   // Cancelled
  TIMEOUT     // Exceeded time limit
  
  @@map("execution_status")
}

model ExecutionFeedback {
  id          String          @id @default(cuid())
  executionId String
  execution   WorkerExecution @relation(fields: [executionId], references: [id], onDelete: Cascade)
  
  userId      String
  user        User            @relation(fields: [userId], references: [id])
  
  // Feedback
  rating      Int             // 1-5
  helpful     Boolean
  comments    String?         @db.Text
  
  // Issues reported
  issues      Json?           // Array of issue types
  
  createdAt   DateTime        @default(now())
  
  @@index([executionId])
  @@index([userId])
  @@map("execution_feedback")
}

// ============================================================================
// MEMORY & CONTEXT MODELS
// ============================================================================

model MemoryEntry {
  id        String   @id @default(cuid())
  userId    String
  
  // Content
  content   String   @db.Text
  summary   String?  @db.Text
  
  // Classification
  type      MemoryType
  tags      String[]
  
  // Vector embedding for semantic search
  embedding Unsupported("vector(1536)")?
  
  // Metadata
  sourceType      String?  // 'conversation', 'task', 'execution'
  sourceId        String?
  importance      Decimal  @default(0.5) @db.Decimal(3, 2)
  
  // Lifecycle
  accessCount     Int      @default(0)
  lastAccessedAt  DateTime?
  
  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt
  
  @@index([userId])
  @@index([type])
  @@index([tags])
  @@index([importance])
  @@map("memory_entries")
}

enum MemoryType {
  FACT           // Factual information
  PREFERENCE     // User preference
  DECISION       // Past decision
  PATTERN        // Observed pattern
  CONTEXT        // Background context
  
  @@map("memory_type")
}

model ContextDocument {
  id          String   @id @default(cuid())
  userId      String
  
  // Document details
  title       String
  content     String   @db.Text
  contentType String   // 'text', 'code', 'markdown', etc.
  
  // Source
  sourceUrl   String?
  sourceType  String?  // 'upload', 'url', 'gdrive', etc.
  
  // Vector embedding for semantic search
  embedding   Unsupported("vector(1536)")?
  
  // Metadata
  metadata    Json?
  fileSize    Int?
  
  // Usage tracking
  usageCount  Int      @default(0)
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@index([userId])
  @@index([contentType])
  @@map("context_documents")
}

// ============================================================================
// ANALYTICS & MONITORING MODELS
// ============================================================================

model CostTracking {
  id        String   @id @default(cuid())
  userId    String
  
  // Cost details
  operation String   // 'task_extraction', 'brief_generation', 'worker_execution'
  model     String
  tokens    Int
  costUsd   Decimal  @db.Decimal(10, 6)
  
  // Relations
  taskId      String?
  briefId     String?
  executionId String?
  
  timestamp   DateTime @default(now())
  
  @@index([userId])
  @@index([timestamp])
  @@index([operation])
  @@map("cost_tracking")
}

model PerformanceMetric {
  id        String   @id @default(cuid())
  
  // Metric details
  component String   // 'conversation_listener', 'task_extractor', etc.
  metric    String   // 'latency', 'accuracy', 'throughput'
  value     Decimal  @db.Decimal(10, 4)
  unit      String   // 'ms', 'count', 'percent'
  
  // Metadata
  metadata  Json?
  
  timestamp DateTime @default(now())
  
  @@index([component])
  @@index([metric])
  @@index([timestamp])
  @@map("performance_metrics")
}

model SystemEvent {
  id        String   @id @default(cuid())
  
  // Event details
  eventType String   // 'task_extracted', 'execution_completed', 'error_occurred'
  severity  EventSeverity
  message   String   @db.Text
  
  // Context
  userId    String?
  taskId    String?
  executionId String?
  
  // Data
  data      Json?
  stackTrace String? @db.Text
  
  timestamp DateTime @default(now())
  
  @@index([eventType])
  @@index([severity])
  @@index([timestamp])
  @@map("system_events")
}

enum EventSeverity {
  DEBUG
  INFO
  WARNING
  ERROR
  CRITICAL
  
  @@map("event_severity")
}

// ============================================================================
// GOVERNANCE & POLICY MODELS
// ============================================================================

model PolicyRule {
  id          String   @id @default(cuid())
  orgId       String?
  
  // Rule definition
  name        String
  description String?  @db.Text
  ruleType    PolicyRuleType
  
  // Rule logic (stored as JSON for flexibility)
  conditions  Json     // Condition expressions
  actions     Json     // Actions to take
  
  // Status
  isActive    Boolean  @default(true)
  priority    Int      @default(0)
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@index([orgId])
  @@index([ruleType])
  @@index([isActive])
  @@map("policy_rules")
}

enum PolicyRuleType {
  COST_LIMIT        // Enforce cost limits
  APPROVAL_REQUIRED // Require approval for certain tasks
  BLOCKED_OPERATION // Block certain operations
  DATA_GOVERNANCE   // Data handling rules
  QUALITY_THRESHOLD // Quality requirements
  
  @@map("policy_rule_type")
}

model ApprovalWorkflow {
  id          String   @id @default(cuid())
  taskId      String
  
  // Approval details
  requestedBy String
  approvers   String[] // Array of user IDs
  
  // Status
  status      ApprovalStatus @default(PENDING)
  approvedBy  String?
  approvedAt  DateTime?
  
  rejectedBy  String?
  rejectedAt  DateTime?
  rejectionReason String? @db.Text
  
  // Metadata
  metadata    Json?
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@index([taskId])
  @@index([status])
  @@map("approval_workflows")
}

enum ApprovalStatus {
  PENDING
  APPROVED
  REJECTED
  EXPIRED
  
  @@map("approval_status")
}

// ============================================================================
// QUEUE & JOB MODELS (for async processing)
// ============================================================================

model JobQueue {
  id          String   @id @default(cuid())
  
  // Job details
  jobType     String   // 'extract_task', 'generate_brief', 'execute_worker'
  payload     Json
  
  // Status
  status      JobStatus @default(PENDING)
  attempts    Int       @default(0)
  maxAttempts Int       @default(3)
  
  // Timing
  scheduledFor DateTime @default(now())
  startedAt    DateTime?
  completedAt  DateTime?
  
  // Results
  result      Json?
  error       Json?
  
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
  
  @@index([status])
  @@index([jobType])
  @@index([scheduledFor])
  @@map("job_queue")
}

enum JobStatus {
  PENDING
  PROCESSING
  COMPLETED
  FAILED
  RETRYING
  CANCELLED
  
  @@map("job_status")
}
```

---

## Supporting Files

### 1. **Prisma Migrations Setup**

```bash
# Initialize Prisma
npx prisma init

# Create initial migration
npx prisma migrate dev --name init

# Generate Prisma Client
npx prisma generate
```

### 2. **Vector Extension Setup**

```sql
-- migrations/001_enable_vector_extension.sql
CREATE EXTENSION IF NOT EXISTS vector;

-- Create vector indexes for semantic search
CREATE INDEX conversation_contexts_embedding_idx 
ON conversation_contexts 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX memory_entries_embedding_idx 
ON memory_entries 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX context_documents_embedding_idx 
ON context_documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### 3. **Seed Data**

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  // Create demo organization
  const org = await prisma.organization.upsert({
    where: { slug: 'demo-org' },
    update: {},
    create: {
      name: 'Demo Organization',
      slug: 'demo-org',
      dailyCostLimit: 100.00,
      taskApprovalLimit: 1.00,
    },
  });

  // Create demo user
  const user = await prisma.user.upsert({
    where: { email: 'demo@example.com' },
    update: {},
    create: {
      email: 'demo@example.com',
      name: 'Demo User',
      organizationId: org.id,
    },
  });

  // Create default policy rules
  await prisma.policyRule.createMany({
    data: [
      {
        name: 'Auto-approve simple tasks',
        description: 'Automatically approve tasks with complexity SIMPLE',
        ruleType: 'APPROVAL_REQUIRED',
        conditions: { complexity: 'SIMPLE' },
        actions: { autoApprove: true },
        isActive: true,
        priority: 1,
      },
      {
        name: 'Cost limit per task',
        description: 'Block tasks exceeding $5',
        ruleType: 'COST_LIMIT',
        conditions: { estimatedCost: { gte: 5.00 } },
        actions: { block: true, notify: true },
        isActive: true,
        priority: 2,
      },
    ],
  });

  console.log('✅ Seed data created');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

```json
// package.json addition
{
  "prisma": {
    "seed": "tsx prisma/seed.ts"
  }
}
```

### 4. **Environment Variables**

```bash
# .env
DATABASE_URL="postgresql://user:password@localhost:5432/chief_of_staff_ai?schema=public"
DIRECT_URL="postgresql://user:password@localhost:5432/chief_of_staff_ai?schema=public"

# For connection pooling (optional)
DATABASE_URL_POOLED="postgresql://user:password@pooler.host:5432/chief_of_staff_ai"
```

### 5. **Prisma Client Singleton**

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' 
      ? ['query', 'error', 'warn'] 
      : ['error'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

---

## Key Features of This Schema

### **1. Complete Relational Integrity**
- All foreign keys properly defined
- Cascade deletes where appropriate
- Indexes on all frequently queried fields

### **2. Vector Search Ready**
- `pgvector` extension support for semantic search
- Embedding columns on key models
- IVFFlat indexes for fast similarity search

### **3. Comprehensive Enums**
- Type safety for all categorical fields
- Clear state machines for workflows
- Prevents invalid data states

### **4. Audit Trail**
- Timestamps on all models
- Tracking of approvals, rejections
- Full execution history

### **5. Cost Tracking**
- Detailed token usage
- Per-operation cost attribution
- Budget enforcement capability

### **6. Governance Ready**
- Policy rules system
- Approval workflows
- Event logging

### **7. Analytics Support**
- Performance metrics table
- System events logging
- Usage tracking

---

## Next Steps

Would you like me to:

1. **Create the Prisma Client wrapper functions** (CRUD operations for each model)?
2. **Build the migration scripts** with proper rollback support?
3. **Create TypeScript types & Zod schemas** for validation?
4. **Write the database service layer** with business logic?
5. **Design the API endpoints** that use these models?

Let me know which direction to go! 🚀<br>

<i>[10/12/2025, 11:26:57 AM]</i> 👉 <b>👤 User</b>: Create the Prisma Client wrapper functions (CRUD operations for each model)?<br>
<i>[10/12/2025, 11:29:37 AM]</i> 👉 <b>🤖 Assistant</b>: 

The user wants me to create Prisma Client wrapper functions with CRUD operations for each model. This is a substantial task that requires creating a well-organized service layer with:

1. Type-safe CRUD operations
2. Business logic encapsulation
3. Error handling
4. Query optimization
5. Validation
6. Helper methods for common operations

I should organize this by domain/model group and create comprehensive, production-ready service classes. I'll include:
- Basic CRUD (create, read, update, delete)
- Query methods with filters
- Relationship handling
- Transaction support
- Error handling
- Type safety

Let me structure this as separate service files, organized by domain:
- User & Organization services
- Conversation services
- Task services
- Brief services
- Execution services
- Memory services
- Analytics services
- Governance services

I'll also create helper utilities and base classes to reduce repetition.# Prisma Client Wrapper Functions (Service Layer)

## Directory Structure

```
lib/
├── db/
│   ├── prisma.ts                    # Prisma client singleton
│   ├── base-service.ts              # Base service class
│   ├── errors.ts                    # Custom error classes
│   ├── types.ts                     # Shared types
│   └── services/
│       ├── user.service.ts          # User operations
│       ├── organization.service.ts  # Organization operations
│       ├── conversation.service.ts  # Conversation operations
│       ├── delegation.service.ts    # Delegation signal operations
│       ├── task.service.ts          # Task operations
│       ├── brief.service.ts         # Brief operations
│       ├── execution.service.ts     # Execution operations
│       ├── memory.service.ts        # Memory operations
│       ├── analytics.service.ts     # Analytics operations
│       ├── governance.service.ts    # Governance operations
│       └── index.ts                 # Export all services
```

---

## Base Files

### 1. **Custom Error Classes**

```typescript
// lib/db/errors.ts

export class DatabaseError extends Error {
  constructor(
    message: string,
    public code?: string,
    public meta?: any
  ) {
    super(message);
    this.name = 'DatabaseError';
  }
}

export class NotFoundError extends DatabaseError {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, 'NOT_FOUND');
    this.name = 'NotFoundError';
  }
}

export class ValidationError extends DatabaseError {
  constructor(message: string, public fields?: Record<string, string>) {
    super(message, 'VALIDATION_ERROR', fields);
    this.name = 'ValidationError';
  }
}

export class UnauthorizedError extends DatabaseError {
  constructor(message: string = 'Unauthorized access') {
    super(message, 'UNAUTHORIZED');
    this.name = 'UnauthorizedError';
  }
}

export class ConflictError extends DatabaseError {
  constructor(message: string) {
    super(message, 'CONFLICT');
    this.name = 'ConflictError';
  }
}

export class QuotaExceededError extends DatabaseError {
  constructor(message: string, public limit: number, public current: number) {
    super(message, 'QUOTA_EXCEEDED', { limit, current });
    this.name = 'QuotaExceededError';
  }
}
```

### 2. **Shared Types**

```typescript
// lib/db/types.ts

export interface PaginationParams {
  page?: number;
  limit?: number;
  cursor?: string;
}

export interface PaginatedResult<T> {
  data: T[];
  pagination: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

export interface CursorPaginatedResult<T> {
  data: T[];
  cursor: {
    next?: string;
    prev?: string;
    hasNext: boolean;
    hasPrev: boolean;
  };
}

export interface DateRangeFilter {
  from?: Date;
  to?: Date;
}

export interface SortOptions {
  field: string;
  direction: 'asc' | 'desc';
}

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

### 3. **Base Service Class**

```typescript
// lib/db/base-service.ts

import { PrismaClient, Prisma } from '@prisma/client';
import { prisma } from './prisma';
import { NotFoundError, DatabaseError } from './errors';
import type { PaginatedResult, PaginationParams } from './types';

export abstract class BaseService<
  T extends { id: string },
  CreateInput = any,
  UpdateInput = any
> {
  protected prisma: PrismaClient;
  protected abstract modelName: Prisma.ModelName;

  constructor(prismaClient?: PrismaClient) {
    this.prisma = prismaClient || prisma;
  }

  /**
   * Find a record by ID
   */
  protected async findById(
    id: string,
    include?: any
  ): Promise<T> {
    try {
      const record = await (this.prisma[this.modelName] as any).findUnique({
        where: { id },
        include,
      });

      if (!record) {
        throw new NotFoundError(this.modelName, id);
      }

      return record;
    } catch (error) {
      this.handleError(error);
    }
  }

  /**
   * Find many records with filters
   */
  protected async findMany(
    where?: any,
    options?: {
      include?: any;
      orderBy?: any;
      take?: number;
      skip?: number;
    }
  ): Promise<T[]> {
    try {
      return await (this.prisma[this.modelName] as any).findMany({
        where,
        ...options,
      });
    } catch (error) {
      this.handleError(error);
    }
  }

  /**
   * Count records with filters
   */
  protected async count(where?: any): Promise<number> {
    try {
      return await (this.prisma[this.modelName] as any).count({ where });
    } catch (error) {
      this.handleError(error);
    }
  }

  /**
   * Create a new record
   */
  protected async create(
    data: CreateInput,
    include?: any
  ): Promise<T> {
    try {
      return await (this.prisma[this.modelName] as any).create({
        data,
        include,
      });
    } catch (error) {
      this.handleError(error);
    }
  }

  /**
   * Update a record by ID
   */
  protected async update(
    id: string,
    data: UpdateInput,
    include?: any
  ): Promise<T> {
    try {
      return await (this.prisma[this.modelName] as any).update({
        where: { id },
        data,
        include,
      });
    } catch (error) {
      this.handleError(error);
    }
  }

  /**
   * Delete a record by ID
   */
  protected async delete(id: string): Promise<T> {
    try {
      return await (this.prisma[this.modelName] as any).delete({
        where: { id },
      });
    } catch (error) {
      this.handleError(error);
    }
  }

  /**
   * Paginate results
   */
  protected async paginate(
    where: any,
    pagination: PaginationParams,
    options?: {
      include?: any;
      orderBy?: any;
    }
  ): Promise<PaginatedResult<T>> {
    const page = pagination.page || 1;
    const limit = Math.min(pagination.limit || 20, 100);
    const skip = (page - 1) * limit;

    const [data, total] = await Promise.all([
      this.findMany(where, {
        ...options,
        take: limit,
        skip,
      }),
      this.count(where),
    ]);

    const totalPages = Math.ceil(total / limit);

    return {
      data,
      pagination: {
        total,
        page,
        limit,
        totalPages,
        hasNext: page < totalPages,
        hasPrev: page > 1,
      },
    };
  }

  /**
   * Error handler
   */
  protected handleError(error: any): never {
    if (error instanceof DatabaseError) {
      throw error;
    }

    if (error.code === 'P2002') {
      throw new DatabaseError(
        'Unique constraint violation',
        'UNIQUE_VIOLATION',
        error.meta
      );
    }

    if (error.code === 'P2025') {
      throw new NotFoundError(this.modelName, 'unknown');
    }

    throw new DatabaseError(
      error.message || 'Database operation failed',
      error.code,
      error.meta
    );
  }
}
```

---

## Service Implementations

### 1. **User Service**

```typescript
// lib/db/services/user.service.ts

import { Prisma, User } from '@prisma/client';
import { BaseService } from '../base-service';
import { ConflictError } from '../errors';

export interface CreateUserInput {
  email: string;
  name?: string;
  avatarUrl?: string;
  clerkId?: string;
  organizationId?: string;
}

export interface UpdateUserInput {
  name?: string;
  avatarUrl?: string;
  organizationId?: string;
}

export class UserService extends BaseService<
  User,
  CreateUserInput,
  UpdateUserInput
> {
  protected modelName = Prisma.ModelName.User;

  /**
   * Create a new user
   */
  async createUser(data: CreateUserInput): Promise<User> {
    // Check if user already exists
    const existing = await this.prisma.user.findUnique({
      where: { email: data.email },
    });

    if (existing) {
      throw new ConflictError(`User with email ${data.email} already exists`);
    }

    return this.create(data, {
      organization: true,
    });
  }

  /**
   * Get user by ID
   */
  async getUser(id: string): Promise<User> {
    return this.findById(id, {
      organization: true,
    });
  }

  /**
   * Get user by email
   */
  async getUserByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
      include: {
        organization: true,
      },
    });
  }

  /**
   * Get user by Clerk ID
   */
  async getUserByClerkId(clerkId: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { clerkId },
      include: {
        organization: true,
      },
    });
  }

  /**
   * Update user
   */
  async updateUser(id: string, data: UpdateUserInput): Promise<User> {
    return this.update(id, data, {
      organization: true,
    });
  }

  /**
   * Delete user
   */
  async deleteUser(id: string): Promise<User> {
    return this.delete(id);
  }

  /**
   * Get users by organization
   */
  async getUsersByOrganization(organizationId: string): Promise<User[]> {
    return this.findMany(
      { organizationId },
      {
        orderBy: { createdAt: 'desc' },
      }
    );
  }

  /**
   * Get user statistics
   */
  async getUserStats(userId: string) {
    const [
      conversationCount,
      taskCount,
      executionCount,
      totalCost,
    ] = await Promise.all([
      this.prisma.conversation.count({ where: { userId } }),
      this.prisma.extractedTask.count({
        where: { conversation: { userId } },
      }),
      this.prisma.workerExecution.count({
        where: { brief: { task: { conversation: { userId } } } },
      }),
      this.prisma.costTracking.aggregate({
        where: { userId },
        _sum: { costUsd: true },
      }),
    ]);

    return {
      conversations: conversationCount,
      tasks: taskCount,
      executions: executionCount,
      totalCost: totalCost._sum.costUsd || 0,
    };
  }
}
```

### 2. **Organization Service**

```typescript
// lib/db/services/organization.service.ts

import { Prisma, Organization } from '@prisma/client';
import { BaseService } from '../base-service';
import { ConflictError } from '../errors';

export interface CreateOrganizationInput {
  name: string;
  slug: string;
  settings?: any;
  dailyCostLimit?: number;
  taskApprovalLimit?: number;
}

export interface UpdateOrganizationInput {
  name?: string;
  settings?: any;
  dailyCostLimit?: number;
  taskApprovalLimit?: number;
}

export class OrganizationService extends BaseService<
  Organization,
  CreateOrganizationInput,
  UpdateOrganizationInput
> {
  protected modelName = Prisma.ModelName.Organization;

  /**
   * Create a new organization
   */
  async createOrganization(
    data: CreateOrganizationInput
  ): Promise<Organization> {
    const existing = await this.prisma.organization.findUnique({
      where: { slug: data.slug },
    });

    if (existing) {
      throw new ConflictError(
        `Organization with slug ${data.slug} already exists`
      );
    }

    return this.create(data);
  }

  /**
   * Get organization by ID
   */
  async getOrganization(id: string): Promise<Organization> {
    return this.findById(id, {
      users: {
        orderBy: { createdAt: 'desc' },
        take: 10,
      },
    });
  }

  /**
   * Get organization by slug
   */
  async getOrganizationBySlug(slug: string): Promise<Organization | null> {
    return this.prisma.organization.findUnique({
      where: { slug },
      include: {
        users: {
          orderBy: { createdAt: 'desc' },
        },
      },
    });
  }

  /**
   * Update organization
   */
  async updateOrganization(
    id: string,
    data: UpdateOrganizationInput
  ): Promise<Organization> {
    return this.update(id, data);
  }

  /**
   * Delete organization
   */
  async deleteOrganization(id: string): Promise<Organization> {
    return this.delete(id);
  }

  /**
   * Get organization usage stats
   */
  async getOrganizationUsage(orgId: string, dateRange?: { from: Date; to: Date }) {
    const where = {
      organization: { id: orgId },
      ...(dateRange && {
        createdAt: {
          gte: dateRange.from,
          lte: dateRange.to,
        },
      }),
    };

    const [userCount, totalCost, taskCount] = await Promise.all([
      this.prisma.user.count({ where: { organizationId: orgId } }),
      this.prisma.costTracking.aggregate({
        where: {
          user: { organizationId: orgId },
          ...(dateRange && {
            timestamp: {
              gte: dateRange.from,
              lte: dateRange.to,
            },
          }),
        },
        _sum: { costUsd: true },
      }),
      this.prisma.extractedTask.count({
        where: {
          conversation: { user: { organizationId: orgId } },
          ...(dateRange && {
            createdAt: {
              gte: dateRange.from,
              lte: dateRange.to,
            },
          }),
        },
      }),
    ]);

    return {
      users: userCount,
      totalCost: totalCost._sum.costUsd || 0,
      tasks: taskCount,
    };
  }

  /**
   * Check if organization is within cost limits
   */
  async checkCostLimit(orgId: string, additionalCost: number): Promise<boolean> {
    const org = await this.getOrganization(orgId);
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const todayCost = await this.prisma.costTracking.aggregate({
      where: {
        user: { organizationId: orgId },
        timestamp: { gte: today },
      },
      _sum: { costUsd: true },
    });

    const currentCost = Number(todayCost._sum.costUsd || 0);
    const limit = Number(org.dailyCostLimit);

    return currentCost + additionalCost <= limit;
  }
}
```

### 3. **Conversation Service**

```typescript
// lib/db/services/conversation.service.ts

import { Prisma, Conversation, Message, MessageRole } from '@prisma/client';
import { BaseService } from '../base-service';
import { PaginationParams } from '../types';

export interface CreateConversationInput {
  userId: string;
  title?: string;
}

export interface UpdateConversationInput {
  title?: string;
  summary?: string;
  isActive?: boolean;
}

export interface CreateMessageInput {
  conversationId: string;
  role: MessageRole;
  content: string;
  tokenCount?: number;
  modelUsed?: string;
}

export class ConversationService extends BaseService<
  Conversation,
  CreateConversationInput,
  UpdateConversationInput
> {
  protected modelName = Prisma.ModelName.Conversation;

  /**
   * Create a new conversation
   */
  async createConversation(
    data: CreateConversationInput
  ): Promise<Conversation> {
    return this.create(data);
  }

  /**
   * Get conversation by ID
   */
  async getConversation(id: string): Promise<Conversation> {
    return this.findById(id, {
      user: true,
      messages: {
        orderBy: { createdAt: 'asc' },
        take: 100,
      },
      tasks: {
        orderBy: { createdAt: 'desc' },
        take: 10,
      },
    });
  }

  /**
   * Get conversations for a user
   */
  async getUserConversations(
    userId: string,
    pagination?: PaginationParams
  ) {
    return this.paginate(
      { userId, isActive: true },
      pagination || {},
      {
        include: {
          messages: {
            orderBy: { createdAt: 'desc' },
            take: 1,
          },
          _count: {
            select: { messages: true, tasks: true },
          },
        },
        orderBy: { updatedAt: 'desc' },
      }
    );
  }

  /**
   * Update conversation
   */
  async updateConversation(
    id: string,
    data: UpdateConversationInput
  ): Promise<Conversation> {
    return this.update(id, data);
  }

  /**
   * Archive conversation
   */
  async archiveConversation(id: string): Promise<Conversation> {
    return this.update(id, {
      isActive: false,
      archivedAt: new Date(),
    });
  }

  /**
   * Delete conversation
   */
  async deleteConversation(id: string): Promise<Conversation> {
    return this.delete(id);
  }

  /**
   * Add message to conversation
   */
  async addMessage(data: CreateMessageInput): Promise<Message> {
    const message = await this.prisma.message.create({
      data,
      include: {
        conversation: true,
      },
    });

    // Update conversation timestamp
    await this.prisma.conversation.update({
      where: { id: data.conversationId },
      data: { updatedAt: new Date() },
    });

    return message;
  }

  /**
   * Get conversation messages
   */
  async getMessages(
    conversationId: string,
    options?: {
      limit?: number;
      cursor?: string;
      order?: 'asc' | 'desc';
    }
  ): Promise<Message[]> {
    return this.prisma.message.findMany({
      where: { conversationId },
      orderBy: { createdAt: options?.order || 'asc' },
      take: options?.limit || 100,
      ...(options?.cursor && {
        cursor: { id: options.cursor },
        skip: 1,
      }),
    });
  }

  /**
   * Get recent context (last N messages)
   */
  async getRecentContext(
    conversationId: string,
    messageCount: number = 10
  ): Promise<Message[]> {
    return this.prisma.message.findMany({
      where: { conversationId },
      orderBy: { createdAt: 'desc' },
      take: messageCount,
    });
  }

  /**
   * Search conversations
   */
  async searchConversations(
    userId: string,
    query: string,
    pagination?: PaginationParams
  ) {
    return this.paginate(
      {
        userId,
        isActive: true,
        OR: [
          { title: { contains: query, mode: 'insensitive' } },
          { summary: { contains: query, mode: 'insensitive' } },
          {
            messages: {
              some: {
                content: { contains: query, mode: 'insensitive' },
              },
            },
          },
        ],
      },
      pagination || {},
      {
        include: {
          messages: {
            orderBy: { createdAt: 'desc' },
            take: 1,
          },
        },
        orderBy: { updatedAt: 'desc' },
      }
    );
  }
}
```

### 4. **Delegation Service**

```typescript
// lib/db/services/delegation.service.ts

import { Prisma, DelegationSignal, SignalType } from '@prisma/client';
import { BaseService } from '../base-service';

export interface CreateDelegationSignalInput {
  messageId: string;
  contextId?: string;
  type: SignalType;
  confidence: number;
  triggerPhrase: string;
  contextSnippet: string;
  suggestedAction?: string;
}

export interface UpdateDelegationSignalInput {
  processed?: boolean;
  processedAt?: Date;
}

export class DelegationService extends BaseService<
  DelegationSignal,
  CreateDelegationSignalInput,
  UpdateDelegationSignalInput
> {
  protected modelName = Prisma.ModelName.DelegationSignal;

  /**
   * Create a new delegation signal
   */
  async createSignal(
    data: CreateDelegationSignalInput
  ): Promise<DelegationSignal> {
    return this.create(data, {
      message: {
        include: {
          conversation: true,
        },
      },
    });
  }

  /**
   * Get signal by ID
   */
  async getSignal(id: string): Promise<DelegationSignal> {
    return this.findById(id, {
      message: {
        include: {
          conversation: true,
        },
      },
      extractedTask: true,
    });
  }

  /**
   * Get signals for a message
   */
  async getSignalsByMessage(messageId: string): Promise<DelegationSignal[]> {
    return this.findMany(
      { messageId },
      {
        orderBy: { confidence: 'desc' },
      }
    );
  }

  /**
   * Get unprocessed signals
   */
  async getUnprocessedSignals(
    options?: {
      minConfidence?: number;
      limit?: number;
    }
  ): Promise<DelegationSignal[]> {
    return this.findMany(
      {
        processed: false,
        confidence: { gte: options?.minConfidence || 0.7 },
      },
      {
        include: {
          message: {
            include: {
              conversation: true,
            },
          },
        },
        orderBy: { confidence: 'desc' },
        take: options?.limit || 10,
      }
    );
  }

  /**
   * Mark signal as processed
   */
  async markProcessed(id: string): Promise<DelegationSignal> {
    return this.update(id, {
      processed: true,
      processedAt: new Date(),
    });
  }

  /**
   * Get signal statistics
   */
  async getSignalStats(conversationId?: string) {
    const where = conversationId
      ? { message: { conversationId } }
      : {};

    const [total, processed, byType] = await Promise.all([
      this.count(where),
      this.count({ ...where, processed: true }),
      this.prisma.delegationSignal.groupBy({
        by: ['type'],
        where,
        _count: true,
        _avg: { confidence: true },
      }),
    ]);

    return {
      total,
      processed,
      unprocessed: total - processed,
      byType: byType.map(t => ({
        type: t.type,
        count: t._count,
        avgConfidence: t._avg.confidence,
      })),
    };
  }
}
```

### 5. **Task Service**

```typescript
// lib/db/services/task.service.ts

import {
  Prisma,
  ExtractedTask,
  TaskType,
  ComplexityRating,
  TaskStatus,
} from '@prisma/client';
import { BaseService } from '../base-service';
import { PaginationParams } from '../types';
import { QuotaExceededError, ValidationError } from '../errors';

export interface CreateTaskInput {
  conversationId: string;
  signalId: string;
  objective: string;
  scope: any[];
  constraints: any[];
  deliverables: any[];
  taskType: TaskType;
  complexity: ComplexityRating;
  estimatedTokens?: number;
  estimatedDuration?: number;
  estimatedCost?: number;
  relevantContext?: string;
  approvalRequired?: boolean;
  costCeiling?: number;
}

export interface UpdateTaskInput {
  objective?: string;
  scope?: any[];
  constraints?: any[];
  deliverables?: any[];
  status?: TaskStatus;
  approvedBy?: string;
  approvedAt?: Date;
  rejectionReason?: string;
}

export interface TaskFilters {
  conversationId?: string;
  userId?: string;
  status?: TaskStatus | TaskStatus[];
  taskType?: TaskType;
  complexity?: ComplexityRating;
  dateRange?: {
    from: Date;
    to: Date;
  };
}

export class TaskService extends BaseService<
  ExtractedTask,
  CreateTaskInput,
  UpdateTaskInput
> {
  protected modelName = Prisma.ModelName.ExtractedTask;

  /**
   * Create a new task
   */
  async createTask(data: CreateTaskInput): Promise<ExtractedTask> {
    // Check if approval is required
    if (data.approvalRequired) {
      data['status'] = TaskStatus.PENDING_APPROVAL;
    }

    return this.create(data, {
      conversation: true,
      signal: true,
    });
  }

  /**
   * Get task by ID
   */
  async getTask(id: string): Promise<ExtractedTask> {
    return this.findById(id, {
      conversation: {
        include: {
          user: true,
        },
      },
      signal: true,
      approver: true,
      briefs: {
        include: {
          executions: {
            orderBy: { requestTimestamp: 'desc' },
            take: 1,
          },
        },
      },
    });
  }

  /**
   * Get tasks with filters
   */
  async getTasks(
    filters: TaskFilters,
    pagination?: PaginationParams
  ) {
    const where: any = {};

    if (filters.conversationId) {
      where.conversationId = filters.conversationId;
    }

    if (filters.userId) {
      where.conversation = { userId: filters.userId };
    }

    if (filters.status) {
      where.status = Array.isArray(filters.status)
        ? { in: filters.status }
        : filters.status;
    }

    if (filters.taskType) {
      where.taskType = filters.taskType;
    }

    if (filters.complexity) {
      where.complexity = filters.complexity;
    }

    if (filters.dateRange) {
      where.createdAt = {
        gte: filters.dateRange.from,
        lte: filters.dateRange.to,
      };
    }

    return this.paginate(
      where,
      pagination || {},
      {
        include: {
          conversation: {
            include: {
              user: true,
            },
          },
          briefs: {
            take: 1,
            orderBy: { createdAt: 'desc' },
          },
        },
        orderBy: { createdAt: 'desc' },
      }
    );
  }

  /**
   * Update task
   */
  async updateTask(id: string, data: UpdateTaskInput): Promise<ExtractedTask> {
    return this.update(id, data, {
      conversation: true,
      approver: true,
    });
  }

  /**
   * Approve task
   */
  async approveTask(id: string, approverId: string): Promise<ExtractedTask> {
    const task = await this.getTask(id);

    if (task.status !== TaskStatus.PENDING_APPROVAL) {
      throw new ValidationError('Task is not pending approval');
    }

    return this.update(id, {
      status: TaskStatus.APPROVED,
      approvedBy: approverId,
      approvedAt: new Date(),
    });
  }

  /**
   * Reject task
   */
  async rejectTask(
    id: string,
    approverId: string,
    reason: string
  ): Promise<ExtractedTask> {
    const task = await this.getTask(id);

    if (task.status !== TaskStatus.PENDING_APPROVAL) {
      throw new ValidationError('Task is not pending approval');
    }

    return this.update(id, {
      status: TaskStatus.REJECTED,
      approvedBy: approverId,
      rejectionReason: reason,
    });
  }

  /**
   * Cancel task
   */
  async cancelTask(id: string): Promise<ExtractedTask> {
    return this.update(id, {
      status: TaskStatus.CANCELLED,
    });
  }

  /**
   * Get pending approval tasks
   */
  async getPendingApprovalTasks(userId: string) {
    return this.findMany(
      {
        status: TaskStatus.PENDING_APPROVAL,
        conversation: { userId },
      },
      {
        include: {
          conversation: true,
          signal: true,
        },
        orderBy: { createdAt: 'desc' },
      }
    );
  }

  /**
   * Get task statistics
   */
  async getTaskStats(filters: TaskFilters) {
    const where: any = {};

    if (filters.conversationId) {
      where.conversationId = filters.conversationId;
    }

    if (filters.userId) {
      where.conversation = { userId: filters.userId };
    }

    if (filters.dateRange) {
      where.createdAt = {
        gte: filters.dateRange.from,
        lte: filters.dateRange.to,
      };
    }

    const [
      total,
      byStatus,
      byType,
      byComplexity,
      totalCost,
    ] = await Promise.all([
      this.count(where),
      this.prisma.extractedTask.groupBy({
        by: ['status'],
        where,
        _count: true,
      }),
      this.prisma.extractedTask.groupBy({
        by: ['taskType'],
        where,
        _count: true,
      }),
      this.prisma.extractedTask.groupBy({
        by: ['complexity'],
        where,
        _count: true,
      }),
      this.prisma.extractedTask.aggregate({
        where,
        _sum: { estimatedCost: true },
      }),
    ]);

    return {
      total,
      byStatus: byStatus.map(s => ({
        status: s.status,
        count: s._count,
      })),
      byType: byType.map(t => ({
        type: t.taskType,
        count: t._count,
      })),
      byComplexity: byComplexity.map(c => ({
        complexity: c.complexity,
        count: c._count,
      })),
      totalEstimatedCost: totalCost._sum.estimatedCost || 0,
    };
  }

  /**
   * Check if user can create task (quota check)
   */
  async checkTaskQuota(
    userId: string,
    estimatedCost: number
  ): Promise<boolean> {
    // Get user's organization
    const user = await this.prisma.user.findUnique({
      where: { id: userId },
      include: { organization: true },
    });

    if (!user?.organization) {
      return true; // No organization limits
    }

    // Check daily cost limit
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const todayCost = await this.prisma.costTracking.aggregate({
      where: {
        userId,
        timestamp: { gte: today },
      },
      _sum: { costUsd: true },
    });

    const currentCost = Number(todayCost._sum.costUsd || 0);
    const limit = Number(user.organization.dailyCostLimit);

    if (currentCost + estimatedCost > limit) {
      throw new QuotaExceededError(
        'Daily cost limit exceeded',
        limit,
        currentCost + estimatedCost
      );
    }

    return true;
  }
}
```

### 6. **Brief Service**

```typescript
// lib/db/services/brief.service.ts

import { Prisma, WorkerBrief, BriefStatus } from '@prisma/client';
import { BaseService } from '../base-service';

export interface CreateBriefInput {
  taskId: string;
  systemPrompt: string;
  userPrompt: string;
  contextDocuments?: any;
  relevantMemory?: any;
  examples?: any;
  outputFormat: any;
  successCriteria: any[];
  qualityThresholds?: any;
  modelConfig: any;
  maxTokens: number;
  temperature: number;
  stopSequences?: string[];
  costLimit?: number;
  timeLimit?: number;
  retryPolicy?: any;
}

export interface UpdateBriefInput {
  status?: BriefStatus;
  systemPrompt?: string;
  userPrompt?: string;
  outputFormat?: any;
  successCriteria?: any[];
}

export class BriefService extends BaseService<
  WorkerBrief,
  CreateBriefInput,
  UpdateBriefInput
> {
  protected modelName = Prisma.ModelName.WorkerBrief;

  /**
   * Create a new brief
   */
  async createBrief(data: CreateBriefInput): Promise<WorkerBrief> {
    return this.create(data, {
      task: {
        include: {
          conversation: {
            include: {
              user: true,
            },
          },
        },
      },
    });
  }

  /**
   * Get brief by ID
   */
  async getBrief(id: string): Promise<WorkerBrief> {
    return this.findById(id, {
      task: {
        include: {
          conversation: true,
        },
      },
      executions: {
        orderBy: { requestTimestamp: 'desc' },
      },
    });
  }

  /**
   * Get briefs for a task
   */
  async getBriefsByTask(taskId: string): Promise<WorkerBrief[]> {
    return this.findMany(
      { taskId },
      {
        include: {
          executions: {
            orderBy: { requestTimestamp: 'desc' },
            take: 1,
          },
        },
        orderBy: { createdAt: 'desc' },
      }
    );
  }

  /**
   * Update brief
   */
  async updateBrief(
    id: string,
    data: UpdateBriefInput
  ): Promise<WorkerBrief> {
    return this.update(id, data);
  }

  /**
   * Mark brief as dispatched
   */
  async markDispatched(id: string): Promise<WorkerBrief> {
    return this.update(id, {
      status: BriefStatus.DISPATCHED,
    });
  }

  /**
   * Mark brief as executing
   */
  async markExecuting(id: string): Promise<WorkerBrief> {
    return this.update(id, {
      status: BriefStatus.EXECUTING,
    });
  }

  /**
   * Mark brief as completed
   */
  async markCompleted(id: string): Promise<WorkerBrief> {
    return this.update(id, {
      status: BriefStatus.COMPLETED,
    });
  }

  /**
   * Mark brief as failed
   */
  async markFailed(id: string): Promise<WorkerBrief> {
    return this.update(id, {
      status: BriefStatus.FAILED,
    });
  }

  /**
   * Get brief statistics
   */
  async getBriefStats(taskId?: string) {
    const where = taskId ? { taskId } : {};

    const [total, byStatus] = await Promise.all([
      this.count(where),
      this.prisma.workerBrief.groupBy({
        by: ['status'],
        where,
        _count: true,
      }),
    ]);

    return {
      total,
      byStatus: byStatus.map(s => ({
        status: s.status,
        count: s._count,
      })),
    };
  }
}
```

### 7. **Execution Service**

```typescript
// lib/db/services/execution.service.ts

import { Prisma, WorkerExecution, ExecutionStatus } from '@prisma/client';
import { BaseService } from '../base-service';
import { PaginationParams } from '../types';

export interface CreateExecutionInput {
  briefId: string;
  modelUsed: string;
  requestPayload: any;
  maxTokens?: number;
  temperature?: number;
}

export interface UpdateExecutionInput {
  status?: ExecutionStatus;
  responseContent?: string;
  responseMetadata?: any;
  responseTimestamp?: Date;
  promptTokens?: number;
  completionTokens?: number;
  totalTokens?: number;
  latencyMs?: number;
  costUsd?: number;
  error?: any;
  retryCount?: number;
  qualityScore?: number;
  meetsSuccessCriteria?: boolean;
  validationResults?: any;
}

export interface ExecutionFilters {
  briefId?: string;
  taskId?: string;
  userId?: string;
  status?: ExecutionStatus | ExecutionStatus[];
  modelUsed?: string;
  dateRange?: {
    from: Date;
    to: Date;
  };
}

export class ExecutionService extends BaseService<
  WorkerExecution,
  CreateExecutionInput,
  UpdateExecutionInput
> {
  protected modelName = Prisma.ModelName.WorkerExecution;

  /**
   * Create a new execution
   */
  async createExecution(
    data: CreateExecutionInput
  ): Promise<WorkerExecution> {
    return this.create(data, {
      brief: {
        include: {
          task: {
            include: {
              conversation: true,
            },
          },
        },
      },
    });
  }

  /**
   * Get execution by ID
   */
  async getExecution(id: string): Promise<WorkerExecution> {
    return this.findById(id, {
      brief: {
        include: {
          task: {
            include: {
              conversation: {
                include: {
                  user: true,
                },
              },
            },
          },
        },
      },
      feedback: true,
    });
  }

  /**
   * Get executions with filters
   */
  async getExecutions(
    filters: ExecutionFilters,
    pagination?: PaginationParams
  ) {
    const where: any = {};

    if (filters.briefId) {
      where.briefId = filters.briefId;
    }

    if (filters.taskId) {
      where.brief = { taskId: filters.taskId };
    }

    if (filters.userId) {
      where.brief = {
        task: {
          conversation: { userId: filters.userId },
        },
      };
    }

    if (filters.status) {
      where.status = Array.isArray(filters.status)
        ? { in: filters.status }
        : filters.status;
    }

    if (filters.modelUsed) {
      where.modelUsed = filters.modelUsed;
    }

    if (filters.dateRange) {
      where.requestTimestamp = {
        gte: filters.dateRange.from,
        lte: filters.dateRange.to,
      };
    }

    return this.paginate(
      where,
      pagination || {},
      {
        include: {
          brief: {
            include: {
              task: true,
            },
          },
        },
        orderBy: { requestTimestamp: 'desc' },
      }
    );
  }

  /**
   * Update execution
   */
  async updateExecution(
    id: string,
    data: UpdateExecutionInput
  ): Promise<WorkerExecution> {
    // If status is changing to completed, set completedAt
    if (data.status === ExecutionStatus.COMPLETED) {
      data.completedAt = new Date();
    }

    return this.update(id, data);
  }

  /**
   * Mark execution as running
   */
  async markRunning(id: string): Promise<WorkerExecution> {
    return this.update(id, {
      status: ExecutionStatus.RUNNING,
    });
  }

  /**
   * Complete execution
   */
  async completeExecution(
    id: string,
    data: {
      responseContent: string;
      responseMetadata: any;
      promptTokens: number;
      completionTokens: number;
      totalTokens: number;
      latencyMs: number;
      costUsd: number;
      qualityScore?: number;
      meetsSuccessCriteria?: boolean;
      validationResults?: any;
    }
  ): Promise<WorkerExecution> {
    return this.update(id, {
      ...data,
      status: ExecutionStatus.COMPLETED,
      responseTimestamp: new Date(),
      completedAt: new Date(),
    });
  }

  /**
   * Fail execution
   */
  async failExecution(
    id: string,
    error: any
  ): Promise<WorkerExecution> {
    return this.update(id, {
      status: ExecutionStatus.FAILED,
      error,
      completedAt: new Date(),
    });
  }

  /**
   * Retry execution
   */
  async retryExecution(id: string): Promise<WorkerExecution> {
    const execution = await this.getExecution(id);
    
    return this.update(id, {
      status: ExecutionStatus.RETRYING,
      retryCount: execution.retryCount + 1,
    });
  }

  /**
   * Cancel execution
   */
  async cancelExecution(id: string): Promise<WorkerExecution> {
    return this.update(id, {
      status: ExecutionStatus.CANCELLED,
      completedAt: new Date(),
    });
  }

  /**
   * Get execution statistics
   */
  async getExecutionStats(filters: ExecutionFilters) {
    const where: any = {};

    if (filters.briefId) {
      where.briefId = filters.briefId;
    }

    if (filters.userId) {
      where.brief = {
        task: {
          conversation: { userId: filters.userId },
        },
      };
    }

    if (filters.dateRange) {
      where.requestTimestamp = {
        gte: filters.dateRange.from,
        lte: filters.dateRange.to,
      };
    }

    const [
      total,
      byStatus,
      byModel,
      aggregates,
    ] = await Promise.all([
      this.count(where),
      this.prisma.workerExecution.groupBy({
        by: ['status'],
        where,
        _count: true,
      }),
      this.prisma.workerExecution.groupBy({
        by: ['modelUsed'],
        where,
        _count: true,
        _avg: {
          latencyMs: true,
          costUsd: true,
        },
      }),
      this.prisma.workerExecution.aggregate({
        where,
        _sum: {
          totalTokens: true,
          costUsd: true,
        },
        _avg: {
          latencyMs: true,
          qualityScore: true,
        },
      }),
    ]);

    return {
      total,
      byStatus: byStatus.map(s => ({
        status: s.status,
        count: s._count,
      })),
      byModel: byModel.map(m => ({
        model: m.modelUsed,
        count: m._count,
        avgLatency: m._avg.latencyMs,
        avgCost: m._avg.costUsd,
      })),
      totals: {
        tokens: aggregates._sum.totalTokens || 0,
        cost: aggregates._sum.costUsd || 0,
      },
      averages: {
        latency: aggregates._avg.latencyMs || 0,
        qualityScore: aggregates._avg.qualityScore || 0,
      },
    };
  }

  /**
   * Add execution feedback
   */
  async addFeedback(
    executionId: string,
    userId: string,
    data: {
      rating: number;
      helpful: boolean;
      comments?: string;
      issues?: any;
    }
  ) {
    return this.prisma.executionFeedback.create({
      data: {
        executionId,
        userId,
        ...data,
      },
    });
  }
}
```

### 8. **Memory Service** (Partial - Key Methods)

```typescript
// lib/db/services/memory.service.ts

import { Prisma, MemoryEntry, MemoryType } from '@prisma/client';
import { BaseService } from '../base-service';

export interface CreateMemoryInput {
  userId: string;
  content: string;
  summary?: string;
  type: MemoryType;
  tags?: string[];
  embedding?: number[];
  sourceType?: string;
  sourceId?: string;
  importance?: number;
}

export interface UpdateMemoryInput {
  content?: string;
  summary?: string;
  tags?: string[];
  importance?: number;
}

export class MemoryService extends BaseService<
  MemoryEntry,
  CreateMemoryInput,
  UpdateMemoryInput
> {
  protected modelName = Prisma.ModelName.MemoryEntry;

  /**
   * Create a new memory entry
   */
  async createMemory(data: CreateMemoryInput): Promise<MemoryEntry> {
    return this.create(data);
  }

  /**
   * Get memory by ID
   */
  async getMemory(id: string): Promise<MemoryEntry> {
    // Increment access count
    await this.prisma.memoryEntry.update({
      where: { id },
      data: {
        accessCount: { increment: 1 },
        lastAccessedAt: new Date(),
      },
    });

    return this.findById(id);
  }

  /**
   * Search memories by semantic similarity
   */
  async searchMemories(
    userId: string,
    embedding: number[],
    options?: {
      limit?: number;
      threshold?: number;
      type?: MemoryType;
    }
  ): Promise<MemoryEntry[]> {
    const limit = options?.limit || 10;
    const threshold = options?.threshold || 0.7;

    // Use pgvector similarity search
    const memories = await this.prisma.$queryRaw<MemoryEntry[]>`
      SELECT *
      FROM memory_entries
      WHERE user_id = ${userId}
        ${options?.type ? Prisma.sql`AND type = ${options.type}::memory_type` : Prisma.empty}
        AND embedding IS NOT NULL
      ORDER BY embedding <=> ${JSON.stringify(embedding)}::vector
      LIMIT ${limit}
    `;

    return memories;
  }

  /**
   * Get memories by tags
   */
  async getMemoriesByTags(
    userId: string,
    tags: string[]
  ): Promise<MemoryEntry[]> {
    return this.findMany(
      {
        userId,
        tags: { hasSome: tags },
      },
      {
        orderBy: [
          { importance: 'desc' },
          { lastAccessedAt: 'desc' },
        ],
      }
    );
  }

  /**
   * Update memory
   */
  async updateMemory(
    id: string,
    data: UpdateMemoryInput
  ): Promise<MemoryEntry> {
    return this.update(id, data);
  }

  /**
   * Delete memory
   */
  async deleteMemory(id: string): Promise<MemoryEntry> {
    return this.delete(id);
  }
}
```

### 9. **Analytics Service**

```typescript
// lib/db/services/analytics.service.ts

import { PrismaClient } from '@prisma/client';
import { prisma } from '../prisma';

export interface DateRange {
  from: Date;
  to: Date;
}

export class AnalyticsService {
  private prisma: PrismaClient;

  constructor(prismaClient?: PrismaClient) {
    this.prisma = prismaClient || prisma;
  }

  /**
   * Track cost for an operation
   */
  async trackCost(data: {
    userId: string;
    operation: string;
    model: string;
    tokens: number;
    costUsd: number;
    taskId?: string;
    briefId?: string;
    executionId?: string;
  }) {
    return this.prisma.costTracking.create({ data });
  }

  /**
   * Get cost summary
   */
  async getCostSummary(
    userId: string,
    dateRange: DateRange
  ) {
    const costs = await this.prisma.costTracking.groupBy({
      by: ['operation', 'model'],
      where: {
        userId,
        timestamp: {
          gte: dateRange.from,
          lte: dateRange.to,
        },
      },
      _sum: {
        costUsd: true,
        tokens: true,
      },
      _count: true,
    });

    const total = await this.prisma.costTracking.aggregate({
      where: {
        userId,
        timestamp: {
          gte: dateRange.from,
          lte: dateRange.to,
        },
      },
      _sum: {
        costUsd: true,
        tokens: true,
      },
    });

    return {
      total: {
        cost: total._sum.costUsd || 0,
        tokens: total._sum.tokens || 0,
      },
      byOperation: costs.map(c => ({
        operation: c.operation,
        model: c.model,
        cost: c._sum.costUsd || 0,
        tokens: c._sum.tokens || 0,
        count: c._count,
      })),
    };
  }

  /**
   * Record performance metric
   */
  async recordMetric(data: {
    component: string;
    metric: string;
    value: number;
    unit: string;
    metadata?: any;
  }) {
    return this.prisma.performanceMetric.create({ data });
  }

  /**
   * Get performance metrics
   */
  async getMetrics(
    component: string,
    metric: string,
    dateRange: DateRange
  ) {
    return this.prisma.performanceMetric.findMany({
      where: {
        component,
        metric,
        timestamp: {
          gte: dateRange.from,
          lte: dateRange.to,
        },
      },
      orderBy: { timestamp: 'asc' },
    });
  }

  /**
   * Log system event
   */
  async logEvent(data: {
    eventType: string;
    severity: any;
    message: string;
    userId?: string;
    taskId?: string;
    executionId?: string;
    data?: any;
    stackTrace?: string;
  }) {
    return this.prisma.systemEvent.create({ data });
  }

  /**
   * Get recent events
   */
  async getRecentEvents(
    options: {
      severity?: any;
      eventType?: string;
      limit?: number;
    }
  ) {
    return this.prisma.systemEvent.findMany({
      where: {
        severity: options.severity,
        eventType: options.eventType,
      },
      orderBy: { timestamp: 'desc' },
      take: options.limit || 100,
    });
  }
}
```

---

## Service Index

```typescript
// lib/db/services/index.ts

export { UserService } from './user.service';
export { OrganizationService } from './organization.service';
export { ConversationService } from './conversation.service';
export { DelegationService } from './delegation.service';
export { TaskService } from './task.service';
export { BriefService } from './brief.service';
export { ExecutionService } from './execution.service';
export { MemoryService } from './memory.service';
export { AnalyticsService } from './analytics.service';

// Create service instances
import { prisma } from '../prisma';

export const userService = new UserService(prisma);
export const organizationService = new OrganizationService(prisma);
export const conversationService = new ConversationService(prisma);
export const delegationService = new DelegationService(prisma);
export const taskService = new TaskService(prisma);
export const briefService = new BriefService(prisma);
export const executionService = new ExecutionService(prisma);
export const memoryService = new MemoryService(prisma);
export const analyticsService = new AnalyticsService(prisma);
```

---

## Usage Examples

```typescript
// Example 1: Create a user and conversation
import { userService, conversationService } from '@/lib/db/services';

const user = await userService.createUser({
  email: 'john@example.com',
  name: 'John Doe',
});

const conversation = await conversationService.createConversation({
  userId: user.id,
  title: 'Planning Q4 Strategy',
});

// Example 2: Add a message and track delegation signal
import { delegationService } from '@/lib/db/services';

const message = await conversationService.addMessage({
  conversationId: conversation.id,
  role: 'USER',
  content: 'Can we analyze our competitor landscape?',
  tokenCount: 10,
});

const signal = await delegationService.createSignal({
  messageId: message.id,
  type: 'IMPLICIT',
  confidence: 0.85,
  triggerPhrase: 'Can we analyze',
  contextSnippet: 'competitor landscape',
  suggestedAction: 'Create competitive analysis task',
});

// Example 3: Create and approve a task
import { taskService } from '@/lib/db/services';

const task = await taskService.createTask({
  conversationId: conversation.id,
  signalId: signal.id,
  objective: 'Analyze top 5 competitors in our market',
  scope: ['Market share', 'Product features', 'Pricing'],
  constraints: ['Use public data only', 'Complete within 24 hours'],
  deliverables: [
    {
      name: 'Competitive Analysis Report',
      format: 'markdown',
      qualityRequirements: 'Comprehensive with data sources',
    },
  ],
  taskType: 'ANALYSIS',
  complexity: 'MODERATE',
  estimatedCost: 0.50,
  approvalRequired: false,
});

// Example 4: Create a brief and execute
import { briefService, executionService } from '@/lib/db/services';

const brief = await briefService.createBrief({
  taskId: task.id,
  systemPrompt: 'You are a competitive intelligence analyst...',
  userPrompt: 'Analyze the top 5 competitors...',
  outputFormat: { type: 'markdown', validationRules: [] },
  successCriteria: ['Identifies all 5 competitors', 'Includes market share data'],
  modelConfig: {
    provider: 'anthropic',
    model: 'claude-3-opus',
    fallbackModels: ['gpt-4-turbo'],
  },
  maxTokens: 4000,
  temperature: 0.3,
});

const execution = await executionService.createExecution({
  briefId: brief.id,
  modelUsed: 'claude-3-opus',
  requestPayload: { /* ... */ },
});

// Example 5: Get analytics
import { analyticsService } from '@/lib/db/services';

const costSummary = await analyticsService.getCostSummary(
  user.id,
  {
    from: new Date('2025-01-01'),
    to: new Date('2025-01-31'),
  }
);

console.log('Total cost:', costSummary.total.cost);
console.log('Total tokens:', costSummary.total.tokens);
```

---

## Next Steps

Would you like me to:

1. **Create the API route handlers** that use these services?
2. **Build the OpenRouter integration** with the execution service?
3. **Create validation schemas (Zod)** for all inputs?
4. **Write unit tests** for the service layer?
5. **Design the real-time WebSocket** event system?

Let me know what to tackle next! 🚀<br>

<i>[10/12/2025, 11:48:17 AM]</i> 👉 <b>👤 User</b>: Create the API route handlers that use these services?<br>
<i>[10/12/2025, 11:50:27 AM]</i> 👉 <b>🤖 Assistant</b>: 

The user wants me to create API route handlers that use the Prisma services we just built. I should create Next.js API routes (App Router format) that implement the REST API endpoints outlined in the system blueprint.

I'll organize this as:
1. API route structure for Next.js App Router
2. Route handlers for each domain (users, conversations, tasks, briefs, executions)
3. Middleware for auth, error handling, validation
4. WebSocket handlers for real-time updates
5. Helper utilities

I should use the App Router format (app/api/...) rather than Pages Router since that's the modern Next.js approach.# API Route Handlers (Next.js App Router)

## Directory Structure

```
app/
├── api/
│   ├── v1/
│   │   ├── users/
│   │   │   ├── route.ts                    # GET, POST /api/v1/users
│   │   │   ├── [userId]/
│   │   │   │   ├── route.ts                # GET, PATCH, DELETE /api/v1/users/:userId
│   │   │   │   └── stats/route.ts          # GET /api/v1/users/:userId/stats
│   │   ├── organizations/
│   │   │   ├── route.ts
│   │   │   └── [orgId]/
│   │   │       ├── route.ts
│   │   │       └── usage/route.ts
│   │   ├── conversations/
│   │   │   ├── route.ts                    # GET, POST /api/v1/conversations
│   │   │   └── [conversationId]/
│   │   │       ├── route.ts                # GET, PATCH, DELETE
│   │   │       ├── messages/route.ts       # GET, POST messages
│   │   │       ├── archive/route.ts        # POST archive
│   │   │       └── context/route.ts        # GET recent context
│   │   ├── signals/
│   │   │   ├── route.ts                    # GET, POST delegation signals
│   │   │   ├── [signalId]/route.ts
│   │   │   ├── unprocessed/route.ts        # GET unprocessed signals
│   │   │   └── stats/route.ts
│   │   ├── tasks/
│   │   │   ├── route.ts                    # GET, POST tasks
│   │   │   ├── [taskId]/
│   │   │   │   ├── route.ts                # GET, PATCH, DELETE
│   │   │   │   ├── approve/route.ts        # POST approve task
│   │   │   │   ├── reject/route.ts         # POST reject task
│   │   │   │   └── cancel/route.ts         # POST cancel task
│   │   │   ├── pending/route.ts            # GET pending approval tasks
│   │   │   └── stats/route.ts
│   │   ├── briefs/
│   │   │   ├── route.ts                    # GET, POST briefs
│   │   │   └── [briefId]/
│   │   │       ├── route.ts                # GET, PATCH
│   │   │       ├── dispatch/route.ts       # POST dispatch to worker
│   │   │       └── validate/route.ts       # POST validate brief
│   │   ├── executions/
│   │   │   ├── route.ts                    # GET, POST executions
│   │   │   └── [executionId]/
│   │   │       ├── route.ts                # GET, PATCH
│   │   │       ├── stream/route.ts         # GET stream execution
│   │   │       ├── retry/route.ts          # POST retry
│   │   │       ├── cancel/route.ts         # POST cancel
│   │   │       └── feedback/route.ts       # POST feedback
│   │   ├── memory/
│   │   │   ├── route.ts                    # GET, POST memory entries
│   │   │   ├── [memoryId]/route.ts
│   │   │   └── search/route.ts             # POST semantic search
│   │   └── analytics/
│   │       ├── costs/route.ts              # GET cost analytics
│   │       ├── performance/route.ts        # GET performance metrics
│   │       └── events/route.ts             # GET system events
│   └── middleware.ts
├── lib/
│   └── api/
│       ├── middleware/
│       │   ├── auth.ts                     # Authentication middleware
│       │   ├── error-handler.ts            # Error handling
│       │   ├── rate-limit.ts               # Rate limiting
│       │   └── validation.ts               # Request validation
│       ├── utils/
│       │   ├── response.ts                 # Response helpers
│       │   ├── pagination.ts               # Pagination helpers
│       │   └── errors.ts                   # API error classes
│       └── schemas/
│           ├── user.schema.ts              # Zod schemas for users
│           ├── conversation.schema.ts
│           ├── task.schema.ts
│           ├── brief.schema.ts
│           └── execution.schema.ts
```

---

## Core Utilities & Middleware

### 1. **Response Helpers**

```typescript
// lib/api/utils/response.ts

import { NextResponse } from 'next/server';

export class ApiResponse {
  /**
   * Success response
   */
  static success<T>(data: T, status: number = 200) {
    return NextResponse.json(
      {
        success: true,
        data,
      },
      { status }
    );
  }

  /**
   * Created response
   */
  static created<T>(data: T) {
    return this.success(data, 201);
  }

  /**
   * No content response
   */
  static noContent() {
    return new NextResponse(null, { status: 204 });
  }

  /**
   * Error response
   */
  static error(
    message: string,
    status: number = 500,
    errors?: any
  ) {
    return NextResponse.json(
      {
        success: false,
        error: {
          message,
          ...(errors && { errors }),
        },
      },
      { status }
    );
  }

  /**
   * Bad request response
   */
  static badRequest(message: string, errors?: any) {
    return this.error(message, 400, errors);
  }

  /**
   * Unauthorized response
   */
  static unauthorized(message: string = 'Unauthorized') {
    return this.error(message, 401);
  }

  /**
   * Forbidden response
   */
  static forbidden(message: string = 'Forbidden') {
    return this.error(message, 403);
  }

  /**
   * Not found response
   */
  static notFound(message: string = 'Resource not found') {
    return this.error(message, 404);
  }

  /**
   * Conflict response
   */
  static conflict(message: string) {
    return this.error(message, 409);
  }

  /**
   * Too many requests response
   */
  static tooManyRequests(message: string = 'Too many requests') {
    return this.error(message, 429);
  }

  /**
   * Internal server error response
   */
  static internalError(message: string = 'Internal server error') {
    return this.error(message, 500);
  }

  /**
   * Paginated response
   */
  static paginated<T>(data: {
    data: T[];
    pagination: {
      total: number;
      page: number;
      limit: number;
      totalPages: number;
      hasNext: boolean;
      hasPrev: boolean;
    };
  }) {
    return NextResponse.json({
      success: true,
      ...data,
    });
  }
}
```

### 2. **Pagination Helpers**

```typescript
// lib/api/utils/pagination.ts

export interface PaginationParams {
  page: number;
  limit: number;
}

export function parsePaginationParams(
  searchParams: URLSearchParams
): PaginationParams {
  const page = Math.max(1, parseInt(searchParams.get('page') || '1'));
  const limit = Math.min(
    100,
    Math.max(1, parseInt(searchParams.get('limit') || '20'))
  );

  return { page, limit };
}

export function buildPaginationLinks(
  baseUrl: string,
  pagination: {
    page: number;
    limit: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  }
): {
  first?: string;
  prev?: string;
  next?: string;
  last?: string;
} {
  const links: any = {};
  const url = new URL(baseUrl);

  if (pagination.page > 1) {
    url.searchParams.set('page', '1');
    url.searchParams.set('limit', pagination.limit.toString());
    links.first = url.toString();
  }

  if (pagination.hasPrev) {
    url.searchParams.set('page', (pagination.page - 1).toString());
    url.searchParams.set('limit', pagination.limit.toString());
    links.prev = url.toString();
  }

  if (pagination.hasNext) {
    url.searchParams.set('page', (pagination.page + 1).toString());
    url.searchParams.set('limit', pagination.limit.toString());
    links.next = url.toString();
  }

  if (pagination.page < pagination.totalPages) {
    url.searchParams.set('page', pagination.totalPages.toString());
    url.searchParams.set('limit', pagination.limit.toString());
    links.last = url.toString();
  }

  return links;
}
```

### 3. **Error Handler Middleware**

```typescript
// lib/api/middleware/error-handler.ts

import { NextResponse } from 'next/server';
import {
  DatabaseError,
  NotFoundError,
  ValidationError,
  UnauthorizedError,
  ConflictError,
  QuotaExceededError,
} from '@/lib/db/errors';
import { ApiResponse } from '../utils/response';
import { ZodError } from 'zod';

export function handleApiError(error: unknown): NextResponse {
  console.error('API Error:', error);

  // Zod validation errors
  if (error instanceof ZodError) {
    return ApiResponse.badRequest(
      'Validation failed',
      error.errors.map(e => ({
        path: e.path.join('.'),
        message: e.message,
      }))
    );
  }

  // Database errors
  if (error instanceof NotFoundError) {
    return ApiResponse.notFound(error.message);
  }

  if (error instanceof ValidationError) {
    return ApiResponse.badRequest(error.message, error.fields);
  }

  if (error instanceof UnauthorizedError) {
    return ApiResponse.unauthorized(error.message);
  }

  if (error instanceof ConflictError) {
    return ApiResponse.conflict(error.message);
  }

  if (error instanceof QuotaExceededError) {
    return ApiResponse.error(
      error.message,
      429,
      {
        limit: error.limit,
        current: error.current,
      }
    );
  }

  if (error instanceof DatabaseError) {
    return ApiResponse.internalError(error.message);
  }

  // Generic errors
  if (error instanceof Error) {
    return ApiResponse.internalError(error.message);
  }

  return ApiResponse.internalError('An unexpected error occurred');
}

/**
 * Wrap an API handler with error handling
 */
export function withErrorHandler<T extends any[]>(
  handler: (...args: T) => Promise<NextResponse>
) {
  return async (...args: T): Promise<NextResponse> => {
    try {
      return await handler(...args);
    } catch (error) {
      return handleApiError(error);
    }
  };
}
```

### 4. **Auth Middleware**

```typescript
// lib/api/middleware/auth.ts

import { NextRequest } from 'next/server';
import { auth, currentUser } from '@clerk/nextjs';
import { UnauthorizedError } from '@/lib/db/errors';
import { userService } from '@/lib/db/services';
import { User } from '@prisma/client';

export interface AuthContext {
  userId: string;
  user: User;
  clerkUser: any;
}

/**
 * Get authenticated user context
 */
export async function getAuthContext(
  request: NextRequest
): Promise<AuthContext> {
  const { userId: clerkUserId } = auth();

  if (!clerkUserId) {
    throw new UnauthorizedError('Authentication required');
  }

  const clerkUser = await currentUser();
  
  if (!clerkUser) {
    throw new UnauthorizedError('User not found');
  }

  // Get or create user in database
  let user = await userService.getUserByClerkId(clerkUserId);

  if (!user) {
    // Create user if doesn't exist
    user = await userService.createUser({
      email: clerkUser.emailAddresses[0]?.emailAddress || '',
      name: `${clerkUser.firstName} ${clerkUser.lastName}`.trim(),
      clerkId: clerkUserId,
      avatarUrl: clerkUser.imageUrl,
    });
  }

  return {
    userId: user.id,
    user,
    clerkUser,
  };
}

/**
 * Require authentication for a route handler
 */
export function requireAuth<T extends any[]>(
  handler: (context: AuthContext, ...args: T) => Promise<NextResponse>
) {
  return async (request: NextRequest, ...args: T): Promise<NextResponse> => {
    const context = await getAuthContext(request);
    return handler(context, request, ...args);
  };
}

/**
 * Check if user owns a resource
 */
export async function requireOwnership(
  userId: string,
  resourceUserId: string,
  resourceType: string = 'resource'
) {
  if (userId !== resourceUserId) {
    throw new UnauthorizedError(
      `You don't have permission to access this ${resourceType}`
    );
  }
}
```

### 5. **Validation Schemas**

```typescript
// lib/api/schemas/conversation.schema.ts

import { z } from 'zod';

export const createConversationSchema = z.object({
  title: z.string().min(1).max(200).optional(),
});

export const updateConversationSchema = z.object({
  title: z.string().min(1).max(200).optional(),
  summary: z.string().max(1000).optional(),
  isActive: z.boolean().optional(),
});

export const createMessageSchema = z.object({
  role: z.enum(['USER', 'ASSISTANT', 'SYSTEM']),
  content: z.string().min(1),
  tokenCount: z.number().int().positive().optional(),
  modelUsed: z.string().optional(),
});

// lib/api/schemas/task.schema.ts

export const createTaskSchema = z.object({
  conversationId: z.string().cuid(),
  signalId: z.string().cuid(),
  objective: z.string().min(10).max(1000),
  scope: z.array(z.string()),
  constraints: z.array(z.string()),
  deliverables: z.array(
    z.object({
      name: z.string(),
      description: z.string(),
      format: z.string(),
      qualityRequirements: z.string().optional(),
    })
  ),
  taskType: z.enum([
    'RESEARCH',
    'ANALYSIS',
    'GENERATION',
    'TRANSFORMATION',
    'SYNTHESIS',
    'MONITORING',
  ]),
  complexity: z.enum(['SIMPLE', 'MODERATE', 'COMPLEX', 'EPIC']),
  estimatedTokens: z.number().int().positive().optional(),
  estimatedDuration: z.number().int().positive().optional(),
  estimatedCost: z.number().positive().optional(),
  relevantContext: z.string().optional(),
  approvalRequired: z.boolean().optional(),
  costCeiling: z.number().positive().optional(),
});

export const updateTaskSchema = z.object({
  objective: z.string().min(10).max(1000).optional(),
  scope: z.array(z.string()).optional(),
  constraints: z.array(z.string()).optional(),
  deliverables: z.array(z.any()).optional(),
  status: z
    .enum([
      'EXTRACTED',
      'PENDING_APPROVAL',
      'APPROVED',
      'REJECTED',
      'BRIEF_GENERATED',
      'EXECUTING',
      'COMPLETED',
      'FAILED',
      'CANCELLED',
    ])
    .optional(),
});

export const approveTaskSchema = z.object({
  approverId: z.string().cuid(),
});

export const rejectTaskSchema = z.object({
  approverId: z.string().cuid(),
  reason: z.string().min(10).max(500),
});

// lib/api/schemas/brief.schema.ts

export const createBriefSchema = z.object({
  taskId: z.string().cuid(),
  systemPrompt: z.string().min(10),
  userPrompt: z.string().min(10),
  contextDocuments: z.any().optional(),
  relevantMemory: z.any().optional(),
  examples: z.any().optional(),
  outputFormat: z.object({
    type: z.enum(['text', 'json', 'markdown', 'code', 'structured']),
    schema: z.any().optional(),
    template: z.string().optional(),
    validationRules: z.array(z.any()),
  }),
  successCriteria: z.array(z.string()),
  qualityThresholds: z.any().optional(),
  modelConfig: z.object({
    provider: z.enum(['openai', 'anthropic', 'google', 'meta']),
    model: z.string(),
    fallbackModels: z.array(z.string()).optional(),
  }),
  maxTokens: z.number().int().positive(),
  temperature: z.number().min(0).max(2),
  stopSequences: z.array(z.string()).optional(),
  costLimit: z.number().positive().optional(),
  timeLimit: z.number().int().positive().optional(),
  retryPolicy: z.any().optional(),
});

// lib/api/schemas/execution.schema.ts

export const createExecutionSchema = z.object({
  briefId: z.string().cuid(),
  modelUsed: z.string(),
  requestPayload: z.any(),
});

export const completeExecutionSchema = z.object({
  responseContent: z.string(),
  responseMetadata: z.any(),
  promptTokens: z.number().int().positive(),
  completionTokens: z.number().int().positive(),
  totalTokens: z.number().int().positive(),
  latencyMs: z.number().int().positive(),
  costUsd: z.number().positive(),
  qualityScore: z.number().min(0).max(1).optional(),
  meetsSuccessCriteria: z.boolean().optional(),
  validationResults: z.any().optional(),
});

export const addFeedbackSchema = z.object({
  rating: z.number().int().min(1).max(5),
  helpful: z.boolean(),
  comments: z.string().max(1000).optional(),
  issues: z.any().optional(),
});
```

---

## API Route Implementations

### 1. **Conversation Routes**

```typescript
// app/api/v1/conversations/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { parsePaginationParams } from '@/lib/api/utils/pagination';
import { conversationService } from '@/lib/db/services';
import { createConversationSchema } from '@/lib/api/schemas/conversation.schema';

/**
 * GET /api/v1/conversations
 * List user's conversations
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const { searchParams } = new URL(request.url);
    const pagination = parsePaginationParams(searchParams);

    const result = await conversationService.getUserConversations(
      context.userId,
      pagination
    );

    return ApiResponse.paginated(result);
  })
);

/**
 * POST /api/v1/conversations
 * Create a new conversation
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const body = await request.json();
    const data = createConversationSchema.parse(body);

    const conversation = await conversationService.createConversation({
      userId: context.userId,
      ...data,
    });

    return ApiResponse.created(conversation);
  })
);
```

```typescript
// app/api/v1/conversations/[conversationId]/route.ts

import { NextRequest } from 'next/server';
import {
  requireAuth,
  requireOwnership,
  withErrorHandler,
} from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { conversationService } from '@/lib/db/services';
import { updateConversationSchema } from '@/lib/api/schemas/conversation.schema';

interface RouteParams {
  params: { conversationId: string };
}

/**
 * GET /api/v1/conversations/:conversationId
 * Get a specific conversation
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const conversation = await conversationService.getConversation(
      params.conversationId
    );

    await requireOwnership(
      context.userId,
      conversation.userId,
      'conversation'
    );

    return ApiResponse.success(conversation);
  })
);

/**
 * PATCH /api/v1/conversations/:conversationId
 * Update a conversation
 */
export const PATCH = withErrorHandler(
  requireAuth(
    async (context, request: NextRequest, { params }: RouteParams) => {
      const conversation = await conversationService.getConversation(
        params.conversationId
      );

      await requireOwnership(
        context.userId,
        conversation.userId,
        'conversation'
      );

      const body = await request.json();
      const data = updateConversationSchema.parse(body);

      const updated = await conversationService.updateConversation(
        params.conversationId,
        data
      );

      return ApiResponse.success(updated);
    }
  )
);

/**
 * DELETE /api/v1/conversations/:conversationId
 * Delete a conversation
 */
export const DELETE = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const conversation = await conversationService.getConversation(
      params.conversationId
    );

    await requireOwnership(
      context.userId,
      conversation.userId,
      'conversation'
    );

    await conversationService.deleteConversation(params.conversationId);

    return ApiResponse.noContent();
  })
);
```

```typescript
// app/api/v1/conversations/[conversationId]/messages/route.ts

import { NextRequest } from 'next/server';
import {
  requireAuth,
  requireOwnership,
  withErrorHandler,
} from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { conversationService } from '@/lib/db/services';
import { createMessageSchema } from '@/lib/api/schemas/conversation.schema';

interface RouteParams {
  params: { conversationId: string };
}

/**
 * GET /api/v1/conversations/:conversationId/messages
 * Get conversation messages
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const conversation = await conversationService.getConversation(
      params.conversationId
    );

    await requireOwnership(
      context.userId,
      conversation.userId,
      'conversation'
    );

    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '100');
    const cursor = searchParams.get('cursor') || undefined;
    const order = (searchParams.get('order') as 'asc' | 'desc') || 'asc';

    const messages = await conversationService.getMessages(
      params.conversationId,
      { limit, cursor, order }
    );

    return ApiResponse.success(messages);
  })
);

/**
 * POST /api/v1/conversations/:conversationId/messages
 * Add a message to conversation
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const conversation = await conversationService.getConversation(
      params.conversationId
    );

    await requireOwnership(
      context.userId,
      conversation.userId,
      'conversation'
    );

    const body = await request.json();
    const data = createMessageSchema.parse(body);

    const message = await conversationService.addMessage({
      conversationId: params.conversationId,
      ...data,
    });

    return ApiResponse.created(message);
  })
);
```

```typescript
// app/api/v1/conversations/[conversationId]/archive/route.ts

import { NextRequest } from 'next/server';
import {
  requireAuth,
  requireOwnership,
  withErrorHandler,
} from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { conversationService } from '@/lib/db/services';

interface RouteParams {
  params: { conversationId: string };
}

/**
 * POST /api/v1/conversations/:conversationId/archive
 * Archive a conversation
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const conversation = await conversationService.getConversation(
      params.conversationId
    );

    await requireOwnership(
      context.userId,
      conversation.userId,
      'conversation'
    );

    const archived = await conversationService.archiveConversation(
      params.conversationId
    );

    return ApiResponse.success(archived);
  })
);
```

### 2. **Task Routes**

```typescript
// app/api/v1/tasks/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { parsePaginationParams } from '@/lib/api/utils/pagination';
import { taskService } from '@/lib/db/services';
import { createTaskSchema } from '@/lib/api/schemas/task.schema';
import { TaskStatus, TaskType, ComplexityRating } from '@prisma/client';

/**
 * GET /api/v1/tasks
 * List tasks with filters
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const { searchParams } = new URL(request.url);
    const pagination = parsePaginationParams(searchParams);

    // Parse filters
    const filters: any = {
      userId: context.userId,
    };

    const conversationId = searchParams.get('conversationId');
    if (conversationId) {
      filters.conversationId = conversationId;
    }

    const status = searchParams.get('status');
    if (status) {
      filters.status = status.split(',') as TaskStatus[];
    }

    const taskType = searchParams.get('taskType');
    if (taskType) {
      filters.taskType = taskType as TaskType;
    }

    const complexity = searchParams.get('complexity');
    if (complexity) {
      filters.complexity = complexity as ComplexityRating;
    }

    const from = searchParams.get('from');
    const to = searchParams.get('to');
    if (from || to) {
      filters.dateRange = {
        from: from ? new Date(from) : undefined,
        to: to ? new Date(to) : undefined,
      };
    }

    const result = await taskService.getTasks(filters, pagination);

    return ApiResponse.paginated(result);
  })
);

/**
 * POST /api/v1/tasks
 * Create a new task
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const body = await request.json();
    const data = createTaskSchema.parse(body);

    // Check quota if cost is estimated
    if (data.estimatedCost) {
      await taskService.checkTaskQuota(context.userId, data.estimatedCost);
    }

    const task = await taskService.createTask(data);

    return ApiResponse.created(task);
  })
);
```

```typescript
// app/api/v1/tasks/[taskId]/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { taskService } from '@/lib/db/services';
import { updateTaskSchema } from '@/lib/api/schemas/task.schema';

interface RouteParams {
  params: { taskId: string };
}

/**
 * GET /api/v1/tasks/:taskId
 * Get a specific task
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const task = await taskService.getTask(params.taskId);

    // Check ownership via conversation
    if (task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    return ApiResponse.success(task);
  })
);

/**
 * PATCH /api/v1/tasks/:taskId
 * Update a task
 */
export const PATCH = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const task = await taskService.getTask(params.taskId);

    if (task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    const body = await request.json();
    const data = updateTaskSchema.parse(body);

    const updated = await taskService.updateTask(params.taskId, data);

    return ApiResponse.success(updated);
  })
);

/**
 * DELETE /api/v1/tasks/:taskId
 * Cancel a task
 */
export const DELETE = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const task = await taskService.getTask(params.taskId);

    if (task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    const cancelled = await taskService.cancelTask(params.taskId);

    return ApiResponse.success(cancelled);
  })
);
```

```typescript
// app/api/v1/tasks/[taskId]/approve/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { taskService } from '@/lib/db/services';

interface RouteParams {
  params: { taskId: string };
}

/**
 * POST /api/v1/tasks/:taskId/approve
 * Approve a task
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const task = await taskService.getTask(params.taskId);

    if (task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    const approved = await taskService.approveTask(
      params.taskId,
      context.userId
    );

    return ApiResponse.success(approved);
  })
);
```

```typescript
// app/api/v1/tasks/[taskId]/reject/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { taskService } from '@/lib/db/services';
import { rejectTaskSchema } from '@/lib/api/schemas/task.schema';

interface RouteParams {
  params: { taskId: string };
}

/**
 * POST /api/v1/tasks/:taskId/reject
 * Reject a task
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const task = await taskService.getTask(params.taskId);

    if (task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    const body = await request.json();
    const { reason } = rejectTaskSchema.parse(body);

    const rejected = await taskService.rejectTask(
      params.taskId,
      context.userId,
      reason
    );

    return ApiResponse.success(rejected);
  })
);
```

```typescript
// app/api/v1/tasks/pending/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { taskService } from '@/lib/db/services';

/**
 * GET /api/v1/tasks/pending
 * Get tasks pending approval
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const tasks = await taskService.getPendingApprovalTasks(context.userId);

    return ApiResponse.success(tasks);
  })
);
```

```typescript
// app/api/v1/tasks/stats/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { taskService } from '@/lib/db/services';

/**
 * GET /api/v1/tasks/stats
 * Get task statistics
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const { searchParams } = new URL(request.url);

    const filters: any = {
      userId: context.userId,
    };

    const from = searchParams.get('from');
    const to = searchParams.get('to');
    if (from || to) {
      filters.dateRange = {
        from: from ? new Date(from) : undefined,
        to: to ? new Date(to) : undefined,
      };
    }

    const stats = await taskService.getTaskStats(filters);

    return ApiResponse.success(stats);
  })
);
```

### 3. **Brief Routes**

```typescript
// app/api/v1/briefs/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { briefService, taskService } from '@/lib/db/services';
import { createBriefSchema } from '@/lib/api/schemas/brief.schema';

/**
 * GET /api/v1/briefs
 * List briefs for a task
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const { searchParams } = new URL(request.url);
    const taskId = searchParams.get('taskId');

    if (!taskId) {
      return ApiResponse.badRequest('taskId is required');
    }

    // Verify ownership
    const task = await taskService.getTask(taskId);
    if (task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    const briefs = await briefService.getBriefsByTask(taskId);

    return ApiResponse.success(briefs);
  })
);

/**
 * POST /api/v1/briefs
 * Create a new brief
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const body = await request.json();
    const data = createBriefSchema.parse(body);

    // Verify ownership
    const task = await taskService.getTask(data.taskId);
    if (task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    const brief = await briefService.createBrief(data);

    return ApiResponse.created(brief);
  })
);
```

```typescript
// app/api/v1/briefs/[briefId]/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { briefService } from '@/lib/db/services';

interface RouteParams {
  params: { briefId: string };
}

/**
 * GET /api/v1/briefs/:briefId
 * Get a specific brief
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const brief = await briefService.getBrief(params.briefId);

    // Check ownership
    if (brief.task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    return ApiResponse.success(brief);
  })
);
```

### 4. **Execution Routes**

```typescript
// app/api/v1/executions/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { parsePaginationParams } from '@/lib/api/utils/pagination';
import { executionService } from '@/lib/db/services';
import { createExecutionSchema } from '@/lib/api/schemas/execution.schema';
import { ExecutionStatus } from '@prisma/client';

/**
 * GET /api/v1/executions
 * List executions with filters
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const { searchParams } = new URL(request.url);
    const pagination = parsePaginationParams(searchParams);

    const filters: any = {
      userId: context.userId,
    };

    const briefId = searchParams.get('briefId');
    if (briefId) {
      filters.briefId = briefId;
    }

    const taskId = searchParams.get('taskId');
    if (taskId) {
      filters.taskId = taskId;
    }

    const status = searchParams.get('status');
    if (status) {
      filters.status = status.split(',') as ExecutionStatus[];
    }

    const modelUsed = searchParams.get('modelUsed');
    if (modelUsed) {
      filters.modelUsed = modelUsed;
    }

    const from = searchParams.get('from');
    const to = searchParams.get('to');
    if (from || to) {
      filters.dateRange = {
        from: from ? new Date(from) : undefined,
        to: to ? new Date(to) : undefined,
      };
    }

    const result = await executionService.getExecutions(filters, pagination);

    return ApiResponse.paginated(result);
  })
);

/**
 * POST /api/v1/executions
 * Create a new execution
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const body = await request.json();
    const data = createExecutionSchema.parse(body);

    // Note: Ownership check would be done in the orchestration layer
    // that calls this endpoint

    const execution = await executionService.createExecution(data);

    return ApiResponse.created(execution);
  })
);
```

```typescript
// app/api/v1/executions/[executionId]/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { executionService } from '@/lib/db/services';
import { completeExecutionSchema } from '@/lib/api/schemas/execution.schema';

interface RouteParams {
  params: { executionId: string };
}

/**
 * GET /api/v1/executions/:executionId
 * Get a specific execution
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const execution = await executionService.getExecution(params.executionId);

    // Check ownership
    if (execution.brief.task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    return ApiResponse.success(execution);
  })
);

/**
 * PATCH /api/v1/executions/:executionId
 * Update execution (typically called by worker)
 */
export const PATCH = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const body = await request.json();
    const data = completeExecutionSchema.parse(body);

    const execution = await executionService.completeExecution(
      params.executionId,
      data
    );

    return ApiResponse.success(execution);
  })
);
```

```typescript
// app/api/v1/executions/[executionId]/feedback/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { executionService } from '@/lib/db/services';
import { addFeedbackSchema } from '@/lib/api/schemas/execution.schema';

interface RouteParams {
  params: { executionId: string };
}

/**
 * POST /api/v1/executions/:executionId/feedback
 * Add feedback to an execution
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const execution = await executionService.getExecution(params.executionId);

    // Check ownership
    if (execution.brief.task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    const body = await request.json();
    const data = addFeedbackSchema.parse(body);

    const feedback = await executionService.addFeedback(
      params.executionId,
      context.userId,
      data
    );

    return ApiResponse.created(feedback);
  })
);
```

```typescript
// app/api/v1/executions/[executionId]/retry/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { executionService } from '@/lib/db/services';

interface RouteParams {
  params: { executionId: string };
}

/**
 * POST /api/v1/executions/:executionId/retry
 * Retry a failed execution
 */
export const POST = withErrorHandler(
  requireAuth(async (context, request: NextRequest, { params }: RouteParams) => {
    const execution = await executionService.getExecution(params.executionId);

    // Check ownership
    if (execution.brief.task.conversation.userId !== context.userId) {
      return ApiResponse.forbidden();
    }

    const retried = await executionService.retryExecution(params.executionId);

    return ApiResponse.success(retried);
  })
);
```

### 5. **Analytics Routes**

```typescript
// app/api/v1/analytics/costs/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { analyticsService } from '@/lib/db/services';

/**
 * GET /api/v1/analytics/costs
 * Get cost analytics
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const { searchParams } = new URL(request.url);

    const from = searchParams.get('from');
    const to = searchParams.get('to');

    if (!from || !to) {
      return ApiResponse.badRequest('from and to dates are required');
    }

    const dateRange = {
      from: new Date(from),
      to: new Date(to),
    };

    const summary = await analyticsService.getCostSummary(
      context.userId,
      dateRange
    );

    return ApiResponse.success(summary);
  })
);
```

```typescript
// app/api/v1/analytics/performance/route.ts

import { NextRequest } from 'next/server';
import { requireAuth, withErrorHandler } from '@/lib/api/middleware';
import { ApiResponse } from '@/lib/api/utils/response';
import { executionService } from '@/lib/db/services';

/**
 * GET /api/v1/analytics/performance
 * Get performance analytics
 */
export const GET = withErrorHandler(
  requireAuth(async (context, request: NextRequest) => {
    const { searchParams } = new URL(request.url);

    const filters: any = {
      userId: context.userId,
    };

    const from = searchParams.get('from');
    const to = searchParams.get('to');
    if (from && to) {
      filters.dateRange = {
        from: new Date(from),
        to: new Date(to),
      };
    }

    const stats = await executionService.getExecutionStats(filters);

    return ApiResponse.success(stats);
  })
);
```

---

## WebSocket Handler (Optional for Real-time Updates)

```typescript
// app/api/ws/route.ts

import { NextRequest } from 'next/server';
import { Server } from 'socket.io';

// This would need to be set up with a custom server
// or use a service like Pusher/Ably for real-time updates

export async function GET(request: NextRequest) {
  // WebSocket upgrade logic would go here
  // For Next.js, you might want to use a separate WebSocket server
  // or integrate with Pusher/Ably for production
  
  return new Response('WebSocket endpoint - use dedicated WS server', {
    status: 426,
    headers: {
      'Upgrade': 'Required',
    },
  });
}
```

---

## Testing Examples

```typescript
// Example: Testing conversation routes

// Create conversation
const createResponse = await fetch('/api/v1/conversations', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'Q4 Planning',
  }),
});

const { data: conversation } = await createResponse.json();

// Add message
await fetch(`/api/v1/conversations/${conversation.id}/messages`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    role: 'USER',
    content: 'Can we analyze our competitors?',
    tokenCount: 10,
  }),
});

// Get messages
const messagesResponse = await fetch(
  `/api/v1/conversations/${conversation.id}/messages`
);
const { data: messages } = await messagesResponse.json();

// Get conversations with pagination
const listResponse = await fetch('/api/v1/conversations?page=1&limit=10');
const { data: conversations, pagination } = await listResponse.json();
```

---

## Next Steps

Would you like me to:

1. **Create the OpenRouter integration** for dispatching briefs to AI workers?
2. **Build the WebSocket/SSE implementation** for real-time execution streaming?
3. **Create API client/SDK** for frontend consumption?
4. **Write integration tests** for the API routes?
5. **Build the orchestration layer** that connects all components (listener → extractor → brief → dispatcher)?

Let me know which piece to build next! 🚀<br>


---

<div align="center">

### Made with Echoes by R2bits

<a href="https://echoes.r2bits.com">
  <img src="https://images.squarespace-cdn.com/content/v1/6493af4741c13939d335f0b8/18b27467-2da2-43b7-8d44-234bccf4f462/MINI_ECHOES_LOGO_NORMAL_WHITE_TEXT_SMALL-05-14+%281%29.png?format=300w" alt="Echoes Logo" width="200"/>
</a>

</div>

---

<div style="display: flex; justify-content: space-between;">
  <span>This conversation was exported on 2025-10-17T18:36:04.334Z using <a href="https://echoes.r2bits.com">Echoes</a> by R2bits.</span>
  <span>Export Format Version: 1.0</span>
</div>
