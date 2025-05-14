# Simplified Logic Theory Machine (LT) Implementation

class Expression:
    def __init__(self, connective=None, left=None, right=None, variable=None):
        self.connective = connective  # '->', 'v', '~'
        self.left = left
        self.right = right
        self.variable = variable

    def __repr__(self):
        if self.variable:
            return self.variable
        elif self.connective == '~':
            return f"~{self.left}"
        else:
            return f"({self.left} {self.connective} {self.right})"

# Axioms
axioms = [
    Expression('->', Expression('v', Expression(variable='p'), Expression(variable='p')), Expression(variable='p')),  # Axiom 1.2
    # Add more Axioms here
]

theorems = []  # Proven theorems stored here

# Helper functions
def count_levels(expr):
    if expr.variable:
        return 1
    return 1 + max(count_levels(expr.left), count_levels(expr.right))

def count_variables(expr):
    if expr.variable:
        return {expr.variable}
    return set(count_variables(expr.left)).union(count_variables(expr.right))

def is_similar(expr1, expr2):
    return (count_levels(expr1) == count_levels(expr2) and
            count_variables(expr1) == count_variables(expr2))

def find_similar(expr, memory):
    return [e for e in memory if is_similar(expr, e)]

def match_expressions(expr1, expr2, substitutions=None):
    if substitutions is None:
        substitutions = {}

    if expr1.variable:
        if expr1.variable in substitutions:
            return substitutions[expr1.variable] == expr2
        else:
            substitutions[expr1.variable] = expr2
            return True

    if expr1.connective != expr2.connective:
        return False

    left_match = match_expressions(expr1.left, expr2.left, substitutions)
    right_match = match_expressions(expr1.right, expr2.right, substitutions)
    return left_match and right_match

# Main methods
def substitution_method(expr):
    candidates = find_similar(expr, axioms + theorems)
    for candidate in candidates:
        if match_expressions(candidate, expr):
            theorems.append(expr)
            return True
    return False

def detachment_method(expr):
    for theorem in axioms + theorems:
        if theorem.connective == '->' and match_expressions(theorem.right, expr):
            if substitution_method(theorem.left):
                theorems.append(expr)
                return True
    return False

def chaining_method(expr):
    for theorem in axioms + theorems:
        if theorem.connective == '->':
            if match_expressions(theorem.left, expr.left):
                intermediate = Expression('->', theorem.right, expr.right)
                if substitution_method(intermediate):
                    theorems.append(expr)
                    return True
    return False

# Executive routine
def executive_routine(expr):
    if substitution_method(expr):
        print(f"Proved by substitution: {expr}")
        theorems.append(expr)
        return True
    elif detachment_method(expr):
        print("Proved by detachment.")
        return True
    elif chaining_method(expr):
        print("Proved by chaining.")
        return True
    else:
        print("No proof found.")
        return False

# Example usage
def main():
    # Example theorem to prove: p -> ~p -> ~p
    p = Expression(variable='p')
    not_p = Expression('~', left=p)
    theorem_2_01 = Expression('->', Expression(variable='p'), Expression('->', Expression('~', Expression(variable='p')), Expression('~', None, Expression(variable='p'))))

    result = executive_routine(theorem)
    if result:
        print("Theorem successfully proven.")
    else:
        print("Failed to prove theorem.")

if __name__ == "__main__":
    main()
