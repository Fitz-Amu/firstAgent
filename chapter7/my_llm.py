from typing import Optional
from hello_agents import HelloAgentsLLM

class MyLLM(HelloAgentsLLM):
    def __init__(
        self,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        provider: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(model=model, base_url=base_url, api_key=api_key, timeout=timeout, provider=provider, **kwargs)
