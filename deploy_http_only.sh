#!/bin/bash

# HTTPのみのデプロイスクリプト
set -e

echo "=== HTTPのみのデプロイ開始 ==="

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

# nginx設定を修正
echo "nginx設定を修正中..."
./fix_nginx.sh

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

echo "=== HTTPのみのデプロイ完了 ==="
echo ""
echo "アクセスURL: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo ""
echo "後でSSL証明書を追加する場合:"
echo "1. ドメイン名を取得"
echo "2. ./setup_ssl.sh を実行" 