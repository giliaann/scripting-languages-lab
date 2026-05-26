import functools


def count_calls(func):
    func.called = 0
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.called += 1
        return func(*args, **kwargs)
    return wrapper
        


@count_calls
def add(a, b):
    return a+b


if __name__=='__main__':
    print(add(1,2))
    add(3,4)
    print(add.called)