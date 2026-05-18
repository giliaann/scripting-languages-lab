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

def pierwiastek(x: float, epsilon: float) -> float:
    def aux(y: float) -> float:
        return y if abs(y*y - x) < epsilon else aux(0.5 * (y + x/y))
    return aux(x) if x != 0.0 else 0.0

print(pierwiastek(5.0, 0.01))


def make_alpha_dict(text: str) -> dict[str, list[str]]:
    words = text.split()
    return {
        char: [word for word in words if char in word]
        for char in dict.fromkeys(text) if char.isalpha()
    }

print(make_alpha_dict("on i ona"))

def flatten(data: list) -> list:
    match data:
        case [] | ():
            return []
        case [h, *t] if not isinstance(data, (str, bytes)):
            return flatten(h) + flatten(t)
        case _:
            return [data]

print(flatten([[[],1], [2, 3], [[4, 5], 6]]))

def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    keys = dict.fromkeys("".join(sorted(word)) for word in words)
    
    return {
        key: [word for word in words if "".join(sorted(word)) == key]
        for key in keys
    }


print(group_anagrams(['kot', 'tok', 'pies', 'kep','pek']))