import pulp
prob = pulp.LpProblem("gcd",pulp.LpMaximize)

#data
I = [i for i in range(1,50)]
J = [i for i in range(1,541)] 

#variables
x = pulp.LpVariable.dicts("x",I, lowBound = 1, upBound = 540, cat = pulp.LpInteger)
q = pulp.LpVariable.dicts("q",I, lowBound = 1, upBound = 540, cat = pulp.LpInteger)
y = pulp.LpVariable.dicts("y",J, lowBound = 0, upBound = 1, cat = pulp.LpInteger)

#objectif 
prob += pulp.lpSum([j*y[j] for j in J])


prob += pulp.lpSum([x[i] for i in I ]) == 540
prob += pulp.lpSum([y[j] for j in J ]) == 1
for i in I :
    prob += q[i]<= x[i]
    for j in J :
        prob += x[i] <= j*q[i]+540*(1-y[j])
        prob += x[i] >= j*q[i]-49*540*(1-y[j])
"""
    if i <= 48:
        prob += x[i] == 10
        prob += q[i] == 1
    if i == 49 :
        prob += x[i] == 60
        prob += q[i] == 6
prob += y[10]==1
"""
    
#prob.solve() 
prob.solve(pulp.solvers.CPLEX_CMD(msg=1))
#prob.solve(pulp.solvers.PULP_CBC_CMD(msg=True))
print("Status:", pulp.LpStatus[prob.status])
print("Objective:", pulp.value(prob.objective))

for j in J:
    if pulp.value(y[j])> 0.9:
        print('gcd =',j)
        p=j
for i in I:
    # x = p q
    print(x[i],"=",pulp.value(x[i]),'=',p,"x",pulp.value(q[i]))