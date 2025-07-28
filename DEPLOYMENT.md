# Renderデプロイメントガイド

このドキュメントでは、questionnaire-web-appをRenderにデプロイする手順を説明します。

## 前提条件

- GitHubアカウント
- Renderアカウント（無料で作成可能）
- プロジェクトがGitHubリポジトリにプッシュされていること

## デプロイ手順

### 1. Renderでのサービス作成

1. [Render](https://render.com)にログイン
2. "New" → "Web Service"を選択
3. GitHubリポジトリを連携・選択
4. 以下の設定を入力：
   - **Name**: `questionnaire-web-app`（任意の名前）
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi:application`

### 2. データベース作成

1. Renderダッシュボードで "New" → "PostgreSQL"を選択
2. 以下の設定を入力：
   - **Name**: `questionnaire-db`（任意の名前）
   - **Plan**: `Free`（開発用）
3. 作成後、データベースのInternal Database URLをコピー

### 3. 環境変数設定

Webサービスの設定画面で以下の環境変数を設定：

#### 必須環境変数

```bash
# Django設定
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com,localhost

# Render識別用
RENDER=true
RENDER_EXTERNAL_HOSTNAME=your-app-name.onrender.com

# データベース（PostgreSQLのInternal Database URLを使用）
DATABASE_URL=postgresql://username:password@hostname:port/database_name

# スーパーユーザー作成（オプション）
CREATE_SUPERUSER=true
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=secure_password

# サンプルデータ読み込み（推奨：初回デプロイ時に有効）
LOAD_SAMPLE_DATA=true
```

#### SECRET_KEYの生成方法

Pythonで新しいシークレットキーを生成：

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 4. デプロイの実行

1. 環境変数設定後、"Deploy"ボタンをクリック
2. ビルドプロセスが完了するまで待機（初回は10-15分程度）
3. デプロイ完了後、提供されるURLでアプリケーションにアクセス

## 本番環境での設定

### セキュリティ設定

本番環境では以下のセキュリティ設定が自動的に有効になります：

- HTTPS強制リダイレクト
- HSTS（HTTP Strict Transport Security）
- XSS保護
- CSRF保護
- クリックジャッキング保護

### 静的ファイル

- WhiteNoiseを使用して静的ファイルを配信
- 自動的に圧縮・最適化

### データベース

- PostgreSQLを使用
- 自動バックアップ（有料プランの場合）

## トラブルシューティング

### よくある問題

#### 1. ビルドエラー

**症状**: `requirements.txt`関連のエラー
**解決**: 以下のコマンドでローカル環境の依存関係を確認

```bash
pip freeze > requirements.txt
```

#### 2. 静的ファイルが表示されない

**症状**: CSSが適用されない
**解決**: `collectstatic`コマンドの実行を確認

```bash
python manage.py collectstatic --no-input
```

#### 3. データベース接続エラー

**症状**: データベースに接続できない
**解決**: `DATABASE_URL`環境変数を確認

#### 4. グラフ生成エラー

**症状**: アンケート結果でグラフが表示されない
**解決**: 
- メモリ不足の可能性。Renderの有料プランへのアップグレードを検討
- ログでエラー詳細を確認

### ログ確認方法

Renderダッシュボードの"Logs"タブでアプリケーションログを確認可能。

### パフォーマンス最適化

#### 1. 画像最適化

グラフ画像のファイルサイズを最適化：
- DPI: 100（画質と容量のバランス）
- 図のサイズ: 適度に調整済み

#### 2. データベース最適化

- インデックスの追加を検討
- クエリ最適化

#### 3. キャッシュ設定

将来的にRedisキャッシュの導入を検討。

## 更新デプロイ

コードを更新してGitHubにプッシュすると、自動的に再デプロイされます。

## 料金について

### 無料プラン制限

- Webサービス: 750時間/月まで無料
- PostgreSQL: 1GB、90日間無料
- 非アクティブ時のスリープ機能あり

### 有料プラン

- より高いパフォーマンス
- 24/7稼働
- 自動バックアップ
- カスタムドメイン

## サポート

問題が発生した場合は：
1. Renderのドキュメントを確認
2. ログを詳細に確認
3. 環境変数設定を再確認

---

**注意**: 本番環境では必ず`DEBUG=False`に設定し、強力な`SECRET_KEY`を使用してください。 
