# -*- coding: utf-8 -*-
"""
Nathan Rice
Best first 0-1 Knapsack Problem with list of items in best solution
Draft Kings Implementation
"""
import pandas as pd
df = pd.read_csv(r'testdf.csv')

n = 142 # number of players
W = 50000 # DraftKings Salary cap
maxplayers = 8
p = list(df['dkfp']) # profit is draft kings fantasy points
w = list(df['Salary']) # players' salary is the weight
p_per_weight = list(df['points_per_dollar'])

class Priority_Queue:
    def __init__(self):
        self.pqueue = []
        self.length = 0
    
    def insert(self, node):
        for i in self.pqueue:
            get_bound(i)
        i = 0
        while i < len(self.pqueue):
            if self.pqueue[i].bound > node.bound:
                break
            i+=1
        self.pqueue.insert(i,node)
        self.length += 1

    def print_pqueue(self):
        for i in list(range(len(self.pqueue))):
            print ("pqueue",i, "=", self.pqueue[i].bound)
                    
    def remove(self):
        try:
            result = self.pqueue.pop()
            self.length -= 1
        except: 
            print("Priority queue is empty, cannot pop from empty list.")
        else:
            return result
        
class Node:
    def __init__(self, level, profit, weight):
        self.level = level
        self.profit = profit
        self.weight = weight
        self.items = []
        self.numplayers = 0

        
            
def get_bound(node):
    if node.weight >= W:
        return 0
    if node.numplayers >= maxplayers:
        return 0

    else:
        result = node.profit
        j = node.level + 1
        totweight = node.weight
        while j <= n-1 and totweight + w[j] <= W:
            totweight = totweight + w[j]
            result = result + p[j]
            j+=1
        k = j
        if k<=n-1:
            result = result + (W - totweight) * p_per_weight[k]
        return result


nodes_generated = 0
pq = Priority_Queue()

v = Node(-1, 0, 0) # v initialized to be the root with level = 0, profit = $0, weight = 0
nodes_generated+=1
maxprofit = 0 # maxprofit initialized to $0
v.bound = get_bound(v)
#print("v.bound = ", v.bound)
v.numplayers = 0
lineups = []
bestitems = []
pq.insert(v)


while pq.length != 0:
    
    v = pq.remove() #remove node with best bound
    #print("\nNode removed from pq.")
    #print("Priority Queue: ") 
    #pq.print_pqueue()
    
    #print("\nmaxprofit = ", maxprofit)
    #print("Parent Node: ")
    #print("v.level = ", v.level, "v.profit = ", v.profit, "v.weight = ", v.weight, "v.bound = ", v.bound, "v.items = ", v.items)

    if v.bound > maxprofit: #check if node is still promising
        #set u to the child that includes the next item
        u = Node(-1, 0, 0)
        nodes_generated+=1
        u.level = v.level + 1
        u.profit = v.profit + p[u.level]
        print("v.items = ", v.items)
        print("u.level = ", u.level)
        u.weight = v.weight + w[u.level]
        #take v's list and add u's list
        u.items = v.items.copy()
        u.items.append(u.level) # adds next item
        u.numplayers = len(u.items)
        #print("child that includes the next item: ")
        #print("Child 1:")
        #print("u.level = ", u.level, "u.profit = ", u.profit, "u.weight = ", u.weight)
        #print("u.items = ", u.items)
        if u.weight <= W and u.profit > maxprofit: 
            #update maxprofit
            maxprofit = u.profit
            #print("\nmaxprofit updated = ", maxprofit)
            bestitems = u.items
            lineups.append(bestitems)
            #print("bestitems = ", bestitems)
        u.bound = get_bound(u)
        #print("u.bound = ", u.bound)
        if u.bound > maxprofit:
            pq.insert(u)
            #print("Node u1 inserted into pq.")
            #print("Priority Queue : ") 
            #pq.print_pqueue()
        #set u to the child that does not include the next item
        u2 = Node(u.level, v.profit, v.weight)
        nodes_generated+=1
        u2.bound = get_bound(u2)
        u2.items = v.items.copy()
        u2.numplayers = len(u2.items)
        #print("child that doesn't include the next item: ")
        #print("Child 2:")
        #print("u2.level = ", u2.level, "u2.profit = ", u2.profit, "u2.weight = ", u2.weight, "u2.bound = ", u2.bound)
        #print("u2.items = ", u2.items)
        if u2.bound > maxprofit:
            pq.insert(u2)
            #print("Node u2 inserted into pq.")
            #print("Priority Queue : ") 
            #pq.print_pqueue()


    
print("\nEND maxprofit = ", maxprofit, "nodes generated = ", nodes_generated)
print("bestitems = ", bestitems)
