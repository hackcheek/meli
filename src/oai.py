"""
Este módulo contiene la clase Prompt, que permite construir prompts para la API de OpenAI.
Y la clase LLM, que permite realizar llamadas a la API de OpenAI especificando el modelo.
"""

from openai import AsyncOpenAI
from enum import Enum
from typing import Callable
from pydantic import BaseModel
from src.utils import address_openai_rate_limit
from env import env_settings


class ModelEnum(Enum):
    GPT4O = 'gpt-4o'
    GPT4O_MINI = 'gpt-4o-mini'


class Prompt(BaseModel):
    system: str
    instruction: str
    images: list[str] = []

    @property
    def messages(self):
        messages = []
        user = []
        if self.system:
            messages.append({'role': 'system', 'content': self.system})

        if self.instruction:
            user.append({'type': 'text', 'text': self.instruction})
            
        if self.images:
            for i in self.images:
                user.append({'type': 'image_url', 'image_url': {'url': i}})

        user = {'role': 'user', 'content': user}
        if user:
            messages.append(user)
        return messages


class LLM(BaseModel):
    model: ModelEnum
    api_key: str | None = None

    def model_post_init(self, __context):
        if self.api_key is None:
            self.api_key = env_settings().openai_api_key
        self._client = AsyncOpenAI(api_key=self.api_key)
        self._postprocess = []

    @property
    def client(self):
        return self._client

    @property
    def postprocess(self):
        return self._postprocess

    @address_openai_rate_limit(10)
    async def call(self, prompt: Prompt, temperature: float = 0.0):
        resp = await self.client.chat.completions.create(
            model=self.model.value,
            messages=prompt.messages,
            temperature=temperature,
        )
        if self.postprocess:
            for process in self.postprocess:
                if isinstance(process, Callable):
                    resp = process(resp)
        return resp

    def add_postprocess(self, func: Callable):
        self._postprocess.append(func)
    
    def pop_postprocess(self):
        return self._postprocess.pop()

