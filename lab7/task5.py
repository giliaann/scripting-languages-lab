import functools
import sys
from task4 import make_generator, catalan_nth, fibonacci_nth
import types



def make_generator_mem(f):
    new_globals = f.__globals__.copy()
    function_copy = types.FunctionType(
        f.__code__,
        new_globals,
        name=f.__name__,
        argdefs=f.__defaults__,
        closure=f.__closure__
    )
    
    cached = functools.lru_cache(maxsize=None)(function_copy)
    new_globals[f.__name__] = cached
    
    return make_generator(cached)



    

if __name__ == '__main__':
    gen_mem = make_generator_mem(fibonacci_nth)
    for _ in range(38):
        print(next(gen_mem))
    
    gen = make_generator(fibonacci_nth)
    for _ in range(38):
        print(next(gen))

    

    #module = sys.modules[f.__module__]
    #setattr(module, f.__name__, cached)