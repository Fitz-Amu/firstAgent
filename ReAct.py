from LLMClient import HelloAgentsLLM
from tools import ToolExecutor, search
import re

# ReAct prompt 模板
REACT_PROMPT_TEMPLATE = """
    请注意，你是一个有能力调用外部工具的智能助手。
    可用工具如下:
    {tools}
    请严格按照以下格式进行回应:
    Thought: 你的思考过程，用于分析问题、拆解任务和规划下一步行动。
    Action: 你决定采取的行动，必须是以下格式之一:
    - `{{tool_name}}[{{tool_input}}]`:调用一个可用工具。
    - `Finish[最终答案]`:当你认为已经获得最终答案时。
    - 当你收集到足够的信息，能够回答用户的最终问题时，你必须在Action:字段后使用 finish(answer="...") 来
    输出最终答案。
    现在，请开始解决以下问题:
    Question: {question}
    History: {history}
"""

class ReActAgent:
    def __init__(self, llm: HelloAgentsLLM, tool_executor: ToolExecutor, max_steps: int = 5):
        self.llm = llm
        self.tool_executor = tool_executor
        self.max_steps = max_steps
        self.history = []

    def run(self, question: str):
        self.history = []
        current_step = 0

        while current_step < self.max_steps:
            print(f"Step {current_step+1}:")

            tools_dec = self.tool_executor.get_available_tools()
            history_str = "\n".join(self.history)
            prompt = REACT_PROMPT_TEMPLATE.format(
                tools=tools_dec,
                question=question,
                history=history_str
            )

            # call llm 
            messages = [
                {"role": "user", "content": prompt},
            ]
            response = self.llm.thinking(messages)

            if not response:
                print(f"错误: LLM 思考失败")
                break

            # parse response
            thought, action = self._parse_output(response)
            if thought:
                print(f"Thought: {thought}")

            if not action:
                print(f"错误: 无法解析 Action")
                break

            if action.startswith("Finish"):
                final_answer = re.match(r"Finish\[(.*)\]", action).group(1).strip()
                print(f"最终答案: {final_answer}")
                return final_answer

            tool_name, tool_input = self._parse_action(action)
            if not tool_name or not tool_input:
                continue

            print(f"Action: {tool_name} 输入参数: {tool_input}")
            tool_function = self.tool_executor.get_tool(tool_name)
            if not tool_function:
                observation = f"工具 {tool_name} 未找到"
            else:
                observation = tool_function(tool_input)

            print(f"Observation: {observation}")
            self.history.append(f"Action: {action}")
            self.history.append(f"Observation: {observation}")
            current_step += 1


        print(f"错误: 达到最大步骤限制，无法获得最终答案")
        return None


    def _parse_output(self, response: str):
        """解析 LLM 响应的输出，返回 Thought 和 Action """
        thought_match = re.search(r"Thought:\s*(.*)", response)
        action_match = re.search(r"Action:\s*(.*)", response)
        thought = thought_match.group(1).strip() if thought_match else None
        action = action_match.group(1).strip() if action_match else None
        return thought, action

    def _parse_action(self, action_text: str):
        """解析 Action 文本，返回 Tool 名称和输入参数"""
        match = re.match(r"(\w+)\[(.*)\]", action_text)
        if match:
            return match.group(1), match.group(2)
        else:
            return None, None

    

if __name__ == "__main__":
    llmClient = HelloAgentsLLM()
    toolExecutor = ToolExecutor()
    search_desc = "一个网页搜索引擎。当你需要回答关于时事、事实以及在你的知识库中找不到的信息时，应使用此工具。"
    toolExecutor.register_tool("search", search_desc, search)
    agent = ReActAgent(llmClient, toolExecutor)
    question = "华为最新的手机是哪一款？它的主要卖点是什么？"
    agent.run(question)


