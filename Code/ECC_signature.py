#!/usr/bin/env python
# coding: utf-8

# In[1]:


# R: y**2 = x**3 + a*x + b mod p
# s = (y2 - y1) / (x2 - x1) mod p (addition)
# s = (3*(x1**2) + a) / 2*y1 mod p (doubling)
# x3 = s**2 - x1 - x2 mod p
# y3 = s*(x1-x3)-y1 mod p


# In[33]:


import random
import numpy as np


# In[77]:


a = 2
b = 2
p = 17
base = point(5,1)
n = 19 # order


def div(a, p):
    for i in range(p):
        if i * a % p == 1:
            return i
    print(a)

class point():
    def __init__(self, x, y):
        self.x = x
        self.y = y



def ecc_function(base, n, p):
    ecc = []
    for i in range(1,n):
        if i == 1:
            A = base
            ecc.append(A)
            continue
        B = point(5,1)
        # tmp = 0 # 0 addition, 1 doubling


        if A.x != B.x or A.y != B.y:
            s = ((B.y - A.y) * div(B.x - A.x, p)) % p
            tx = ((s**2) - A.x - B.x) % p
            ty = (s*(A.x - tx) - A.y) % p
            ans = point(tx, ty)
        else:
            s = ((3*(A.x**2) + a) * div(2*A.y, p)) % p
            tx = ((s**2) - A.x - A.x) % p
            ty = (s*(A.x - tx) - A.y) % p
            ans = point(tx, ty)
        A = ans
        ecc.append(ans)
    return ecc
ecc = ecc_function(base, n, p)


# In[80]:


for i in range(n-1):
    print(ecc[i].x, ecc[i].y)


# In[95]:


m = "I'm peanut!"
e = hash(m)
if e < 0:
    z = int((str(bin(e))[3:n+3]), 2)
else:
    z = int((str(bin(e))[2:n+2]), 2)
print(z)
dA = 6 # choose by yourself
QA = ecc[dA-1]
while(1):
    k = random.randint(1,n-1)
    secret = ecc[k-1]
    r = secret.x % n
    s = div(k, n) * (z + r*dA) % n
    if r == 0 or s == 0:
        continue
    signature = (r, s)
    break


# In[96]:


signature, k


# In[99]:


e = hash(m)
if e < 0:
    z = int((str(bin(e))[3:n+3]), 2)
else:
    z = int((str(bin(e))[2:n+2]), 2)
w = div(signature[1], n)
u1 = (z * w) % n
u2 = (signature[0] * w) % n
tmp = (u1 + u2*dA)%n
if u2 * dA % n != 0:
    verify = ecc[tmp-1]
else:
    print("Error!")
if verify.x == signature[0]:
    print("No problem!")
else:
    print("Error")

