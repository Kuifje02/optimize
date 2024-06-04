from pulp import *

# define data
players = ["Bill", "Ernie", "Oscar", "Sammy", "Tony"]
nicknames = ["Slats", "Stretch", "Tiny", "Tower", "Tree"]
heights = [6, 6.1, 6.3, 6.5, 6.6]

# create problem
prob = LpProblem("B_Balls", LpMinimize)

# define variables
x = LpVariable.dicts("x", (players, nicknames, heights), cat=LpBinary)

# add dummy objective function
prob += 0

# each player has a unique nickame and height
for p in players:
    prob += lpSum(x[p][n][h] for n in nicknames for h in heights) == 1

# each nickname has a unique player and height
for n in nicknames:
    prob += lpSum(x[p][n][h] for p in players for h in heights) == 1

# each height has a unique player and nickname
for h in heights:
    prob += lpSum(x[p][n][h] for n in nicknames for p in players) == 1

# Oscar is taller than Tree
for n in nicknames:
    for h in heights:
        prob += x["Oscar"][n][h] <= lpSum(
            x[p]["Tree"][k] for p in players for k in heights if k < h
        )

# Tree is taller than Tony
for p in players:
    for h in heights:
        prob += x[p]["Tree"][h] <= lpSum(
            x["Tony"][n][k] for n in nicknames for k in heights if k < h
        )

# Bill is taller than Sammy
for n in nicknames:
    for h in heights:
        prob += x["Bill"][n][h] <= lpSum(
            x["Sammy"][m][k] for m in nicknames for k in heights if k < h
        )

# Bill is shorter than Slats
for n in nicknames:
    for h in heights:
        prob += x["Bill"][n][h] <= lpSum(
            x[p]["Slats"][k] for p in players for k in heights if k > h
        )

# Tony is not Tiny
for h in heights:
    prob += x["Tony"]["Tiny"][h] == 0

# Stretch is taller than Oscar
for p in players:
    for h in heights:
        prob += x[p]["Stretch"][h] <= lpSum(
            x["Oscar"][n][k] for n in nicknames for k in heights if k < h
        )

# Stretch is not the tallest
for p in players:
    prob += x[p]["Stretch"][6.6] == 0

# solve problem
# prob.writeLP("basketball.lp")
k = 1
while True:
    print()
    print("solution %s" % k)
    k += 1
    # prob.solve(pulp.PULP_CBC_CMD(msg=0))
    prob.solve(CPLEX_CMD(msg=1))
    print("Status:", LpStatus[prob.status])
    # The solution is printed if it was deemed "optimal" i.e met the constraints
    if LpStatus[prob.status] == "Optimal":
        # print solution
        for p in players:
            for n in nicknames:
                for h in heights:
                    if value(x[p][n][h]) > 0.1:
                        print(p, n, h)
        # The constraint is added that the same solution cannot be returned again
        prob += (
            lpSum(
                [
                    x[p][n][h]
                    for p in players
                    for n in nicknames
                    for h in heights
                    if value(x[p][n][h]) > 0.1
                ]
            )
            <= 5 - 1
        )
    # If a new optimal solution cannot be found, we end the program
    else:
        break
