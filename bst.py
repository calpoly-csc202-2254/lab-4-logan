import sys
# import random - for data collecting !!
# import time
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#

BinTree: TypeAlias = Union["Node",None]

@dataclass(frozen=True)
class Node:
    val: Any
    left: BinTree
    right: BinTree

#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#

# returns True if current value is greater than other one
def comes_before(cval:Any,oval:Any) -> bool:
    if cval < oval:
        return True
    else:
        return False

@dataclass(frozen=True)
class BinarySearchTree:
    cb: Callable[[any, any], bool]
    rest: BinTree

#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#

# return true if BST is empty, false if otherwise
def is_empty(bst:BinarySearchTree) -> bool:
    match bst:
        case BinarySearchTree(_,None):
            return True
        case BinarySearchTree(_,_):
            return False

# correctly insert given value into BST using comes_before()
def insert(bst:BinarySearchTree,val:Any) -> BinarySearchTree:
    def ins_helper(bt:BinTree) -> BinTree:
        if bt is None:
            return Node(val,None,None)
        if bst.cb(val,bt.val):
            return Node(bt.val,ins_helper(bt.left),bt.right)
        else:
            return Node(bt.val,bt.left,ins_helper(bt.right))
    return BinarySearchTree(bst.cb,ins_helper(bst.rest))

'''
# example by logan (other logan) to explain elif's lol
def f(x: int):
    val = 0
    if x > 10:
        val += 2
    else:
        val += 1
    return val
'''

# return True if given value is in BST, return False if not
def lookup(bst:BinarySearchTree,val:Any) -> bool:
    def lkp_helper(bt:BinTree) -> bool:
        if bt is None:
            return False
        if bst.cb(bt.val,val) is False and bst.cb(val,bt.val) is False:
            return True
        if bst.cb(val,bt.val) is True:
            return lkp_helper(bt.left)
        if bst.cb(val,bt.val) is False:
            return lkp_helper(bt.right)
    return lkp_helper(bst.rest)

# delete Node whose value matches given value, return BST
def delete(bst:BinarySearchTree,val:Any) -> BinarySearchTree:
    def del_helper(bt:BinTree) -> BinTree:
        if bt is None:
            return None
        if bst.cb(bt.val,val) is False and bst.cb(val,bt.val) is False:
            if bt.left is None and bt.right is None:
                return None
            elif bt.left is None:
                return bt.right
            elif bt.right is None:
                return bt.left
            else:  # AAEGGEGHHEGGRGGRGGRHHRGGRGHRHHRGGHGHGHHRGGHGHGHHGHRGHRG
                def remove_min(bt0:BinTree) -> (Any,BinTree):
                    if bt0.left is None:
                        return bt0.val, bt0.right
                    min_val,new_left = remove_min(bt0.left)
                    return min_val, Node(bt0.val,new_left,bt0.right)
                mv,nr = remove_min(bt.right)
                return Node(mv,bt.left,nr)
        if bst.cb(val,bt.val) is True:
            return Node(bt.val,del_helper(bt.left),bt.right)
        if bst.cb(val,bt.val) is False:
            return Node(bt.val,bt.left,del_helper(bt.right))
    return BinarySearchTree(bst.cb,del_helper(bst.rest))

#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#

'''
# makes a BST of given size with random numbers (for testing) :3
def build_random_bst(size:int) -> BinarySearchTree:
    bst = BinarySearchTree(comes_before,None)
    for idx in range(size):
        bst = insert(bst,random.random())
    return bst

# tests time for insert()
for num in [100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000]:
    times = []
    for _ in [1,2,3]:
        inst = build_random_bst(num)
        start = time.perf_counter()
        insert(inst,2)
        end = time.perf_counter()
        times.append(end-start)
    avgtime = sum(times)/3
    print("insert("+str(num)+") time:",avgtime)

# tests time for lookup()
for num in [100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000]:
    times = []
    for _ in [1,2,3]:
        inst = build_random_bst(num)
        start = time.perf_counter()
        lookup(inst,2)
        end = time.perf_counter()
        times.append(end-start)
    avgtime = sum(times)/3
    print("lookup("+str(num)+") time:",avgtime)
'''

#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#

# test cases:

class TestCase(unittest.TestCase):
    def test_is_empty_1(self):
        ex = BinarySearchTree(comes_before,None)
        self.assertTrue(is_empty(ex))

    def test_is_empty_2(self):
        ex = BinarySearchTree(comes_before,Node("twenty wan",None,None))
        self.assertFalse(is_empty(ex))

    def test_insert_1(self):
        ex = insert(BinarySearchTree(comes_before,None),5)
        self.assertEqual(5,ex.rest.val)

    def test_insert_2(self):
        ex = insert(BinarySearchTree(comes_before,Node(4,None,None)),5)
        self.assertEqual(5,ex.rest.right.val)

    def test_lookup_1(self):
        ex = BinarySearchTree(comes_before,Node(6,None,None))
        self.assertFalse(lookup(ex,66))

    def test_lookup_2(self):
        ex = BinarySearchTree(comes_before,Node("yah yah",None,None))
        self.assertTrue(lookup(ex,"yah yah"))

if __name__ == '__main__':
    unittest.main()
