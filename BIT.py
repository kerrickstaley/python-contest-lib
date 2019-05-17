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
    while i <= N:
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
    while del_ and r <= N:
      q = r + del_
      if self.A[q] <= thresh:
        r = q
        thresh -= self.A[q]
      del //= 2
    return r - 1
