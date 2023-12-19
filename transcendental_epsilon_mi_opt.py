import sympy as sp

# Define the symbols
kappa = sp.symbols('kappa')
M_i = sp.symbols('M_i')
epsilon_i = sp.symbols('epsilon_i')
M_iter = 2.8  # This is the given guess value for the iterative process

# Define the equation for epsilon_i based on the given formula
equation = sp.Eq(epsilon_i, (1 + (kappa - 1)/2 * M_i**2)**((kappa + 1)/(2 * (kappa - 1))) / M_i / ((kappa + 1)/2)**((kappa + 1)/(2 * (kappa - 1))))

# Solve the equation for M_i
solution = sp.solve(equation, M_i)

# Assuming we are interested in real and positive solutions only
real_positive_solutions = [sol.evalf() for sol in solution if sol.is_real and sol > 0]

# If you want to use an iterative solver like the one implied by "find(Miter)",
# you could use numerical methods in libraries like scipy.optimize
# but that requires a function definition and an initial guess.
