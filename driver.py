#! /usr/bin/env python3

import argparse, os, sys

module = os.path.realpath(__file__).split(os.path.sep)[:-2]
module = os.path.sep.join(module)
if module not in sys.path:
  sys.path.insert(0, module)

sys.dont_write_bytecode = True
from cv_star_sensor.data.negatives.get_negs import get_negs
from cv_star_sensor.data.positives.mkpositive import markimg
from cv_star_sensor.test.detect import runtest

if __name__ == '__main__':
  parser = argparse.ArgumentParser(add_help=False,
                                formatter_class=argparse.RawTextHelpFormatter,
                                description=sys.argv[0] + \
                                  ' the star CV thesis application',
                                argument_default=argparse.SUPPRESS,
                                prog=sys.argv[0])
  parser.add_argument('-h', '--help', action='store_true',
                      help='show this help message.')
  parser.add_argument('--negatives', metavar='negative1,negative2',
                      default='neg_southern2',
                      help='select negative groups to use')
  parser.add_argument('--positive', metavar='img.png',
                      help='select a single positive image to use')
  parser.add_argument('--test', metavar='img.png',
                      help='run test on marked image')
  args = vars(parser.parse_args())
  if 'help' in args:
    parser.print_help()
    sys.exit(0)
  negatives = args['negatives'].split(',')
  get_negs(negatives)
  if 'positive' in args:
    markimg(args['positive']) #,'testbig.png','testsm.png')
  if 'test' in args:
    runtest(args['test'])

