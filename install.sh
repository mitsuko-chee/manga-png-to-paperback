#!/bin/bash
set -e

REPO_URL="https://raw.githubusercontent.com/mitsuko-chee/manga-png-to-paperback/main"
COMMANDS_DIR="$HOME/.claude/commands"
WORKSPACE_DIR="$HOME/my-workspace"

mkdir -p "$COMMANDS_DIR"
mkdir -p "$WORKSPACE_DIR"

curl -fsSL "$REPO_URL/commands/manga-png-to-paperback.md" -o "$COMMANDS_DIR/manga-png-to-paperback.md"
curl -fsSL "$REPO_URL/manga_pdf_maker.py" -o "$WORKSPACE_DIR/manga_pdf_maker.py"

echo "✓ スキルをインストールしました: $COMMANDS_DIR/manga-png-to-paperback.md"
echo "✓ スクリプトをインストールしました: $WORKSPACE_DIR/manga_pdf_maker.py"

echo "必要なライブラリをインストールしています..."
pip3 install Pillow reportlab -q
echo "✓ ライブラリのインストール完了"
echo "  Claude Code で /manga-png-to-paperback と入力して使えます。"
