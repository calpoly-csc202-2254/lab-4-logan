import sys
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
    cb: Callable
    rest: BinTree

#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#

# return true if BST is empty, false if otherwise
def is_empty(bst:BinarySearchTree) -> bool:
    match bst:
        case BinarySearchTree(c,None):
            return True
        case BinarySearchTree(c,r):
            return False

# correctly insert given value into BST using comes_before()
def insert(bst:BinarySearchTree,val:Any) -> BinarySearchTree:
    def ins_helper(bt:BinTree) -> BinTree:
        if bt is None:
            return Node(val,None,None)
        if bst.cb(val,bt.val) is True:
            return Node(bt.val,ins_helper(bt.left),bt.right)
        if bst.cb(val,bt.val) is False:
            return Node(bt.val,bt.left,ins_helper(bt.right))
    return BinarySearchTree(bst.cb,ins_helper(bst.rest))

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
            if bt.left is None:
                return bt.right
            if bt.right is None:
                return bt.left
            else:  # AAEGGEGHHEGGRGGRGGRHHRGGRGHRHHRGGHGHGHHRGGHGHGHHGHRGHRG

        if bst.cb(val,bt.val) is True:
            return Node(bt.val,del_helper(bt.left),bt.right)
        if bst.cb(val,bt.val) is False:
            return Node(bt.val,bt.left,del_helper(bt.right))
    return BinarySearchTree(bst.cb,del_helper(bst.rest))

#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#~~~#

tst = BinarySearchTree(comes_before,None)
tst = insert(tst,5)
tst = insert(tst,3)
tst = insert(tst,7)
tst = insert(tst,6)

print("\ndebugging :3\n","\nold:\n",tst,"\n\nnew:\n",delete(tst,5))

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
