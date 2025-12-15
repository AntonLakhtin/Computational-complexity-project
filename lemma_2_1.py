from typing import List

def generate_bin_types(values_cnt, values_list, ind_values, capacity=1.0):
    all_bin_types = []
    if (ind_values == len(values_list)):
        return [[]]
    cnt = 0
    cur_cap = capacity
    while (cnt <= values_cnt[values_list[ind_values]] and cur_cap >= 0):
        bins = generate_bin_types(values_cnt, values_list, ind_values + 1, cur_cap)
        for bin in bins:
            for j in range(cnt):
                bin.append(values_list[ind_values])
        all_bin_types.extend(bins)
        cnt += 1
        cur_cap -= values_list[ind_values]
    return all_bin_types

def lemma2_1(items: List[float]) -> List[List[int]]:
        """
        Лемма 2.1: Оптимальная упаковка для случая с постоянным числом размеров.
        
        Получает: items: список предметов (все размеры >= epsilon)
            
        Возвращает: Упаковка предметов по корзинам (соответствующие номера предметов) в виде списка корзин
        """
        if not items:
            return []
        
        n = len(items)
        
        set_values = set()
        for item in items:
            set_values.add(item)
        
        values_indexes = {}
        for i in range(len(items)):
            item = items[i]
            if item in values_indexes:
                values_indexes[item].append(i)
            else:
                values_indexes[item] = [i]

        values_list = list(set_values)
        values_cnt = {}
        for item in items:
            if item in values_cnt:
                values_cnt[item] += 1
            else:
                values_cnt[item] = 1

        bin_types = generate_bin_types(values_cnt, values_list, 0)


        def generate_packings(bin_index, remaining_values_cnt):
            if (bin_index == len(bin_types)):
                return [[]]
            if (bin_types[bin_index] == []):
                bin_index += 1
            if (bin_index == len(bin_types)):
                return [[]]
            
            all_packings = []
            cnt = 0
            while (True):
                packings = generate_packings(bin_index + 1, remaining_values_cnt)
                for pack in packings: 
                    for j in range(cnt):
                        pack.append(bin_types[bin_index])
                all_packings.extend(packings)
                cnt += 1

                for item in bin_types[bin_index]:
                    remaining_values_cnt[item] -= 1

                correctness = True
                for (key, value) in remaining_values_cnt.items():
                    if (value < 0):
                        correctness = False
                    
                if (not correctness):
                    break
            for item in bin_types[bin_index]:
                remaining_values_cnt[item] += cnt

            return all_packings
        
        all_packings = generate_packings(0, values_cnt)

        opt = n + 1
        best_packing = []
        for packing in all_packings:
            general_cnt = 0
            for bin in packing:
                general_cnt += len(bin)
            if (general_cnt == n):
                if (len(packing) < opt):
                    opt = len(packing)
                    best_packing = packing
        
        curent_indexes = {}
        for value in values_list:
            curent_indexes[value] = 0

        answer = [[] for _ in range(len(best_packing))]
        for i, bin in enumerate(best_packing):
            for item in bin:
                answer[i].append(values_indexes[item][curent_indexes[item]])
                curent_indexes[item] += 1
        return answer