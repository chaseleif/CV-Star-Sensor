#! /usr/bin/env python3

import os, zipfile

# Negatives to use
negatives=['neg_southern2']

# Get a list of negative files within all negative folders
files = []
for negative in negatives:
  # If we don't have the folder
  if not os.path.isdir(negative):
    # If we don't have the zip
    if not os.path.isfile(negative+'.zip'):
      print(f'Cannot use negative {negative}, no folder or zip file found')
      continue
    # Make the folder and extract the zip
    os.mkdir(negative)
    with zipfile.ZipFile(negative+'.zip','r') as inzip:
      inzip.extractall(negative)
  # Add all names within the folder
  files += [os.path.sep.join([negative,name]) for name in os.listdir(negative)]

# Create bg.txt with names of all negatives
with open('bg.txt','w') as outfile:
  outfile.write('\n'.join(files))

