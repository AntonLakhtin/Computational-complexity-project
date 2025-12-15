from BinPacking import BinPackingAeps
import numpy as np
import tests
import time
import matplotlib.pyplot as plt

def testing_correstness():
    for epsilon in [0.3, 0.2, 0.1, 0.05]:
        for answer in range(2, 8):
            for size in range(answer, answer * 2):
                items = tests.correctness_test(size, answer)
                algorithm = BinPackingAeps(epsilon=epsilon)
                bins_count, bins = algorithm.solve(items)

                if bins_count > (1 + 2 * epsilon) * answer + 1:
                    print('Incorrect OPT!')
                    return False
                
                result = []
                for bin in bins:
                    result.extend(bin)
                    if (sum(bin) > 1.0 + 1e-10):
                        print('Incorrect packing!')
                        return False

                if sorted(result) != sorted(items):
                    print('Incorrect packing!')
                    return False
    return True

def time_testing(test_distribution):
    epsilon_0 = 0.1
    size_0 = 9
    
    epsilons = [0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.03, 0.02, 0.01]
    times_eps = []

    for eps in epsilons:
        time_ans = 0
        for i in range(20):
            algorithm = BinPackingAeps(epsilon=eps)
            items = test_distribution(size_0)
            start = time.time()
            algorithm.solve(items)
            end = time.time()
            time_ans += end - start
        times_eps.append(time_ans / 10)

    sizes = np.arange(2, 11, 1)
    times_size = []

    for size in sizes:
        time_ans = 0
        for i in range(20):
            algorithm = BinPackingAeps(epsilon=epsilon_0)
            items = tests.random_uniform_test(size)
            start = time.time()
            algorithm.solve(items)
            end = time.time()
            time_ans += end - start
        times_size.append(time_ans / 10)

    return epsilons, times_eps, sizes, times_size
    

if __name__ == '__main__':
    test1 = testing_correstness()
    print(test1)
    eps, time_eps, size, time_size = time_testing(test_distribution = tests.random_beta_test)

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    plt.title("Зависимость времени работы от epsilon")
    plt.plot(eps, time_eps)
    plt.xlabel('Epsilon')
    plt.ylabel("Время, с")

    plt.subplot(1, 2, 2)
    plt.title("Зависимость времени работы от количества предметов")
    plt.plot(size, time_size)
    plt.xlabel("Количество предметов")
    plt.ylabel("Время, с")
    plt.show()