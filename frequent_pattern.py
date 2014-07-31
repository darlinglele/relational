from apriori import Apriori


class Node():

    def __init__(self, name, count, parent=None):
        self.name = name
        self.count = count
        self.parent = parent
        self.children = {}
        self.next = None

    def incr_count(self, count):
        self.count += count

    def draw(self, depth=1):
        print ' ' * depth, self.name, self.count
        for child in self.children.values():
            child.draw(depth=depth + 1)


class FrequentPattern(Apriori):

    def __init__(self, min_support, min_conf, max_rule_length=100):
        Apriori.__init__(self, min_support, min_conf)
        self.max_rule_length = max_rule_length

    def find_freqsets(self, dataset):
        freqsets = {}
        self.ds_num = sum(dataset.itervalues())
        self._find_freqsets(dataset, freqsets)
        freqsets_lst = [[] for x in xrange(self.max_rule_length)]
        support_counter = {}
        for freqset, count in freqsets.items():
            freqsets_lst[len(freqset) - 1].append(freqset)
            support_counter[freqset] = support_counter.get(freqset, 0) + count
        return freqsets_lst, support_counter

    def _create_tree(self, dataset):
        item_header = {}
        for items in dataset:
            for item in items:
                item_header[item] = item_header.get(item, 0) + dataset[items]

        for item, count in item_header.items():
            if float(count) / self.ds_num < self.min_support:
                del item_header[item]

        for key in item_header:
            item_header[key] = [item_header[key], None]

        tree = Node(None, 0)

        for items in dataset:
            sorted_item_counts = sorted([(item_header[item][0], item)
                                        for item in items if item in item_header], reverse=True)
            sorted_items = [item_count[1] for item_count in sorted_item_counts]
            self._insert(sorted_items, tree, item_header, dataset[items])
        return tree, item_header

    def _append_to_link_list(self, item_header, item, node):
        if item_header[item][1] is None:
            item_header[item][1] = node
        else:
            begin = item_header[item][1]
            while begin.next:
                begin = begin.next
            begin.next = node

    def _insert(self, items, node, item_header, count):
        if len(items) == 0:
            return
        first_item = items[0]
        if first_item in node.children:
            node.children[first_item].incr_count(count)
        else:
            node.children[first_item] = Node(first_item, count, parent=node)
            self._append_to_link_list(
                item_header, first_item, node.children[first_item])

        if len(items) > 1:
            self._insert(
                items[1:], node.children[first_item], item_header, count)

    def _append_prefix_itemset(self, node, itemsets):
        if node and node.name:
            itemsets.add(node.name)
        else:
            return 1
        if node.parent is not None:
            self._append_prefix_itemset(node.parent, itemsets)

    def _find_sub_dataset(self, item, item_header):
        sub_dataset = {}
        node = item_header[item][1]
        while node:
            itemsets = set()
            self._append_prefix_itemset(node.parent, itemsets)
            if len(itemsets) > 0:
                sub_dataset[frozenset(itemsets)] = node.count
            node = node.next
        return sub_dataset

    def _find_freqsets(self, dataset, freqsets, base_item=set()):
        tree, item_header = self._create_tree(dataset)
        for item in item_header:
            new_base_item = base_item.copy()
            new_base_item.add(item)
            freqsets[frozenset(new_base_item)] = item_header[item][0]
            sub_dataset = self._find_sub_dataset(item, item_header)
            if len(sub_dataset) > 0:
                self._find_freqsets(sub_dataset, freqsets, new_base_item)

if __name__=='__main__':
	dataset = {frozenset('rzhjp'): 1, frozenset('zyxwvuts'): 1, frozenset('z'): 1,
	           frozenset('rxnos'): 1, frozenset('yrxzqtp'): 1, frozenset('yzxeqstm'): 1}

	fp = FrequentPattern(min_support=0.5, min_conf=0.1)
	freqsets_lst, support_counter = fp.find_freqsets(dataset)

	print freqsets_lst
	print support_counter
	rules = fp.generate_rules(freqsets_lst, support_counter)
	print rules
