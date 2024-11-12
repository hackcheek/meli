#!/bin/bash

python run_meli_pipeline.py \
    --access-token $MELI_ACCESS_TOKEN \
    --k 50 \
    --output-path ./datos/meli_a.json \
    --query ab
