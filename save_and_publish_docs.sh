#!/bin/bash

# create the docs directory if it doesn't exist
if [ ! -d "docs" ]; then
  mkdir docs
fi

# copy the manifest.json, catalog.json, and index.html files to the docs directory
cp project_goes_here/target/manifest.json docs/manifest.json
cp project_goes_here/target/catalog.json docs/catalog.json
cp project_goes_here/target/index.html docs/index.html

# publish the docs directory to GitHub Pages using ghp-import
ghp-import -n -p -f docs/