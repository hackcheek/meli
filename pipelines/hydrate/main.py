"""
Esta pipeline sirve para "hidratar" o mejorar descripciones de mercado libre anteriormente 
extraidas por la pipeline pipeliens/meli/main.py:SaveShorterDescriptionsPipeline
Los resultados se guardan de forma estructurada donde el usuario quiera (--output-path)
"""
import pandas as pd
import ast
import asyncio
from pipelines.base import Pipeline
from src.oai import LLM, ModelEnum
from src.prompts.improve_description import ImproveDescriptionPrompt
from src.prompts.reduce_description import ReduceDescriptionPrompt
from src.utils import response2string, parse_description
from tqdm import tqdm


class HydratePipeline(Pipeline):
    max_words: int
    output_path: str
    input_path: str
    api_key: str

    def load_data(self):
        return pd.read_json(self.input_path)

    async def _task(self, j, bar):
        llm = LLM(model=ModelEnum.GPT4O_MINI, api_key=self.api_key)
        llm.add_postprocess(response2string)

        result = {
            'id': j['id'],
            'title': j['title'],
            'description': j['description'],
            'category': j['category'],
            'hydrated_description': '',
        }
        
        if not isinstance(j['description'], str) or not j['description']:
            return result

        if isinstance(j['attributes'], str):
            j['attributes'] = ast.literal_eval(j['attributes'])

        prompt = ImproveDescriptionPrompt(
            title=j['title'],
            description=j['description'],
            attributes=j['attributes'],
            category=j['category'],
            images=j['images']
        )
        llm.add_postprocess(parse_description)
        resp = await llm.call(prompt)

        prompt = ReduceDescriptionPrompt(
            description=resp.description,
            n=self.max_words
        )

        llm.pop_postprocess()

        resp = await llm.call(prompt)

        result['hydrated_description'] = resp
        bar.update(1)
        return result

    async def run(self):
        data = self.load_data()

        bar = tqdm(total=len(data))
        tasks = [self._task(j, bar) for _, j in data.iterrows()]
        results = await asyncio.gather(*tasks)

        bar.close()

        df = pd.DataFrame(results)
        df.to_csv(self.output_path, index=False)
