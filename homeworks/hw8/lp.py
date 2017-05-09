from pulp import *
 
# declare your variables
x1 = LpVariable("x1", 0, 1)   # 0<= x1 <= 40
x2 = LpVariable("x2", 0, 1) # 0<= x2 <= 1000
x3 = LpVariable("x3", 0, 1)
z = LpVariable("z", -10, 10)
 
# defines the problem
prob = LpProblem("problem", LpMaximize)
 
# defines the constraints
prob += 10*x1 - 4*x2 - 6*x3 + z <= 0 
prob += -3*x1+ 1*x2 + 9*x3 + z <= 0 
prob += -3*x1+3*x2-2*x3+z <= 0 
prob += x1+x2+x3 == 1 
prob += x1>=0
prob += x2>=0
prob += x3>=0
 
# defines the objective function to maximize
prob += z
 
# solve the problem
status = prob.solve(GLPK(msg=0))
LpStatus[status]
 
# print the results x1 = 20, x2 = 60
print(value(x1))
print(value(x2))
print(value(x3))
print(value(z))