#!/usr/bin/env python
'''
Implement GREEDYSORTING.
Input: A permutation P.
Output: The sequence of permutations corresponding to applying GREEDYSORTING to P, ending with
the identity permutation.
'''

__author__ = 'Yue Wang'


def output(p):
	'''
	Format p.
	'''
	print "(%s)" % ' '.join(["%+d" % e for e in p])


def greedySorting(p):
	'''
	Turn permutations into identity permutation
	'''
	approxReversalDistance = 0

	for i in range(len(p)):
		if not p[i] == i + 1:
			p = kSorting(p, i + 1, i)
			approxReversalDistance += 1

	return approxReversalDistance


def kSorting(p, k, start):
	'''
	p is the permutation, k is the element to be sorted
	start is the offset of sorted k
	'''
	# case 1: k is in the p
	if k in p:
		offset = p.index(k)
		end = offset + 1
		# extract p[start: end]
		current = p[start: end]
		# reverse
		current = list(reversed(current))

		# operate the direction
		for i in range(len(current)):
			current[i] = (-1) * current[i]

		# paste back to p
		p[start: end] = current
		output(p)

	# case 2: -k is in the p
	if (-1) * k in p:
		rk = (-1) * k
		offset = p.index(rk)
		end = offset + 1
		# extract p[start: end]
		current = p[start: end]
		# reverse
		current = list(reversed(current))
		# operate the direction
		for i in range(len(current)):
			current[i] = (-1) * current[i]
		# paste back to p
		p[start: end] = current
		output(p)

	return p


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
print greedySorting(per)
