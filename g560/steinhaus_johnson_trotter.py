def permutations(seq):
    """Generate Steinhaus Johnson Trotter permutations.

    Also known as Plain Changes.

    Args:
        seq: The sequence to be permuted. Must support both
            slicing and concatenation.

    Yields:
        Sequences of the same type of seq, with successive
        permutations of the values of seq.
    """
    if len(seq) == 0:
        yield type(seq)()
    else:
        for i, item in enumerate(permutations(seq[:-1])):
            if i % 2 == 0:
                yield from (item[:j] + seq[-1:] + item[j:]
                            for j in range(len(item) + 1))
            else:
                yield from (item[:j] + seq[-1:] + item[j:]
                            for j in range(len(item), -1, -1))
