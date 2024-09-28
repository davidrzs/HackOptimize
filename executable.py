
from pyomo.environ import *

# Create a simple model
model = ConcreteModel()

# Define sets for the time periods (3 hours)
model.T = RangeSet(1, 3)

# Define decision variables for whether the chef and cashier are working in each time period
model.chef_work = Var(model.T, domain=Binary)
model.cashier_work = Var(model.T, domain=Binary)

# Define parameters for the maximum hours chef and cashier can work
max_hours_chef = 2
max_hours_cashier = 3

# Objective: Maximize the number of hours the pizzeria is open
# The pizzeria is open if both the chef and cashier are working in a given time period
def total_hours_open(model):
    return sum(model.chef_work[t] * model.cashier_work[t] for t in model.T)

model.obj = Objective(rule=total_hours_open, sense=maximize)

# Constraints

# Chef can only work for a maximum of 2 hours
def chef_work_limit(model):
    return sum(model.chef_work[t] for t in model.T) <= max_hours_chef

model.chef_work_limit = Constraint(rule=chef_work_limit)

# Cashier can work for a maximum of 3 hours
def cashier_work_limit(model):
    return sum(model.cashier_work[t] for t in model.T) <= max_hours_cashier

model.cashier_work_limit = Constraint(rule=cashier_work_limit)

# Both chef and cashier must work during the same hours (this is implicit in the objective but let's add a constraint for clarity)
def both_working_together(model, t):
    return model.chef_work[t] == model.cashier_work[t]

model.work_together = Constraint(model.T, rule=both_working_together)

# Solve the model with Gurobi
solver = SolverFactory('gurobi')
results = solver.solve(model)

# Print the results
print("Pizzeria Schedule:")
for t in model.T:
    print(f"Hour {t}: Chef working = {int(model.chef_work[t]())}, Cashier working = {int(model.cashier_work[t]())}")
    
print(f"Total hours pizzeria is open: {int(sum(model.chef_work[t]() * model.cashier_work[t]() for t in model.T))}")
