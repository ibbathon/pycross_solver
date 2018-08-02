# Puzzle-Solving Logic
#
# Author: Ibb Marsh
# Created: 2018-06-25
#
# Description: Handles the actual logic of each step of solving the picross puzzle.

class Cell:
	"""Helper class to allow multiple arrays to modify the same value."""
	def __init__ (self, val, pos):
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
		self._solved = False

	def set_sibling_blocks (self, prev_block, next_block):
		self.prev_block = prev_block
		self.next_block = next_block

	def solved (self):
		if self._solved:
			return self._solved
		if len(self.possibles) in (0,1):
			self._solved = True
		return self._solved

class Line:
	"""A line contains cells and blocks. It provides helper methods for interacting with the
	blocks as a whole, as well as reporting on whether it is solved."""
	def __init__ (self, cells, block_nums):
		self.cells = cells
		self.blocks = [Block(self,block_nums,i) for i in range(len(block_nums))]
		for i in range(len(block_nums)):
			prev_block = self.blocks[i-1] if i > 0 else None
			next_block = self.blocks[i+1] if i < len(block_nums)-1 else None
			self.blocks[i].set_sibling_blocks(prev_block,next_block)
		self._solved = False

	def solved (self):
		if self._solved:
			return self._solved
		for block in self.blocks:
			if not block.solved():
				return False
		self._solved = True
		return self._solved

class SolverLogic:
	pass
