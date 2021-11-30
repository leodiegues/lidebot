#!/usr/bin/bash

LIDEBOT_VERSION=0.1.0

docker build -t lidebot:$LIDEBOT_VERSION .

docker run -it --rm \
    -v lidebot:/app/lidebot \
    -v data:/app/data \
    lidebot:$LIDEBOT_VERSION \
    ./scripts/run_crawlers && ./scripts/publish_thread.sh
