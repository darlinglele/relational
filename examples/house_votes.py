import sys
sys.path.append('..')
from apriori import Apriori


if __name__ == '__main__':

    def trim_data(file):
        T = [x.strip().split(',') for x in open(file)]
        new_T = []
        for t in T:
            new_t = set()
            for i, x in enumerate(t):
                if x == 'republican':
                    new_t.add(i)
                    continue
                if x != 'n':
                    new_t.add(i + 1)
            new_T.append(new_t)

        f = open('new-house-votes.data', 'w')

        for t in new_T:
            f.write(','.join(str(x) for x in t) + '\n')
        f.close()

    trim_data('house-votes.data')

    X = [set(s.strip().split(',')) for s in open('new-house-votes.data')]
    apriori = Apriori(min_support=0.45, min_conf=0.918)
    freqsets_lst, support_counter = apriori.find_freqsets(X)
    for x in apriori.generate_rules(freqsets_lst, support_counter):
        print x
