'''
http://www.codeproject.com/Articles/70371/Apriori-Algorithm

1. Scan transactions to get support S of each item
2. If S >= min. support: Add to frequent 1-itemsets L1
3. Loop:
		a) Use L(k-1) join L(k-1) to generate set of candidate k-items-sets > each k-1 item of the k-item must also be a freq item
		b) Scan transactions to get support S of each candidate k-items-set 
		c) if S >= min. support, add to K-frequent itemsets
		d) if generated set is null, break out of loop
4. For each frequent itemset L, generate all non-empty subsets of L
5. For each non-empty subset s of L, find confidence C of s
6. If C >= min. confidence, add to strong rules 
'''
import sys
import codecs
from time import time
from itertools import combinations, permutations, imap
from collections import OrderedDict, Counter
import numpy as np

def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    '''http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression'''
    z = x.copy()
    z.update(y)
    return z

class APriori:
	def __init__(self, data, sep, support=0.5, confidence=0.0, k=2):
		self.data = data
		self.data_list = []
		self.sep = sep
		self.support = support
		self.confidence = confidence
		self.k = k
		self.total_items = 0.0
		self.freq_item_set = []
		self.association_rules = {}

		self.run()

	def set_data(self):
		for row in self.data:	
			items = row.strip("\n").strip("\r").strip().split(self.sep) #*********************This needs to go
			items = [str(item).strip() for item in items if str(item).strip() is not ""]
			self.data_list.append(items)

	def run(self):
		self.get_freq_items()
		self.get_freq_itemsets()

	frequent_set_list = {}

	def func(self, key, items):
		if set(key).issubset(set(items)):
			frequent_set_list[key] = frequent_set_list[key] + 1

	def get_freq_itemsets(self):
		# do for each k-item set
		for ik in xrange(1, self.k):
			print "Iteration: ", ik
			frequent_set_list = {}
			frequent_set_list2 = {}
				
			iter1 = self.freq_item_set[ik-1].keys()

			if ik == 1:
				for item in combinations(iter1, 2):
					frequent_set_list[item] = 0
			else:
				allitems = ()
				for itm in iter1:
					allitems = allitems + tuple(itm)

				allitems = set(allitems)

				for i in xrange(0, len(iter1)-1):

					keys = allitems - set(iter1[i])

					for key in keys:
						x = list(iter1[i])
						x.append(key)
						
						c = list(combinations(x, ik))
						check = map(lambda cc: any(map(lambda x: True if set(cc).issubset(x) else False, iter1)), c)
						# print x, "-->", c, "-->", all(check)
						if all(check):
							# check if key already present
							check2 = map(lambda y: True if set(x).issubset(y) else False, frequent_set_list.keys())
							if any(check2):
								continue
							frequent_set_list[tuple(x)] = 0

			# for item in combinations(iter1, 2):
			# 	if ik > 1:
			# 		i = ()
			# 		for itm in item:	
			# 			i = i + tuple(itm)
					
			# 		for j in combinations(set(i), ik+1):
			# 			# print "first check ", i, "--", j
			# 			# check if j already exists in frequent item keys
			# 			check = map(lambda x: True if set(j).issubset(x) else False, frequent_set_list.keys())
			# 			if any(check):
			# 				continue
			# 			# print "second check", i, "--", j

			# 			k_check = []
			# 			for k in combinations(set(j), ik):
			# 				# check if all subsets are also frequent
			# 				check = map(lambda x: True if set(k).issubset(x) else False, iter1)
			# 				k_check.append(any(check))
			# 			if all(k_check):
			# 				# print "all good"
			# 				frequent_set_list[j] = 0
			# 	else:
			# 		frequent_set_list[item] = 0


			# print "got frequent itemssets, now to get support"
			# for k, v in frequent_set_list.iteritems():
			# 	print k, v
			# print frequent_set_list
			
			# scan transactions to get support for each item set
			for items in self.data_list:
				for key in frequent_set_list.keys():
					if set(key).issubset(items):
						frequent_set_list[key] = frequent_set_list[key] + 1
			
			# frequent_set_list
			# print "got support, now to prune"	

			# prune
			frequent_set_list2 = {k: v for k, v in frequent_set_list.iteritems() if float(v)/float(self.total_items) >= self.support}
			self.freq_item_set.append(frequent_set_list2)

			print "Size of frequent ", str(ik+1), "-items: ", len(frequent_set_list2)
			print
			# print "Freq item set: ", OrderedDict(sorted(frequent_set_list2.items(), key=lambda t: t[1]))
			# print "-------------------------------"
			
			if not frequent_set_list2:
				print "Found stopping criteria: Empty pruned freq item set list"
				print
				break

	def get_freq_items(self):
		# set data
		self.set_data()

		# build 1-items list
		items_list = Counter()

		# build initial count list of items
		for item in self.data_list:
			items_list.update(item)
		items_list = dict(items_list)

		# get all items above support threshold
		self.total_items = len(self.data_list)

		freq_items = {}
		freq_items = dict(filter(lambda (k,v): float(v)/float(self.total_items) >= self.support, items_list.iteritems()))

		print 'Iteration: 0'
		print "Size of frequent 1-items: ", len(freq_items)
		print
		self.freq_item_set.append(freq_items)
		# print "Freq item set: ", OrderedDict(sorted(freq_items.items(), key=lambda t: t[1]))
		# print "-------------------------------"

	def get_association_rules(self, savefile):
		# merge item sets
		final_dict = {}
		# print 'length: ', len(self.freq_item_set)
		for i in xrange(1, len(self.freq_item_set)): # changed this to + 1
			final_dict = merge_two_dicts(final_dict, self.freq_item_set[i])

		print self.freq_item_set[0]
		print
		print final_dict

		f = codecs.open(savefile, 'a', encoding="utf-8")
		f.write("LHS^RHS^Support^Confidence^Lift" + "\n")

		for key in final_dict.keys():
			count_key = final_dict[key]
			for j in xrange(1, len(key)):
				for p in permutations(key, j):
					p1 = (p)
					if len(p1) == 1:
						if self.freq_item_set[0].has_key(p1[0]):
							count_lhs = self.freq_item_set[0][p1[0]]
							p = p1
					elif final_dict.has_key(p):
						count_lhs = final_dict[p]
					else:
						continue

					count_rhs = 0
					rhs = tuple(set(key) - set(p))
					print rhs
					if len(rhs) == 1:
						if self.freq_item_set[0].has_key(rhs[0]):
							count_rhs = self.freq_item_set[0][rhs[0]]
					else:
						for k in permutations(rhs, len(rhs)):
							if final_dict.has_key(k):
								count_rhs = final_dict[k]
								break

					support = float(count_key) / self.total_items
					confidence = float(count_key)/float(count_lhs)
					lift = (float(count_key) / float(self.total_items)) / ((float(count_lhs)/ float(self.total_items)) * (float(count_rhs) / float(self.total_items)))

					# save to file
					row = [str(p), str(rhs), str(support), str(confidence), str(lift)]
					f.write("^".join(row) + "\n")

def main():
	filename = sys.argv[1]
	savefile = sys.argv[2]

	f = "D:/datasets/market-basket-analysis/groceries.txt"
	savef = "D:/datasets/market-basket-analysis/association_rules.txt"

	data = codecs.open(filename, 'r', encoding="utf-8") # "D:/datasets/market-basket-analysis/groceries.txt"
	t = time()
	ap = APriori(data, sep=",", support=0.001, k=4)
	print "total time for execution: ", (time() - t)
	# print
	ap.get_association_rules(savefile)
	# print
	# print "Association_rules over confidence threshold, sorted:"
	# for key, val in rules.iteritems():
	# 	print key[0], "-->", key[1], " confidence: ", val
	
	# data = codecs.open("D:/datasets/market-basket-analysis/sample.txt", 'r', encoding="utf-8")
	# t = time()
	# ap = APriori(data, sep=",", support=0.1, k=4)
	# print "total time for execution: ", (time() - t)
	# rules = ap.get_association_rules(confidence=0.57)
	# print "association_rules over threshold, sorted:"
	# for key, val in rules.iteritems():
	# 	print key[0], "-->", key[1], " confidence: ", val


	# data = codecs.open("D:/datasets/market-basket-analysis/retail.txt", 'r', encoding="utf-8")
	# t = time()
	# ap = APriori(data, sep=" ", support=0.06, k=3)
	# print "total time for execution: ", (time() - t)
	# rules = ap.get_association_rules(confidence=0.6)
	# print "association_rules over threshold, sorted:"
	# for key, val in rules.iteritems():
	# 	print key[0], "-->", key[1], " confidence: ", val


	# data = codecs.open("D:/datasets/market-basket-analysis/T10I4D100K.txt", 'r', encoding="utf-8")
	# t = time()
	# ap = APriori(data, sep=" ", support=0.03, k=4)
	# print "total time for execution: ", (time() - t)
	# _ = ap.get_association_rules(confidence=0.9)

if __name__ == '__main__':
	main()