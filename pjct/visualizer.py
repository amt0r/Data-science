import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams


class CorrelationVisualizer:

    def __init__(self):
        rcParams["figure.dpi"] = 120
        rcParams["axes.spines.top"] = False
        rcParams["axes.spines.right"] = False
        rcParams["font.size"] = 10

    def _add_trendline(self, ax, x, y, color):
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        x_sorted = np.sort(x)
        ax.plot(x_sorted, p(x_sorted), color=color, linewidth=2.5, linestyle="--", alpha=0.9)

    def _style_scatter(self, ax, x, y, color, alpha=0.35, size=12):
        ax.scatter(x, y, c=color, alpha=alpha, s=size, edgecolors="none")

    def _annotate_r(self, ax, r_value, position="upper right"):
        bbox = dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="gray", alpha=0.85)
        if position == "upper right":
            xy = (0.95, 0.92)
        else:
            xy = (0.05, 0.92)
        ax.annotate(
            f"r = {r_value:+.4f}",
            xy=xy,
            xycoords="axes fraction",
            fontsize=12,
            fontweight="bold",
            ha="right" if "right" in position else "left",
            bbox=bbox,
        )

    def plot(self, data: pd.DataFrame, correlation_results: dict):
        fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
        fig.suptitle("Кореляційний аналіз: погода → генерація енергії", fontsize=14, fontweight="bold", y=1.02)

        self._plot_solar(axes[0], data, correlation_results["solar"]["coefficient"])
        self._plot_wind(axes[1], data, correlation_results["wind"]["coefficient"])

        plt.tight_layout()
        plt.savefig("correlation_analysis.png", bbox_inches="tight", facecolor="white")
        plt.show()

    def _plot_solar(self, ax, data, r_value):
        x = data["cloud_cover"]
        y = data["solar_output_kw"]
        self._style_scatter(ax, x, y, color="#FF6B35")
        self._add_trendline(ax, x, y, color="#C74B1A")
        self._annotate_r(ax, r_value)
        ax.set_xlabel("Хмарність (%)")
        ax.set_ylabel("Сонячна генерація (кВт)")
        ax.set_title("Хмарність vs Сонячна генерація")

    def _plot_wind(self, ax, data, r_value):
        x = data["wind_speed"]
        y = data["wind_output_kw"]
        self._style_scatter(ax, x, y, color="#4ECDC4")
        self._add_trendline(ax, x, y, color="#2A9D8F")
        self._annotate_r(ax, r_value, position="upper left")
        ax.set_xlabel("Швидкість вітру (м/с)")
        ax.set_ylabel("Вітрова генерація (кВт)")
        ax.set_title("Швидкість вітру vs Вітрова генерація")
