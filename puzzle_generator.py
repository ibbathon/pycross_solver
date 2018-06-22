#!/usr/local/bin/python3
# Picross Puzzle Generator
#
# Author: Ibb Marsh
# Created: 2018-06-20
#
# Description: Generates a 2D array of bits and 2 1D arrays of counts of those bits for each
#  column/row. Outputs that data to an indicated JSON file.

import sys, argparse, random, json

class PuzzleGenerator:

  DEFAULT_PARAMS = {
    'width': 10,
    'height': 10,
    'size': 0,
    'base': 2,
    'filename': 'puzzle.json',
    'countsonly': False,
    'print': False,
  }

  def __init__ (self, argv):
    parser = self.build_parser()
    args = parser.parse_args(argv[1:])
    if args.size != self.DEFAULT_PARAMS['size']:
      args.width = args.height = args.size

    self.width = args.width
    self.height = args.height
    self.base = args.base
    self.filename = args.filename
    self.countsonly = args.countsonly
    self.printsolved = args.printsolved

  def run (self):
    grid = [[self.rand_value() for i in range(self.width)] for j in range(self.height)]
    rows = [self.count_blocks(grid[j]) for j in range(self.height)]
    cols = [self.count_blocks([row[i] for row in grid]) for i in range(self.width)]

    if self.printsolved:
      self.print_puzzle(grid,rows,cols,solved=True)

    jsondata = {
      'grid': grid if self.countsonly else [],
      'rows': rows,
      'cols': cols,
      'base': self.base,
    }
    with open(self.filename,'w') as f:
      json.dump(jsondata,f,indent=2)

  def build_parser (self):
    parser = argparse.ArgumentParser(description='Generates a 2D array of bits and 2 1D arrays'+ \
      ' of counts of those bits for each column/row. Outputs that data to an indicated JSON file.')
    parser.add_argument('-x','--width',default=self.DEFAULT_PARAMS['width'],type=int,
      help="Sets width of grid (default: {})".format(self.DEFAULT_PARAMS['width']))
    parser.add_argument('-y','--height',default=self.DEFAULT_PARAMS['height'],type=int,
      help="Sets height of grid (default: {})".format(self.DEFAULT_PARAMS['height']))
    parser.add_argument('-s','--size',default=self.DEFAULT_PARAMS['size'],type=int,
      help="Overrides both width and height")
    parser.add_argument('-b','--base',default=self.DEFAULT_PARAMS['base'],type=int,
      help="Sets base of grid values (default: {}; does not currently affect anything)".format(
        self.DEFAULT_PARAMS['base']))
    parser.add_argument('-f','--filename',default=self.DEFAULT_PARAMS['filename'],type=str,
      help="Sets output filename (default: {})".format(self.DEFAULT_PARAMS['filename']))
    parser.add_argument('-co','--countsonly',action='store_true',
      help="Do not write the full grid to the file (default: write full grid)")
    parser.add_argument('-p','--printsolved',action='store_true',
      help="Print the solved puzzle after generation (default: do not print)")
    return parser

  def rand_value (self):
    return random.randrange(self.base)

  def count_blocks (self, row):
    blocks = []
    acc = 0
    for v in row:
      if v == 0 and acc > 0:
        blocks.append(acc)
        acc = 0
      else:
        acc += v
    if acc > 0:
      blocks.append(acc)
    return blocks

  def max_blocks_len (self, blockslist):
    return max([self.blocks_len(blocks) for blocks in blockslist])

  def blocks_len (self, blocks):
    return len(' '.join([str(block) for block in blocks]))

  def max_num_blocks (self, blockslist):
    return max([len(blocks) for blocks in blockslist])

  def print_puzzle (self, grid, rows, cols, solved=True):
    maxrowblockslen = self.max_blocks_len(rows)
    maxcolnumblocks = self.max_num_blocks(cols)

    for i in range(maxcolnumblocks):
      print(' '*(maxrowblockslen+2),end='')
      print(' '.join([
        str(col[i+len(col)-maxcolnumblocks]) if (i+len(col)-maxcolnumblocks >= 0) else ' '
        for col in cols
      ]))
    print(' '*maxrowblockslen+' +'+'-'*(2*len(cols)-1))

    for i in range(len(rows)):
      row = rows[i]
      cellrow = grid[i]
      print(' '*(maxrowblockslen-self.blocks_len(row)),end='')
      print(' '.join([str(block) for block in row]),end='')
      print(' |',end='')
      if solved:
        print(' '.join([('*' if cell==1 else ' ') for cell in cellrow]),end='')
      print()


if __name__ == '__main__':
  pg = PuzzleGenerator(sys.argv)
  pg.run()
