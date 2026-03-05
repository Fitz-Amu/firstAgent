from typing import Optional
from my_llm import MyLLM
from hello_agents import SimpleAgent, Config
class MySimpleAgent(SimpleAgent):
    def __init__(
        self, 
        name: str, 
        llm: MyLLM, 
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None,
    ):
        super().__init__(name, llm, system_prompt, config)

    def run(self, input_text: str, max_tool_iterations: int = 3, **kwargs) -> str:
        """执行Agent的推理过程"""
        print(f"MySimpleAgent {self.name} 正在处理: {input_text}")
