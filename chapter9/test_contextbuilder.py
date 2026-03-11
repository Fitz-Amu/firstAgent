from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from hello_agents.context import ContextBuilder, ContextConfig
from hello_agents.tools import RAGTool, MemoryTool
from hello_agents.core.message import Message
from datetime import datetime


#1. 初始化 tool
memory_tool = MemoryTool(user_id="user123")
rag_tool = RAGTool(knowledge_base_path="./knowledge_base")

#2. 创建 context builder
config = ContextConfig(
    max_tokens= 3000,
    reserve_ratio=0.2,
    min_relevance=0.2,
    enable_compression=True,
)

builder = ContextBuilder(
    memory_tool,
    rag_tool,
    config
)

# 3.准备对话历史
conversation_history = [
    Message(role="user", content="我正在开发一个数据分析工具", timestamp=datetime.now()),
    Message(role="assistant", content="好的,数据分析工具通常需要处理大量数据。你计划使用什么技术栈？", timestamp=datetime.now()),
    Message(role="user", content="我计划使用Python和Pandas,已经完成了读取 CSV 读取模块的开发", timestamp=datetime.now()),
    Message(role="assistant", content="不错的选择,Pandas 是处理结构化数据的好选择。接下来你要考虑数据清洗和转换？", timestamp=datetime.now()),
]

# 4. 添加一些记忆
memory_tool.execute(
    "add",
    content="用户正在开发一个数据分析工具,使用Python和Pandas",
    memory_type="semantic",
    importance=0.8
)

memory_tool.execute(
    "add",
    content="用户已经完成了读取 CSV 读取模块的开发",
    memory_type="semantic",
    importance=0.7
)

# 5. 构建上下文
context = builder.build(
    user_query="如何优化Pandas的内存占用？",
    conversation_history=conversation_history,
    system_instructions="你是一个数据分析助手，帮助用户完成数据分析任务。你的回答:1)提供具体可执行建议 2)解释技术和原理 3） 给出示例代码"
)

print ("=" * 80)
print ("构建上下文: ")
print ("=" * 80)
print (context)
print ("=" * 80)