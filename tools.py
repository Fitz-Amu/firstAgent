import os
from serpapi import GoogleSearch
from typing import Dict, Any

def search(query: str) -> str:
    """
    使用serpapi进行搜索
    """

    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise ValueError("SERPAPI_API_KEY is not set")

        params = {
            "engine": "google",
            "q": query,
            "api_key": api_key,
            "gl": "cn",
            "hl": "zh-CN",
        }
        
        client = GoogleSearch(params)
        results = client.get_dict()

        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            snippets = [
                f"{i+1} {res.get('title', '')} \n{res.get('snippet','')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)

        return "No search results found"
    except Exception as e:
        print(f"搜索失败: {e}")
        return None


class ToolExecutor:
    """
    工具执行器
    """
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, description: str, func: callable):
        """
        注册工具
        """

        if name in self.tools:
            print(f"Tool {name} already registered")
        self.tools[name] = {
            "description": description,
            "func": func
        }
        print(f"Tool {name} registered successfully")

    def get_tool(self, name: str) -> callable:
        """
        获取工具
        """
        if name not in self.tools:
            raise ValueError(f"Tool {name} not found")
        return self.tools[name]["func"]

    def get_available_tools(self) -> str:
        """
        获取可用的工具
        """
        return "\n".join([f" - {name}: {tool['description']}" for name, tool in self.tools.items()])

