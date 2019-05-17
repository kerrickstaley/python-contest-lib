#!/usr/bin/python3
# This file is a bonus; it's not based on anything in
# https://github.com/atmorgan/ICPC2014

# Returns an iterator over all permutations of `elems`, in lexicographical order.
# Equivalent elements of `elems` will reduce the total number of permutations; for example, the
# permutations of aab are aab, aba, and baa.
# Takes 8.5 seconds to go through all permutations of 10 elements and no-op, anything larger than
# that is not contest viable (and if you're doing any non-trivial work in the loop it's not viable
# either).
def permutations(elems):
  return _permutations([], list(sorted(elems)))


def _permutations(initial, remaining):
  if not remaining:
    yield initial

  seen = set()
  for idx, next_ in enumerate(remaining):
    if next_ in seen:
      continue
    seen.add(next_)
    yield from _permutations(initial + [next_], remaining[:idx] + remaining[idx + 1:])


# END

import sys


def test_permutations():
  print('test permutations', file=sys.stderr)
  expected = [
    ['a', 'b', 'c'],
    ['a', 'c', 'b'],
    ['b', 'a', 'c'],
    ['b', 'c', 'a'],
    ['c', 'a', 'b'],
    ['c', 'b', 'a'],
  ]
  actual = list(permutations('bac'))
  if actual != expected:
    raise Exception(f"expected permutations('bac') = {expected}, actual was {actual}")

  expected = [
    [1, 1, 2],
    [1, 2, 1],
    [2, 1, 1],
  ]
  actual = list(permutations([1, 2, 1]))
  if actual != expected:
    raise Exception(f"expected permutations([1, 2, 1]) = {expected}, actual was {actual}")



if __name__ == '__main__' and not hasattr(sys, 'ps1'):
  test_permutations()
