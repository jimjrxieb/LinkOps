#!/bin/bash

echo "🔁 Validating all Helm charts and YAML..."

for chart in ./helm/*/; do
  svc=$(basename "$chart")
  echo "🔧 [$svc] Helm Lint:"
  helm lint "$chart" || echo "❌ Helm lint failed for $svc"

  if [ -f "$chart/values.yaml" ]; then
    echo "🎨 [$svc] Formatting values.yaml with Prettier..."
    npx prettier --write "$chart/values.yaml"
  else
    echo "⚠️ [$svc] Skipping Prettier — values.yaml missing"
  fi

  echo "🛡️ [$svc] Yamllint on rendered template:"
  helm template "$chart" | yamllint - || echo "❌ Yamllint failed for $svc"

  echo "✅ [$svc] Done."
  echo "---------------------------"
done
