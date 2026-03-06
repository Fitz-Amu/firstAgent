from multiprocessing import context
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from hello_agents.tools import MemoryTool
from hello_agents import HelloAgentsLLM, SimpleAgent
from hello_agents import ToolRegistry

# agent
llm = HelloAgentsLLM()
agent = SimpleAgent(
    name="test_memory_agent",
    llm=llm,
    system_prompt="你是一个记忆助手。",
)

# 注册记忆工具
memory_tool = MemoryTool(user_id="user123")
tool_registry = ToolRegistry()
tool_registry.register_tool(memory_tool)
agent.tool_registry = tool_registry

print(f"添加多个记忆")


# 第1个
result1 = memory_tool.execute("add", content="用户张三是一名Python开发人员，专注于机器学习与数据分析", memory_type="semantic", importance=0.8)
print(f"第1个记忆: {result1}")

# 第2个
result2 = memory_tool.execute("add", content="用户李四是一名前端开发人员，擅长 React 与 Vue 开发", memory_type="semantic", importance=0.7)
print(f"第2个记忆: {result2}")

# 第3个
result3 = memory_tool.execute("add", content="用户王五是一名产品经理，擅长需求分析与项目管理", memory_type="semantic", importance=0.6)
print(f"第3个记忆: {result3}")

print(f"\n搜索特定记忆")
print(f"搜索 '前端工程师':")
results = memory_tool.execute("search", query="前端工程师")
print(f"搜索结果: {results}")

print(f"\n记忆摘要:")
summary = memory_tool.execute("summary")
print(f"记忆摘要: {summary}")
