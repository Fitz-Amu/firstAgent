from LLMClient import HelloAgentsLLM
from Memory import Memory

# 初始提示词：指导模型编写 Python 函数
INITIAL_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。请根据以下要求,编写一个Python函数。
你的代码必须包含完整的函数签名、文档字符串,并遵循PEP 8编码规范。
要求:{task}
请直接输出代码,不要包含任何额外的解释。
"""

# 反思提示词：代码评审，找出算法效率瓶颈
REFLECT_PROMPT_TEMPLATE = """
你是一位极其严格的代码评审专家和资深算法工程师,对代码的性能有极致的要求。
你的任务是审查以下Python代码,并专注于找出其在**算法效率**上的主要瓶颈。

#原始任务:
{task}

#待审查的代码:
```python
{code}
```

请分析该代码的时间复杂度,并思考是否存在一种**算法上更优**的解决方案来显著提升性能。
如果存在,请清晰地指出当前算法的不足,并提出具体的、可行的改进算法建议(例如,使用筛法替代试除法)。
如果代码在算法层面已经达到最优,才能回答"无需改进"。
请直接输出你的反馈,不要包含任何额外的解释。
"""

# 优化提示词：根据评审反馈优化代码
REFINE_PROMPT_TEMPLATE = """
你是一位资深的Python程序员。你正在根据一位代码评审专家的反馈来优化你的代码。

#原始任务:
{task}

#你上一轮尝试的代码:
{last_code_attempt}

评审员的反馈:
{feedback}

请根据评审员的反馈,生成一个优化后的新版本代码。
你的代码必须包含完整的函数签名、文档字符串,并遵循PEP 8编码规范。
请直接输出优化后的代码,不要包含任何额外的解释。
"""


class Reflection:
    def __init__(self, llm: HelloAgentsLLM, memory: Memory):
        self.llm = llm
        self.memory = memory
    
    def run(self, question: str, max_iterations: int = 3):
        print(f"\n--- 开始处理问题 --- \n问题: {question}")

        init_prompt = INITIAL_PROMPT_TEMPLATE.format(task=question)
        messages = [{"role": "user", "content": init_prompt}]
        code = self.llm.thinking(messages) or ""
        self.memory.add_record("execution", code)

        for i in range(max_iterations):
            print(f"\n--- 第 {i+1} 轮反思 --- \n 代码: {code}")

            reflect_prompt = REFLECT_PROMPT_TEMPLATE.format(task=question, code=code)
            messages = [{"role": "user", "content": reflect_prompt}]
            feedback = self.llm.thinking(messages) or ""
            self.memory.add_record("reflection", feedback)

            print(f"\n --- 评审员反思结果 --- \n", feedback)

            if("无需改进" in feedback):
                print(f"\n --- 无需改进，结束反思 --- \n 最终代码: {code}")
                return code

            print(f"\n --- 开始优化代码 --- \n")
            refine_prompt = REFINE_PROMPT_TEMPLATE.format(task=question, last_code_attempt=code, feedback=feedback)
            messages = [{"role": "user", "content": refine_prompt}]
            code = self.llm.thinking(messages) or ""
            self.memory.add_record("execution", code)

        print(f"\n --- 达到最大迭代次数，结束反思 --- \n 最终代码: {code}")



if __name__ == "__main__":
    llmClient = HelloAgentsLLM()
    memory = Memory()
    reflection = Reflection(llmClient, memory)
    question = "编写一个Python函数，找出 1 到 n 之间的所有素数(prime numbers)。"
    reflection.run(question)







