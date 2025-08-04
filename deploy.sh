#!/bin/bash

# デプロイスクリプト
set -e

echo "=== デプロイ開始 ==="

# 環境変数の読み込み
source .env

# 依存関係のインストール
echo "依存関係をインストール中..."
pip install -r requirements.txt

# 静的ファイルの収集
echo "静的ファイルを収集中..."
python manage.py collectstatic --noinput --settings=config.settings.production

# データベースマイグレーション
echo "データベースマイグレーションを実行中..."
python manage.py migrate --settings=config.settings.production

# ログディレクトリの作成
echo "ログディレクトリを作成中..."
sudo mkdir -p /var/log/django
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R $USER:$USER /var/log/django
sudo chown -R $USER:$USER /var/log/gunicorn
sudo chown -R $USER:$USER /var/run/gunicorn

# Gunicornの再起動
echo "Gunicornを再起動中..."
sudo systemctl restart gunicorn

# Nginxの再起動
echo "Nginxを再起動中..."
sudo systemctl restart nginx

echo "=== デプロイ完了 ===" 