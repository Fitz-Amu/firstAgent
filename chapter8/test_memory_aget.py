from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
from hello_agents.tools import MemoryTool, RAGTool
from dotenv import load_dotenv

load_dotenv()

llm = HelloAgentsLLM()

agent = SimpleAgent(
    name="test_memory_agent",
    llm=llm,
    system_prompt="你是一个记忆助手。",
)

tool_registry = ToolRegistry()

memory_tool = MemoryTool(user_id="123")
tool_registry.register_tool(memory_tool)

rag_tool = RAGTool(knowledge_base_name="./knowledge_base")
tool_registry.register_tool(rag_tool)

agent.tool_registry = tool_registry

response = agent.run("我叫超仔，正在学习 agent 开发, 目前刚接触基本概念")
print(response)