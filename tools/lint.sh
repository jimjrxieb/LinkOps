#!/bin/bash
for file in $(find backend -name "*.py"); do
  echo "Fixing $file"
  autopep8 --in-place --max-line-length=79 --aggressive --aggressive "$file"
done
