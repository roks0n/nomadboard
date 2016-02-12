#!/bin/sh
cd "${BASH_SOURCE%/*}" || exit  # cd into the bundle and use relative paths
spider_slug="$1"
DJANGO_CMD="run_spider --scraper_slug $spider_slug" make django
