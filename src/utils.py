"""
Utilidades, entre ellas, para manejar el rate limit de la API de OpenAI
"""
import openai
import sys
import time
import asyncio
from functools import wraps
from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Callable, Any


class ImprovedDescription(BaseModel):
    reasoning: str | None
    description: str | None


def response2string(resp):
    return resp.choices[0].message.content


def parse_description(resp):
    bs = BeautifulSoup(resp)
    reasoning = bs.find('reasoning')
    if reasoning:
        reasoning = reasoning.text.strip()

    desc = bs.find('description')

    if not desc:
        return ImprovedDescription(reasoning=reasoning, description=resp)

    desc = desc.text.strip()

    return ImprovedDescription(reasoning=reasoning, description=desc)


def retry(retry_delay: int, exceptions=(Exception,)) -> Any:
    def deco(func: Callable):
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def awrapper(*args, **kwargs):
                while True:
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as err:
                        print(f"  [!] Error {err}, waiting {retry_delay} seconds before next request", file=sys.stderr)
                        await asyncio.sleep(retry_delay)
            return awrapper

        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    print(f"  [!] Error {err}, waiting {retry_delay} seconds before next request", file=sys.stderr)
                    time.sleep(retry_delay)
        return wrapper
    return deco


def address_openai_rate_limit(retry_delay: int) -> Any:
    return retry(retry_delay, exceptions=(openai.OpenAIError,))

