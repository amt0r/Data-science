import sys
sys.stdout.reconfigure(encoding="utf-8")

from data_provider import HistoricalDataGenerator, WeatherScenarioProvider
from analyst import CorrelationAnalyst
from energy_agent import EnergyAgent
from visualizer import CorrelationVisualizer


def run_training_phase():
    print("=" * 55)
    print("🧠 ЕТАП 1: НАВЧАННЯ (аналіз історичних даних)")
    print("=" * 55)
    generator = HistoricalDataGenerator(days=365)
    data = generator.generate()
    print(f"  📅 Згенеровано {len(data)} днів історичних даних")
    analyst = CorrelationAnalyst(data)
    results = analyst.run_full_analysis()
    analyst.print_report()
    return data, results


def run_visualization(data, correlation_results):
    print("\n📈 Побудова графіків кореляції...")
    visualizer = CorrelationVisualizer()
    visualizer.plot(data, correlation_results)
    print("  ✅ Графік збережено: correlation_analysis.png")


def run_interactive_loop():
    print("\n" + "=" * 55)
    print("🔄 ЕТАП 2: ЕКСПЛУАТАЦІЯ (реальний час)")
    print("=" * 55)
    agent = EnergyAgent()
    provider = WeatherScenarioProvider()

    while True:
        print(provider.get_menu_text())
        raw = input("\n👉 Ваш вибір: ").strip()
        if raw == "5":
            print("\n👋 Завершення роботи агента. До побачення!")
            break
        if not raw.isdigit() or int(raw) not in provider.SCENARIOS:
            print("⚠️  Невірний вибір, спробуйте ще раз.")
            continue
        scenario = provider.get_scenario(int(raw))
        result = agent.evaluate(scenario["cloud_cover"], scenario["wind_speed"])
        agent.print_decision(scenario["name"], result)


def main():
    print("\n🏡 Smart Home Energy Agent")
    print("━" * 55)
    data, correlations = run_training_phase()
    run_visualization(data, correlations)
    run_interactive_loop()


if __name__ == "__main__":
    main()
