# calculator.py
# Interactive Calculator & Unit Converter

# Conversion factors dictionary
CONVERSION_FACTORS = {
    'km_to_miles': 0.621371,
    'kg_to_pounds': 2.20462
}

def read_number(prompt):
    '''Reads input and safely converts it to a float.'''
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a number, for example 12 or 3.5.")

def add(a, b):
    '''Adds two numbers.'''
    return a + b

def subtract(a, b):
    '''Subtracts the second number from the first.'''
    return a - b

def multiply(a, b):
    '''Multiplies two numbers.'''
    return a * b

def divide(a, b):
    '''Divides the first number by the second. Handles zero division safely.'''
    if b == 0:
        return "Cannot divide by zero."
    return a / b

def km_to_miles(km):
    '''Converts kilometers to miles.'''
    return km * CONVERSION_FACTORS['km_to_miles']

def celsius_to_fahrenheit(c):
    '''Converts Celsius to Fahrenheit.'''
    return c * 9 / 5 + 32

def kg_to_pounds(kg):
    '''Converts kilograms to pounds.'''
    return kg * CONVERSION_FACTORS['kg_to_pounds']

def main():
    '''Main menu loop for the calculator.'''
    while True:
        print("\n1) Add 2) Subtract 3) Multiply 4) Divide 5) Convert units 6) Quit")
        choice = input("Choose an option: ").strip()

        if choice == "6":
            print("Goodbye!")
            break
        
        if choice in ("1", "2", "3", "4"):
            a = read_number("First number: ")
            b = read_number("Second number: ")
            
            if choice == "1":
                print("Result:", add(a, b))
            elif choice == "2":
                print("Result:", subtract(a, b))
            elif choice == "3":
                print("Result:", multiply(a, b))
            elif choice == "4":
                print("Result:", divide(a, b))
        elif choice == "5":
            print("\nUnit Conversions:")
            print("a) km to miles")
            print("b) Celsius to Fahrenheit")
            print("c) kg to pounds")
            sub_choice = input("Choose a conversion: ").strip().lower()
            
            if sub_choice == 'a':
                km = read_number("Kilometers: ")
                print("Result:", km_to_miles(km), "miles")
            elif sub_choice == 'b':
                c = read_number("Celsius: ")
                print("Result:", celsius_to_fahrenheit(c), "F")
            elif sub_choice == 'c':
                kg = read_number("Kilograms: ")
                print("Result:", kg_to_pounds(kg), "pounds")
            else:
                print("Invalid conversion choice.")
        else:
            print("Please pick a number from 1 to 6.")

if __name__ == '__main__':
    main()
