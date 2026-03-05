from pathlib import Path
from dotenv import load_dotenv

# 必须在 import hello_agents 之前加载项目根目录的 .env，否则记忆会连到本地 Qdrant
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
from hello_agents.tools import MemoryTool, RAGTool

llm = HelloAgentsLLM()

agent = SimpleAgent(
    name="test_memory_agent",
    llm=llm,
    system_prompt="你是一个记忆助手。",
)

tool_registry = ToolRegistry()

print("注册记忆工具")
memory_tool = MemoryTool(user_id="user123")
tool_registry.register_tool(memory_tool)

print("注册 RAG 工具")
rag_tool = RAGTool(knowledge_base_path="./knowledge_base")
tool_registry.register_tool(rag_tool)

agent.tool_registry = tool_registry

response = agent.run("我叫超仔，正在学习 agent 开发, 目前刚接触基本概念")
print(response)