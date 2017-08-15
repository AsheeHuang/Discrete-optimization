#!/usr/bin/python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Carleton Coffrin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from collections import namedtuple
from gurobipy import *

Set = namedtuple("Set", ['index', 'cost', 'items'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    item_count = int(parts[0])
    set_count = int(parts[1])
    
    sets = []
    for i in range(1, set_count+1):
        parts = lines[i].split()
        sets.append(Set(i-1, float(parts[0]), parts[1:]))

    # build a trivial solution
    # pick add sets one-by-one until all the items are covered
    solution = [0]*set_count
    coverted = set()

    for s in sets:
        solution[s.index] = 1
        coverted |= set(s.items)
        if len(coverted) >= item_count:
            break
    """===========Gurobi==========="""
    m = Model("model")
    #set variable
    x = m.addVars(set_count,vtype = GRB.BINARY,name = 'x') #whether the set is chosen
    y = m.addVars(set_count,item_count,vtype = GRB.BINARY,name = 'y')
    #set objective
    m.setObjective(sum([x[i] * sets[i].cost for i in range(set_count)]),GRB.MINIMIZE)

    #set constraint
    for i in range(item_count):
        m.addConstr(y.sum("*",i) >= 1 ,"c0") #at least 1 element is chosen
    for i in range(set_count):
        m.addConstr(y.sum(i,"*")==x[i]*len(sets[i].items) , '123')

    for i in range(len(sets)):
        for j in sets[i].items:
                m.addConstr(x[i] == y[i,int(j)] , "c1")

    m.optimize()
    s = ''
    for i in m.getVars()[:set_count:]:
        s += str(int(i.x))
        s += ' '
    #print (s)

    """=========Gurobi End=========="""
    # calculate the cost of the solution
    obj = sum([s.cost*solution[s.index] for s in sets])

    # prepare the solution in the specified output format
    output_data = str(m.objVal) + ' ' + str(0) + '\n'
    output_data += s

    return output_data


import sys

if __name__ != '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/sc_6_1)')

if __name__ == '__main__' :
    f = open('./data/sc_192_0','r')
    input_data = f.read()
    print (solve_it(input_data))