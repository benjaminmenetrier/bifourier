#!/usr/bin/env python3

import math
import matplotlib.pyplot as plt
import numpy as np
import os
import copy

# Step 0
step0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])

# Sizes
nx = step0.shape[1]
ny = step0.shape[0]
nk = int(nx/2)+1
nl = int(ny/2)+1

# Truncation
ellips = np.zeros(nk, dtype=int)
ellips[0] = nl-1
for jk in range(0, nk-1):
  ellips[jk] = int((nl-1)/(nk-1)*np.sqrt((nk-1)*(nk-1)-(jk+1)*(jk+1))+1.0e-10)
ellips[nk-1] = -1
trunc = np.zeros((nl, nk))
for jk in range(nk):
  for jl in range(nl):
    trunc[jl, jk] = np.nan
for jk in range(nk):
  for jl in range(ellips[jk]+1):
    trunc[nl-1-jl, jk] = 1

# Step 1
step1 = np.zeros((ny, nx))
nyLocal = ny/3
it = 0
iyDone = 0
for iy in range(ny):
  step1[iy,:] = it
  iyDone += 1
  if iyDone >= nyLocal:
    it += 1
    iyDone = 0

# Step 2
step2 = np.zeros((ny, nk))
it = 0
iyDone = 0
for iy in range(ny):
  step2[iy,:] = it
  iyDone += 1
  if iyDone >= nyLocal:
    it += 1
    iyDone = 0

# Step 3
step3 = np.zeros((ny, nk))
nkLocal = nk/3
it = 0
ikDone = 0
for ik in range(nk):
  step3[:,ik] = it
  ikDone += 1
  if ikDone >= nkLocal:
    it += 1
    ikDone = 0

# Step 4
step4 = np.zeros((nl, nk))
it = 0
ikDone = 0
for ik in range(nk):
  step4[:,ik] = it
  ikDone += 1
  if ikDone >= nkLocal:
    it += 1
    ikDone = 0

# Step 5
step5_0 = copy.deepcopy(step4)
step5_1 = copy.deepcopy(step4)
step5_2 = copy.deepcopy(step4)
step5_3 = copy.deepcopy(step4)
step5_1[0,0] = np.nan
step5_2[0,0] = np.nan
step5_3[0,0] = np.nan
for il in range(nl):
  step5_2[il,0] = np.nan
  step5_3[il,0] = np.nan
  step5_2[il,nk-1] = np.nan
  step5_3[il,nk-1] = np.nan
for ik in range(nk):
  step5_1[0,ik] = np.nan
  step5_3[0,ik] = np.nan
  step5_1[nl-1,ik] = np.nan
  step5_3[nl-1,ik] = np.nan

# Step 6 
step6_0 = copy.deepcopy(step5_0)*trunc
step6_1 = copy.deepcopy(step5_1)*trunc
step6_2 = copy.deepcopy(step5_2)*trunc
step6_3 = copy.deepcopy(step5_3)*trunc

# Step 7
step7_0 = np.array([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [2, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [1, 1, 2, np.nan, np.nan, np.nan],
                    [0, 0, 1, 2, np.nan, np.nan],
                    [0, 0, 1, 1, 2, np.nan]])
step7_1 = copy.deepcopy(step7_0)
step7_2 = copy.deepcopy(step7_0)
step7_3 = copy.deepcopy(step7_0)
step7_1[0,0] = np.nan
step7_2[0,0] = np.nan
step7_3[0,0] = np.nan
for il in range(nl):
  step7_2[il,0] = np.nan
  step7_3[il,0] = np.nan
  step7_2[il,nk-1] = np.nan
  step7_3[il,nk-1] = np.nan
for ik in range(nk):
  step7_1[0,ik] = np.nan
  step7_3[0,ik] = np.nan
  step7_1[nl-1,ik] = np.nan
  step7_3[nl-1,ik] = np.nan

# Colormap
cmap = 'Paired'

# Plot step0
fig,ax = plt.subplots(ncols=1, nrows=1, figsize=(nx, ny))
ax.set_title('Physical space', fontsize=18)
ax.imshow(step0, interpolation ='nearest', cmap=cmap)
ax.set_xticks([0, nx-1], ['0', 'nx-1'], fontsize=14)
ax.set_yticks([0, ny-1], ['ny-1', '0'], fontsize=14)
for ix in range(nx):
  ax.axvline(x = float(ix)+0.5, color = 'k', linestyle = '-') 
for iy in range(ny):
  ax.axhline(y = float(iy)+0.5, color = 'k', linestyle = '-') 
plt.savefig('step0.pdf', format='pdf', dpi=300)
plt.close()
os.system('pdfcrop step0.pdf step0.pdf')

# Plot step1
fig,ax = plt.subplots(ncols=1, nrows=1,figsize=(nx, ny))
ax.set_title('Physical space', fontsize=18)
ax.imshow(step1, interpolation ='nearest', cmap=cmap)
ax.set_xticks([0, nx-1], ['0', 'nx-1'], fontsize=14)
ax.set_yticks([0, ny-1], ['ny-1', '0'], fontsize=14)
for ix in range(nx):
  ax.axvline(x = float(ix)+0.5, color = 'k', linestyle = '-') 
for iy in range(ny):
  ax.axhline(y = float(iy)+0.5, color = 'k', linestyle = '-') 
plt.savefig('step1.pdf', format='pdf', dpi=300)
plt.close()
os.system('pdfcrop step1.pdf step1.pdf')

# Plot step2
fig,ax = plt.subplots(ncols=2, nrows=1,figsize=(nx, ny))
ax[0].set_title('Real', fontsize=18)
ax[0].imshow(step2, interpolation ='nearest', cmap=cmap)
ax[0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0].set_yticks([0, ny-1], ['ny-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for iy in range(ny):
  ax[0].axhline(y = float(iy)+0.5, color = 'k', linestyle = '-') 
ax[1].set_title('Imaginary', fontsize=18)
ax[1].imshow(step2, interpolation ='nearest', cmap=cmap)
ax[1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1].set_yticks([0, ny-1], ['ny-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for iy in range(ny):
  ax[1].axhline(y = float(iy)+0.5, color = 'k', linestyle = '-')
plt.savefig('step2.pdf', format='pdf', dpi=300)
plt.close()
os.system('pdfcrop step2.pdf step2.pdf')

# Plot step3
fig,ax = plt.subplots(ncols=2, nrows=1,figsize=(nx, ny))
ax[0].set_title('Real', fontsize=18)
ax[0].imshow(step3, interpolation ='nearest', cmap=cmap)
ax[0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0].set_yticks([0, ny-1], ['ny-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for iy in range(ny):
  ax[0].axhline(y = float(iy)+0.5, color = 'k', linestyle = '-')
ax[1].set_title('Imaginary', fontsize=18)
ax[1].imshow(step3, interpolation ='nearest', cmap=cmap)
ax[1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1].set_yticks([0, ny-1], ['ny-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for iy in range(ny):
  ax[1].axhline(y = float(iy)+0.5, color = 'k', linestyle = '-')
plt.savefig('step3.pdf', format='pdf', dpi=300)
plt.close()
os.system('pdfcrop step3.pdf step3.pdf')

# Plot step4
fig,ax = plt.subplots(ncols=2, nrows=2,figsize=(nx, ny))
ax[0][0].set_title('Real/Real (q=0)', fontsize=18)
ax[0][0].imshow(step4, interpolation ='nearest', cmap=cmap)
ax[0][0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0][0].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0][0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[0][0].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
ax[0][1].set_title('Imaginary/Real (q=2)', fontsize=18)
ax[0][1].imshow(step4, interpolation ='nearest', cmap=cmap)
ax[0][1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0][1].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0][1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[0][1].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
ax[1][0].set_title('Real/Imaginary (q=1)', fontsize=18)
ax[1][0].imshow(step4, interpolation ='nearest', cmap=cmap)
ax[1][0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1][0].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1][0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[1][0].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
ax[1][1].set_title('Imaginary/Imaginary (q=3)', fontsize=18)
ax[1][1].imshow(step4, interpolation ='nearest', cmap=cmap)
ax[1][1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1][1].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1][1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[1][1].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
plt.savefig('step4.pdf', format='pdf', dpi=300)
plt.close()
os.system('pdfcrop step4.pdf step4.pdf')

# Plot step5
fig,ax = plt.subplots(ncols=2, nrows=2,figsize=(nx, ny))
ax[0][0].set_title('Real/Real (q=0)', fontsize=18)
ax[0][0].imshow(step5_0, interpolation ='nearest', cmap=cmap)
ax[0][0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0][0].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0][0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[0][0].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
ax[0][1].set_title('Imaginary/Real (q=2)', fontsize=18)
ax[0][1].imshow(step5_2, interpolation ='nearest', cmap=cmap)
ax[0][1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0][1].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0][1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[0][1].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
ax[1][0].set_title('Real/Imaginary (q=1)', fontsize=18)
ax[1][0].imshow(step5_1, interpolation ='nearest', cmap=cmap)
ax[1][0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1][0].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1][0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[1][0].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
ax[1][1].set_title('Imaginary/Imaginary (q=3)', fontsize=18)
ax[1][1].imshow(step5_3, interpolation ='nearest', cmap=cmap)
ax[1][1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1][1].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1][1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[1][1].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
plt.savefig('step5.pdf', format='pdf', dpi=300)
plt.close()
os.system('pdfcrop step5.pdf step5.pdf')

# Plot step6
fig,ax = plt.subplots(ncols=2, nrows=2,figsize=(nx, ny))
ax[0][0].set_title('Real/Real (q=0)', fontsize=18)
ax[0][0].imshow(step6_0, interpolation ='nearest', cmap=cmap)
ax[0][0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0][0].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0][0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[0][0].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')

ax[0][1].set_title('Imaginary/Real (q=2)', fontsize=18)
ax[0][1].imshow(step6_2, interpolation ='nearest', cmap=cmap)
ax[0][1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0][1].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0][1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[0][1].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')

ax[1][0].set_title('Real/Imaginary (q=1)', fontsize=18)
ax[1][0].imshow(step6_1, interpolation ='nearest', cmap=cmap)
ax[1][0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1][0].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1][0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[1][0].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')

ax[1][1].set_title('Imaginary/Imaginary (q=3)', fontsize=18)
ax[1][1].imshow(step6_3, interpolation ='nearest', cmap=cmap)
ax[1][1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1][1].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1][1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[1][1].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
plt.savefig('step6.pdf', format='pdf', dpi=300)
plt.close()
os.system('pdfcrop step6.pdf step6.pdf')

# Plot step7
fig,ax = plt.subplots(ncols=2, nrows=2,figsize=(nx, ny))
ax[0][0].set_title('Real/Real (q=0)', fontsize=18)
ax[0][0].imshow(step7_0, interpolation ='nearest', cmap=cmap)
ax[0][0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0][0].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0][0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[0][0].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')

ax[0][1].set_title('Imaginary/Real (q=2)', fontsize=18)
ax[0][1].imshow(step7_2, interpolation ='nearest', cmap=cmap)
ax[0][1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[0][1].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[0][1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[0][1].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')

ax[1][0].set_title('Real/Imaginary (q=1)', fontsize=18)
ax[1][0].imshow(step7_1, interpolation ='nearest', cmap=cmap)
ax[1][0].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1][0].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1][0].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[1][0].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')

ax[1][1].set_title('Imaginary/Imaginary (q=3)', fontsize=18)
ax[1][1].imshow(step7_3, interpolation ='nearest', cmap=cmap)
ax[1][1].set_xticks([0, nk-1], ['0', 'nk-1'], fontsize=14)
ax[1][1].set_yticks([0, nl-1], ['nl-1', '0'], fontsize=14)
for ik in range(nk):
  ax[1][1].axvline(x = float(ik)+0.5, color = 'k', linestyle = '-') 
for il in range(nl):
  ax[1][1].axhline(y = float(il)+0.5, color = 'k', linestyle = '-')
plt.savefig('step7.pdf', format='pdf', dpi=300)
plt.close()
os.system('pdfcrop step7.pdf step7.pdf')

