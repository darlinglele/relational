import sys
sys.path.append('..')
from apriori import Apriori
from frequent_pattern import FrequentPattern
import unittest


def apriori_test():
    apriori = Apriori(min_support=0.45, min_conf=0.918)
    freqsets_lst, support_counter = apriori.find_freqsets(dataset)
    rules = apriori.generate_rules(freqsets_lst, support_counter)
    return rules


def frequent_pattern_test():
    new_dataset = {}
    for data in dataset:
        new_dataset[frozenset(data)] = new_dataset.get(frozenset(data), 0) + 1

    fp = FrequentPattern(min_support=0.45, min_conf=0.918)
    freqsets_lst, support_counter = fp.find_freqsets(new_dataset)
    rules = fp.generate_rules(freqsets_lst, support_counter)
    return rules


def prepare_data(file):
    dataset = [x.strip().split(',') for x in open(file)]
    new_dataset = []
    for data in dataset:
        new_data = set()
        for i, x in enumerate(data):
            if x == 'republican':
                new_data.add(i)
                continue
            if x != 'n':
                new_data.add(i + 1)
        new_dataset.append(new_data)
    f = open('new-house-votes.data', 'w')
    for t in new_dataset:
        f.write(','.join(str(x) for x in t) + '\n')
    f.close()

if __name__ == '__main__':
    
    prepare_data('house-votes.data')
    dataset = [set(s.strip().split(',')) for s in open('new-house-votes.data')]
    for x, y in zip(sorted(frequent_pattern_test(), key=lambda x: x[1]), sorted(apriori_test(), key=lambda x: x[1])):
        print x, y
