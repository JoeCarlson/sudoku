#!/usr/bin/env python
"""Solve a sudoku puzzle by optimization"""

import numpy as np
from scipy.optimize import basinhopping
import subprocess
import json
import time
import sys
import random
import re


# the size
size = 3
siz2 = size*size

# columns of data
cols = np.full((siz2,siz2,siz2),.1)

# the coupling matrix
mat = np.full((siz2,siz2,siz2,siz2),0.)

for i in range(siz2):
  for j in range(siz2):
    for k in range(siz2):
      cols[i][j][k] = random.random()
      for l in range(siz2):
        if i==k and j==l:
           mat[i][j][k][l] = 0
        else:
          if i==k:
            mat[i][j][k][l] = 1
          if j==l:
            mat[i][j][k][l] = 1
          if i/size == k/size and j/size == l/size:
            mat[i][j][k][l] = 1

soln = {}
for i in range(siz2):
  const = np.full((siz2),0)
  const[i] = 1;
  soln[i] =  { 'vec': const, 'locs' : [] }

data = []
line =  raw_input()
if line == None:
  exit();
ctr = 0
for item in list(line):
  row = (ctr/9) + 1
  col = (ctr%9) + 1
  ctr = ctr + 1
  if re.search('^\d$',item):
    data.append([row,col,int(item)])

print data


for d in data:
  soln[d[2]-1]['locs'].append([d[0]-1,d[1]-1])

print soln

calcEval = 0
theTime = time.time()
numEval = 0
proc = subprocess.Popen(["./sudoku_display.py"], stdin=subprocess.PIPE)

def calccost(columns):
  cost = 0
  global theTime
  global soln
  global mat
  global numEval
  global proc
  global siz2
  numEval = numEval + 1
  cols = np.reshape(columns,(siz2,siz2,siz2))
  norm = 1./(np.sqrt(np.sum(np.square(cols),axis=2)));
  normcols = cols*norm;
  for s in soln:
    for p in soln[s]['locs']:
      cost = cost + np.sum(np.square(normcols[p[0]][p[1]] - soln[s]['vec']))

  cost = cost + np.einsum('jklm,jklm',mat,np.square(np.einsum('ijk,lmk->ijlm',normcols,normcols)))

  nowTime = time.time()
  if (nowTime - theTime > 1):
    jSon = { 'iteration': numEval, 'value': str(cost) }
    jdata = []
    for row in range(siz2):
        for col in range(siz2):
           dd = normcols[row][col];
           dd2 = dd.tolist();
           ele = { 'row':row+1, 'col':col+1,'data':dd2 }
           jdata.append(ele)
    jSon['data'] = jdata;
    proc.stdin.write(json.dumps(jSon)+'\n')
    print str(numEval)+"\t"+str(cost)
    theTime = nowTime;

  return cost

def calccost2(columns):
  cost = 0
  global theTime
  global soln
  global mat
  global numEval
  global proc
  global siz2
  cols = np.reshape(columns,(siz2,siz2,siz2))
  for s in soln:
    for p in soln[s]['locs']:
      cost = cost + np.sum(np.square(cols[p[0]][p[1]] - soln[s]['vec']))
  if cost < 0.1:
    return 0
  else:
    return cost



def calccost3(columns):
  cost = 0
  global theTime
  global soln
  global mat
  global numEval
  global proc
  global siz2
  numEval = numEval + 1
  cols = np.reshape(columns,(siz2,siz2,siz2))
  cost = cost + np.einsum('jklm,jklm',mat,np.square(np.einsum('ijk,lmk->ijlm',cols,cols)-dot))
  return cost

colArray = np.reshape(cols,(siz2*siz2*siz2))
lastCost = calccost(colArray)
while lastCost > 1:
  cc = basinhopping(calccost,colArray)
  lastCost = 0*calccost(cc.x)
  c2 = np.abs(np.reshape(cc.x,(siz2,siz2,siz2)))
  whichRC = np.argmax(c2,2)
  print whichRC
  colArray = np.reshape(np.full(siz2*siz2*siz2,0),(siz2,siz2,siz2))
  for r in range(siz2):
    for c in range(siz2):
      colArray[r][c][whichRC[r][c]] = 1
  colArray = np.reshape(colArray,(siz2*siz2*siz2))
  print 'total cost '+str(calccost(colArray))
  print 'fixed number cost '+str(calccost2(colArray))
  print 'orthonormal cost '+str(calccost3(colArray))
  exit
  
proc.stdin.close()

