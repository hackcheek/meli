#!/bin/bash


python run_hydrate_pipeline.py \
  --max-words 200 \
  --output-path ./datos/results_a.csv \
  --input-path ./datos/meli_a.json \
  --api-key $OPENAI_API_KEY

