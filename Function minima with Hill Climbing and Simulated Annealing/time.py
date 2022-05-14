import math
import random
import csv
import time


data = []

def bit_to_real_converter(sol, nr_of_param, left_limit, right_limit):
    nr_of_bits = math.ceil(math.log2((right_limit-left_limit)*(10**5)))
    for i in range(0, nr_of_param):
        decimal = 0
        for j in range(0, nr_of_bits):
            decimal += sol[i*nr_of_bits+j] * (1 << (nr_of_bits-j-1))
        real = left_limit + decimal * (right_limit-left_limit) / ((1 << nr_of_bits)-1)
        yield real


def de_jong1(sol, nr_of_param):
    function_value = 0
    list_valori = list(bit_to_real_converter(sol, nr_of_param, -5.12, 5.12))
    for i in list_valori:
        function_value += i**2
    return function_value


def schwefel(sol, nr_of_param):
    function_value = 0
    list_valori = list(bit_to_real_converter(sol, nr_of_param, -500, 500))
    for i in list_valori:
        function_value += i * math.sin(math.sqrt(abs(i)))
    function_value = 418.9829 * nr_of_param - function_value
    return function_value


def rastrigin(sol, nr_of_param):
    function_value = 0
    list_valori = list(bit_to_real_converter(sol, nr_of_param, -5.12, 5.12))
    for i in list_valori:
        function_value += (i**2) - (10 * math.cos(2*i*math.pi))
    function_value += 10 * nr_of_param
    return function_value


def michalewicz(sol, nr_of_param):
    function_value = 0
    nr_of_bits = math.ceil(math.log2((math.pi - 0) * (10 ** 5)))
    for i in range(0, nr_of_param):
        decimal = 0
        for j in range(0, nr_of_bits):
            decimal += sol[i*nr_of_bits+j] * (1 << (nr_of_bits-j-1))
        real = 0 + decimal * (math.pi-0) / ((1 << nr_of_bits)-1)
        function_value += math.sin(real) * (math.sin(i*(real**2)/math.pi)**20)
    return -function_value


def random_bitstring(nr_of_bits, nr_of_param):
    bitstring = list()
    for i in range(0, nr_of_param):
        for j in range(0, nr_of_bits):
            bitstring.append(round(random.uniform(0, 1)))
    return bitstring


def first_improvement(bitstring, function, nr_of_param):
    copy = list(bitstring)
    best_sol = function(bitstring, nr_of_param)
    for i in range(0, len(bitstring)):
        copy[i] = int(not copy[i])
        if function(copy, nr_of_param) < best_sol:
            return copy
        copy[i] = int(not copy[i])
    return bitstring


def best_improvement(bitstring, function, nr_of_param):
    copy = list(bitstring)
    best_sol = function(bitstring, nr_of_param)
    bit_sol = list(bitstring)
    for i in range(0, len(bitstring)):
        copy[i] = int(not copy[i])
        sol = function(copy, nr_of_param)
        if sol < best_sol:
            bit_sol = list(copy)
            best_sol = sol
        copy[i] = int(not copy[i])
    return bit_sol


def hill_climbing_first(function, left_limit, right_limit, nr_of_param):
    global data
    start = time.time()
    nr_of_bits = math.ceil(math.log2((right_limit - left_limit) * (10 ** 5)))
    best_bit = random_bitstring(nr_of_bits, nr_of_param)
    best_sol = function(best_bit, nr_of_param)
    random_bit = list(best_bit)
    random_sol = best_sol
    for steps in range(0, 1000):
        local = True
        while local:
            local = False
            improved_random_bit = first_improvement(random_bit, function, nr_of_param)
            improved_sol = function(improved_random_bit, nr_of_param)
            if improved_sol < random_sol:
                local = True
                random_bit = list(improved_random_bit)
                random_sol = improved_sol
        if random_sol < best_sol:
            best_sol = random_sol
            best_bit = list(random_bit)
        random_bit = random_bitstring(nr_of_bits, nr_of_param)
        random_sol = function(random_bit, nr_of_param)
    end = time.time()
    data.append(end-start)
    return best_sol


def hill_climbing_best(function, left_limit, right_limit, nr_of_param):
    global data
    start = time.time()
    nr_of_bits = math.ceil(math.log2((right_limit - left_limit) * (10 ** 5)))
    best_bit = random_bitstring(nr_of_bits, nr_of_param)
    best_sol = function(best_bit, nr_of_param)
    random_bit = list(best_bit)
    random_sol = best_sol
    for steps in range(0, 1000):
        local = True
        while local:
            local = False
            improved_random_bit = best_improvement(random_bit, function, nr_of_param)
            improved_sol = function(improved_random_bit, nr_of_param)
            if improved_sol < random_sol:
                local = True
                random_bit = list(improved_random_bit)
                random_sol = improved_sol
        if random_sol < best_sol:
            best_sol = random_sol
            best_bit = list(random_bit)
        random_bit = random_bitstring(nr_of_bits, nr_of_param)
        random_sol = function(random_bit, nr_of_param)
    end = time.time()
    data.append(end-start)
    return best_sol


def simulated_annealing(function, left_limit, right_limit, nr_of_param):
    start = time.time()
    nr_of_bits = math.ceil(math.log2((right_limit-left_limit)*(10**5)))
    T = 50
    alph = 0.99
    random_bits = random_bitstring(nr_of_bits, nr_of_param)
    while T > 0.00001:
        for i in range(0, 1000):
            index = random.randint(0, nr_of_bits*nr_of_param-1)
            random_bits[index] = int(not random_bits[index])
            flipped_random = list(random_bits)
            random_bits[index] = int(not random_bits[index])
            r = random.uniform(0, 1)
            flipped_sol = function(flipped_random, nr_of_param)
            random_sol = function(random_bits, nr_of_param)
            e = math.exp(-abs(flipped_sol-random_sol)/T)
            if flipped_sol < random_sol:
                random_bits = list(flipped_random)
            elif r < e:
                random_bits = list(flipped_random)
        T = T * alph
    end = time.time()
    data.append(end-start)
    return function(random_bits, nr_of_param)


if __name__ == '__main__':
    header = ['Dejong1 hill first 5',
              'Dejong1 hill first 10',
              'Dejong1 hill first 30',
              'Dejong1 hill best 5',
              'Dejong1 hill best 10',
              'Dejong1 hill best 30',
              'Dejong1 simulated 5',
              'Dejong1 simulated 10',
              'Dejong1 simulated 30',
              'Schwefel hill first 5',
              'Schwefel hill first 10',
              'Schwefel hill first 30',
              'Schwefel hill best 5',
              'Schwefel hill best 10',
              'Schwefel hill best 30',
              'Schwefel simulated 5',
              'Schwefel simulated 10',
              'Schwefel simulated 30',
              'Rastrigin hill first 5',
              'Rastrigin hill first 10',
              'Rastrigin hill first 30',
              'Rastrigin hill best 5',
              'Rastrigin hill best 10',
              'Rastrigin hill best 30',
              'Rastrigin simulated 5',
              'Rastrigin simulated 10',
              'Rastrigin simulated 30',
              'Michalewicz hill first 5',
              'Michalewicz hill first 10',
              'Michalewicz hill first 30',
              'Michalewicz hill best 5',
              'Michalewicz hill best 10',
              'Michalewicz hill best 30'
              'Michalewicz simulated 5',
              'Michalewicz simulated 10',
              'Michalewicz simulated 30']
    table = []
    global data
    for u in range(0, 30):
        data.append(hill_climbing_first(de_jong1, -5.12, 5.12, 5))
        data.append(hill_climbing_first(de_jong1, -5.12, 5.12, 10))
        data.append(hill_climbing_first(de_jong1, -5.12, 5.12, 30))
        data.append(hill_climbing_best(de_jong1, -5.12, 5.12, 5))
        data.append(hill_climbing_best(de_jong1, -5.12, 5.12, 10))
        data.append(hill_climbing_best(de_jong1, -5.12, 5.12, 30))
        data.append(simulated_annealing(de_jong1, -5.12, 5.12, 5))
        data.append(simulated_annealing(de_jong1, -5.12, 5.12, 10))
        data.append(simulated_annealing(de_jong1, -5.12, 5.12, 30))
        data.append(hill_climbing_first(schwefel, -500, 500, 5))
        data.append(hill_climbing_first(schwefel, -500, 500, 10))
        data.append(hill_climbing_first(schwefel, -500, 500, 30))
        data.append(hill_climbing_best(schwefel, -500, 500, 5))
        data.append(hill_climbing_best(schwefel, -500, 500, 10))
        data.append(hill_climbing_best(schwefel, -500, 500, 30))
        data.append(simulated_annealing(schwefel, -500, 500, 5))
        data.append(simulated_annealing(schwefel, -500, 500, 10))
        data.append(simulated_annealing(schwefel, -500, 500, 30))
        data.append(hill_climbing_first(rastrigin, -5.12, 5.12, 5))
        data.append(hill_climbing_first(rastrigin, -5.12, 5.12, 10))
        data.append(hill_climbing_first(rastrigin, -5.12, 5.12, 30))
        data.append(hill_climbing_best(rastrigin, -5.12, 5.12, 5))
        data.append(hill_climbing_best(rastrigin, -5.12, 5.12, 10))
        data.append(hill_climbing_best(rastrigin, -5.12, 5.12, 30))
        data.append(simulated_annealing(rastrigin, -5.12, 5.12, 5))
        data.append(simulated_annealing(rastrigin, -5.12, 5.12, 10))
        data.append(simulated_annealing(rastrigin, -5.12, 5.12, 30))
        data.append(hill_climbing_first(michalewicz, 0, math.pi, 5))
        data.append(hill_climbing_first(michalewicz, 0, math.pi, 10))
        data.append(hill_climbing_first(michalewicz, 0, math.pi, 30))
        data.append(hill_climbing_best(michalewicz, 0, math.pi, 5))
        data.append(hill_climbing_best(michalewicz, 0, math.pi, 10))
        data.append(hill_climbing_best(michalewicz, 0, math.pi, 30))
        data.append(simulated_annealing(michalewicz, 0, math.pi, 5))
        data.append(simulated_annealing(michalewicz, 0, math.pi, 10))
        data.append(simulated_annealing(michalewicz, 0, math.pi, 30))
        table.append(data)
        data = []
    with open('time.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(table)
    f.close()
