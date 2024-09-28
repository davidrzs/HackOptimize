
import pulp

# --- Data Representation ---

# Production Rates (example)
production_rates = {
    'Cheese': {'Line1': 100, 'Line2': 150},
    'Pepperoni': {'Line1': 80, 'Line2': 120},
    'Hawaiian': {'Line1': 90, 'Line2': 130},
}

# Time Constraints (example)
time_constraints = {
    'Cheese': {'Cleaning': (6, 8)},  # Cleaning from 6am to 8am
    'Pepperoni': {'Maintenance': (10, 12)},  # Maintenance from 10am to 12pm
}

# Quotas (example)
quotas = {'Cheese': 500, 'Pepperoni': 400, 'Hawaiian': 300}

# Operating Hours (24/7)
operating_hours = [(t, t + 1) for t in range(24)]

# Production Run Minimum (2 hours)
production_run_min = 2

# --- MILP Formulation ---

# Decision Variables
x = pulp.LpVariable.dicts(
    "x",
    ((p, l, t) for p in production_rates for l in production_rates[p] for t in operating_hours),
    cat="Binary",
)

# Objective Function
prob = pulp.LpProblem("PizzaProduction", pulp.LpMaximize)
prob.setObjective(pulp.lpSum(x[p, l, t] for p, l, t in x), sense=pulp.LpMaximize)

# Constraints

# Production Rate
for p, l, t in x:
    prob += x[p, l, t] * production_rates[p][l] <= quotas[p]

# Time Constraints
for p, l, t in x:
    # 1-hour gap between different pizza types
    prob += x[p, l, t] * x[p, l, t + 1] == 0
    # 2-hour gap for maintenance every 24 hours
    prob += x[p, l, t] * x[p, l, t + 24] == 0

# Line Availability
for l in production_rates:
    prob += pulp.lpSum(x[p, l, t] for p in production_rates for t in operating_hours) <= 2

# Production Run Minimum
for p, l, t in x:
    prob += x[p, l, t] + x[p, l, t + 1] >= 2

# --- Handling Unexpected Events ---

# Example: Hawaiian Topping Shortage
hawaiian_shortage = False  # Set to True if shortage occurs
if hawaiian_shortage:
    for t in operating_hours:
        prob += x['Hawaiian', 'Line1', t] + x['Hawaiian', 'Line2', t] <= 2  # Reduce production rate

# --- Solver ---

prob.solve()

# --- Results ---

print("Status:", pulp.LpStatus[prob.status])
print("Total Pizzas Produced:", pulp.value(prob.objective))

# Analyze the solution and print the schedule for each pizza type on each line and time slot.
for p in production_rates:
    for l in production_rates[p]:
        for t in operating_hours:
            if x[p, l, t].varValue == 1:
                print(f"Pizza {p} produced on Line {l} at time {t}")

