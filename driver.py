#! /usr/bin/env python3

import argparse, os, sys
from contextlib import redirect_stdout
from random import seed
import numpy as np

module = os.path.realpath(__file__).split(os.path.sep)[:-2]
module = os.path.sep.join(module)
if module not in sys.path:
  sys.path.insert(0, module)

sys.dont_write_bytecode = True
from cv_star_sensor.data.negatives.get_negs import get_negs
from cv_star_sensor.data.positives.mkpositive import markimg
from cv_star_sensor.test.detect import runtest
from cv_star_sensor.test.train import train

if __name__ == '__main__':
  parser = argparse.ArgumentParser(add_help=False,
                                formatter_class=argparse.RawTextHelpFormatter,
                                description=sys.argv[0] + \
                                  ' - the star CV thesis application',
                                argument_default=argparse.SUPPRESS,
                                prog=sys.argv[0],
                                epilog='Minimum arguments:\n' + \
                                'train or test')
  parser.add_argument('-h', '--help', action='store_true',
                      help='show this help message.')
  parser.add_argument('--seed', default=None, metavar=42,
                      help='set a constant random seed for reproducability')
  parser.add_argument('--negatives', metavar='ng1,ng2',
                      default='neg_southern2',
                      help='select negative groups to use')
  parser.add_argument('--noerode', action='store_true', default=False,
                      help='don\'t erode positive image in preprocessing')
  parser.add_argument('--cascade', metavar='new', default='cascades',
                      help='set cascade folder, either old or new')
  parser.add_argument('--nomarkpos', action='store_true', default=False,
                      help='don\'t mark the positive image before use')
  parser.add_argument('--train', metavar='img.png',
                      help='train from a fg marked positive image')
  parser.add_argument('--test', metavar='img.png',
                      help='run test on positive image')
  args = vars(parser.parse_args())
  if 'help' in args or ('train' not in args and 'test' not in args):
    parser.print_help()
    sys.exit(0)
  seed(args['seed'])
  np.random.seed(args['seed'])
  if 'train' in args:
    negatives = args['negatives'].split(',')
    get_negs(negatives)
    with open(os.devnull,'w') as devnull:
      img = markimg(args['train'], doerosion=(not args['noerode']))
      with redirect_stdout(devnull):
        boxes = runtest(img, args['cascade'].split(','), getboxes=True)
      boxes = [(x0,y0,x1,y1) for (_,x0,y0,x1,y1) in boxes]
    img = args['train'] if args['nomarkpos'] else \
          markimg(args['train'], doerosion=(not args['noerode']))
    train(img, boxes)
  if 'test' in args:
    img = args['test'] if args['nomarkpos'] else \
          markimg(args['test'], doerosion=(not args['noerode']))
    runtest(img, cascades=args['cascade'].split(','))

