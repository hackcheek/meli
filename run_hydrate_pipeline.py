"""
Ejecución de la pipeline de hidratación
"""
import asyncio
from pipelines.hydrate.main import HydratePipeline


if __name__ == "__main__":
    asyncio.run(HydratePipeline.cli())
