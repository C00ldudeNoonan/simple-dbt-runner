#!/bin/bash
set -e

git fetch

# try to get the manifest from the gh-pages branch
git checkout origin/gh-pages manifest.json

# create the target directory if it doesn't exist
if [ ! -d "project_goes_here/target" ]; then
  mkdir project_goes_here/target
fi

# copy the manifest.json to the target directory
cp manifest.json project_goes_here/target/manifest.json
