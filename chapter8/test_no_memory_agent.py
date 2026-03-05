from hello_agents import SimpleAgent, HelloAgentsLLM
from dotenv import load_dotenv

load_dotenv()

agent = SimpleAgent(
    name="test_no_memory_agent",
    llm=HelloAgentsLLM())

response = agent.run("我叫超仔，正在学习 agent 开发, 目前刚接触基本概念")
print(response)

response = agent.run("你还记得我的学习进度吗?")
print(response)


