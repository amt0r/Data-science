import pandas as pd
import numpy as np
import time
from dataclasses import dataclass
from typing import Callable

@dataclass
class ExecutionTime:
    method_name: str
    duration: float
    
    def __str__(self) -> str:
        return f"{self.method_name}: {self.duration:.6f}s"

class RevenueAnalyzer:
    
    def __init__(self, data: pd.DataFrame, value_col: str = 'revenue', date_col: str = 'date'):
        self.date_col = date_col
        self.value_col = value_col
        self.df = data.sort_values(by=self.date_col).reset_index(drop=True)
        self.execution_times: list[ExecutionTime] = []

    def _measure_execution(self, func: Callable, method_name: str, *args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start_time
        
        self.execution_times.append(ExecutionTime(method_name, duration))
        return result

    def compare_methods(self, window: int = 7) -> float:
        pd_result = self._measure_execution(
            self.calculate_pandas_rolling, 
            "Pandas rolling", 
            window
        ).values
        
        np_result = self._measure_execution(
            self.calculate_numpy_rolling, 
            "NumPy rolling", 
            window
        )
        
        diff = np.abs(pd_result - np_result)
        max_diff = np.nanmax(diff)
        
        return max_diff

    def calculate_pandas_rolling(self, window: int = 7) -> pd.Series:
        return self.df[self.value_col].rolling(window=window).mean()

    def calculate_numpy_rolling(self, window: int = 7) -> np.ndarray:
        arr = self.df[self.value_col].values
        
        cumsum_vec = np.insert(arr, 0, 0).cumsum()
        rolling_sum = cumsum_vec[window:] - cumsum_vec[:-window]
        rolling_mean = rolling_sum / window
        
        result = np.full(len(arr), np.nan)
        result[window - 1:] = rolling_mean
        
        return result
    
    def print_execution_times(self) -> None:
        print("\nЧас виконання:")
        for exec_time in self.execution_times:
            print(f"  {exec_time}")

if __name__ == "__main__":
    np.random.seed(42)
    dates = pd.date_range(start="1900-01-01", periods=100000, freq="d")
    revenue = np.random.uniform(1000, 5000, size=100000)
    
    df_revenue = pd.DataFrame({'date': dates, 'revenue': revenue})
    
    print("Перші 10 рядків даних:")
    print(df_revenue.head(10))
    print(f"\nКількість записів: {len(df_revenue)}")
    print(f"Дата від {df_revenue['date'].min()} до {df_revenue['date'].max()}")
    
    analyzer = RevenueAnalyzer(df_revenue)
    
    window_size = 7
    max_difference = analyzer.compare_methods(window=window_size)
    
    print(f"\nМаксимальна абсолютна різниця між Pandas та NumPy (вікно {window_size}): {max_difference}")
    analyzer.print_execution_times()
