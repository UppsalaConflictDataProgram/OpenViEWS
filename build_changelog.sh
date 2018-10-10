#!/bin/sh
echo "running pandoc -v CHANGELOG.md -o CHANGELOG.html"
pandoc CHANGELOG.md -o CHANGELOG.html
