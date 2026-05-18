import functools
import sys
from task4 import make_generator, catalan_nth, fibonacci_nth




def make_generator_mem(f):
    cached = functools.lru_cache(maxsize=None)(f)
    module = sys.modules[f.__module__]
    setattr(module, f.__name__, cached)
    return make_generator(cached)



    

if __name__ == '__main__':
    gen = make_generator_mem(fibonacci_nth)
    for _ in range(40):
        print(next(gen))