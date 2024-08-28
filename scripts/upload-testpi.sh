#!/usr/bin/env sh
# Run from project dir
echo "build dist..."
./scripts/create-dist.sh
twine upload --repository testpypi dist/*
