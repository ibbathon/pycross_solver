# Puzzle-Solving Logic
#
# Author: Ibb Marsh
# Created: 2018-06-25
#
# Description: Handles the actual logic of each step of solving the picross puzzle.

class Cell:
	"""Helper class to allow multiple arrays to modify the same value."""
	def __init__ (self, val):
		self.value = val
		self.parent_lines = []
		self.parent_blocks = []

class Block:
	"""A block defines a complete, contiguous, same-color part of a line.
	e.g. if a line is [1,2,5,2] then one of the blocks would correspond to the 5"""
	def __init__ (self, line, block_nums, block_index):
		self.parent_line = line
		# Now determine in what range the block could exist
		cells_start_index = sum(block_nums[:block_index])+(block_index)
		buffer_end = sum(block_nums[block_index+1:])+(len(block_nums)-block_index-1)
		cells_end_index = len(self.parent_line.cells) - buffer_end
		# So the block exists somewhere in the range(cells_start_index,cells_end_index).
		# Now we just iterate through the range and make lists of those cells which would work.
		self.possibles = []
		block_len = block_nums[block_index]
		for i in range(cells_start_index,cells_end_index-block_len+1):
			self.possibles.append(self.parent_line.cells[i:i+block_len])

class SolverLogic:
	pass
