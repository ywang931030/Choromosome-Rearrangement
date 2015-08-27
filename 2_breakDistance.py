#!/usr/bin/env python
'''
Calculating 2-break distance between genomes P and Q
'''
__author__ = 'Yue Wang'


import time


def breakDistance(cycleNumber, blocks):
	'''
	2_breakDistance = blocks - cycleNumber
	'''
	d = blocks - cycleNumber
	return d


def DFScycle(graph):
	'''
	No direction graph;
	Implement deep first searching algorithm:
		Mark every nodes in three colors:
			'white': unscanned
			'grey': once scanned
			'black': twice scanned
	a black node denote a cycle, number of black nodes is the amount of cycles
	'''
	cycleNumber = 0
	# initiate nodes color
	color = {}
	for node in graph.keys():
		color[node] = 'white'

	# start searching
	for key in graph.keys():
		# search only when the node is white
		if color[key] == 'white':
			# print key
			# change color to grey, denote scanned once
			color[key] = 'grey'
			# initiate a start node
			# the start node is the root of the current tree
			currentNode = graph[key][0]
			fatherNode = key

			# assumed that every node in a cycle can be scanned twice after the cycle has been scanned thoroughly
			while color[currentNode] != 'black':

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

	return cycleNumber


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


def graph2Genome(genomegraph):
	'''
	Turn the graph back to genome
	genomegraph consists of the node created by cycle2Chr
	'''
	P = []
	for each in genomegraph:
		P.append(cycle2Chr(each))
	return P


def coloredEdges(P):
	'''
	connect the red edges
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
	# starttime1 = time.clock()
	# data = readData('test.txt')
	# endtime1 = time.clock()
	# P = data[0]
	# D = data[1]

	# test1
	P = [[1, 2, 3, 4, 5, 6]]
	D = [[1, -3, -6, -5], [2, -4]]
	starttime2 = time.clock()

	# Turn chromosome into cycles:
	Pnode = []
	for each in P:
		Pnode.append(chr2Cycle(each))
	# breakpoint: print Pnode
	Dnode = []
	for each in D:
		Dnode.append(chr2Cycle(each))
	# breakpoint: print Dnode

	# build graph
	graph = {}
	PEdges = coloredEdges(P)
	DEdges = coloredEdges(D)
	blocks = len(PEdges)
	graph = graphBuilt(PEdges, DEdges)
	# breakpoint: print graph

	# DFS cycles
	cycleNumber = DFScycle(graph)
	endtime2 = time.clock()
	# breakpoint: print DFScycle(graph)

	# 2_break distance
	print breakDistance(cycleNumber, blocks)
	# print endtime1 - starttime1
	print endtime2 - starttime2


if __name__ == '__main__':
	main()
