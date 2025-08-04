#!/bin/bash

# AWS EC2 Ubuntuインスタンス用セットアップスクリプト
set -e

echo "=== AWS EC2 Ubuntuインスタンスセットアップ開始 ==="

# システムの更新
echo "システムを更新中..."
sudo apt update && sudo apt upgrade -y

# 必要なパッケージのインストール
echo "必要なパッケージをインストール中..."
sudo apt install -y python3 python3-pip python3-venv nginx mysql-server mysql-client git curl

# Python仮想環境の作成
echo "Python仮想環境を作成中..."
python3 -m venv venv
source venv/bin/activate

# プロジェクトディレクトリの設定
PROJECT_DIR=$(pwd)
echo "プロジェクトディレクトリ: $PROJECT_DIR"

# 依存関係のインストール
echo "依存関係をインストール中..."
pip install -r requirements.txt

# MySQLのセットアップ
echo "MySQLをセットアップ中..."
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

# 環境変数ファイルの作成
echo "環境変数ファイルを作成中..."
cp env.example .env

# ログディレクトリの作成
echo "ログディレクトリを作成中..."
mkdir -p logs
mkdir -p media
mkdir -p staticfiles

# 権限の設定
echo "権限を設定中..."
sudo chown -R $USER:$USER logs media staticfiles

# Nginx設定の更新
echo "Nginx設定を更新中..."
sudo cp nginx.conf /etc/nginx/sites-available/questionnaire
sudo ln -sf /etc/nginx/sites-available/questionnaire /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# プロジェクトパスを設定ファイルに反映
echo "プロジェクトパスを設定ファイルに反映中..."
sudo sed -i "s|/path/to/your/project|$PROJECT_DIR|g" /etc/nginx/sites-available/questionnaire

# Gunicorn設定の更新
echo "Gunicorn設定を更新中..."
sed -i "s|/path/to/your/project|$PROJECT_DIR|g" gunicorn.conf.py

# systemdサービスファイルの作成
echo "Gunicorn systemdサービスファイルを作成中..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << EOF
[Unit]
Description=Gunicorn daemon for Django application
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --config $PROJECT_DIR/gunicorn.conf.py config.wsgi:application
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

# サービスを有効化
echo "Gunicornサービスを有効化中..."
sudo systemctl daemon-reload
sudo systemctl enable gunicorn

# Nginxの設定をテスト
echo "Nginx設定をテスト中..."
sudo nginx -t

# サービスの開始
echo "サービスを開始中..."
sudo systemctl start nginx
sudo systemctl start gunicorn

echo "=== AWS EC2 Ubuntuインスタンスセットアップ完了 ==="
echo ""
echo "次のステップ:"
echo "1. .envファイルを編集して適切な値を設定"
echo "2. python manage.py migrate --settings=config.settings.production"
echo "3. python manage.py collectstatic --settings=config.settings.production"
echo "4. python manage.py createsuperuser --settings=config.settings.production"
echo "5. ドメイン名を設定してSSL証明書を取得" 