#!/usr/bin/env python3
# Picross Puzzle Solver (CLI version)
#
# Author: Ibb Marsh
# Created: 2018-06-25
#
# Description: Accepts a JSON of 2 2D arrays of counts of bit blocks in each row/column.
# Solves for, and then outputs, all grids which fit those constraints.

import sys, argparse, json

class PuzzleSolver:
	DEFAULT_PARAMS = {
		'filename': 'puzzle.json',
	}

	def __init__ (self, argv):
		parser = self.build_parser()
		args = parser.parse_args(argv[1:])

		self.filename = args.filename

	def build_parser (self):
		parser = argparse.ArgumentParser(description='Accepts a JSON of 2 2D arrays of counts of '+ \
			'bit blocks in each row/column. Solves for, and then outputs, all grids which fit those '+ \
			'constraints.')
		parser.add_argument('-f','--filename',default=self.DEFAULT_PARAMS['filename'],type=str,
			help="Sets input filename (default: {})".format(self.DEFAULT_PARAMS['filename']))
		return parser

	def run (self):
		data = {}
		with open(self.filename,'r') as f:
			data = json.load(f)
		self.row_blocks = data['rows']
		self.col_blocks = data['cols']
		self.base = data['base']


if __name__ == '__main__':
	ps = PuzzleSolver(sys.argv)
	ps.run()
