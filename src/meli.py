"""
Este módulo contiene la clase MeliClient, que permite realizar solicitudes a la API de Mercadolibre.
"""

import aiohttp
import base64
from env import env_settings
from src.cache import Cache


class MeliClient:
    def __init__(
        self,
        access_token: str | None = None,
        site_id: str = 'MLA',
        use_cache: bool = False
    ):
        if access_token is None:
            access_token = env_settings().meli_access_token

        self.site_id = site_id
        self.headers = {'authorization': f'Bearer {access_token}'}
        self.api_domain = "https://api.mercadolibre.com"
        self.cache_dir = './datos/_meli_cache'
        self.use_cache = use_cache

    async def get(self, url: str):
        id = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        cache = Cache(id=id, directory=self.cache_dir)

        if self.use_cache and cache.exists():
            return cache.load()

        async with aiohttp.ClientSession(headers=self.headers) as sess:
            async with sess.get(url) as response:
                items = await response.json()
                cache.save(items)
                return items

    async def search_items(self, query):
        url = f"{self.api_domain}/sites/MLA/search?q={query}"
        return (await self.get(url))['results']

    async def get_description(self, item_id):
        url = f"{self.api_domain}/items/{item_id}/description"
        desc = await self.get(url)
        return (desc['text'] + '\n' + desc['plain_text']).strip()

    async def get_attributes(self, item_id):
        url = f"{self.api_domain}/items?ids={item_id}"
        item = await self.get(url)
        return {
            attr['name']: attr['value_name']
            for attr in item[0]['body']['attributes']
        }

    async def get_images(self, item_id):
        url = f"{self.api_domain}/items?ids={item_id}"
        item = await self.get(url)
        return [i['secure_url'] for i in item[0]['body']['pictures']]

    async def get_category_path(self, category_id):
        url = f"{self.api_domain}/categories/{category_id}"
        item = await self.get(url)
        return ' > '.join([i['name'] for i in item['path_from_root']])
