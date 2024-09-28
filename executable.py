import pyomo.environ as pyo

# Define sets
TIRE_TYPES = {
    'Standard', 'Performance', 'All-Terrain', 'Winter', 'Run-Flat'
}

PRODUCTION_LINES = {
    'A', 'B', 'C'
}

TIME_PERIODS = list(range(1, 29))  # 4 weeks * 7 days

# Define parameters
weekly_quotas = {
    'Standard': 500,
    'Performance': 300,
    'All-Terrain': 200,
    'Winter': 100,
    'Run-Flat': 50
}

production_rates = {
    ('Standard', 'A'): 10,
    ('Performance', 'A'): 8,
    ('Standard', 'B'): 12,
    ('Performance', 'B'): 10,
    ('Standard', 'C'): 15,
    ('Performance', 'C'): 12,
    ('All-Terrain', 'B'): 8,
    ('All-Terrain', 'C'): 10,
    ('Winter', 'B'): 6,
    ('Winter', 'C'): 8,
    ('Run-Flat', 'B'): 5,
    ('Run-Flat', 'C'): 7
}

time_constraints = {
    'c_range': [45, 75],
    'd_range': [90, 150],
    'w_time': 4,  # hours
    'q_range': [20, 40],
    'e_time': 6,  # hours
    'p_time': 2.5,  # hours
    'h_range': [0.05, 0.15]
}

raw_materials = {
    t: 10000 for t in TIME_PERIODS
}

storage_capacity = 12000

degradation_factor = 0.001

remaining_usable_tires = 50000

# Define the model
model = pyo.ConcreteModel()

# Define sets in the model
model.TIRE_TYPES = pyo.Set(initialize=TIRE_TYPES)
model.PRODUCTION_LINES = pyo.Set(initialize=PRODUCTION_LINES)
model.TIME_PERIODS = pyo.Set(initialize=TIME_PERIODS)

# Define decision variables
model.x = pyo.Var(model.TIRE_TYPES, model.PRODUCTION_LINES, model.TIME_PERIODS, domain=pyo.NonNegativeReals)
model.s = pyo.Var(model.PRODUCTION_LINES, model.TIME_PERIODS, domain=pyo.NonNegativeReals)
model.d = pyo.Var(model.PRODUCTION_LINES, model.TIME_PERIODS, domain=pyo.NonNegativeReals)
model.c = pyo.Var(model.PRODUCTION_LINES, model.TIME_PERIODS, domain=pyo.NonNegativeReals)
model.w = pyo.Var(model.PRODUCTION_LINES, model.TIME_PERIODS, domain=pyo.NonNegativeReals)
model.q = pyo.Var(model.PRODUCTION_LINES, model.TIME_PERIODS, domain=pyo.NonNegativeReals)
model.e = pyo.Var(model.TIME_PERIODS, domain=pyo.Binary)
model.p = pyo.Var(model.TIME_PERIODS, domain=pyo.Binary)
model.h = pyo.Var(model.TIME_PERIODS, domain=pyo.NonNegativeReals)

# Define the objective function
def obj_rule(model):
    return sum(model.x[i, j, t] for i in model.TIRE_TYPES for j in model.PRODUCTION_LINES for t in model.TIME_PERIODS)

model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

# Define constraints
def production_rates_rule(model, i, t):
    return sum(model.x[i, j, t] for j in model.PRODUCTION_LINES) >= weekly_quotas[i]

model.production_rates = pyo.Constraint(model.TIRE_TYPES, model.TIME_PERIODS, rule=production_rates_rule)

def production_line_capabilities_rule(model, i, j, t):
    if i not in {'Standard', 'Performance'} and j == 'A':
        return model.x[i, j, t] == 0
    else:
        return pyo.Constraint.Skip

model.production_line_capabilities = pyo.Constraint(model.TIRE_TYPES, model.PRODUCTION_LINES, model.TIME_PERIODS, rule=production_line_capabilities_rule)

def time_constraints_rule(model, j, t):
    if t < max(model.TIME_PERIODS):
        return model.s[j, t+1] >= model.s[j, t] + sum(model.x[i, j, t] / production_rates[(i, j)] for i in model.TIRE_TYPES) + model.c[j, t] + model.d[j, t] + model.w[j, t] + model.q[j, t]
    else:
        return pyo.Constraint.Skip

model.time_constraints = pyo.Constraint(model.PRODUCTION_LINES, model.TIME_PERIODS, rule=time_constraints_rule)

def cleaning_and_maintenance_rule(model, j, t):
    return model.c[j, t] >= time_constraints['c_range'][0]

model.cleaning_and_maintenance = pyo.Constraint(model.PRODUCTION_LINES, model.TIME_PERIODS, rule=cleaning_and_maintenance_rule)

def raw_material_deliveries_rule(model, t):
    return sum(model.x[i, j, t] for i in model.TIRE_TYPES for j in model.PRODUCTION_LINES) <= raw_materials[t]

model.raw_material_deliveries = pyo.Constraint(model.TIME_PERIODS, rule=raw_material_deliveries_rule)

def production_run_duration_rule(model, j, t):
    if t < max(model.TIME_PERIODS):
        return 3 <= model.s[j, t+1] - model.s[j, t] <= 8
    else:
        return pyo.Constraint.Skip

model.production_run_duration = pyo.Constraint(model.PRODUCTION_LINES, model.TIME_PERIODS, rule=production_run_duration_rule)

def staffing_issues_rule(model, j, t):
    return model.efficiency[j, t] == base_efficiency * (1 - trainee_factor) * (1 - understaffing_probability)

model.staffing_issues = pyo.Constraint(model.PRODUCTION_LINES, model.TIME_PERIODS, rule=staffing_issues_rule)

def quality_control_rule(model, j, t):
    return model.q[j, t] >= time_constraints['q_range'][0]

model.quality_control = pyo.Constraint(model.PRODUCTION_LINES, model.TIME_PERIODS, rule=quality_control_rule)

def unexpected_events_rule(model, t):
    return model.e[t] == 1

model.unexpected_events = pyo.Constraint(model.TIME_PERIODS, rule=unexpected_events_rule)

def market_demands_rule(model, t):
    if temperature_drops_below_freezing:
        return sum(model.x['Winter', j, t] for j in model.PRODUCTION_LINES) >= 1.3 * weekly_quotas['Winter']
    else:
        return pyo.Constraint.Skip

model.market_demands = pyo.Constraint(model.TIME_PERIODS, rule=market_demands_rule)

def additional_considerations_rule(model, t):
    return sum(model.x[i, j, t] for i in model.TIRE_TYPES for j in model.PRODUCTION_LINES) <= storage_capacity

model.additional_considerations = pyo.Constraint(model.TIME_PERIODS, rule=additional_considerations_rule)

# Solve the model
solver = pyo.SolverFactory('gurobi')
results = solver.solve(model)

# Display the results
model.display()
