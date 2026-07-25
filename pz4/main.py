import networkx as nx
import matplotlib.pyplot as plt
import random

class PowerGridAnalyzer:
    def __init__(self, num_nodes, edge_probability):
        # Create a graph and ensure it's fully connected initially
        self.grid = nx.erdos_renyi_graph(n=num_nodes, p=edge_probability, seed=42)
        seed_val = 42
        while not nx.is_connected(self.grid):
            seed_val += 1
            self.grid = nx.erdos_renyi_graph(n=num_nodes, p=edge_probability, seed=seed_val)
            
        self.grid_after_failure = None
        self.failed_node = None

    def simulate_failure(self):
        self.grid_after_failure = self.grid.copy()
        
        degrees = dict(self.grid_after_failure.degree())
        self.failed_node = max(degrees, key=degrees.get)
        
        self.grid_after_failure.remove_node(self.failed_node)

    def plot_grids(self):
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        pos = nx.spring_layout(self.grid, seed=42)
        
        nx.draw(self.grid, pos, ax=axes[0], with_labels=True, 
                node_color='lightblue', node_size=500, font_weight='bold', edge_color='gray')
        axes[0].set_title("Електромережа до відмови (Цілісна)")

        pos_after = {node: pos[node] for node in self.grid_after_failure.nodes()}
        
        nx.draw(self.grid_after_failure, pos_after, ax=axes[1], with_labels=True, 
                node_color='salmon', node_size=500, font_weight='bold', edge_color='gray')
        axes[1].set_title(f"Після відмови (Видалено ЦВ {self.failed_node})")

        plt.show()

    def analyze(self):
        nodes_before = self.grid.number_of_nodes()
        edges_before = self.grid.number_of_edges()
        
        nodes_after = self.grid_after_failure.number_of_nodes()
        edges_after = self.grid_after_failure.number_of_edges()
        
        connected_before = nx.is_connected(self.grid)
        
        components_after = list(nx.connected_components(self.grid_after_failure))
        connected_after = nx.is_connected(self.grid_after_failure)

        print("--- Графовий аналіз стійкості електромережі ---")
        print(f"Стан ДО відмови:")
        print(f"  Вузлів: {nodes_before}, Ліній: {edges_before}")
        print(f"  Мережа цілісна: {connected_before}")
        
        print(f"\nСтан ПІСЛЯ відмови (найбільш навантажений вузол {self.failed_node}):")
        print(f"  Вузлів: {nodes_after}, Ліній: {edges_after}")
        print(f"  Мережа цілісна: {connected_after}")
        print(f"  Кількість ізольованих фрагментів мережі (островів): {len(components_after)}")
        
        print("\n--- Порівняння зі статистичним методом ---")
        print("Статистичний аналіз: просто каже нам ймовірність, з якою вузол може зламатися (наприклад 0.05).")
        print("Графовий аналіз (NetworkX): показує реалістичні наслідки цієї ізольованої поломки для всієї системи.")

analyzer = PowerGridAnalyzer(num_nodes=15, edge_probability=0.25)
analyzer.simulate_failure()
analyzer.plot_grids()
analyzer.analyze()
