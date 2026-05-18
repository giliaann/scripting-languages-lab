

def make_generator(f):
    x = 0
    while True:
        yield f(x:=x+1)

#def get_fibonacci():
#
#    cache = {
#        0: 0, 
#        1: 1
#        }
#        
#    def fibonacci(x):
#        result = cache[x] if x in cache else fibonacci(x-1) + fibonacci(x-2)
#        cache[x] = result
#        return result
#    
#    return fibonacci


#def get_catalan():
#
#    cache = {
#        0: 1, 
#        }
#        
#    def catalan(x):
#        result = cache[x] if x in cache else (2*(2*(x-1)+1)/((x-1)+2))*catalan(x-1)
#        cache[x] = result
#        return result
#    
#    return catalan

def test_generator(f, limit = 5):
    
    gen = make_generator(f)

    for _ in range(limit):
        print(next(gen))


def fibonacci_nth(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a


def catalan_nth(n):
    if n == 0:
        return 1
    
    result = 0
    for i in range(n):
        result += catalan_nth(i) * catalan_nth(n-1-i)
    return result


if __name__ == '__main__':

    print('Fibonacci test')
    #test_generator(get_fibonacci())
    test_generator(fibonacci_nth)

    print('Catalan test')
    #test_generator(get_catalan(), limit = 8)
    test_generator(catalan_nth, limit=8)

    print('Arithemtic sequence test')
    test_generator(lambda x: 0 + x*10)

    print('Geometric sequence')
    test_generator(lambda x: 5*(2**(x)))
    

