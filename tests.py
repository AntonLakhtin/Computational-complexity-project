from typing import List
import numpy as np
from scipy import stats


def correctness_test(test_size: int, answer: int) -> List[float]:
    """

    Генерирует набор из test_size весов предметов, которые занимают целиком answer корзин

    """
    items = []

    splits = [i * test_size // answer for i in range(answer + 1)]
    
    for i in range(answer):
        cnt = splits[i + 1] - splits[i]
        numbers = np.random.dirichlet([1] * cnt)
        items.extend(numbers)

    return items

def random_uniform_test(test_size: int) -> List[float]:
    """

    Генерирует случайный набор из test_size весов предметов, соответствующих равномерному распределению

    """

    return stats.uniform.rvs(size=test_size, loc=0, scale=1)


def random_beta_test(test_size: int) -> List[float]:
    """

    Генерирует случайный набор из test_size весов предметов, соответствующих распределению Beta(1, 3)

    """
    return stats.beta.rvs(a=1, b=3, size=test_size)
