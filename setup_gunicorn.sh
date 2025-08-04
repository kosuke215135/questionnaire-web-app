#!/bin/bash

# Gunicornサービス設定スクリプト
set -e

echo "=== Gunicornサービス設定開始 ==="

# プロジェクトディレクトリの設定
PROJECT_DIR="/path/to/your/project"  # 実際のパスに変更してください
PROJECT_NAME="questionnaire-web-app"

# systemdサービスファイルの作成
echo "Gunicorn systemdサービスファイルを作成中..."
sudo tee /etc/systemd/system/gunicorn.service > /dev/null << EOF
[Unit]
Description=Gunicorn daemon for Django application
After=network.target

[Service]
User=www-data
Group=www-data
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

# サービスを有効化して開始
echo "Gunicornサービスを有効化して開始中..."
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# サービスの状態確認
echo "Gunicornサービスの状態を確認中..."
sudo systemctl status gunicorn

echo "=== Gunicornサービス設定完了 ==="
echo "プロジェクトディレクトリ: $PROJECT_DIR"
echo "サービス名: gunicorn"
echo "管理コマンド:"
echo "  sudo systemctl start gunicorn"
echo "  sudo systemctl stop gunicorn"
echo "  sudo systemctl restart gunicorn"
echo "  sudo systemctl status gunicorn" 