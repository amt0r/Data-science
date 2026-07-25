import numpy as np
import pandas as pd


class HistoricalDataGenerator:

    def __init__(self, days=365, seed=42):
        self.days = days
        self.rng = np.random.default_rng(seed)

    def _generate_cloud_cover(self):
        return self.rng.uniform(0, 100, self.days)

    def _generate_wind_speed(self):
        return self.rng.weibull(2, self.days) * 8

    def _calculate_solar_output(self, cloud_cover):
        max_solar_kw = 5.0
        efficiency = (100 - cloud_cover) / 100
        noise = self.rng.normal(0, 0.15, self.days)
        return np.clip(max_solar_kw * efficiency + noise, 0, max_solar_kw)

    def _calculate_wind_output(self, wind_speed):
        max_wind_kw = 3.0
        cut_in = 3.0
        rated = 12.0
        cut_out = 25.0
        output = np.zeros_like(wind_speed)
        for i, ws in enumerate(wind_speed):
            if ws < cut_in or ws > cut_out:
                output[i] = 0
            elif ws >= rated:
                output[i] = max_wind_kw
            else:
                output[i] = max_wind_kw * ((ws - cut_in) / (rated - cut_in)) ** 2
        noise = self.rng.normal(0, 0.1, self.days)
        return np.clip(output + noise, 0, max_wind_kw)

    def generate(self):
        cloud_cover = self._generate_cloud_cover()
        wind_speed = self._generate_wind_speed()
        solar_output = self._calculate_solar_output(cloud_cover)
        wind_output = self._calculate_wind_output(wind_speed)
        return pd.DataFrame({
            "cloud_cover": cloud_cover,
            "wind_speed": wind_speed,
            "solar_output_kw": solar_output,
            "wind_output_kw": wind_output,
        })


class WeatherScenarioProvider:

    SCENARIOS = {
        1: {
            "name": "Хмарно та штиль",
            "description": "Критично мало енергії",
            "cloud_cover": 95,
            "wind_speed": 1.5,
        },
        2: {
            "name": "Ідеальна погода",
            "description": "Сонце + Вітер",
            "cloud_cover": 10,
            "wind_speed": 10.0,
        },
        3: {
            "name": "Сонячно, але немає вітру",
            "description": "Тільки сонячна генерація",
            "cloud_cover": 5,
            "wind_speed": 1.0,
        },
        4: {
            "name": "Шторм",
            "description": "Хмарно, але сильний вітер",
            "cloud_cover": 90,
            "wind_speed": 15.0,
        },
    }

    def get_scenario(self, choice):
        return self.SCENARIOS.get(choice)

    def get_menu_text(self):
        lines = ["\n🏠 Оберіть погодний сценарій:"]
        for key, scenario in self.SCENARIOS.items():
            lines.append(f"  {key} — {scenario['name']} ({scenario['description']})")
        lines.append("  5 — Вихід з програми")
        return "\n".join(lines)
