import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import japanize_matplotlib
from typing import List


def plot_graph_with_path(colum: List[str], num: List[int], path: str) -> None:
    """
    colum（ラベル）, num（値）から棒グラフを生成し、指定されたpathに画像として保存する。
    """
    plt.figure(figsize=(6, 4))
    plt.bar(colum, num, color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Value')
    plt.title('Chart')
    plt.tight_layout()
    plt.savefig(path)
    plt.close() 
