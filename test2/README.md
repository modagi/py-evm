# Frontier vs Simple2

```
$ python test.gas.py
Consider installing rusty-rlp to improve pyrlp performance with a rust based backend
BLOCK0(Genesis) SENDER BALANCE : 10000000000000000000
BLOCK0(Genesis) RECEIVER BALANCE : 0
BLOCK1 SENDER BALANCE : 10000000000000000000
BLOCK1 RECEIVER BALANCE : 0
block: Block #2-0xfb6b..6d9a
BLOCK2 SENDER BALANCE : 9999999999995793990
BLOCK2 RECEIVER BALANCE : 10
```

```
$ python test.nogas.py
Consider installing rusty-rlp to improve pyrlp performance with a rust based backend
BLOCK0(Genesis) SENDER BALANCE : 10000000000000000000
BLOCK0(Genesis) RECEIVER BALANCE : 0
BLOCK1 SENDER BALANCE : 10000000000000000000
BLOCK1 RECEIVER BALANCE : 0
block: Block #2-0x44da..bcea
BLOCK2 SENDER BALANCE : 9999999999999999990
BLOCK2 RECEIVER BALANCE : 10
```
