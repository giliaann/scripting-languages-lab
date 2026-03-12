import sys

def countArea(base, height):
    return base * height / 2

def getUserInput():
    print("Enter triangle data.")
    base = input("Base: ")
    height = input("Height: ")
    return base, height

def parsePositiveInteger(n):
    n = int(n) 
    if(n <= 0): 
        raise ValueError("Invalid argument - value must be positive")
    return n

def main():

    base, height = getUserInput()
    
    valid_data = True

    try:
        base = parsePositiveInteger(base)
    except ValueError as e:
        print(f"Invalid base - {e}", file = sys.stderr)
        valid_data = False

    try:
        height = parsePositiveInteger(height)
    except ValueError as e:
        print(f"Invalid height - {e}", file = sys.stderr)
        valid_data = False
    
    if not valid_data:
        return

    print(f"Area of given triangle: {countArea(base,height)}")
    
if __name__ == "__main__":
    main()