#!/usr/bin/python3

# Least significant bit of a. Used throughout.
def LSB(a):
  return a ^ (a & (a-1))


# To use it, instantiate it as `BIT(n)' where n is the size of the underlying
# array. The BIT then assumes a value of 0 for every element. Update each
# index individually (with `add') to use a different set of values.
#
# Note that it is assumed that the underlying array has size a power of 2!
# This mostly just simplifies the implementation without any loss in speed.
# Just use the closest power of 2 larger than the max input size. Even if some test
# cases do not test this high, initialization is extremely quick.
#
# The comments below make reference to an array `arry'. This is the underlying
# array. (A is the data stored in the actual tree.)
class BIT:
  def __init__(self, n):
    # n must be a power of 2
    self.N = n
    self.A = [0] * (n + 1)

  # add v to arry[idx]
  def add(self, idx, v):
    i = idx + 1
    while i <= self.N:
      self.A[i] += v
      i += LSB(i)

  # get sum( arry[0..idx] )
  def sum(self, idx):
    ret = 0
    i = idx + 1
    while i > 0:
      ret += self.A[i]
      i -= LSB(i)
    return ret

  # get sum(arry[l..r])
  def sum_range(self, l, r):
    return self.sum(r) - self.sum(l - 1)

  # Find largest r so that sum( arry[0..r] ) <= thresh
  # This assumes arry[i] >= 0 for all i > 0, for monotonicity.
  # This takes advantage of the specific structure of LSB() to simplify the
  # binary search.
  def largest_at_most(self, thresh):
    r = 0
    del_ = self.N
    while del_ and r <= self.N:
      q = r + del_
      if self.A[q] <= thresh:
        r = q
        thresh -= self.A[q]
      del_ //= 2
    return r - 1


# END

import sys


def test_BIT_correct():
  success = True
  # only two test suites...
  N = 1 << 5
  NN = N * N  # ~1e3
  tr = BIT(NN)  # BIT on NN elts
  # Basic tests
  for i in range(NN):
    tr.add(i, 56 * i * (i + 3))
  A = [0] * (NN + 1)  # prefix sums, for checking
  for i in range(1, tr.N + 1):
    A[i] = A[i - 1] + 56 * (i - 1) * (i + 2)
  for q in range(NN + 1):
    result = tr.sum(q - 1)
    if result != A[q]:
      success = False
      print('Error in BIT.add/sum(', q, '): Expected:', A[q], ', Actual:', result, file=sys.stderr)
  for qL in range(0, N):
    for qR in range(qL, qL + N):
      result = tr.sum_range(qL, qR - 1)
      if result != A[qR] - A[qL]:
        success = False
        print('Error in BIT.sum_range(', qL, ', ', qR - 1, '): ', end='', file=sys.stderr)
        print('Expected: ', A[qR] - A[qL], ', Actual: ', result, file=sys.stderr)

  N = 1 << 7
  tr = BIT(N)
  A = [0] * N
  tr.add( 6, 14 );   A[6]   += 14
  tr.add( 28, 52 );  A[28]  += 52
  tr.add( 24, 2 );   A[24]  += 2
  tr.add( 99, 0 );   A[99]  += 0
  tr.add( 99, 1 );   A[99]  += 1
  tr.add( 99, 3 );   A[99]  += 3
  tr.add( 100, 4 );  A[100] += 4
  tr.add( 91,4 );    A[91]  += 4
  AS = [0] * (len(A) + 1)
  for i in range(1, len(AS)):
    AS[i] = AS[i - 1] + A[i - 1]
  UB = AS[-1]
  for q in range(UB):
    result = tr.largest_at_most(q) + 1
    exp = 0
    while exp + 1 < len(AS) and AS[exp + 1] <= q:
      exp += 1
    if result != exp:
      success = False
      print('Error in BIT.largest_at_most(', q, '): ', end='', file=sys.stderr)
      print('Expected: ', exp, ', Actual: ', result, file=sys.stderr)

  if success:
        print('BIT correct!', file=sys.stderr)


if __name__ == '__main__' and not hasattr(sys, 'ps1'):
  test_BIT_correct()
