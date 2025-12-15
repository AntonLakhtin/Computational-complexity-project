import math
import itertools
from typing import List, Tuple, Dict, Counter
from collections import defaultdict
import numpy as np
from lemma_2_1 import lemma2_1

class BinPackingAeps:
    """
    Алгоритм для задачи упаковки по корзинам.
    """
    
    def __init__(self, epsilon: float = 0.1):
        """
        Инициализация алгоритма с параметром epsilon.
        
        Получает: epsilon: параметр точности (0 < epsilon < 0.5)
        """
        assert 0 < epsilon < 0.5
        self.epsilon = epsilon
    
    def lemma2_1(self, items: List[float]) -> List[List[int]]:
        """
        Лемма 2.1: Оптимальная упаковка для случая с постоянным числом размеров.
        
        Получает: items: список предметов (все размеры >= epsilon)
            
        Возвращает: Упаковка предметов по корзинам (соответствующие номера предметов) в виде списка корзин
        """
        return lemma2_1(items)
    
    def lemma2_2(self, items: List[float]) -> List[List[float]]:
        """
        Лемма 2.2: Алгоритм (1+epsilon)-приближения для предметов размером >= epsilon.

        Получает: items: список предметов (все размеры >= epsilon)
            
        Возвращает: Упаковка предметов по корзинам (соответствующие номера предметов) в виде списка корзин
        """
        
        if not items:
            return []
        
        n = len(items)
        
        items_indexed = [(item, i) for i, item in enumerate(items)]
        items_sorted = sorted(items_indexed)
        
        Q = math.ceil(n * self.epsilon * self.epsilon)

        rounded_items = [0] * n

        for i in range(0, n, Q):
            value = 0
            if (i + Q - 1 < n):
                value = items_sorted[i + Q - 1][0]
            else:
                value = items_sorted[n - 1][0]
            for j in range(Q):
                if (i + j < n):
                    rounded_items[items_sorted[i + j][1]] = value
        
        return self.lemma2_1(rounded_items)
    
    def solve(self, items: List[float]) -> Tuple[int, List[List[float]]]:
        """
        Основной алгоритм 

        Получает: items: список предметов

        Возвращает: Оптимальное количество корзин и упаковка предметов по корзинам (соответствующие номера предметов) в виде списка корзин
        """
        for item in items:
            assert 0 < item <= 1.0, f"Размер предмета должен быть в (0, 1), получено: {item}"
        
        large_items = [item for item in items if item >= self.epsilon]
        small_items = [item for item in items if item < self.epsilon]
        
        if large_items:
            packing = self.lemma2_2(large_items)
        else:
            packing = []

        bins = [[] for bin in packing]
        for i, bin in enumerate(packing):
            for index in bin:
                bins[i].append(large_items[index])

        
        for small_item in small_items:
            placed = False
            for bin in bins:
                if sum(bin) + small_item <= 1.0 + 1e-10:
                    bin.append(small_item)
                    placed = True
                    break
            
            if not placed:
                bins.append([small_item])
        
        total_bins = len(bins)
        
        return total_bins, bins