# Programming Assignment 2: Greedy Algorithms
Name: Nam Tran
UFID: 19547941

## Project Description
This project implements and compares three cache eviction policies on the same request sequence: FIFO (First-In, First-Out), LRU (Least Recently Used), OPTFF (Belady’s Farthest-in-Future, optimal offline). In the written component following the comparison, we will prove that OPTFF is optimal.

## Repository Structure

```text
.
├── src/
│   └── cache.py
│
├── data/
│   ├── file1.in
│   ├── file2.in
│   ├── file3.in
│   ├── file4.in
│   ├── file5.in
│   ├── file6.in
│   ├── file7.in
│   ├── file8.in
│   └── q2_bad_sequence.in
│
├── tests/
│   ├── file1.out
│   ├── file2.out
│   ├── file3.out
│   ├── file4.out
│   ├── file5.out
│   ├── file6.out
│   ├── file7.out
│   ├── file8.out
│   └── q2_bad_sequence.out
│
└── README.md
```
- `src/` contains the Python source code implementation.
- `data/` contains the request sequence inputs.
- `tests/` contains the expected output for testing.

## Running Repository
After cloning the repository, run the following commands in command prompt or gitbash. 

You will run the program with an input file.
Example:
```text
python src/cache.py data/file1.in > tests/file1.out

#output will be written to the out file in the tests folder
```

Example output:
```text
FIFO  : 58
LRU   : 57
OPTFF : 35
```

You can test other files the same way.

## Written Component

### Question 1: Empirical Comparison
### Use at least three nontrivial input files (each containing 50 or more requests).
### For each file, report the number of cache misses for each policy.

| Input File | k | m | FIFO | LRU | OPTFF |
|---|---|---|---|---|---|
| File1 | 3 | 60 | 58 | 57 | 35 |
| File2 | 4 | 60 | 57 | 56 | 29 |
| File3 | 5 | 70 | 70 | 70 | 35 |
| File4 | 4 | 60 | 57 | 58 | 30 |
| File5 | 3 | 55 | 53 | 53 | 30 |
| File6 | 3 | 60 | 45 | 50 | 31 |
| File7 | 4 | 56 | 44 | 48 | 23 |
| File8 | 5 | 64 | 52 | 56 | 23 |

#### Does OPTFF have the fewest misses?
Yes, OPTFF has the fewest misses.

#### How does FIFO compare to LRU?
In several files, FIFO produces slightly fewer misses than LRU, while in some others LRU prudces slightly fewer. Therefore, neither FIFO nor LRU consistently performs better than the other.


### Question 2: Bad Sequence for LRU or FIFO
### For ( k = 3 ), investigate whether there exists a request sequence for which OPTFF incurs strictly fewer misses than LRU (or FIFO).
There exists a request sequence for which OPTFF incurs strictly fewer misses than LRU or FIFO. For this question, I created data/q2_bad_sequence.in:
```text
3 12
1 2 3 4 1 2 5 1 2 3 4 5
```
From the request sequence, I get the output tests/q2_bad_sequence.out:
| Policy | Misses |
|---|---|
| FIFO | 9 |
| LRU | 10 |
| OPTFF | 7 |

As FIFO evicts the page in the cache the longest and LRU evicts the page used least recently, neither considers future requests. Meanwhile, OPTFF evicts the page that has the next request occur farthest in the future. Knowing the entire request sequence, it avoids removing pages soon needed again -> incurs strictly fewer misses.

### Question 3: Prove OPTFF is Optimal
### Let OPTFF be Belady’s Farthest-in-Future algorithm. Let ( A ) be any offline algorithm that knows the full request sequence. Prove that the number of misses of OPTFF is no larger than that of ( A ) on any fixed sequence.
Let S_FF be the schedule produced by OPTFF. In this problem, we will prove the invariant: There exists an optimal reduced schedule that agrees with S_FF for the first j requests.

Proof by induction

Base case: For j = 0 (before any requests occur), the statement is trivially true.

Inductive step: Assume the invariant holds for the first j requests, which means there exists an optimal reduced schedule S that behaves exactly like OPTFF for the first j steps. Let d be the item requested in step j + 1. Since both schedules behave the same up to this point, they must have the same cache contents immediately before processing d -> 3 possibilities

Case 1: d is already in the cache
Both schedules have a cache hit and do not evict any page. Therefore, the schedules still agree after this request.

Case 2: d is a miss and both schedules evict the same page.
Both schedules still agree, so the invariant still holds.

Case 3: d is a miss and the schedules evict different pages.
Suppost OPTFF evicts page e, while the optimal schedule evicts page f, where f is different from e. By definition of OPTFF, page e is the page whose nect request occurs farthest in the future. Therefore, the next request for f occurs sooner than the next request for e. If we modify the optimal schedule so that it evicts e instead of f, then in the modified one, f remains in the cache. Since f is requested sooner than e, keeping f in the cache cannot increase the number of misses, and therefore does not make the schedule worse. As a result, the modified schedule is still optimal and agrees with OPTFF for one additional step, which contradicts with the invariant. 

To conclude, there must exist an optimal schedule that agrees with OPTFF for every request. Therefore, OPTFF is optimal and for any offline algorithm A, misses(OPTFF) <= misses(A).


