# Prueba Tecnica MeLi

## Correr las pipelines

### Setup

instalar dependencias
```bash
pip install -r requirements.txt
```

### Correr Pipeline que "scrapea" data de Mercado Libre

Para correr esta pipeline es necesario contar con un token de acceso de Mercado Libre. Obtenerlo en [https://auth.mercadolibre.com.ar/developers/apps](https://auth.mercadolibre.com.ar/developers/apps)
Parametros de entrada:
- `--access-token`: Token de acceso de Mercado Libre
- `--k`: Cantidad de resultados
- `--output-path`: Ruta donde se guardaran los resultados
- `--query`: Palabra clave de busqueda
```bash
python run_meli_pipeline.py \
    --access-token $MELI_ACCESS_TOKEN \
    --k 50 \
    --output-path ./datos/example.json \
    --query example
```

### Correr Pipeline que "hydrata" (mejora) las descripciones

Para correr esta pipeline es necesario contar con una api_key de OpenAI. Obtenerlo en [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
Parametros de entrada:
- `--max-words`: Cantidad maxima de palabras en la descripcion
- `--output-path`: Ruta donde se guardaran los resultados
- `--input-path`: Ruta del archivo de entrada
- `--api-key`: Api key de OpenAI
```bash
python run_hydrate_pipeline.py \
  --max-words 200 \
  --output-path ./datos/results_example.csv \
  --input-path ./datos/example.json \
  --api-key $OPENAI_API_KEY
```
