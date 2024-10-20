import itertools

# Define the available operations
operations = ['+', '-', '*', '/']

# Helper function to safely evaluate an expression ensuring integer results and non-negative intermediate results
def safe_eval(expression):
    try:
        # Use integer division (//) when dividing to ensure integer results
        value = eval(expression.replace('/', '//'))
        if int(value) == value and value >= 0:  # Ensure non-negative results
            return int(value)
    except ZeroDivisionError:
        return None
    except Exception:
        return None
    return None

# Generate all possible ways to insert operations into the numbers
def generate_expressions(numbers):
    if len(numbers) == 1:
        yield numbers[0]
    else:
        for i in range(1, len(numbers)):
            left_part = numbers[:i]
            right_part = numbers[i:]
            for left in generate_expressions(left_part):
                for right in generate_expressions(right_part):
                    for op in operations:
                        expression = f"({left} {op} {right})"
                        if safe_eval(expression) is not None:  # Ensure valid intermediate results
                            yield expression

# Convert a mathematical expression to a readable English format
def expression_to_english(expression):
    operator_words = {'+': 'plus', '-': 'minus', '*': 'multiplied by', '/': 'divided by'}
    
    def replace_operators(match):
        return operator_words[match.group()]

    import re
    expression_in_words = re.sub(r'[+\-*/]', replace_operators, expression)

    return expression_in_words

# Try all permutations of the numbers with all combinations of operations
def find_closest_expressions(numbers, target, max_attempts=100000):
    closest_expressions = []
    closest_diff = float('inf')
    attempts = 0
    
    for num_perm in itertools.permutations(numbers):
        if attempts >= max_attempts:
            break
        expressions = generate_expressions(list(map(str, num_perm)))
        for expression in expressions:
            if attempts >= max_attempts:
                break
            value = safe_eval(expression)
            attempts += 1
            if value is not None:
                diff = abs(value - target)
                if diff < closest_diff:
                    closest_diff = diff
                    closest_expressions = [(expression, value)]
                elif diff == closest_diff:
                    closest_expressions.append((expression, value))
                
                if diff < 1e-6:
                    return closest_expressions
    
    return closest_expressions

# Main function
def main():
    numbers = input("Enter six numbers separated by spaces: ").split()
    target = int(input("Enter the target number: "))
    
    numbers = [int(num) for num in numbers]
    
    closest_expressions = find_closest_expressions(numbers, target)
    
    if closest_expressions:
        for expr, value in closest_expressions:
            english_expr = expression_to_english(expr)
            print(f"The closest expression that results in the closest value to {target} is: {expr}")
            print(f"In words: {english_expr}")
            print(f"Closest value obtained: {value}")
    else:
        print(f"No possible way to get close to the target number {target} with the given numbers.")

if __name__ == "__main__":
    main()
