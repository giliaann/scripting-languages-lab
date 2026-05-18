import logging
import time
from functools import wraps


logging.basicConfig(level=logging.DEBUG)


def log(level=logging.INFO):
    def decorator(obj):
        if isinstance(obj, type):
            orig_init = obj.__init__
            @wraps(orig_init)
            def new_init(self, *args, **kwargs):
                logging.log(level, f"Instantiating the class: {obj.__name__}")
                orig_init(self, *args, **kwargs)
            obj.__init__ = new_init
            return obj
        else:
            @wraps(obj)
            def wrapper(*args, **kwargs):
                call_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                start_time = time.perf_counter()
                result = obj(*args, **kwargs)
                end_time = time.perf_counter()
                duration = end_time - start_time
                logging.log(
                    level,
                    f"Time: {call_time_str} | Duration: {duration:.6f}s | Function: {obj.__name__} | Args: {args} | Kwargs: {kwargs} | Result: {result}"
                )
                return result
            return wrapper
    return decorator
    


if __name__ ==    '__main__':
    @log(level=logging.INFO)
    def add(a, b):
        return a+b
    
    @log()
    class Dog():
        def __init__(self, name):
            self.name = name

        def bark(self):
            print("hau hau hau")

        def getFullName(self, surname):
            return self.name + " " + surname
        
    res1 = add(1,2)

    res2 = Dog('rufus')
    
        
    