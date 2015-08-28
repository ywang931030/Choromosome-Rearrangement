#!/usr/bin/env python
'''
Find all shared k-mers between two sequences, including k-mers and their reverse complement
Build index is time-consuming, so we only built one
To deduce the runningtime, we do not build index for reverse complement; instead, we do it(revComplement) when comparing
'''

from string import maketrans
import time


def sharedKmers(D, Dindex, P, k):
	'''
	Input: index of D, P, revP
	Process:
		if P[i: i + k], revP[i: i + k] in Dindex.keys():
			return (i, Dindex.keys[P[i: i + k]]) or (j, Dindex.keys[revP[i: i + k]])
	Return: list of sharedKmers (x, y), denoting they share the k-mer from offset x and y
	'''
	shared = []
	for i in range(len(P) - k + 1):
		rev = revComplement(P[i: i + k])
		if P[i: i + k] in D:
			for each in Dindex[P[i: i + k]]:
				shared.append((i, each))
		if rev in D:
			for each in Dindex[rev]:
				shared.append((i, each))

	return shared


def indexBuilt(seq, k):
	'''
	Input: a seq (in str type)
	Process:
		Then build an index, in which the key is the k-mer, and the value is the offset of the k-mer
		To deduce the runningtime, we do not build index for reverse complement; instead, we do it(revComplement) when comparing
	Return: a dictionary
	'''
	# build the index
	index = {}
	for i in range(len(seq) - k + 1):
		if seq[i: i + k] not in index.keys():
			index[seq[i: i + k]] = [i]
		else:
			index[seq[i: i + k]].append(i)

	return index


def revComplement(seq):
	'''
	generate reverse complement seq for each input seq
	seq is in str type
	'''
	re = ''
	re = seq[::-1].translate(maketrans('ATCG', 'TAGC'))

	return re


def readSeq(filename):
	'''
	read file from database
	'''
	with open(filename, 'r') as f:
		seq = []
		for line in f:
			line = line.rstrip()
			seq.append(line)
	return seq


def main():

	# readfile
	seq = readSeq('test.txt')
	P = seq[0]
	D = seq[1]
	k = 17

	# build index
	starttime1 = time.clock()
	Dindex = indexBuilt(D, k)
	endtime1 = time.clock()
	print endtime1 - starttime1
	# breakpoint: print Dindex

	# find shared kmers
	starttime2 = time.clock()
	shared = sharedKmers(D, Dindex, P, k)
	endtime2 = time.clock()
	print endtime2 - starttime2

	for each in shared:
		print each


if __name__ == '__main__':
	main()
