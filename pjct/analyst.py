import pandas as pd
from scipy.stats import pearsonr


class CorrelationAnalyst:

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.results = {}

    def _compute_single_correlation(self, col_x, col_y):
        coefficient, p_value = pearsonr(self.data[col_x], self.data[col_y])
        return {"coefficient": coefficient, "p_value": p_value}

    def analyze_solar_correlation(self):
        result = self._compute_single_correlation("cloud_cover", "solar_output_kw")
        self.results["solar"] = result
        return result

    def analyze_wind_correlation(self):
        result = self._compute_single_correlation("wind_speed", "wind_output_kw")
        self.results["wind"] = result
        return result

    def run_full_analysis(self):
        self.analyze_solar_correlation()
        self.analyze_wind_correlation()
        return self.results

    def print_report(self):
        solar = self.results.get("solar")
        wind = self.results.get("wind")
        print("\n📊 Результати кореляційного аналізу (Пірсон):")
        print("─" * 50)
        if solar:
            print(f"  ☁️  Хмарність → Сонячна генерація:  r = {solar['coefficient']:+.4f}  (p = {solar['p_value']:.2e})")
        if wind:
            print(f"  🌬️  Швидкість вітру → Вітрова генерація: r = {wind['coefficient']:+.4f}  (p = {wind['p_value']:.2e})")
        print("─" * 50)
