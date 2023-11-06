#! /usr/bin/env python3

import os, sys, zipfile

def get_negs(negatives=['neg_southern2']):
  print('Negatives:', ', '.join(negatives))
  # Negatives to use
  thisdir = os.path.realpath(__file__).split(os.path.sep)[:-1]
  negatives = [os.path.sep.join(thisdir+[negative]) for negative in negatives]
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
    files += [os.path.sep.join([negative,name]) \
              for name in os.listdir(negative) \
              if name.endswith('.jpg')]
  # Create bg.txt with names of all negatives
  with open(os.path.sep.join(thisdir+['bg.txt']),'w') as outfile:
    outfile.write('\n'.join(files))

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('This script will decompress (as needed) negative image sets')
    print('A file, bg.txt, will be created which lists negative files')
    print('Usage:')
    print(f'python3 {sys.argv[0]} negative1,negative2')
    sys.exit(1)
  get_negs(sys.argv[1].split(','))
