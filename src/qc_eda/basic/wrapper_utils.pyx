cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def fast_check_sequence(list sequences, pattern):
    cdef int i, n = len(sequences)

    for i in range(n):
        if sequences[i] is None:
            continue
        try:
            if not pattern.fullmatch(sequences[i]):
                return False
        except:
            return False
    return True