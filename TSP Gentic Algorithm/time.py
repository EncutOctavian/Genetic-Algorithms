import math
from operator import indexOf
import random
import csv
import time
import numpy.random
import tsplib95
data = []
size = 2000


def generate_population(nr_of_members, coordinates):
    for i in range(nr_of_members):
        member = list(coordinates)
        random.shuffle(member)
        yield member


def fitness_function(nr_of_cities, population, nr_of_members):
    fitness = []
    score = []
    for i in range(nr_of_members):
        sum = 0
        for j in range(nr_of_cities):
            sum += math.sqrt((population[i][j][0]-population[i][j-1][0])**2+(population[i][j][1]-population[i][j-1][1])**2)
        score.append(sum)
        fitness.append(1/sum)
    return fitness,score


def selection(population, fitness, nr_of_members):
    improved_population = []
    for parent in range(200):
        max_fitness = numpy.where(fitness == numpy.max(fitness))
        max_fitness = max_fitness[0][0]
        improved_population.append(population[max_fitness])
        fitness[max_fitness] = -1
    return improved_population


def mutate(nr_of_cities,nr_of_members, population):
    for i in range(nr_of_members):
        for j in range(nr_of_cities-1):
            probability = random.uniform(0, 1)
            if probability < 0.01:
                index = random.randint(0, nr_of_cities-1)
                population[i][j], population[i][index] = population[i][index],population[i][j]
    return population


def crossover(nr_of_cities, nr_of_members, population):
    for i in range(nr_of_members-200):

        child = []
        childP1 = []
        parent1 = random.randint(0,199)
        parent2 = random.randint(0,199)
        geneA = int(random.uniform(0,1) * len(population[parent1]))
        geneB = int(random.uniform(0,1) * len(population[parent1]))
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)
        childP1[startGene:endGene+1] = list(population[parent1][startGene:endGene+1])
        childP1.extend([item for item in population[parent2] if item not in childP1])
        child = list(childP1)
        population.append(childP1)
    return population


def ga(coordinates, nr_of_cities):
    population = []
    minim = 100000000000
    for i in range(size):
        population.append(next(generate_population(size,coordinates)))
    for i in range(1000):
        fitness,score = list(fitness_function(nr_of_cities, population, size))
        for j in score:
            if j < minim:
                minim = j
                print(minim, i)
        population = list(selection(population, fitness, size))
        population = list(crossover(nr_of_cities, size, population))
        population = list(mutate(nr_of_cities, size, population))
    return minim


def simulated_annealing(coordinates,cities):
    T = 1000
    alph = 0.99
    random_path = list(coordinates)
    random.shuffle(random_path)
    while T > 0.00001:
        for i in range(0, 5000):
            index1 = random.randint(0, cities-1)
            index2 = random.randint(0, cities-1)
            flipped_random = list(random_path)
            flipped_random[index1], flipped_random[index2] = flipped_random[index2], flipped_random[index1]
            flipped_sol = 0
            random_sol = 0
            for j in range(cities):
                random_sol += math.sqrt((random_path[j][0]-random_path[j-1][0])**2+(random_path[j][1]-random_path[j-1][1])**2)
                flipped_sol += math.sqrt((flipped_random[j][0]-flipped_random[j-1][0])**2+(flipped_random[j][1]-flipped_random[j-1][1])**2)
            e = math.exp(-abs(flipped_sol-random_sol)/T)
            r = random.uniform(0, 1)
            if flipped_sol < random_sol:
                random_path = list(flipped_random)
                print(random_sol)
            elif r < e:
                random_path = list(flipped_random)
        T = T * alph
    random_sol = 0
    for j in range(cities):
        random_sol += math.sqrt((random_path[j][0]-random_path[j-1][0])**2+(random_path[j][1]-random_path[j-1][1])**2)
    return random_sol


if __name__ == "__main__":
    coordinates = []
    problem = tsplib95.load('C:/Users/Tavi/Desktop/New folder (9)/Final_Project/rat195.tsp')
    node_size = len(list(problem.get_nodes()))
    for i in range (1, node_size+1):
        coordinates.append(problem.node_coords[i])
    cities = len(coordinates)