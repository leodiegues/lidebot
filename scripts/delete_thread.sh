#!/usr/bin/bash

echo "Deletando última thread"

python -m poetry run python lidebot/main.py --option delete
