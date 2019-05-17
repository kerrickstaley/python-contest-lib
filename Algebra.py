#!/usr/bin/python3

# basic gcd
def gcd(a, b):
  if a < 0:
    return gcd(-a, b)
  if b < 0:
    return gcd(a, -b)
  while b:
    a, b = b, a % b
  return a


# basic lcm
def lcm(a, b):
  if a < 0:
    return lcm(-a, b)
  if b < 0:
    return lcm(a, -b)
  return a // gcd(a, b) * b  # avoids overflow


# returns (gcd(a, b), x, y) such that gcd(a,b) = ax + by
def egcd(a, b):
  if a < 0:
    r, x, y = egcd(-a, b, x, y)
    x *= -1
    return r, x, y
  if b < 0:
    r, x, y = egcd(a, -b, x, y)
    y *= -1
    return r, x, y
  u = y = 0
  v = x = 1
  while b:
    q = a // b
    a, b = b, a % b
    x, y, u, v = u, v, x - q * u, y - q * v
  return a, x, y


# Chinese remainder theorem, simple version.
# Given a, b, n, m, find z which simultaneously satisfies
#     z = a (mod m)  and  z = b (mod n).
# This z, when it exists, is unique mod lcm(n,m).
# If such z does not exist, then return -1.
# z exists iff a == b (mod gcd(m,n))
def CRT(a, m, b, n):
  g, s, t = egcd(m, n)
  l = m // g * n
  r = a % g
  if b % g != r:
    return -1
  if g == 1:
    s = s % abs(l)
    t = t % abs(l)
    r1 = s * b % l
    r2 = t * a % l
    r1 = r1 * m % l
    r2 = r2 * n % l
    return (r1 + r2) % l
  else:
    return g * CRT(a // g, m // g, b // g, n // g) + r


# Chinese remainder theorem, extended version.
# Given a[K] and n[K], find z so that, for every i,
#     z = a[i] (mod n[i])
# The solution is unique mod lcm( n[i] ) when it exists.
# The existence criteria is just the extended version of what it is above.
def CRT_ext(a, n):
  ret = a[0]
  l = n[0]
  for i in range(1, len(a)):
    ret = CRT(ret, l, a[i], n[i])
    l = lcm(l, n[i])
    if ret == -1:
      return -1
  return ret


# END

import sys


def test_gcd():
  print("test gcd", file=sys.stderr)
  if gcd( 4, 7) != 1:
    print('gcd( 4, 7) != 1', file=sys.stderr)
  if gcd( 0, 7) != 7:
    print('gcd( 0, 7) != 7', file=sys.stderr)
  if gcd(14, 7) != 7:
    print('gcd(14, 7) != 7', file=sys.stderr)
  if gcd(14,21) != 7:
    print('gcd(14,21) != 7', file=sys.stderr)
  if gcd(-7, 7) != 7:
    print('gcd(-7, 7) != 7', file=sys.stderr)
  if gcd(-7,-7) != 7:
    print('gcd(-7,-7) != 7', file=sys.stderr)


def test_lcm():
  print("test lcm", file=sys.stderr)
  for a in range(1, 100):
    for b in range(1, 100):
      if gcd(a, b) * lcm(a, b) != a * b:
        print('lcm * gcd != product:', a, b, file=sys.stderr)


def test_egcd():
  print("test egcd", file=sys.stderr)
  for a in range(0, 100):
    for b in range(0, 100):
      g, s, t = egcd(a, b)
      if gcd(a, b) != g:
        print('gcd != egcd:', a, b, file=sys.stderr)
      if s * a + b * t != g:
        print('egcd s*a + t*b = g fail:', a, b, file=sys.stderr)


def test_CRT():
  print("test CRT", file=sys.stderr)
  for m in range(1, 100):
    for n in range(1, 100):
      for a in range(0, m):
        for b in range(0, n):
          z = CRT(a, m, b, n)
          g = gcd(m, n)
          if a % g != b % g and z != -1:
            print('CRT gave an impossible solution:  z =', a, 'mod', m, 'and z =', b, 'mod', n, file=sys.stderr)
          if a % g == b % g:
            if z % m != a or z % n != b:
              print('CRT gave a bad solution: z =', a, 'mod', m, 'and z =', b, 'mod', n, file=sys.stderr)


if __name__ == '__main__' and not hasattr(sys, 'ps1'):
  test_gcd()
  test_lcm()
  test_egcd()
  test_CRT()
