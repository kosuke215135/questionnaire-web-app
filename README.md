# questionnaire-web-app

アンケート作成・回答・結果表示Webアプリケーション

## 開発環境セットアップ

### 1. 仮想環境の作成とアクティベート
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate  # Windows
```

### 2. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 3. 環境変数の設定
```bash
cp env.example .env
# .envファイルを編集して適切な値を設定
```

### 4. データベースのセットアップ
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. 開発サーバーの起動
```bash
python manage.py runserver
```

## AWS EC2 Ubuntuインスタンスでのデプロイ

### 1. EC2インスタンスの準備
- Ubuntu 22.04 LTSインスタンスを作成
- セキュリティグループでHTTP(80)、HTTPS(443)、SSH(22)を開放
- パブリックIPアドレスをメモ

### 2. プロジェクトのアップロード
```bash
# ローカルからEC2にファイルをアップロード
scp -r . ubuntu@your-ec2-public-ip:/home/ubuntu/questionnaire-web-app/
```

### 3. EC2インスタンスでのセットアップ
```bash
# EC2インスタンスにSSH接続
ssh ubuntu@your-ec2-public-ip

# プロジェクトディレクトリに移動
cd questionnaire-web-app

# EC2用セットアップスクリプトを実行
./setup_ec2.sh
```

### 4. 環境変数の設定
```bash
# .envファイルを編集
nano .env

# 以下の値を設定：
# SECRET_KEY=your-secret-key-here
# ALLOWED_HOSTS=your-ec2-public-ip,your-domain.com
# DB_PASSWORD=your-database-password
```

### 5. データベースとアプリケーションの初期化
```bash
# 仮想環境をアクティベート
source venv/bin/activate

# データベースマイグレーション
python manage.py migrate --settings=config.settings.production

# 静的ファイルの収集
python manage.py collectstatic --settings=config.settings.production

# スーパーユーザーの作成
python manage.py createsuperuser --settings=config.settings.production
```

### 6. サービスの確認
```bash
# サービスの状態確認
sudo systemctl status nginx
sudo systemctl status gunicorn

# ログの確認
sudo journalctl -u gunicorn
sudo tail -f /var/log/nginx/error.log
```

## 本番環境デプロイ（ローカルサーバー）

### 1. 環境変数の設定
```bash
cp env.example .env
# .envファイルを編集して本番環境用の値を設定
```

### 2. MySQLのセットアップ
```bash
# スクリプト内のパスワードを.envファイルの値に変更してから実行
./setup_mysql.sh
```

### 3. SSL証明書のセットアップ
```bash
# スクリプト内のドメイン名とメールアドレスを変更してから実行
./setup_ssl.sh
```

### 4. Gunicornサービスの設定
```bash
# スクリプト内のプロジェクトパスを変更してから実行
./setup_gunicorn.sh
```

### 5. 静的ファイルの収集
```bash
python manage.py collectstatic --settings=config.settings.production
```

### 6. データベースマイグレーション
```bash
python manage.py migrate --settings=config.settings.production
```

### 7. デプロイスクリプトの実行
```bash
./deploy.sh
```

## 設定ファイル

- `config/settings/base.py` - 共通設定
- `config/settings/local.py` - 開発環境設定
- `config/settings/production.py` - 本番環境設定

## セットアップスクリプト

- `setup_ec2.sh` - AWS EC2 Ubuntuインスタンス用セットアップ
- `setup_mysql.sh` - MySQLデータベースセットアップ
- `setup_ssl.sh` - Let's Encrypt SSL証明書セットアップ
- `setup_gunicorn.sh` - Gunicornサービス設定
- `deploy.sh` - アプリケーションデプロイ

## 技術スタック

- Django 5.2.3
- MySQL
- Nginx
- Gunicorn
- matplotlib (グラフ描画)
- japanize-matplotlib (日本語対応)
