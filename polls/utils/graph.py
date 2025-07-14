import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import japanize_matplotlib
from typing import List
from matplotlib.ticker import MaxNLocator


def plot_graph_with_path(colum: List[str], num: List[int], path: str) -> None:
    """
    colum（ラベル）, num（値）から棒グラフを生成し、指定されたpathに画像として保存する。
    """
    # 原色中心に色を増やす
    Colors = [
        'red', 'blue', 'green', 'orange', 'skyblue', 'yellow', 'purple', 'pink',
        'black', 'brown', 'cyan', 'magenta', 'lime', 'navy', 'gold', 'violet', 'gray'
    ]
    # ラベル改行処理（元リストを破壊しない）
    colum_kaigyo = [label[:5] + '\n' + label[5:] if len(label) > 5 else label for label in colum]

    plt.figure(figsize=(6, 4))
    # 色数が足りない場合は繰り返す
    color_list = (Colors * ((len(colum_kaigyo) // len(Colors)) + 1))[:len(colum_kaigyo)]
    plt.bar(colum_kaigyo, num, color=color_list)
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.title('Chart')
    plt.tight_layout()
    # 縦軸のメモリを整数のみに変更
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.savefig(path)
    plt.close() 
