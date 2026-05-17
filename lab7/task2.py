def forall (pred, iterable):
    return all(pred(x) for x in iterable)

print(forall(lambda x: x > 5, [6,7,9,9,10]))

def exists (pred, iterable):
    return any(pred(x) for x in iterable)

print(exists(lambda x: x > 5, [6,0,0,0,0]))

def atleast(n, pred, iterable):
    checked = (1 for x in iterable if pred(x))
    count = sum(1 for _ in zip(range(n), checked))
    return count == n

print(atleast(5, lambda x: x > 5, [1,2,3,4,5,6,7,8,9,10]))


def atmost(n, pred, iterable):
    checked = (1 for x in iterable if pred(x))
    count = sum(1 for _ in zip(range(n+1), checked))
    return count != n+1

print(atmost(5, lambda x: x > 1, [1,2,3,4,5,6,7,8,9,10]))