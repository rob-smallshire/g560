import random
from functools import lru_cache
from itertools import accumulate, zip_longest, tee, chain, islice

import math
from networkx import average_shortest_path_length

from g560.gp_graph import make_symmetrical_from_permutation
from g560.permute import make_perms, permute_by_distance
from g560.zipf import zipf


def make_random_genotype(num_genes, gene_length):
    perms = make_perms(gene_length)
    genome = tuple(random.choice(perms) for _ in range(num_genes))
    return genome


def make_random_population(population_size, num_genes, gene_length):
    return tuple(make_random_genotype(num_genes, gene_length)
            for _ in range(population_size))


def rank(fitnesses, individuals, most_to_least_fit_survival_ratio=2, maximize=True):
    # Sort from most fit to least fit
    ranked_fitnesses, ranked_individuals = map(list, zip(*sorted(zip(fitnesses, individuals), reverse=maximize)))
    base = exponent_base(most_to_least_fit_survival_ratio, len(ranked_fitnesses))
    scaled_fitnesses = [pow(base, -i) for i in range(len(ranked_fitnesses))]
    return scaled_fitnesses, ranked_individuals


def exponent_base(r, n):
    return math.pow(1 / r, 1 / (1 - n))


def stochastic_universal_sample(sorted_fitnesses, sorted_individuals, num_selected, phase=None):
    if phase is None:
        phase = random.uniform(0.0, 1.0)
    elif not (0.0 <= phase <= 1.0):
        raise ValueError("phase {} out of range 0 to 1")
    cumulative_fitness = list(accumulate(sorted_fitnesses))
    total_fitness = cumulative_fitness[-1]
    spacing = total_fitness / num_selected
    start = phase * spacing
    pointers = [start + i * spacing for i in range(num_selected)]

    survivors = []
    index = 0
    for pointer in pointers:
        while cumulative_fitness[index] < pointer:
            index += 1
        survivors.append(sorted_individuals[index])

    return survivors


def batches(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def single(first):
    yield first


def wrapped_pairwise(iterable):
    a, b = tee(iterable)
    first = next(b, None)
    return zip(a, chain(b, single(first)))


def uniform_crossover(parents):
    return tuple(map(random.choice, zip(*parents)))


def zipf_mutation(individual, mutation_distribution):
    return type(individual)(permute_by_distance(perm, distance)
                            for perm, distance in zip(individual, iter(mutation_distribution.rvs, None)))


@lru_cache(maxsize=10000)
def fitness(genome):
    # Construct a 560 according the the genome
    graph = make_symmetrical_from_permutation(genome)
    # Return the average shortest path length
    aspl = average_shortest_path_length(graph)
    print(aspl, genome)
    return aspl


def shuffle(lst):
    items = lst.copy()
    random.shuffle(items)
    return items


def main(population_size):
    num_children_per_couple = 2
    if population_size % num_children_per_couple != 0:
        raise ValueError("Population size must be even")

    num_genes = 8
    gene_length = 10

    elite_count = 2  # Retain the best four
    incomers_count = 2

    assert elite_count % num_children_per_couple == 0
    assert incomers_count % num_children_per_couple == 0

    # Create initial population
    elite = (
        (
            (8, 4, 7, 5, 2, 0, 3, 1, 6, 9),
            (8, 0, 2, 9, 7, 6, 1, 5, 4, 3),
            (9, 0, 5, 8, 3, 4, 7, 6, 2, 1),
            (2, 1, 8, 0, 5, 9, 4, 7, 6, 3),
            (8, 3, 1, 4, 0, 9, 5, 6, 2, 7),
            (4, 5, 3, 7, 8, 2, 6, 1, 9, 0),
            (0, 5, 9, 4, 6, 3, 2, 8, 1, 7),
            (8, 4, 6, 2, 7, 1, 9, 0, 5, 3)
        ),
    )

    individuals = make_random_population(population_size - len(elite), num_genes, gene_length) + elite

    mutation_distribution = zipf(population_size * num_genes, 2.5)

    best = None

    try:
        while True:

            # Selection
            fitnesses = [fitness(individual) for individual in individuals]
            print(sorted(fitnesses))
            ranked_fitnesses, ranked_individuals = rank(fitnesses, individuals, most_to_least_fit_survival_ratio=10,  maximize=False)  # minimize

            best = ranked_individuals[0]
            elite = ranked_individuals[:elite_count]

            num_survivors = (len(individuals) - elite_count - incomers_count) // num_children_per_couple
            survivors = stochastic_universal_sample(ranked_fitnesses, ranked_individuals, num_survivors)

            # Combination
            shuffled_parents = shuffle(survivors)
            couples = list(wrapped_pairwise(shuffled_parents))
            children = [uniform_crossover(couple) for couple in couples for _ in range(num_children_per_couple)]

            # Mutation
            mutated_child_population = [zipf_mutation(individual, mutation_distribution) for individual in children]

            # Make room for the elite
            mutated_child_population.extend(elite)
            mutated_child_population.extend(make_random_population(incomers_count, num_genes, gene_length))
            assert len(mutated_child_population) == len(individuals)
            individuals = mutated_child_population
    finally:
        print("Best :", best)


if __name__ == '__main__':
    main(100)
