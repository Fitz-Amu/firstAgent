import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict


load_dotenv()

class HelloAgentsLOM:
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

            print("llm 响应成功")
            collected_content = []

        except Exception as e:
            print(f"调用 {self.model} 接口失败: {e}")
            return None



