#!/bin/bash

# 手動nginx設定修正スクリプト
set -e

echo "=== 手動nginx設定修正 ==="

# 現在のEC2インスタンスのパブリックIPを取得
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "EC2パブリックIP: $PUBLIC_IP"

# プロジェクトパスを取得
PROJECT_DIR=$(pwd)
echo "プロジェクトパス: $PROJECT_DIR"

# HTTPのみの設定ファイルを作成
echo "HTTPのみのnginx設定を作成中..."
sudo tee /etc/nginx/sites-available/questionnaire > /dev/null << EOF
server {
    listen 80;
    server_name $PUBLIC_IP;

    # 静的ファイル
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # メディアファイル
    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Djangoアプリケーション
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }

    # ログ設定
    access_log /var/log/nginx/questionnaire_access.log;
    error_log /var/log/nginx/questionnaire_error.log;
}
EOF

# nginx設定をテスト
echo "nginx設定をテスト中..."
sudo nginx -t

# nginxを再起動
echo "nginxを再起動中..."
sudo systemctl restart nginx

echo "=== 手動nginx設定修正完了 ==="
echo "HTTPでアクセス可能になりました: http://$PUBLIC_IP" 