# AutoGen Multi-Agent Development: implementation guidance

## AgentChat versus older APIs

Modern packages autogen-agentchat, autogen-core, and autogen-ext have distinct
roles. Do not mix older ConversableAgent/GroupChat patterns with current
AssistantAgent, RoundRobinGroupChat, SelectorGroupChat, or Swarm examples. Teams
need termination conditions and budgets; a user proxy is not automatically a
code executor. Use supported CodeExecutorAgent or an explicit executor integration,
not an unsupported code_executor argument on AssistantAgent. Current Core event
patterns use documented message handlers and runtime subscriptions; do not import
an invented generic Event API.

## Execution, state, and reliability

Never expose Python eval as a calculator tool. Use validated typed operations or
a constrained parser. Container execution still requires reviewed mounts, network,
capabilities, secrets, resource limits, and user authority; Docker alone is not a
complete security boundary. Manage executor startup/shutdown and close model
clients. Use save_state/load_state for persistence; a run result's message list
is not the complete persistent team state. Retrying a whole conversation can
repeat tool side effects: classify failures and resume safely instead. Limit and
redact logs; evaluate task quality and tool behavior as well as process success.

## Primary documentation

- [AgentChat save_state/load_state](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html).
- [CodeExecutorAgent and executor lifecycle](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/code-execution.html).

Examples and APIs must be checked against the project’s installed versions.

---

Adapted from Mindrally/skills and modified by Andrew Cox (2026), under Apache-2.0. See [package notices](../../../NOTICE.md).
