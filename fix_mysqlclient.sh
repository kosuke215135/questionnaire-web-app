#!/bin/bash

# mysqlclientインストールエラー修正スクリプト
set -e

echo "=== mysqlclientインストールエラー修正 ==="

# 必要な開発ライブラリをインストール
echo "MySQL開発ライブラリをインストール中..."
sudo apt update
sudo apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

# 仮想環境をアクティベート（存在する場合）
if [ -d "venv" ]; then
    echo "仮想環境をアクティベート中..."
    source venv/bin/activate
fi

# mysqlclientを再インストール
echo "mysqlclientを再インストール中..."
pip uninstall mysqlclient -y || true
pip install mysqlclient

echo "=== mysqlclientインストールエラー修正完了 ==="
echo "これで requirements.txt のインストールが可能になります" 