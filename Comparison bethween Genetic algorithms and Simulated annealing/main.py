import math
import random
import csv
import time
import numpy.random

data = []
size = 200

def bit_to_real_converter(sol, nr_of_param, left_limit, right_limit):
    nr_of_bits = math.ceil(math.log2((right_limit - left_limit) * (10 ** 5)))
    for i in range(0, nr_of_param):
        decimal = 0
        for j in range(0, nr_of_bits):
            decimal += sol[i * nr_of_bits + j] * (1 << (nr_of_bits - j - 1))
        real = left_limit + decimal * (right_limit - left_limit) / ((1 << nr_of_bits) - 1)
        yield real


def de_jong1(sol, nr_of_param):
    function_value = 0
    list_valori = list(bit_to_real_converter(sol, nr_of_param, -5.12, 5.12))
    for i in list_valori:
        function_value += i ** 2
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
        function_value += (i ** 2) - (10 * math.cos(2 * i * math.pi))
    function_value += 10 * nr_of_param
    return function_value


def michalewicz(sol, nr_of_param):
    function_value = 0
    nr_of_bits = math.ceil(math.log2((math.pi - 0) * (10 ** 5)))
    for i in range(0, nr_of_param):
        decimal = 0
        for j in range(0, nr_of_bits):
            decimal += sol[i * nr_of_bits + j] * (1 << (nr_of_bits - j - 1))
        real = 0 + decimal * (math.pi - 0) / ((1 << nr_of_bits) - 1)
        function_value += math.sin(real) * (math.sin(i * (real ** 2) / math.pi) ** 20)
    return -function_value


def random_bitstring(nr_of_bits, nr_of_param):
    bitstring = list()
    for i in range(0, nr_of_param):
        for j in range(0, nr_of_bits):
            bitstring.append(round(random.uniform(0, 1)))
    return bitstring


def generate_population(nr_of_members, nr_of_bits, nr_of_param):
    for i in range(nr_of_members):
        yield random_bitstring(nr_of_bits, nr_of_param)


def fitness_function(function, nr_of_param, population):
    fitness = []
    score = []
    if function == de_jong1:
        for i in population:
            score.append(de_jong1(i, nr_of_param))
            fitness.append(1 / score[-1])
    elif function == schwefel:
        for i in population:
            score.append(schwefel(i, nr_of_param))
            fitness.append(1 / (score[-1]))
    elif function == rastrigin:
        for i in population:
            score.append(rastrigin(i, nr_of_param))
            fitness.append(1 / score[-1])
    elif function == michalewicz:
        for i in population:
            score.append(michalewicz(i, nr_of_param))
            fitness.append(1 / score[-1])
    return fitness, score


def selection(population, fitness):
    improved_population = []
    for parent in range(50):
        max_fitness = numpy.where(fitness == numpy.max(fitness))
        max_fitness = max_fitness[0][0]
        improved_population.append(population[max_fitness])
        fitness[max_fitness] = -1
    return improved_population


def mutate(nr_of_bits, nr_of_param, population):
    for i in range(size):
        for j in range(nr_of_bits*nr_of_param):
            probability = random.uniform(0, 1)
            if probability < 0.01:
                population[i][j] = 1-population[i][j]
    return population


def crossover(nr_of_bits, nr_of_param, population):
    for i in range(size-50):
        child = []
        for k in range(50-1):
            for j in range(nr_of_bits*nr_of_param):
                    probability = random.uniform(0, 1)
                    if probability < 0.5:
                        child.append(population[k][j])
                    else:
                        child.append(population[k+1][j])
            break
        population.append(child)
    return population


def ga(function, left_limit, right_limit, nr_of_param):
    nr_of_bits = math.ceil(math.log2((right_limit - left_limit) * (10 ** 5)))
    population = []
    minim = 1000000
    for i in range(200):
        population.append(next(generate_population(200, nr_of_bits, nr_of_param)))
    for i in range(1000):
        fitness, score = list(fitness_function(function, nr_of_param, population))
        for j in score:
            if j < minim:
                minim = j
                print(minim)
        population = list(selection(population, fitness))
        population = list(crossover(nr_of_bits, nr_of_param, population))
        population = list(mutate(nr_of_bits, nr_of_param, population))
    return minim


if __name__ == '__main__':
    header = ['Dejong1 5',
              'Dejong1 10',
              'Dejong1 30',
              'Schwefel 5',
              'Schwefel 10',
              'Schwefel 30',
              'Rastrigin 5',
              'Rastrigin 10',
              'Rastrigin 30',
              'Michalewicz 5',
              'Michalewicz 10',
              'Michalewicz 30']
    table = []
    for i in range(30):
        data.append(round(ga(de_jong1, -5.12, 5.12, 5), 6))
        data.append(round(ga(de_jong1, -5.12, 5.12, 10), 6))
        data.append(round(ga(de_jong1, -5.12, 5.12, 30), 6))
        data.append(round(ga(schwefel, -500, 500, 5), 6))
        data.append(round(ga(schwefel, -500, 500, 10), 6))
        data.append(round(ga(schwefel, -500, 500, 30), 6))
        data.append(round(ga(rastrigin, -5.12, 5.12, 5), 6))
        data.append(round(ga(rastrigin, -5.12, 5.12, 10), 6))
        data.append(round(ga(rastrigin, -5.12, 5.12, 30), 6))
        data.append(round(ga(michalewicz, 0, math.pi, 5), 6))
        data.append(round(ga(michalewicz, 0, math.pi, 10), 6))
        data.append(round(ga(michalewicz, 0, math.pi, 30), 6))
        table.append(data)
        data = []
    with open('time.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(table)
    f.close()
