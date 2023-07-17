# Import PuLP modeler functions
from pulp import *


def print_optimal_solution_table(warehouses, projects, prob):
    # Print the variables optimized value
    for v in prob.variables():
        print(v.name, "=", v.varValue)

    # Create the optimal solution table
    table = []
    for w in warehouses:
        row = []
        for b in projects:
            var_name = "Route_{}_{}".format(w, b)
            var_value = value(prob.variablesDict()[var_name])
            row.append(var_value)
        table.append(row)

    # Print the optimal solution table
    print("\nOptimal Solution Table:")
    print("\t" + "\t".join(projects))
    for i, w in enumerate(warehouses):
        print(w, end="\t")
        for j, b in enumerate(projects):
            print(table[i][j], end="\t")
        print()

    # Print the optimized objective function value
    print("\nTotal optimal cost =", value(prob.objective))


# Creates a list of all the supply nodes
warehouses = ["A", "B", "C"]

# Creates a dictionary for the number of units of supply for each supply node
supply = {}
for warehouse in warehouses:
    supply[warehouse] = int(
        input("Enter supply for warehouse {}: ".format(warehouse)))

# Creates a list of all demand nodes
projects = ["1", "2", "3"]

# Creates a dictionary for the number of units of demand for each demand node
demand = {}
for project in projects:
    demand[project] = int(
        input("Enter demand for project {}: ".format(project)))

# Creates a list of costs of each transportation path
costs = []
for warehouse in warehouses:
    cost_row = []
    for project in projects:
        cost = int(input("Enter cost for transporting from warehouse {} to project {}: ".format(
            warehouse, project)))
        cost_row.append(cost)
    costs.append(cost_row)

# The cost data is made into a dictionary
costs = makeDict([warehouses, projects], costs, 0)

# Creates the 'prob' variable to contain the problem data
prob = LpProblem("Material Supply Problem", LpMinimize)

# Creates a list of tuples containing all the possible routes for transport
Routes = [(w, b) for w in warehouses for b in projects]

# A dictionary called 'route_vars' is created to contain the referenced variables (the routes)
route_vars = LpVariable.dicts(
    "Route", (warehouses, projects), 0, None, LpInteger)

# The minimum objective function is added to 'prob' first
prob += (
    lpSum([route_vars[w][b] * costs[w][b] for (w, b) in Routes]),
    "Sum_of_Transporting_Costs",
)

# The supply maximum constraints are added to prob for each supply node (warehouses)
for w in warehouses:
    prob += (
        lpSum([route_vars[w][b] for b in projects]) <= supply[w],
        "Sum_of_Products_out_of_warehouses_%s" % w,
    )

# The demand minimum constraints are added to prob for each demand node (project)
for b in projects:
    prob += (
        lpSum([route_vars[w][b] for w in warehouses]) >= demand[b],
        "Sum_of_Products_into_projects%s" % b,
    )

# The problem is solved using PuLP's choice of Solver
prob.solve()

# Print the optimal solution table
print_optimal_solution_table(warehouses, projects, prob)
