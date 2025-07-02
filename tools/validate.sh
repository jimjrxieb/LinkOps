#!/bin/bash

echo "🔍 Running black..."
black . || echo "⚠️ Black format issues found."

echo "🔍 Running flake8..."
flake8 . || echo "⚠️ Flake8 lint issues found."

echo "🔍 Running yamllint..."
yamllint . || echo "⚠️ YAML lint issues found."

echo "✅ Validation complete."

