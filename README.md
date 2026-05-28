# Agent Learning Checklist

## Foundation
- [x] LLM completions via HTTP
- [x] Multi-turn context management
- [x] Tool calling loop
- [x] Modular project structure

## Tools & Actions
- [x] Web search tool (tinyfish API)
- [x] Run shell commands
- [x] Read/write files
- [x] Fetch and summarize a URL
- [x] Get current time/weather
- [ ] Code execution sandbox (e2b or subprocess)
- [ ] Send email / calendar event (external action)

## Reliability
- [ ] Recursion/depth guard on tool calls
- [ ] Retry on API failure
- [ ] Graceful error reporting back to LLM (tool errors as tool results)
- [ ] Timeout on tool execution
- [ ] Tool input schema validation before calling
- [ ] Max token budget enforcement per run

## Memory
- [x] Sliding window — summarize old context when too long
- [ ] Persist context across sessions (JSON file)
- [ ] Semantic memory — embed + retrieve relevant past messages
- [ ] Entity extraction — track people / places / facts

## Planning & Reasoning
- [ ] ReAct loop (Reason → Act → Observe → repeat)
- [ ] Chain-of-thought via system prompt
- [ ] Multi-step task decomposition
- [ ] Self-critique — agent reviews its own output before responding
- [ ] Tree-of-thought / beam search over plans
- [ ] Explicit confidence scoring on tool results

## Multi-Agent
- [ ] Spawning subagents for subtasks
- [ ] Orchestrator / worker pattern
- [ ] Agents communicating via shared context or message passing
- [ ] Agent roles + permissions model
- [ ] Human-in-the-loop approval step

## Evals
- [ ] Build a small benchmark of tasks the agent should complete
- [ ] Score pass/fail per task
- [ ] Measure tool call accuracy and hallucination rate
- [ ] Regression testing when changing prompts or models
- [ ] Latency + cost tracking per run
- [ ] Adversarial / jailbreak robustness tests

## Safety & Observability
- [ ] Structured logging — every tool call in/out
- [ ] Prompt injection detection
- [ ] Action dry-run mode (plan without executing)
- [ ] Sandboxed file system for agent writes
- [ ] Rate limiting on destructive tool use