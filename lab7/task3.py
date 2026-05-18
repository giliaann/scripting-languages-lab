import random
import string

class PasswordGenerator:

    def __init__(self, length, count, charset = string.ascii_letters + string.digits):
        self.length = length
        self.max_count = count
        self.current_count = 0
        self.charset = charset

    def __iter__(self):
        return self
    
    def __next__(self):

        if self.current_count >= self.max_count:
            raise StopIteration
        
        password_chars = random.choices(self.charset, k = self.length)
        password = "".join(password_chars)
        self.current_count += 1

        return password
    
    def __len__(self):
        return self.max_count
    

if __name__ == '__main__':

    generator = PasswordGenerator(5, 10)

    
    print('For loop test')
    for password, i in zip(generator, range(len(generator))):
        print(f'Password {i}: {password}')

    generator = PasswordGenerator(10, 5)

    print('Next method test')
    for i in range(len(generator)):
        print(f'Password {i}: {next(generator)}')

    try:
        next(generator)
    except StopIteration as e:
        print(f'Stop iterationn exception caught')