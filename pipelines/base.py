"""
Clase base para las pipelines
Esta clase permite crear una cli para las pipelines de forma sencilla
"""
import argparse
from abc import ABC, abstractmethod
from pydantic import BaseModel


class Pipeline(ABC, BaseModel):

    @abstractmethod
    async def run(self):...

    @classmethod
    async def cli(cls):
        props = cls.model_json_schema()['properties']
        parser = argparse.ArgumentParser()
        for p, v in props.items():
            if v['type'] == 'boolean':
                parser.add_argument(f"--{p.replace('_', '-')}", action='store_true')
                continue
            parser.add_argument(f"--{p.replace('_', '-')}")
        args = parser.parse_args()
        pipeline = cls(**{p: getattr(args, p) for p in props})
        await pipeline.run()
