
def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if all(n % p > 0 for p in primes):
            primes.append(n)
    return primes

"""
def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if not any(n % p == 0 for p in primes):
            primes.append(n)
    return primes

def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if all(n % p for p in primes):
            primes.append(n)
    return primes

def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if not any(n % p for p in primes):
            primes.append(n)
    return primes

"""
