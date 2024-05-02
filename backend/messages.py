from typing import Literal, Optional
from pydantic import BaseModel
from langchain_core.messages.base import BaseMessage
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage


class Message(BaseModel):
    content: str
    type: Literal["human"] | Literal["ai"] | Literal["system"]

    def as_lc_base_message(self):
        if type == "human":
            return HumanMessage(content=self.content)

        if type == "ai":
            return AIMessage(content=self.content)
        if type == "system":
            return SystemMessage(content=self.content)

