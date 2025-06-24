#!/bin/bash

# Usage: ./git_push.sh "your commit message"

# Default commit message
MESSAGE=${1:-"update"}

echo "🔄 Adding all changes..."
git add .

echo "📝 Committing with message: $MESSAGE"
git commit -m "$MESSAGE"

echo "🚀 Pushing to origin main..."
git push origin main
#!/bin/bash

# Usage: ./git_push.sh "your commit message"

# Default commit message
MESSAGE=${1:-"update"}

echo "🔄 Adding all changes..."
git add .

echo "📝 Committing with message: $MESSAGE"
git commit -m "$MESSAGE"

echo "🚀 Pushing to origin main..."
git push origin main
#!/bin/bash

# Usage: ./git_push.sh "your commit message"

# Default commit message
MESSAGE=${1:-"update"}

echo "🔄 Adding all changes..."
git add .

echo "📝 Committing with message: $MESSAGE"
git commit -m "$MESSAGE"

echo "🚀 Pushing to origin main..."
git push origin main

