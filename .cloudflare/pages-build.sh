#!/bin/sh
set -eu

rm -rf _site
mkdir -p _site/works _site/press _site/tally _site/carve

cp index.html 404.html site.css site.js apps.css 404.css favicon.svg og-raito.png robots.txt sitemap.xml llms.txt .nojekyll _site/
cp -R assets _site/
cp works/index.html works/works.css works/works.js _site/works/
cp press/index.html press/press.css _site/press/
cp tally/index.html _site/tally/
cp carve/index.html _site/carve/
