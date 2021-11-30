#!/usr/bin/bash

echo "Publicando thread"

python -m poetry run python lidebot/main.py --option publish
