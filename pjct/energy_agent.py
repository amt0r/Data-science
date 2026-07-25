class EnergyAgent:

    HOUSE_DEMAND_KW = 4.5
    SOLAR_MAX_KW = 5.0
    WIND_MAX_KW = 3.0
    WIND_CUT_IN = 3.0
    WIND_RATED = 12.0
    WIND_CUT_OUT = 25.0
    GENERATOR_OUTPUT_KW = 5.0

    def __init__(self):
        self.generator_active = False

    def _estimate_solar(self, cloud_cover):
        efficiency = (100 - cloud_cover) / 100
        return self.SOLAR_MAX_KW * efficiency

    def _estimate_wind(self, wind_speed):
        if wind_speed < self.WIND_CUT_IN or wind_speed > self.WIND_CUT_OUT:
            return 0.0
        if wind_speed >= self.WIND_RATED:
            return self.WIND_MAX_KW
        return self.WIND_MAX_KW * ((wind_speed - self.WIND_CUT_IN) / (self.WIND_RATED - self.WIND_CUT_IN)) ** 2

    def _calculate_deficit(self, total_green):
        return self.HOUSE_DEMAND_KW - total_green

    def _decide_generator_action(self, deficit):
        if deficit > 0:
            self.generator_active = True
            return "START"
        self.generator_active = False
        return "STOP"

    def evaluate(self, cloud_cover, wind_speed):
        solar = self._estimate_solar(cloud_cover)
        wind = self._estimate_wind(wind_speed)
        total_green = solar + wind
        deficit = self._calculate_deficit(total_green)
        action = self._decide_generator_action(deficit)
        return {
            "solar_kw": solar,
            "wind_kw": wind,
            "total_green_kw": total_green,
            "demand_kw": self.HOUSE_DEMAND_KW,
            "deficit_kw": max(deficit, 0),
            "surplus_kw": max(-deficit, 0),
            "action": action,
            "generator_active": self.generator_active,
        }

    def print_decision(self, scenario_name, result):
        print(f"\n⚡ Сценарій: {scenario_name}")
        print("─" * 50)
        print(f"  ☀️  Сонячна генерація:   {result['solar_kw']:.2f} кВт")
        print(f"  🌬️  Вітрова генерація:    {result['wind_kw']:.2f} кВт")
        print(f"  🔋 Загальна зелена:      {result['total_green_kw']:.2f} кВт")
        print(f"  🏠 Споживання будинку:   {result['demand_kw']:.2f} кВт")
        print("─" * 50)

        if result["action"] == "START":
            print(f"  🚨 ДЕФІЦИТ: {result['deficit_kw']:.2f} кВт")
            print(f"  🔌 Рішення: УВІМКНУТИ бензиновий генератор (+{self.GENERATOR_OUTPUT_KW} кВт)")
            print(f"  ✅ Статус генератора: [ПРАЦЮЄ]")
        else:
            print(f"  💚 НАДЛИШОК: {result['surplus_kw']:.2f} кВт")
            print(f"  🔌 Рішення: генератор НЕ ПОТРІБЕН")
            print(f"  ✅ Статус генератора: [ВИМКНЕНО]")
        print("─" * 50)
