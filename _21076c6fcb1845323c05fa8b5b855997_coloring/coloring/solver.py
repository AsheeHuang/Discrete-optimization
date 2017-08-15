#!/usr/bin/python
# -*- coding: utf-8 -*-

class vertice(object):
    def __init__(self,index,node_count):
        self.index = index
        self.edge = []
        self.color = -1 #undefine
        self.feasible_color=[True for i in range(node_count)]#up is node_count
    def __repr__(self):
        s = []
        for i in self.edge:
            s.append(i.index)
        return "index:"+str(self.index)+"   edge:"+" ".join(map(str,s))+"   color:"+str(self.color)
    def hasfeasible(self,color_num):
        for i in range(color_num):
            if self.feasible_color[i] == True:
                return i
        return -1

def solve_it(input_data):
    def insert(queue,node):
        queue.append(node)
        for i in node.edge :
            i.feasible_color[node.color] = False
    def delete(queue):
        return queue.pop(0)
    def check_true(visited):
        for i in visited :
            if i == False :
                return False
        return True
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    vertices = []
    for i in range(node_count):
        vertices.append(vertice(i,node_count))
    """add edge in every node"""
    for i in edges:
        first ,second = i[0],i[1]
        vertices[first].edge.append(vertices[second])
        vertices[second].edge.append(vertices[first])
    """ find max edge node"""
    max = 0
    for i in vertices :
        if len(i.edge) > max:
            first_node = i
            max = len(i.edge)

    """using BFS to find next node"""
    visited = [False for i in range(node_count)]

    color_num = 0

    while not check_true(visited): #all node have been visited
        first_node.color = 0
        for i in vertices:
            for j in range(color_num):
                i.feasible_color[j] = True
        BFS_queue = [] #reset queue
        insert(BFS_queue,first_node)
        visited  = [False for i in range(node_count)]
        visited[first_node.index] = True
        infeasible = False
        color_num+=1
        if color_num > node_count:
            print ("error")
            break
        while  BFS_queue : #queue is not empty
            node = delete(BFS_queue)
            for i in node.edge :
                color = i.hasfeasible(color_num) # has feasible solution
                if visited[i.index] == False and color >= 0:
                    i.color = color
                    insert(BFS_queue,i)
                    visited[i.index] = True
                    #print (i)
                elif color < 0:
                    infeasible = True
                    break
            if infeasible :
                break
    for i in vertices:
        print (i)
    solution = [i.color for i in vertices]

    # prepare the solution in the specified output format
    output_data = str(color_num) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

if __name__ == '__main__':   #for test
    f = open('./data/gc_50_1','r')
    input_data = f.read()
    print(solve_it(input_data))