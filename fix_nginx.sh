#!/bin/bash

# nginx設定修正スクリプト
set -e

echo "=== nginx設定修正 ==="

# 現在のEC2インスタンスのパブリックIPを取得
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "EC2パブリックIP: $PUBLIC_IP"

# HTTPのみの設定ファイルを使用
echo "HTTPのみのnginx設定を適用中..."
sudo cp nginx_http.conf /etc/nginx/sites-available/questionnaire

# パブリックIPを設定ファイルに反映
echo "パブリックIPを設定ファイルに反映中..."
sudo sed -i "s/your-ec2-public-ip/$PUBLIC_IP/g" /etc/nginx/sites-available/questionnaire

# プロジェクトパスを設定ファイルに反映
PROJECT_DIR=$(pwd)
echo "プロジェクトパス: $PROJECT_DIR"
echo "プロジェクトパスを設定ファイルに反映中..."
sudo sed -i "s|/home/ubuntu/questionnaire-web-app|$PROJECT_DIR|g" /etc/nginx/sites-available/questionnaire

# nginx設定をテスト
echo "nginx設定をテスト中..."
sudo nginx -t

# nginxを再起動
echo "nginxを再起動中..."
sudo systemctl restart nginx

echo "=== nginx設定修正完了 ==="
echo "HTTPでアクセス可能になりました: http://$PUBLIC_IP" 