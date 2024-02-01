import sys
import random

# Numbers
num1 = int(sys.argv[1])
num2 = int(sys.argv[2])


def generate_random_number(min_value, max_value):
    return random.randint(min_value, max_value)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 random_number.py <number1> <number2>")
        sys.exit(1)

    if num1 >= num2:
        print("Error: First number should be lesser than second number.")
        sys.exit(1)

    result = generate_random_number(num1, num2)
    print(f"Random number between {num1} and {num2}: {result}")


if __name__ == "__main__":
    main()
