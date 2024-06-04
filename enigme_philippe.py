import pulp
prob = pulp.LpProblem("enigme",pulp.LpMinimize)

# https://www.eurodecision.com/les-casse-tetes-eurodecision/casse-tete-automne-2019

#data
I = ['A','B','C','D']
J = [1,2,3,4,5,6,7,8,9] #1 = modelisation 2 = statistiques 3 = informatique
K = [x for x in range(1,11)]
L = []
for i in I :
    for j in J :
        L.append((i,j))

#variables
x = {}
for (i,j) in L :
    x[(i,j)] = pulp.LpVariable.dicts("x_(%s,%s)"%(i,j),K, lowBound = 0, upBound = 1, cat = pulp.LpInteger)
y = pulp.LpVariable.dicts("y",J, lowBound = 0, upBound = 1, cat = pulp.LpInteger)
A = pulp.LpVariable.dicts("A",K, lowBound = 0, upBound = 1, cat = pulp.LpInteger)
B = pulp.LpVariable.dicts("B",K, lowBound = 0, upBound = 1, cat = pulp.LpInteger)
C = pulp.LpVariable.dicts("C",K, lowBound = 0, upBound = 1, cat = pulp.LpInteger)
D = pulp.LpVariable.dicts("D",K, lowBound = 0, upBound = 1, cat = pulp.LpInteger)
a = pulp.LpVariable('a', lowBound = 4, upBound = 10,cat = pulp.LpInteger )
b = pulp.LpVariable('b', lowBound = 3, upBound = 9,cat = pulp.LpInteger )
c = pulp.LpVariable('c', lowBound = 2, upBound = 8,cat = pulp.LpInteger )
d = pulp.LpVariable('d', lowBound = 1, upBound = 7,cat = pulp.LpInteger )

#objectif 
prob += a

# a>b>c>d
prob += a >= b + 1
prob += b >= c + 1
prob += c >= d + 1

#a = note maximale
for k in K :
    for j in J :
        for i in I :
            prob += k*x[(i,j)][k] <= a

# a = k <=> A[k] = 1
prob += a == sum([k*A[k] for k in K])
prob += b == sum([k*B[k] for k in K])
prob += c == sum([k*C[k] for k in K])
prob += d == sum([k*D[k] for k in K])
prob += sum([A[k] for k in K]) == 1
prob += sum([B[k] for k in K]) == 1
prob += sum([C[k] for k in K]) == 1
prob += sum([D[k] for k in K]) == 1


#les notes a,b,c,d, toujours atteintes par un candidat si le test est actif
for j in J :
    for k in K :
        prob+= sum([k*x[(i,j)][k] for i in I]) >= a - 10*(1-y[j]) - 10*(1-A[k])
        prob+= sum([k*x[(i,j)][k] for i in I]) >= b - 10*(1-y[j]) - 10*(1-B[k])
        prob+= sum([k*x[(i,j)][k] for i in I]) >= c - 10*(1-y[j]) - 10*(1-C[k])
        prob+= sum([k*x[(i,j)][k] for i in I]) >= d - 10*(1-y[j]) - 10*(1-D[k])


#d = note min
for j in J :
    for i in I :
        prob +=  sum([k*x[(i,j)][k] for k in K]) >= d - 10*(1-y[j])

#modelisation, stats, info actifs
for j in [1,2,3] :
    prob += y[j] == 1

#note positive => test passé
for i in I :
    for j in J :
            for k in K :
                prob += x[(i,j)][k] <= y[j]

#test passé => note positive 
for i in I :
    for j in J :
        prob += y[j] <= sum([x[(i,j)][k] for k in K])  

#une seule note par test
for i in I :
    for j in J :
        prob += sum([x[(i,j)][k] for k in K ]) <= y[j]

#scores des candidats
prob += sum([k*x[('A',j)][k] for k in K for j in J]) == 25
prob += sum([k*x[('B',j)][k] for k in K for j in J]) == 20
prob += sum([k*x[('C',j)][k] for k in K for j in J]) == 28
prob += sum([k*x[('D',j)][k] for k in K for j in J]) == 19

#C ne gagne jamais
for k in K :
    for j in J :
        prob += k*x[('C',j)][k] <= a-1

#D fait dernier en info
prob += sum([k*x[('D',3)][k] for k in K]) == d        
       
#C fait moins bien en modélisation qu'en algorithmique
prob += sum([k*x[('C',1)][k] for k in K]) <= sum([k*x[('C',2)][k] for k in K]) - 1

#scores différents pour chaque test actif, pour chaque candidat
for j in J :
    for k in K :
        prob += sum([x[(i,j)][k] for i in I]) <= 1 + 10*(1-y[j])

#solution réalisable avec 4 tests ?
prob+= sum([y[j] for j in J]) == 4                        

#prob.solve() 
prob.solve(pulp.solvers.CPLEX_CMD(msg=1))
#prob.solve(pulp.solvers.PULP_CBC_CMD(msg=True))
print("Status:", pulp.LpStatus[prob.status])
print('a =',round(pulp.value(a)))
print('b =',round(pulp.value(b)))
print('c =',round(pulp.value(c)))
print('d =',round(pulp.value(d)))
print()
for j in J :
    if pulp.value(y[j]) is not None :
        if pulp.value(y[j]) > 0 :
            print('test',j)

print("")
for i in I :
    print("candidat",i,sum([k*pulp.value(x[(i,j)][k]) for k in K for j in J]),"pts")
print("")
for j in J :
    if pulp.value(y[j]) > 0 :
        print("")
    for i in I :
        for k in K :
            if pulp.value(x[(i,j)][k]) is not None :
                if pulp.value(x[(i,j)][k]) >0 :
                    print('candidat',i,'test',j,'valeur',k)
     