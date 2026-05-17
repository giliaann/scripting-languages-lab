from functools import reduce, partial
import operator

def acronym(xs: list[str]) -> str:
    return reduce(operator.add, map(lambda xs: xs[0], xs))

print(acronym(['Wielkie', 'Zagłębie', 'Lubin']))


def median(xs: list[int | float]) -> int | float:
    length = len(xs)
    ys = sorted(xs)
    middle = length//2
    return ys[middle] if length % 2 == 1 else (ys[middle - 1] + ys[middle]) / 2

print(median([1,1,19,2,3,4,4,5,1]))

def root(x: int | float, epislon: int | float) -> int | float:
    
    def root_in(y: int | float) -> int | float:
        return y if abs(y**2 - x) < epislon else root_in(0.5*(y + x/y))
        
    return root_in(1)

print(root(3, 0.1))