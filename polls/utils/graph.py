import matplotlib
matplotlib.use('Agg')  # バックエンドをAggに設定（サーバー環境用）
import matplotlib.pyplot as plt
import japanize_matplotlib
from typing import List
from matplotlib.ticker import MaxNLocator
import matplotlib.patheffects as pe
import numpy as np
import os


def plot_graph_with_path(colum: List[str], num: List[int], path: str, graph_type: str = 'bar') -> None:
    """
    colum（ラベル）, num（値）からグラフを生成し、指定されたpathに画像として保存する。
    graph_type: 'bar' または 'pie'
    """
    try:
        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        if graph_type == 'pie':
            plot_pie_chart_with_path(colum, num, path)
        else:
            plot_bar_chart_with_path(colum, num, path)
    except Exception as e:
        print(f"Graph generation error: {e}")
        # エラー時でもアプリケーションを継続させる
        return


def plot_bar_chart_with_path(colum: List[str], num: List[int], path: str) -> None:
    """
    棒グラフを生成して保存する（アクセシビリティ対応、パフォーマンス最適化済み）
    """
    # データが空の場合は処理をスキップ
    if not num or not colum:
        return
    
    try:
        # Matplotlibの設定を最適化
        plt.rcParams.update({
            'font.size': 14,  # デフォルトフォントサイズを調整
            'figure.dpi': 100,  # DPIを抑えてファイルサイズを最適化
            'savefig.dpi': 100,
            'figure.max_open_warning': 0  # 警告を抑制
        })
        
        # 単色の配色（洗練された青）
        single_color = '#4e79a7'  # スレートブルー
        
        # ラベル改行処理（元リストを破壊しない）
        colum_kaigyo = [label[:5] + '\n' + label[5:] if len(label) > 5 else label for label in colum]

        # グラフサイズを最適化（メモリ使用量とのバランス）
        plt.figure(figsize=(10, 6))
        
        # 棒グラフを作成し、barsオブジェクトを取得（単色で統一）
        bars = plt.bar(colum_kaigyo, num, color=single_color)
        
        # 不要なラベルを削除
        plt.xlabel('')
        plt.ylabel('')
        plt.title('')
        
        # 文字サイズをアンケートの回答選択肢に合わせて調整
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        
        # 各棒の上に数値を表示（文字サイズを大きく）
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.1,  # 棒の上に少し余白を設ける
                int(height),
                ha='center', va='bottom', fontsize=20, fontweight='bold',  # 文字サイズを20pxに調整
                color='black'
            )
        
        # y軸のメモリを整数のみに変更
        plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
        
        # y軸のメモリの最大値を設定（安全な最大値計算）
        max_value = max(num) if num else 0
        plt.ylim(0, max_value + 1)
        
        # レイアウトを自動調整
        plt.tight_layout()
        
        # ファイルサイズを最適化して保存
        plt.savefig(path, bbox_inches='tight', dpi=100, optimize=True)
        
    except Exception as e:
        print(f"Bar chart generation error: {e}")
    finally:
        # メモリリークを防ぐため、図を閉じる
        plt.close('all')


def plot_pie_chart_with_path(colum: List[str], num: List[int], path: str) -> None:
    """
    円グラフを生成して保存する（アクセシビリティ対応、パフォーマンス最適化済み）
    """
    # データが空の場合は処理をスキップ
    if not num or not colum:
        return
    
    try:
        # Matplotlibの設定を最適化
        plt.rcParams.update({
            'font.size': 12,
            'figure.dpi': 100,
            'savefig.dpi': 100,
            'figure.max_open_warning': 0
        })
        
        # データを値が大きい順にソート
        data_pairs = sorted(zip(colum, num), key=lambda pair: pair[1], reverse=True)
        sorted_colum = [pair[0] for pair in data_pairs]
        sorted_num = [pair[1] for pair in data_pairs]
        
        # ラベルと数値を結合
        combined_labels = [f"{label} ({value})" for label, value in zip(sorted_colum, sorted_num)]
        
        # 図のサイズを最適化
        plt.figure(figsize=(8, 8))
        
        # アクセシブルなカラーマップから色を取得
        # cividisは色覚多様性に対応
        num_slices = len(sorted_num)
        if num_slices > 0:
            colors = plt.cm.get_cmap('cividis', num_slices)(np.linspace(0, 1, num_slices))
        else:
            colors = ['#4e79a7']  # デフォルト色
        
        def custom_autopct(pct):
            return f'{pct:.1f}%'
        
        # 円グラフを作成
        wedges, texts, autotexts = plt.pie(
            sorted_num, 
            labels=combined_labels, 
            autopct=custom_autopct,
            startangle=90, 
            counterclock=False, 
            colors=colors
        )
        
        plt.axis('equal')
        
        # 各数値テキストに白い縁取りを設定（視認性向上）
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_weight('bold')
            autotext.set_fontsize(14)
            autotext.set_path_effects([
                pe.Stroke(linewidth=2, foreground='white'),
                pe.Normal()
            ])
        
        # ラベルテキストのサイズ調整
        for text in texts:
            text.set_fontsize(12)
        
        # レイアウト調整
        plt.tight_layout()
        
        # ファイルサイズを最適化して保存
        plt.savefig(path, bbox_inches='tight', dpi=100, optimize=True)
        
    except Exception as e:
        print(f"Pie chart generation error: {e}")
    finally:
        # メモリリークを防ぐため、図を閉じる
        plt.close('all') 
