from functools import lru_cache
from random import randrange, choice

from g560.steinhaus_johnson_trotter import permutations


@lru_cache()
def make_perms(size):
    return list(permutations(tuple(range(size))))


def permute_by_distance(seq, distance):
    """Randomly permute the given sequence a given Cayley distance."""
    perms = make_perms(len(seq))
    source_index = randrange(len(perms))
    target_index = (source_index + choice((+distance, -distance))) % len(perms)
    source_indexes = perms[source_index]
    target_indexes = perms[target_index]
    items = type(seq)(seq[source_indexes.index(target_index)] for target_index in target_indexes)
    return items