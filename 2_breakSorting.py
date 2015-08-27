#!/usr/bin/env python
'''
2-Break Sorting Problem: Find a shortest transformation of one genome into another by 2-breaks.
	Input: Two genomes with circular chromosomes on the same set of synteny blocks.
	Output: The sequence of genomes resulting from applying a shortest sequence of 2-breaks
			transforming one genome into the other.
'''
__author__ = 'Yue Wang'


import time
import random
import sys


def output(p):
	'''
	Format p.
	if p is in one genome with many chromosomes, then this enables output in a same line
	'''
	sys.stdout.write("(%s)" % ' '.join(["%+d" % e for e in p]))


def shrtReSnr(P, D):
	'''
	Shortest rearrangement scenario
	'''
	for each in P:
		output(each)
	print ''

	Pred = coloredEdges(P)
	Pblack = blackEdges(P)
	redEdges = coloredEdges(P)
	blueEdges = coloredEdges(D)
	# breakpoint: print redEdges
	# breakpoint: print blueEdges

	breakPointGraph = graphBuilt(redEdges, blueEdges)
	cycleSearch = DFScycle(breakPointGraph)
	cycleNumber = cycleSearch[0]
	cycles = cycleSearch[1]
	nonTrivalCycle = cycleSearch[2]

	# increase number of trival cycles
	while nonTrivalCycle != []:
		# (n, j): randomly choose an arbitary edge from blueEdges in a non-trival cycle
		blue_nontrival = []
		for each in blueEdges:
			if each[0] in nonTrivalCycle[0] and each[1] in nonTrivalCycle[0]:
				blue_nontrival.append(each)
		ranchoice = random.randint(0, len(blue_nontrival) - 1)
		n, j = blue_nontrival[ranchoice][0], blue_nontrival[ranchoice][1]

		# (i, n) an edge from redEdges originate at node n
		for each in redEdges:
			if n in each:
				for k in each:
					if k != n:
						i = k
			else:
				continue

		# (j, m) an edge from redEdges originate at node j
		for each in redEdges:
			if j in each:
				for k in each:
					if k != j:
						m = k
			else:
				continue

		# remove (i, n), (j, m) from redEdges
		# add new edge (n, j) (m, i)
		redEdges = breakOnGenoGraph(redEdges, i, j, n, m)
		# breakpoint: print redEdges

		# update the breakpointgraph
		breakPointGraph = graphBuilt(redEdges, blueEdges)
		cycleSearch = DFScycle(breakPointGraph)
		cycleNumber = cycleSearch[0]
		cycles = cycleSearch[1]
		nonTrivalCycle = cycleSearch[2]

		# change P
		# remove edges from Pgraph using blackEdges and DFScycle
		selfGraph = graphBuilt(redEdges, Pblack)
		selfCycle = DFScycle(selfGraph)[1]
		# breakpoint: print DFScycle(selfGraph)[2]
		P = graph2Genome(selfCycle)
		for each in P:
			output(each)
		print ''


def DFScycle(graph):
	'''
	No direction graph;
	Implement deep first searching algorithm:
		Mark every nodes in three colors:
			'white': unscanned
			'grey': once scanned
			'black': twice scanned
	a black node denote a cycle, number of black nodes is the amount of cycles
	return: cycleNumber, cycle
	'''
	cycleNumber = 0

	# record the cycle
	cycle = []

	# initiate nodes color
	color = {}
	for node in graph.keys():
		color[node] = 'white'

	# start searching
	for key in graph.keys():

		# search only when the node is white
		if color[key] == 'white':
			# initiate a new cycle
			cycle.append([])
			offset = cycle.index([])
			# print key
			# change color to grey, denote scanned once
			color[key] = 'grey'
			# initiate a start node
			# the start node is the root of the current tree
			currentNode = graph[key][0]
			fatherNode = key

			# assumed that every node in a cycle can be scanned twice after the cycle has been scanned thoroughly
			while color[currentNode] != 'black':
				cycle[offset].append(currentNode)
				# scan once
				if color[currentNode] == 'white':
					color[currentNode] = 'grey'
				# scan twice
				elif color[currentNode] == 'grey':
					color[currentNode] = 'black'
					# end to a cycle
					cycleNumber += 1
					break

				# grow the tree
				# current can prevent 'currentnode' value changing while iteration
				current = currentNode
				for i in range(len(graph[current])):
					# avoid coming back
					if graph[current][i] != fatherNode:
						# update the currentNode and start next searching
						currentNode = graph[current][i]
				fatherNode = current

		else:
			continue

	# reverse every cycle in dict(cycle) in positive direction
	nonTrivalCycle = []
	for each in cycle:
		each.reverse()
		if len(each) > 2:
			nonTrivalCycle.append(each)
	return cycleNumber, cycle, nonTrivalCycle


def graphBuilt(PEdges, DEdges):
	'''
	Build a graph contain every nodes and its adajcent nodes
	'''
	graph = {}
	for p in PEdges:
		if p[0] not in graph.keys():
			graph[p[0]] = []
			if p[1] not in graph[p[0]]:
				graph[p[0]].append(p[1])
		if p[1] not in graph.keys():
			graph[p[1]] = []
			if p[0] not in graph[p[1]]:
				graph[p[1]].append(p[0])

	for d in DEdges:
		if d[1] not in graph[d[0]]:
			graph[d[0]].append(d[1])
		if d[0] not in graph[d[1]]:
			graph[d[1]].append(d[0])

	return graph


def chr2Cycle(chromosome):
	'''
	Turn chromosome into a series of number, which can represent the direction of each block.
	chromosome is a list
	e.g. edge '1' denote as 1, 2; edge '-2' denote as 4, 3
	'''
	node = [0] * 2 * len(chromosome)
	for j in range(len(chromosome)):
		i = chromosome[j]
		if i > 0:
			# node[2j + 1] > node[2j]
			node[2 * j + 1] = 2 * i
			node[2 * j] = 2 * i - 1
		else:
			# node[2j + 1] < node[2j]
			node[2 * j + 1] = -2 * i - 1
			node[2 * j] = -2 * i
	return node


def cycle2Chr(node):
	'''
	Invertible chr2Cycle
	'''
	chromosome = [0] * (len(node) / 2)
	for j in range(len(node) / 2):
		if node[2 * j + 1] > node[2 * j]:
			# edge is positive
			chromosome[j] = node[2 * j + 1] / 2
		else:
			# edge is negative
			chromosome[j] = (-1) * node[2 * j] / 2
	return chromosome


def graph2Genome(genomegraph):
	'''
	Turn the edge graph back to genome
	genomegraph consists of the node created by cycle2Chr and edges created by redEdges
	breakpoint returned by DFScycle, denoting breakpoints in genome graph
	'''
	P = []
	for each in genomegraph:
		chromosome = cycle2Chr(each)
		P.append(chromosome)
	return P


def coloredEdges(P):
	'''
	connect the red edges
	red edges is considered to be changed during sorting
	'''
	edges = []
	node = []
	for i in range(len(P)):
		node.append(chr2Cycle(P[i]))

		for j in range(len(P[i])):
			if j <= len(P[i]) - 2:
				# avoid index out of range
				# connect two black edges; denote red edges
				edges.append((node[i][2 * j + 1], node[i][2 * j + 2]))
			else:
				# end problem
				edges.append((node[i][2 * j + 1], node[i][0]))
	return edges


def blackEdges(P):
	'''
	connect the blue edges
	blue edges are solid edges which mantain during sorting
	'''
	edges = []
	node = []
	for i in range(len(P)):
		node.append(chr2Cycle(P[i]))

		for j in range(len(P[i])):
			if j <= len(P[i]) - 1:
				# avoid index out of range
				# connect two black edges; denote red edges
				edges.append((node[i][2 * j], node[i][2 * j + 1]))
	return edges


def breakOnGenoGraph(graph, i, j, n, m):
	'''
	graph: edge graph of input chromosome
	(i, j)(n, m) -> (i, n)(j, m)
	'''
	# break first edge
	if (i, n) in graph:
		graph.remove((i, n))
		# generate new edge
		graph.append((n, j))
	elif (n, i) in graph:
		graph.remove((n, i))
		# generate new edge
		graph.append((j, n))

	# break second edge
	if (m, j) in graph:
		graph.remove((m, j))
		# generate new edge
		graph.append((i, m))
	elif (j, m) in graph:
		graph.remove((j, m))
		# generate new edge
		graph.append((m, i))

	return graph


def readData(filename):
	'''
	read file from database
	'''
	with open(filename, 'r') as f:
		total = []
		for line in f:
			per = []
			line = line.rstrip()
			pre = []
			suf = []
			# remove '(' and ')'
			for i in range(len(line)):
				if line[i] == '(':
					pre.append(i)
				elif line[i] == ')':
					suf.append(i)
			# scratch str between '(' and ')'
			for i in range(len(pre)):
				per.append((line[pre[i] + 1: suf[i]]).split(' '))
			# turn str into int
			for each in per:
				for i in range(len(each)):
					each[i] = int(each[i])
			# put all in total
			total.append(per)

	return total


def main():

	# readfile
	data = readData('test.txt')

	P = data[0]
	D = data[1]

	# test1
	# P = [[1, -2, -4, 3]]

	# visual sorting
	starttime1 = time.clock()
	shrtReSnr(P, D)
	endtime1 = time.clock()
	print endtime1 - starttime1

if __name__ == '__main__':
	main()
