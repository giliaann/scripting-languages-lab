from functools import reduce
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

def make_alpha_dict(text: str) -> dict[str, list[str]]:
    words = text.split()
    return {
        char: [word for word in words if char in word]
        for char in dict.fromkeys(text) if char.isalpha()
    }

print(make_alpha_dict("on i ona"))

def extend_and_return(x, y):
    x.extend(y)
    return x

def flatten(xs: list) -> list:
    return reduce(extend_and_return ,([x] if not isinstance(x, (list, tuple)) else flatten(x) for x in xs), [])

print(flatten([[[],1], [2, 3], [[4, 5], 6]]))

def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    
    keys = dict.fromkeys("".join(sorted(word)) for word in words)
    
    return {
        key: [word for word in words if "".join(sorted(word)) == key]
        for key in keys
    }

print(group_anagrams(['kot', 'tok', 'pies', 'kep','pek']))