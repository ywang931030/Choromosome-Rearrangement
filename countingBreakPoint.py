#!/usr/bin/env python
'''
Count the breakpoint of a premutation
	An adjacent is p[i + 1] - p[i] == 1
	A breakpoint is p[i + 1] - p[i] != 1
For counting the begin and the end of a premutation,
	we add 0 to the beginning and n + 1 to the end
'''

__author__ = 'Yue Wang'


def countingBreakPoint(p):
	adjacent = 0
	breakpoint = 0
	for i in range(len(p) - 1):
		# adjacent
		if p[i + 1] - p[i] == 1:
			adjacent += 1
		else:
			breakpoint += 1
	return breakpoint


def readData(filename):
	with open(filename, 'r') as f:
		permutation = []

		# split the elements with space
		for line in f:
			line = line.split(' ')
			permutation = line

		# turn type into int
		for i in range(len(permutation)):
			permutation[i] = int(permutation[i])

	return permutation


per = readData('test.txt')
per[0:0] = [0]
per.append(len(per))
print countingBreakPoint(per)
