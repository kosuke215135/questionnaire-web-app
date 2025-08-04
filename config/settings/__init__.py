# Settings package 
# Settings package
import os

# デフォルトでproduction設定を使用
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')