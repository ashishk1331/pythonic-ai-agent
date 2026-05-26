# Agent Learning Checklist

## Foundation
- [x] LLM completions via HTTP
- [x] Multi-turn context management
- [x] Tool calling loop
- [x] Modular project structure

## Tools & Actions
- [ ] Web search tool (Brave/Serper API)
- [ ] Run shell commands
- [ ] Read/write files
- [ ] Fetch and summarize a URL
- [ ] Get current time/weather

## Reliability
- [ ] Recursion/depth guard on tool calls
- [ ] Retry on API failure
- [ ] Graceful error reporting back to LLM (tool errors as tool results)
- [ ] Timeout on tool execution

## Memory
- [ ] Sliding window — summarize old context when too long
- [ ] Persist context across sessions (JSON file)
- [ ] Semantic memory — embed + retrieve relevant past messages

## Planning & Reasoning
- [ ] ReAct loop (Reason → Act → Observe → repeat)
- [ ] Chain-of-thought via system prompt
- [ ] Multi-step task decomposition
- [ ] Self-critique — agent reviews its own output before responding

## Multi-Agent
- [ ] Spawning subagents for subtasks
- [ ] Orchestrator / worker pattern
- [ ] Agents communicating via shared context or message passing

## Evals
- [ ] Build a small benchmark of tasks the agent should complete
- [ ] Score pass/fail per task
- [ ] Measure tool call accuracy and hallucination rate
- [ ] Regression testing when changing prompts or models