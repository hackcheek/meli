"""
Esta pipeline guarda en un csv todos los items basados en la busqueda de mercadolibre.
Guardando id, titulo, descripcion, imagenes, atributos y categoria
"""

import pandas as pd
from src.meli import MeliClient
from pipelines.base import Pipeline
from tqdm import tqdm


class SaveShorterDescriptionsPipeline(Pipeline):
    access_token: str
    output_path: str
    query: str
    use_cache: bool = False
    k: int = 5

    async def run(self):
        client = MeliClient(
            access_token=self.access_token,
            use_cache=self.use_cache,
        )
        k = int(self.k)
        data = []
        print(f"[MELI] Buscando items; query={self.query}")
        items = await client.search_items(self.query)
        for i in tqdm(items):
            item = {}
            item['id'] = i['id']
            item['title'] = i['title']
            item['description'] = await client.get_description(i['id'])
            item['images'] = await client.get_images(i['id'])
            item['attributes'] = await client.get_attributes(i['id'])
            item['category'] = await client.get_category_path(i['category_id'])
            data.append(item)

        data = sorted(data, key=lambda x: len(x['description'].split()), reverse=False)
        data = data[:k]

        print(f"[MELI] Guardando data en {self.output_path}")
        df = pd.DataFrame(data)
        df.to_json(self.output_path, index=False)
