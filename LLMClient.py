
import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict


load_dotenv()

class HelloAgentsLLM:
    def __init__(self, model: str = None, base_url: str = None, api_key: str = None, timeout: int = None):
        self.model = model or os.getenv("LLM_MODEL_ID")
        self.base_url = base_url or os.getenv("LLM_BASE_URL")
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.timeout = timeout or int(os.getenv("LLM_TIMEOUT", 30))

        if not all([self.model, self.base_url, self.api_key]):
            raise ValueError("LLM_MODEL_ID, LLM_BASE_URL, and LLM_API_KEY must be set")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout
        )

    def thinking(self, messages: List[Dict[str, str]], temperature: float = 0.0) -> str:
        print(f"正在调用 {self.model} 进行思考...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True
            )

            # print("llm 响应成功")
            collected_content = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                # print(content, end="", flush=True)
                collected_content.append(content)
            # print()
            return "".join(collected_content)


        except Exception as e:
            print(f"调用 {self.model} 接口失败: {e}")
            return None



if __name__ == "__main__":
    try:
        llmClient = HelloAgentsLLM()
        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes python code."},
            {"role": "user", "content": "写一个Python代码，实现一个简单的Hello World程序。"}
        ]
        print("calling llm...")
        response = llmClient.thinking(exampleMessages)
        if response:
            print("\n\n完整模型输出")
            print(response)
    except Exception as e:

        print(f"程序运行失败: {e}")


