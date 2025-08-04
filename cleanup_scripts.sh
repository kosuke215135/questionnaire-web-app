#!/bin/bash

# 不要なセットアップファイルを削除するスクリプト
echo "=== 不要なセットアップファイルの削除 ==="

# 個別セットアップファイルを削除（setup_ec2.shが全て含んでいるため）
echo "個別セットアップファイルを削除中..."
rm -f setup_mysql.sh
rm -f setup_gunicorn.sh

echo "削除完了:"
echo "- setup_mysql.sh (setup_ec2.shに統合済み)"
echo "- setup_gunicorn.sh (setup_ec2.shに統合済み)"

echo ""
echo "残るファイル:"
echo "- setup_ec2.sh (AWS EC2用 - 推奨)"
echo "- setup_ssl.sh (SSL証明書用 - ドメインがある場合のみ)"
echo "- deploy.sh (アプリケーションデプロイ用)"
echo ""
echo "使用方法:"
echo "1. AWS EC2: ./setup_ec2.sh"
echo "2. ローカルサーバー: ./deploy.sh"
echo "3. SSL証明書: ./setup_ssl.sh (ドメインがある場合)" 