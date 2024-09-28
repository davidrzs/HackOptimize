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
                        You are professional mathematical modeler that's expert in pyomo and gurobi. 
                        Here is an example of a pyomo model and solving it with gurobi:
                        import matplotlib.pyplot as plt
                        from IPython.display import display
                        import pandas as pd

                        import shutil
                        import sys
                        import os.path

                        # test for pyomo and install if necessary
                        if not shutil.which("pyomo"):
                            !pip install -q pyomo
                            assert(shutil.which("pyomo"))

                        # test for cbc and install if necessary
                        if not (shutil.which("cbc") or os.path.isfile("cbc")):
                            if "google.colab" in sys.modules:
                                !apt-get install -y -qq coinor-cbc
                            else:
                                try:
                                    !conda install -c conda-forge coincbc 
                                except:
                                    pass
                                
                        assert(shutil.which("cbc") or os.path.isfile("cbc"))

                        from pyomo.environ import *
                        from pyomo.gdp import *

                        JOBS = {
                            'A': {'release': 2, 'duration': 5, 'due': 10},
                            'B': {'release': 5, 'duration': 6, 'due': 21},
                            'C': {'release': 4, 'duration': 8, 'due': 15},
                            'D': {'release': 0, 'duration': 4, 'due': 10},
                            'E': {'release': 0, 'duration': 2, 'due':  5},
                            'F': {'release': 8, 'duration': 3, 'due': 15},
                            'G': {'release': 9, 'duration': 2, 'due': 22},
                        }

                        def schedule(JOBS, order=sorted(JOBS.keys())):
                            start = 0
                            finish = 0
                            SCHEDULE = {}
                            for job in order:
                                start = max(JOBS[job]['release'], finish)
                                finish = start + JOBS[job]['duration']
                                SCHEDULE[job] = {'start': start, 'finish': finish}
                            return SCHEDULE
                        
                        SCHEDULE = schedule(JOBS)
                        
                        def kpi(JOBS, SCHEDULE):
                            KPI = {}
                            KPI['Makespan'] = max(SCHEDULE[job]['finish'] for job in SCHEDULE)
                            KPI['Max Pastdue'] = max(max(0, SCHEDULE[job]['finish'] - JOBS[job]['due']) for job in SCHEDULE)
                            KPI['Sum of Pastdue'] = sum(max(0, SCHEDULE[job]['finish'] - JOBS[job]['due']) for job in SCHEDULE)
                            KPI['Number Pastdue'] = sum(SCHEDULE[job]['finish'] > JOBS[job]['due'] for job in SCHEDULE)
                            KPI['Number on Time'] = sum(SCHEDULE[job]['finish'] <= JOBS[job]['due'] for job in SCHEDULE)
                            KPI['Fraction on Time'] = KPI['Number on Time']/len(SCHEDULE)
                            return KPI
                        
                        kpi(JOBS, SCHEDULE)

                        order = sorted(JOBS, reverse=True)
                        gantt(JOBS, schedule(JOBS,order))
                        kpi(JOBS, schedule(JOBS,order))

                        def opt_schedule(JOBS):

                            # create model
                            m = ConcreteModel()

                            # index set to simplify notation
                            m.J = Set(initialize=JOBS.keys())
                            m.PAIRS = Set(initialize = m.J * m.J, dimen=2, filter=lambda m, j, k : j < k)

                            # upper bounds on how long it would take to process all jobs
                            tmax = max([JOBS[j]['release'] for j in m.J]) + sum([JOBS[j]['duration'] for j in m.J])

                            # decision variables
                            m.start      = Var(m.J, domain=NonNegativeReals, bounds=(0, tmax))
                            m.pastdue    = Var(m.J, domain=NonNegativeReals, bounds=(0, tmax))
                            m.early      = Var(m.J, domain=NonNegativeReals, bounds=(0, tmax))

                            # additional decision variables for use in the objecive
                            m.makespan   = Var(domain=NonNegativeReals, bounds=(0, tmax))
                            m.maxpastdue = Var(domain=NonNegativeReals, bounds=(0, tmax))
                            m.ispastdue  = Var(m.J, domain=Binary)

                            # objective function
                            m.OBJ = Objective(expr = sum([m.pastdue[j] for j in m.J]), sense = minimize)

                            # constraints
                            m.c1 = Constraint(m.J, rule=lambda m, j: m.start[j] >= JOBS[j]['release'])
                            m.c2 = Constraint(m.J, rule=lambda m, j: 
                                    m.start[j] + JOBS[j]['duration'] + m.early[j] == JOBS[j]['due'] + m.pastdue[j])
                            m.c3 = Disjunction(m.PAIRS, rule=lambda m, j, k:
                                [m.start[j] + JOBS[j]['duration'] <= m.start[k], 
                                 m.start[k] + JOBS[k]['duration'] <= m.start[j]])    

                            m.c4 = Constraint(m.J, rule=lambda m, j: m.pastdue[j] <= m.maxpastdue)
                            m.c5 = Constraint(m.J, rule=lambda m, j: m.start[j] + JOBS[j]['duration'] <= m.makespan)
                            m.c6 = Constraint(m.J, rule=lambda m, j: m.pastdue[j] <= tmax*m.ispastdue[j])

                            TransformationFactory('gdp.chull').apply_to(m)
                            SolverFactory('gurobi').solve(m).write()

                            SCHEDULE = {}
                            for j in m.J:
                                SCHEDULE[j] = {'machine': 1, 'start': m.start[j](), 'finish': m.start[j]() + JOBS[j]['duration']}

                            return SCHEDULE

                        SCHEDULE = opt_schedule(JOBS)
                        gantt(JOBS, SCHEDULE)
                        kpi(JOBS, SCHEDULE)
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
