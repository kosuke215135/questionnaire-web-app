#!/bin/bash

# Let's Encrypt SSL証明書セットアップスクリプト
set -e

# ドメイン名を設定（実際のドメインに変更してください）
DOMAIN="your-domain.com"
EMAIL="your-email@example.com"

echo "=== Let's Encrypt SSL証明書セットアップ開始 ==="

# Certbotのインストール
echo "Certbotをインストール中..."
sudo apt update
sudo apt install -y certbot python3-certbot-nginx

# Nginxの設定ファイルを更新
echo "Nginx設定ファイルを更新中..."
sudo cp nginx.conf /etc/nginx/sites-available/questionnaire
sudo ln -sf /etc/nginx/sites-available/questionnaire /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# ドメイン名を設定ファイルに反映
echo "ドメイン名を設定ファイルに反映中..."
sudo sed -i "s/your-domain.com/$DOMAIN/g" /etc/nginx/sites-available/questionnaire

# Nginxの設定をテスト
echo "Nginx設定をテスト中..."
sudo nginx -t

# Nginxを再起動
echo "Nginxを再起動中..."
sudo systemctl restart nginx

# SSL証明書の取得
echo "SSL証明書を取得中..."
sudo certbot --nginx -d $DOMAIN --email $EMAIL --agree-tos --non-interactive

# 自動更新の設定
echo "SSL証明書の自動更新を設定中..."
sudo crontab -l 2>/dev/null | { cat; echo "0 12 * * * /usr/bin/certbot renew --quiet"; } | sudo crontab -

echo "=== Let's Encrypt SSL証明書セットアップ完了 ==="
echo "ドメイン: $DOMAIN"
echo "メール: $EMAIL"
echo "証明書の自動更新が設定されました" 