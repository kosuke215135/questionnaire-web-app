import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import japanize_matplotlib
from typing import List
from matplotlib.ticker import MaxNLocator
import matplotlib.patheffects as pe
import numpy as np


def plot_graph_with_path(colum: List[str], num: List[int], path: str, graph_type: str = 'bar') -> None:
    """
    colum（ラベル）, num（値）からグラフを生成し、指定されたpathに画像として保存する。
    graph_type: 'bar' または 'pie'
    """
    if graph_type == 'pie':
        plot_pie_chart_with_path(colum, num, path)
    else:
        plot_bar_chart_with_path(colum, num, path)


def plot_bar_chart_with_path(colum: List[str], num: List[int], path: str) -> None:
    """
    棒グラフを生成して保存する（アクセシビリティ対応）
    """
    # データが空の場合は処理をスキップ
    if not num or not colum:
        return
    
    # 単色の配色（洗練された青）
    single_color = '#4e79a7'  # スレートブルー
    
    # ラベル改行処理（元リストを破壊しない）
    colum_kaigyo = [label[:5] + '\n' + label[5:] if len(label) > 5 else label for label in colum]

    # グラフの大きさを大きくし、文字サイズを調整
    plt.figure(figsize=(12, 8))
    
    # 棒グラフを作成し、barsオブジェクトを取得（単色で統一）
    bars = plt.bar(colum_kaigyo, num, color=single_color)
    
    # 不要なラベルを削除
    plt.xlabel('')
    plt.ylabel('')
    plt.title('')
    
    # 文字サイズをアンケートの回答選択肢に合わせて大きくする
    plt.xticks(fontsize=18)  # アンケートの質問文サイズ(1.1rem)より大きく
    plt.yticks(fontsize=18)  # アンケートの質問文サイズ(1.1rem)より大きく
    
    # 各棒の上に数値を表示（文字サイズを大きく）
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.1,  # 棒の上に少し余白を設ける
            int(height),
            ha='center', va='bottom', fontsize=24, fontweight='bold',  # 文字サイズを24pxに拡大
            color='black'
        )
    
    # y軸の最大値を調整（数値表示のための余白を追加）
    max_value = max(num) if num else 0
    plt.ylim(0, max_value + 1)
    
    plt.tight_layout()
    # 縦軸のメモリを整数のみに変更
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close()


def plot_pie_chart_with_path(colum: List[str], num: List[int], path: str) -> None:
    """
    円グラフを生成して保存する（アクセシビリティ対応）
    """
    # データが空の場合は処理をスキップ
    if not num or not colum:
        return
    
    # グラフ全体のフォントサイズを調整（アンケートの回答選択肢に合わせる）
    plt.rcParams.update({'font.size': 18})

    # データを値が大きい順にソート
    data_pairs = sorted(zip(colum, num), key=lambda pair: pair[1], reverse=True)
    sorted_colum = [pair[0] for pair in data_pairs]
    sorted_num = [pair[1] for pair in data_pairs]

    # ラベルと数値を結合
    combined_labels = [f"{label} ({value})" for label, value in zip(sorted_colum, sorted_num)]

    # グラフの大きさを大きくする
    plt.figure(figsize=(12, 10))

    # 洗練された色パレット（円グラフ用、原色を避けた落ち着いた色合い）
    # 理由：
    # 1. 原色を避けて、より洗練された印象に
    # 2. 円グラフでは隣接する色の区別が重要
    # 3. ビジネス用途に適した、落ち着いた色合い
    refined_pie_colors = [
        '#4e79a7',  # スレートブルー
        '#f28e2c',  # テラコッタ
        '#e15759',  # コーラル
        '#76b7b2',  # ティール
        '#59a14f',  # オリーブグリーン
        '#edc949',  # マスタード
        '#af7aa1',  # ラベンダー
        '#ff9da7',  # ピーチ
        '#9c755f',  # タウニー
        '#bab0ab',  # グレージュ
        '#6b6b6b',  # チャコール
        '#b07aa1',  # プラム
        '#d37295',  # ローズ
        '#faa757',  # アプリコット
        '#b07aa1',  # ラベンダーグレー
        '#ff9da7',  # サルモン
    ]

    # スライスの数に応じて色を割り当て
    num_slices = len(sorted_num)
    if num_slices <= len(refined_pie_colors):
        colors = refined_pie_colors[:num_slices]
    else:
        # 色が足りない場合は、洗練されたカラーマップを使用
        # viridisは色覚多様性に配慮して設計されたカラーマップ
        colors = plt.cm.get_cmap('viridis', num_slices)(np.linspace(0, 1, num_slices))

    def custom_autopct(pct):
        return f'{pct:.1f}%'

    # pie関数を実行し、テキストオブジェクトを取得
    wedges, texts, autotexts = plt.pie(sorted_num,
                                       labels=combined_labels,
                                       autopct=custom_autopct,
                                       startangle=90,
                                       counterclock=False,
                                       colors=colors)
    plt.axis('equal')

    # 各数値テキストに白い縁取りを設定（アクセシビリティ向上）
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_weight('bold')
        autotext.set_path_effects([
            pe.Stroke(linewidth=3, foreground='white'),
            pe.Normal()
        ])

    # タイトルを削除
    plt.title('')
    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight', dpi=300)
    plt.close() 
