from typing import Any, List, Dict


class Memory:
    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, record_content: str):
        record = {"type": record_type, "content": record_content}
        self.records.append(record)
        print(f"记忆已更新，新增一条: {record}")

    def get_trajectory(self) -> str:
        trajectory_parts = []
        for record in self.records:
            if(record["type"] == "execution"):
                trajectory_parts.append(f"--- 上一轮尝试 ---\n {record['content']}")
            elif(record["type"] == "reflection"):
                trajectory_parts.append(f"--- 评审员反馈 ---\n {record['content']}")
        return "\n\n".join(trajectory_parts)
    
    def get_last_execution(self) -> str:
        for record in reversed(self.records):
            if(record["type"] == "execution"):
                return record["content"]
        return None
                