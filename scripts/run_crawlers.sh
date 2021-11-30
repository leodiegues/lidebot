#!/usr/bin/bash

mkdir -p data

cd lidebot

spiders_dir="crawler/spiders"

spiders=$(ls $spiders_dir | grep -v "^_" | grep -v "^\.DS_Store$")

for spider in $spiders; do
    echo "Running $spider"
    spider_file=$(basename $spider)
    spider_name=${spider_file%.*}
    python -m poetry run python -m scrapy runspider $spiders_dir/$spider -O "../data/latest_$spider_name.csv"
done

cd ..
