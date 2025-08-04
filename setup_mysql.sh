#!/bin/bash

# MySQLセットアップスクリプト
set -e

echo "=== MySQLセットアップ開始 ==="

# MySQLのインストール（Ubuntu/Debian）
echo "MySQLをインストール中..."
sudo apt update
sudo apt install -y mysql-server mysql-client

# MySQLサービスの開始
echo "MySQLサービスを開始中..."
sudo systemctl start mysql
sudo systemctl enable mysql

# MySQLの初期設定
echo "MySQLの初期設定を実行中..."
sudo mysql_secure_installation

# データベースとユーザーの作成
echo "データベースとユーザーを作成中..."
sudo mysql -u root -p << EOF
CREATE DATABASE IF NOT EXISTS questionnaire_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'questionnaire_user'@'localhost' IDENTIFIED BY 'your-database-password';
GRANT ALL PRIVILEGES ON questionnaire_db.* TO 'questionnaire_user'@'localhost';
FLUSH PRIVILEGES;
EOF

echo "=== MySQLセットアップ完了 ==="
echo "データベース名: questionnaire_db"
echo "ユーザー名: questionnaire_user"
echo "パスワード: your-database-password (env.exampleで設定した値に変更してください)" 