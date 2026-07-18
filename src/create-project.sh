#!/bin/bash

show_help() {
  echo ""
  echo "Project Creator Workflow"
  echo "========================"
  echo ""
  echo "This script will:"
  echo ""
  echo "1. Copy atom-starter template"
  echo "   - ignores .git"
  echo "   - ignores dist"
  echo "   - ignores node_modules"
  echo ""
  echo "2. Rename project:"
  echo "   - package.json name"
  echo "   - vite pages path"
  echo "   - publish paths"
  echo ""
  echo "3. Rename project title:"
  echo "   - index.html title"
  echo "   - docs/_config.yml title"
  echo ""
  echo "4. Install dependencies:"
  echo "   pnpm install"
  echo ""
  echo "5. Initialize Git:"
  echo "   git init"
  echo "   git add ."
  echo "   git commit -m \"chore: initialize project with template\""
  echo ""
  echo "6. Create GitHub repository:"
  echo "   - creates public repo"
  echo "   - adds origin remote"
  echo "   - pushes main branch"
  echo ""
  echo "7. Enable GitHub Pages:"
  echo "   - source: main branch"
  echo "   - folder: /docs"
  echo ""
  echo "8. Open project:"
  echo "   - VS Code"
  echo "   - pnpm dev"
  echo "   - browser localhost page"
  echo ""
  echo "Required tools:"
  echo "  git"
  echo "  pnpm"
  echo "  gh (GitHub CLI)"
  echo "  code (VS Code CLI)"
  echo ""
  echo "GitHub CLI installation:"
  echo ""
  echo "Ubuntu:"
  echo "  sudo apt update"
  echo "  sudo apt install gh"
  echo ""
  echo "Login:"
  echo "  gh auth login"
  echo ""
  echo "Then run this script again."
  echo ""
}

if [[ "$1" == "--help" || "$1" == "-h" ]]; then
  show_help
  exit 0
fi


check_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing dependency: $1"
    echo "Run: $0 --help"
    exit 1
  fi
}


check_command git
check_command pnpm


if ! command -v gh >/dev/null 2>&1; then
  echo ""
  echo "GitHub CLI is not installed."
  echo ""
  echo "Install it:"
  echo ""
  echo "sudo apt update"
  echo "sudo apt install gh"
  echo ""
  echo "Then authenticate:"
  echo ""
  echo "gh auth login"
  echo ""
  exit 1
fi


read -p "Project name (e.g. pong-game): " name
read -p "Project title (e.g. Pong Game): " title


SOURCE="/home/atari-monk/atari-monk/project/atom-starter"
DEST="/home/atari-monk/atari-monk/project/$name"


if [ -d "$DEST" ]; then
  echo "Project already exists: $DEST"
  exit 1
fi


echo "Copying template..."

rsync -a \
  --exclude='.git' \
  --exclude='dist' \
  --exclude='node_modules' \
  "$SOURCE/" \
  "$DEST/"


echo "Updating package.json..."
sed -i "s/atom-starter/$name/g" "$DEST/package.json"


echo "Updating index.html..."
sed -i "s/Atom Starter/$title/g" "$DEST/index.html"


echo "Updating vite.config.js..."
sed -i "s#pages/atom-starter#pages/$name#g" "$DEST/vite.config.js"


echo "Updating docs config..."
sed -i "s/title: Atom Starter/title: $title/g" "$DEST/docs/_config.yml"


cd "$DEST" || exit


echo "Installing dependencies..."
pnpm install


echo "Initializing git..."
git init
git branch -M main
git add .
git commit -m "chore: initialize project with template"


echo "Creating GitHub repository..."
gh repo create "$name" \
  --public \
  --source=. \
  --remote=origin \
  --push


echo "Enabling GitHub Pages..."

USER=$(gh api user -q .login)

gh api \
  --method POST \
  "repos/$USER/$name/pages" \
  -f build_type=legacy \
  -f source='{"branch":"main","path":"/docs"}'


echo "Opening VS Code..."
code .


echo "Starting development server..."
pnpm dev &


sleep 3


echo "Opening browser..."
xdg-open "http://localhost:5173/pages/$name/"


echo ""
echo "================================"
echo "Project created successfully!"
echo "Location:"
echo "$DEST"
echo "================================"
