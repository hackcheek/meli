"""
Ejecución de la pipeline de "scrapeo" de mercado libre
"""
import asyncio
from pipelines.meli.main import SaveShorterDescriptionsPipeline


if __name__ == "__main__":
    asyncio.run(SaveShorterDescriptionsPipeline.cli())
