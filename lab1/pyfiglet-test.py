from pyfiglet import Figlet

def main():
    text = input("Type text to be formatted: ")
    f = Figlet(font='slant')
    print(f.renderText(text))

if __name__ == "__main__":
    main()