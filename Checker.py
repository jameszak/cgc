# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 15:14:00 2017

@author: James Zak
"""

import networkx as nx
from numpy.random import choice
import pdb
import copy

##############
###TODO
###DEF CHECK LEGAL
###DEF LEGAL COLORS
###CODE ALICE STRAT

class Graph:
    def __init__(self, graph, numcolors):
        #Creates the graph object. Alice's strategies should be seperate functions, allowing for a graph to be set 
        #and then run with a variety of algorithms. The input graph must be a networkx object
        self.colorset = list(range(numcolors))
        self.graph = graph
        self.nodenum = nx.number_of_nodes(graph)
        self.numele = self.nodenum + nx.number_of_edges(graph)
        #saves the number of elements
        self.elelist = graph.nodes() + graph.edges()
        nx.set_node_attributes(self.graph,'color',-1)
        nx.set_edge_attributes(self.graph,'color',-1)
        self.colorings = []
        #stores the colored or partially colored graphs produced by the strategy as networkx objects
        self.record = []
        self.invalidindices = []
        #stores the indices of graphs that were only partially colored.
        self.lastmove = -1
        #stores the last move
        self.lastcolor = -1
        #stores the color of the last move
        self.neighbors = {}
        for ele in graph.nodes():
            self.neighbors[ele] = graph.neighbors(ele)
            edges = nx.edges(graph,ele)
            for edge in edges:
                self.neighbors[ele].append(tuple(sorted(edge)))
        for ele in graph.edges():
            self.neighbors[ele] = list(ele)
            edges = nx.edges(graph,list(ele))
            for edge in edges:
                if edge != ele:
                    self.neighbors[ele].append(tuple(sorted(edge)))
        self.legalcols = {}
        #creates a dictionary with keys as elements returning a list of legal colors for that element.
        for ele in self.elelist:
            self.legalcols[ele] = list(self.colorset)
        
        
    def Strategy(self,repetitions,strategy,bobstrat = None):
        #Runs the given strategy (given as a string) a set number of times. Will not halt if an unplayable graph is returned.      
        for rep in range(repetitions):
           graph = self.graph.copy()
           #creates a clean copy of the graph
           result,record,invalid = self.RunStrat(graph,strategy,bobstrat)
           self.colorings.append(result)
           self.record.append(record)
           if invalid == 1:
              self.invalidindices.append(rep)
    
    def RunStrat(self,graph,strategy,bobstrat = None):
        uncolored = list(self.elelist)
        legalcols = copy.deepcopy(self.legalcols)
        recordele = []
        recordcol = []
        self.Alice(graph,uncolored,legalcols,strategy)
        #alice makes the first move
        recordele.append(self.lastmove)
        recordcol.append(self.lastcolor)
        while uncolored != [] :
            #recursively play until either the graph is colored or no legal colors remain.
            status = self.CheckLegality(graph,legalcols,uncolored)
            if status == 1:
                break
            self.Bob(graph,uncolored,legalcols,bobstrat)
            recordele.append(self.lastmove)
            recordcol.append(self.lastcolor)
            status = self.CheckLegality(graph,legalcols,uncolored)
            if uncolored == [] or status == 1:
                break
            self.Alice(graph,uncolored,legalcols,strategy)
            recordele.append(self.lastmove)
            recordcol.append(self.lastcolor)
        if status == 1 and uncolored != []:
            validity = 1
        else:
            validity = 0
        record = [recordele,recordcol]
        return graph,record,validity
        
    def Alice(self,graph,uncolored,legalcols,strategy):
        if strategy == "D+3":
            numunc = len(uncolored)
            ele = choice(range(numunc))
            ele = uncolored[ele]
            col = int(choice(legalcols[ele]))
            self.lastmove = ele
            self.lastcolor = col
            if type(ele) == tuple :
                nx.set_edge_attributes(graph,'color',{ele:col})
            else:
                nx.set_node_attributes(graph,'color',{ele:col})  
            uncolored.remove(ele)  
            legalcols[ele].remove(col)
        else:
            print("What")
            
        
    def Bob(self,graph,uncolored,legalcols,bobstrat = None):
        #Algorithm determining Bob's next move. Currently random selection.
        if bobstrat == None:
            numunc = len(uncolored)
            ele = choice(range(numunc))
            ele = uncolored[ele]
            col = int(choice(legalcols[ele]))
            self.lastmove = ele
            self.lastcolor = col
            if type(ele) == tuple :
                nx.set_edge_attributes(graph,'color',{ele:col})
            else:
                nx.set_node_attributes(graph,'color',{ele:col})
            uncolored.remove(ele)  
            legalcols[ele].remove(col)
            
    def CheckLegality(self,graph,legalcols,uncolored):
        val = 0
        for neighbor in set(self.neighbors[self.lastmove]) & set(uncolored):
            if self.lastcolor in legalcols[neighbor]:
                legalcols[neighbor].remove(self.lastcolor)
            if legalcols[neighbor] == []:
                val = 1
        return val
         
    def SaveGraph(self,idx):
        for i in idx:
            nx.write_gexf(self.colorings[i],'renamelater' + str(i) + '.gexf')
        
        
            
            