class Apriori:

    def __init__(self, min_support=0.618, min_conf=0.618):
        self.min_conf = min_conf
        self.min_support = min_support

    def init_condidates(self, T):
        condidates = set()
        for t in T:
            for i in t:
                if i not in condidates:
                    condidates.add(i)

        return [frozenset([item]) for item in condidates]

    def select_freq_sets(self, condidates, T):
        support_counter = {}
        for t in T:
            for c in condidates:
                if c.issubset(t):
                    support_counter.setdefault(c, 1)
                    support_counter[c] += 1
        freqsets = [
            c for c in condidates if c in support_counter and float(support_counter[c]) / len(T) > self.min_support]
        support_counter = {c: support_counter[c] for c in freqsets}
        return freqsets, support_counter

    def generate_condidates(self, freqsets, k):
        condidates = []
        for i in xrange(len(freqsets)):
            for j in xrange(i + 1, len(freqsets)):
                freqset_a = list(freqsets[i])[:k - 2]
                freqset_a.sort()
                freqset_b = list(freqsets[j])[:k - 2]
                freqset_b.sort()
                if freqset_a == freqset_b:
                    condidates.append(freqsets[i] | freqsets[j])
        return condidates

    def find_freqsets(self, T):
        condidates = self.init_condidates(T)
        freqsets, support_counter = self.select_freq_sets(
            condidates, T)
        freqsets_lst = [freqsets]
        k = 2
        while len(freqsets_lst[k - 2]) > 0:
            condidates = self.generate_condidates(freqsets_lst[k - 2], k)
            freqsets, counter = self.select_freq_sets(
                condidates, T)
            freqsets_lst.append(freqsets)
            support_counter.update(counter)
            k += 1
        return freqsets_lst, support_counter

    def generate_rules(self, freqsets_lst, support_counter):
        rule_lst = []
        for i in xrange(1, len(freqsets_lst)):
            for freqset in freqsets_lst[i]:
                conseq_lst = [frozenset([item]) for item in freqset]
                len_conseq = 1
                while True:
                    rule_conf_lst = self.cal_rule_conf(
                        freqset, conseq_lst, support_counter)
                    conseq_lst = []
                    for rule_conf in rule_conf_lst:
                        if rule_conf[1] > self.min_conf:
                            rule_lst.append(rule_conf)
                            conseq_lst.append(rule_conf[0][1])

                    if len_conseq == i or len(conseq_lst) <= 1:
                        break
                    len_conseq += 1
                    conseq_lst = self.generate_condidates(
                        conseq_lst, len_conseq)
        return rule_lst

    def cal_rule_conf(self, freqset, conseq_lst, support_counter):
        rule_conf_lst = []
        for conseq in conseq_lst:
            conf = float(support_counter[freqset]) / support_counter[
                freqset - conseq]
            rule_conf_lst.append(((freqset - conseq, conseq), conf))
        return rule_conf_lst
