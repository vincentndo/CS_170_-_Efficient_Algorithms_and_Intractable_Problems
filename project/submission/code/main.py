""" Main Coding for the Project
    Student: 'Vincent' Ninh DO
    SID: 25949105 """
import time
import collections


class Item:

    def __init__(self, args):
        self.name = args[0]
        self.iclass = int(args[1])
        self.weight = float(args[2])
        self.cost = float(args[3])
        self.resale_value = float(args[4])
        if mode == 3:
            self.effective_value = self.resale_value - self.cost
        elif mode == 21:
            self.effective_value = self.resale_value**2 / (max(self.weight, 1) * max(self.cost, 1))
        else:
            self.effective_value = self.resale_value / self.cost
        self.conflict_status = False

    def get_name(self):
        return self.name

    def get_class(self):
        return self.iclass

    def get_weight(self):
        return self.weight

    def get_cost(self):
        return self.cost

    def get_resale_value(self):
        return self.resale_value

    def get_effective_value(self):
        return self.effective_value

    def set_conflict_status(self, value):
        self.conflict_status = value

    def get_conflict_status(self):
        return self.conflict_status


class Collection:

    def __init__(self):
        self.item_list = []
        self.class_dict = {}
        self.class_conflict_dict = {}
        self.item_conflict_dict = {}

    def set_parameter_tuple(self, parameter_tuple):
        self.parameter_tuple = parameter_tuple

    def get_parameter_tuple(self):
        return self.parameter_tuple

    def get_item_list(self):
        return self.item_list

    def get_class_dict(self):
        return self.class_dict

    def set_class_conflict_dict(self, new_dict):
        self.class_conflict_dict = new_dict

    def get_class_conflict_dict(self):
        return self.class_conflict_dict

    def get_item_conflict_dict(self):
        return self.item_conflict_dict

    def class_to_items(self, iclass):
        return self.class_dict[iclass]

    def is_conflicting(self, item_1, item_2):
        iclass_1 = item_1.get_class()
        iclass_2 = item_2.get_class()
        assert iclass_1 in self.class_conflict_dict[iclass_2] == iclass_2 in self.class_conflict_dict[iclass_1]
        return iclass_1 in self.class_conflict_dict[iclass_2]

    def add_item(self, item):
        self.item_list.append(item)
        iclass = item.get_class()
        if iclass in self.class_dict:
            self.class_dict[iclass].add(item)
        else:
            self.class_dict[iclass] = {item}

    def add_conflict(self, conflict_set):
        conflict_set = {iclass for iclass in conflict_set if iclass in self.class_dict}
        list_of_sets = [ self.class_to_items(iclass) for iclass in conflict_set if iclass in self.class_dict]
        if len(list_of_sets) > 0:
            item_conflict_set = set.union(*list_of_sets)
        for iclass in conflict_set:
            # if iclass in self.class_dict:
            if iclass in self.class_conflict_dict:
                self.class_conflict_dict[iclass] = self.class_conflict_dict[iclass].union(conflict_set)
            else:
                self.class_conflict_dict[iclass] = conflict_set.copy()

            self.class_conflict_dict[iclass].remove(iclass)

    def sort_collection(self, key_function):
        self.item_list.sort(key = key_function, reverse = True)


class GargSack:

    def __init__(self, budget, weight_limit, collection):
        self.sack = []
        self.resale_value = 0
        self.cost = 0
        self.weight = 0
        self.budget = budget
        self.objective = self.resale_value + self.budget - self.cost
        self.weight_limit = weight_limit
        self.collection = collection
        self.class_pool = set()
        self.conflicting_pool = []

    def get_sack(self):
        return self.sack

    def get_resale_value(self):
        return self.resale_value

    def get_cost(self):
        return self.cost

    def get_weight(self):
        return self.weight

    def get_objective(self):
        assert self.objective == self.resale_value + self.budget - self.cost
        return self.objective

    def get_collection(self):
        return self.collection

    def is_full(self, item):
        return self.cost + item.cost > self.budget or self.weight + item.weight > self.weight_limit

    def add_item(self, item):
        self.sack.append(item)
        self.resale_value += item.get_resale_value()
        self.cost += item.get_cost()
        self.weight += item.get_weight()
        if self.weight > self.weight_limit or (self.budget - self.cost) < 0:
            print("Red ALERT!")
            return
        self.objective = self.resale_value + self.budget - self.cost
        iclass = item.get_class()
        if iclass not in self.class_pool:
            self.class_pool.add(iclass)
            class_conflict_dict = self.collection.get_class_conflict_dict()
            if iclass in class_conflict_dict:
                self.conflicting_pool.extend(list(class_conflict_dict[iclass]))
                for conflict_class in class_conflict_dict[iclass]:
                    for i in self.collection.class_to_items(conflict_class):
                        i.set_conflict_status(True)

    def add_item_list(self, items):
        for i in items:
            self.add_item(i)

    def remove_item(self, item):
        if item in self.sack:
            self.sack.remove(item)
            self.resale_value -= item.get_resale_value()
            self.cost -= item.get_cost()
            self.weight -= item.get_weight()
            self.objective = self.resale_value + self.budget - self.cost

    def remove_item_list(self, items):
        for i in items:
            self.remove_item(i)

    def pick_items(self):
        def num_conflict(item, collection):
            ret = 0
            iclass = item.get_class()
            class_conflict_dict = collection.get_class_conflict_dict()
            if iclass in class_conflict_dict:
                for conflict_class in class_conflict_dict[iclass]:
                    ret += len(collection.class_to_items(conflict_class))
            return ret

        print("  Pick items ...")
        self.collection.sort_collection(lambda item: item.get_effective_value() / max(num_conflict(item, self.collection), 1))
        item_list = self.collection.get_item_list().copy()
        for item in item_list:
            if not item.get_conflict_status() and not self.is_full(item):        
                self.add_item(item)
        print("  Done picking items")

    def improve_sack(self):
        def sums(items):
            weight = 0
            cost = 0            
            resale_value = 0
            for i in items:
                weight += i.get_weight()
                cost += i.get_cost()                
                resale_value += i.get_resale_value()

            return (weight, cost, resale_value)

        print("  Improving sack ...")
        class_conflict_dict = self.collection.get_class_conflict_dict()
        sorted_class_list = sorted(class_conflict_dict, key = lambda x: len(class_conflict_dict[x]), reverse = True)
        for iclass in sorted_class_list:
            if iclass in self.class_pool:
                new_conflicting_pool = self.conflicting_pool.copy()
                for conflict_class in class_conflict_dict[iclass]:
                    new_conflicting_pool.remove(conflict_class)

                items = {i for i in self.collection.class_to_items(iclass) if i in self.sack}
                P, M, R = sums(items)
                sack_weight = self.get_weight()
                sack_cost = self.get_cost()                
                sack_resale_value = self.get_resale_value()
                sack_objective = self.get_objective()
                max_objective = sack_objective
                swap_items = set()
                swap_class = iclass
                for conflict_class in class_conflict_dict[iclass]:
                    if conflict_class not in new_conflicting_pool:
                        new_items = list( self.collection.class_to_items(conflict_class) )
                        new_items.sort(key = lambda x: x.get_effective_value(), reverse = True)
                        P_new, M_new, R_new = sums(new_items)
                        sack_weight_new = sack_weight - P + P_new
                        sack_cost_new = sack_cost - M + M_new
                        sack_resale_value_new = sack_resale_value - R + R_new
                        sack_objective_new = sack_resale_value_new + self.budget - sack_cost_new
                        if sack_weight_new < self.weight_limit and sack_cost_new < self.budget and sack_objective_new > max_objective:
                            max_objective = sack_objective_new
                            swap_items = new_items
                            swap_class = conflict_class
                        else:
                            sack_weight_new = sack_weight - P
                            sack_cost_new = sack_cost - M
                            sack_resale_value_new = sack_resale_value - R
                            cutoff_new_items = []
                            item = new_items.pop(0)
                            while sack_weight_new + item.get_weight() < self.weight_limit and sack_cost_new + item.get_cost() < self.budget and len(new_items) > 0:   
                                sack_weight_new += item.get_weight()
                                sack_cost_new += item.get_cost()
                                sack_resale_value_new += item.get_resale_value()
                                cutoff_new_items.append(item)
                                item = new_items.pop(0)
                            sack_objective_new = sack_resale_value_new + self.budget - sack_cost_new
                            if sack_objective_new > max_objective:
                                max_objective = sack_objective_new
                                swap_items = cutoff_new_items
                                swap_class = conflict_class


                if len(swap_items) > 0:
                    self.remove_item_list(items)
                    self.class_pool.remove(iclass)
                    self.conflicting_pool = new_conflicting_pool
                    self.add_item_list(swap_items)

        print("  Done improving.")


def read_file_and_build_collection(index, collection):

    print("  Read file and build tree ...")

    path_to_file = "./project_instances/problem" + str(index) + ".in"
    fid = open(path_to_file, "r")

    # pounds, dollars, number of items and number of constraints
    P = float(fid.readline())
    M = float(fid.readline())
    N = int(fid.readline())
    C = int(fid.readline())
    collection.set_parameter_tuple( (P, M, N, C) )

    for j in range(N):
        item_line = fid.readline()
        item_list = item_line.split(";")
        item = Item(item_list)
        collection.add_item(item)

    for k in range(C):
        constraint_line = fid.readline()
        constraint_set = set( [int(i) for i in constraint_line.split(",")] )
        collection.add_conflict(constraint_set)

    fid.close()
    print("  Done reading file")


def write_output(index, garg_sack):

    print("  Writing output ...")

    path_to_file = "./project_instances/output/problem" + str(i) + ".out"
    fid = open(path_to_file, "w")

    
    for item in garg_sack.get_sack():
        item_name = item.get_name()
        fid.write("%s\n" % item_name)    # fid.write("{0}\n".format(item_name))

    fid.close()

    P, M, N, C = garg_sack.get_collection().get_parameter_tuple() 
    print("    P: {0} pounds. M: {1} dollars".format(P, M))
    print("    Cost: %s dollars" % garg_sack.get_cost())
    print("    Weight: %s pounds" % garg_sack.get_weight())
    print("    Resale_value: %s dollars" % garg_sack.get_resale_value())
    print("    Objective: %s dollars" % garg_sack.get_objective())

if __name__ == "__main__":

    score_list = []
    mode = 0

    for i in range(1,22):

        if i == 3:
            mode = 3
        elif i == 21:
            mode = 21
        else:
            mode = 0

        print("Input " + str(i))
        collection = Collection()
        read_file_and_build_collection(i, collection)
        P, M, N, C = collection.get_parameter_tuple()
        garg_sack = GargSack(M, P, collection)
        garg_sack.pick_items()
        garg_sack.improve_sack()
        write_output(i, garg_sack)
        score_list.append( (garg_sack.get_objective() - M) / M )
        # print(score_list)
        print("    " + str(score_list[i-1]))

    print(sum(score_list) / float(len(score_list)))
    print("Done")
