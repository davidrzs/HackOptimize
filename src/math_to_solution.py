import time

from ai21 import AI21Client
from ai21.models.chat import ChatMessage

model = "jamba-1.5-large"

client = AI21Client(
    api_key="6tHa1Ly9bLfewfSO3gqnYRBQ15FFBhhl",
)


def text_to_math(task_description: str):
    messages_step1 = [
        ChatMessage(content="""
                            You are an Operations Research scientist. You are trying to solve a scheduling problem.
                            You will be given a problem and you will need to translate it into mathematical notation.
                            Your task is to translate the problem into an optimization problem.

                            The problem should be formulated with one the following objectives:
                            1. Minimize time from start to finish of all required jobs
                            2. Minimize resource consumed
                            3. Minimize downtime between jobs
                            4. Maximize an output like number of items produced or profit


                            Decisions variables can for example be:
                            1. Start time for each job, machine pair
                            2. Makespan completion
                            3. Number of items produced by each machine

                            Constraints can for example be:
                            1. Each job must be done once
                            2. Each machine can only do one job at a time
                            3. Each job must be done in a certain order
                            4. Each job must be done within a certain time frame
                            5. Maximum number of jobs that can be done in a day
                            6. There might be downtime required between jobs

                            The problem should be formulated in the following format, :
                            Objective function: Minimize or Maximize
                            Decision variables: x1, x2, x3, ...
                            Constraints: c1, c2, c3, ...
                            """, role="system"),
        ChatMessage(content=task_description, role="user"),
    ]
    chat_completions = client.chat.completions.create(
                messages=messages_step1,
                model=model,
            )

    return chat_completions.choices[0].message.content

def math_to_code(math_input: str):
    messages_step2 = [
            ChatMessage(content="""
                        You are professional mathematical modeler that's expert in pyomo. 
                        Here is an example of a pyomo model:

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

                        # Solve the model
                        solver = SolverFactory('glpk')
                        results = solver.solve(model)

                        # Print the results
                        print("Pizzeria Schedule:")
                        for t in model.T:
                            print(f"Hour {t}: Chef working = {int(model.chef_work[t]())}, Cashier working = {int(model.cashier_work[t]())}")
                            
                        print(f"Total hours pizzeria is open: {int(sum(model.chef_work[t]() * model.cashier_work[t]() for t in model.T))}")
                        """, 
                        role="system"),
            ChatMessage(content="transform this solution into pyomo model that can be solved with gurobi.", role="user"),
            ChatMessage(content=math_input, role="user"),
    ]
    chat_completions = client.chat.completions.create(
                messages=messages_step2,
                model=model,
            )
    return chat_completions.choices[0].message.content
    


def process_task(task_description):
    # Simulating work
    time.sleep(2)
    return f"Task '{task_description}' has been processed successfully!"
