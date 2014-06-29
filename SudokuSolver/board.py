"""
Models a Sudoku board - this file can be run for a command-line interface

Author: Rajiv Thamburaj
"""

class Board(object):
	"""
	Models a Sudoku board
	"""
	
	def __init__(self, board_numbers, board_size=9):
		"""
		Initialize the board
		"""
		self.numbers = board_numbers
		self.size = board_size
	
	def is_solvable(self):
		"""
		Returns a boolean that corresponds to the solvability of the puzzle
		"""
		# A Sudoku puzzle requires at least 17 entries to have a
		# unique solution
		MINIMUM_ENTRIES = 17
		MAXIMUM_EMPTY_CELLS = self.size*self.size - MINIMUM_ENTRIES
		num_empty_cells = self.numbers.count('0')
		
		if num_empty_cells > MAXIMUM_EMPTY_CELLS:
			return False
		elif not(self.is_valid()):
			return False
		return True
	
	def is_valid(self):
		"""
		Make sure that the puzzle is valid (no repeated numbers in a row,
		column, or square)
		"""
		N = self.size
		n = N/3
		
		# Loop through all rows/columns/squares
		for i in xrange(N):
			row_numbers = []
			column_numbers = []
			square_numbers = []
			
			# Loop through the numbers in each row/column/square
			for j in xrange(N):
				row_index = N*i + j
				column_index = i + N*j
				square_index = (i/n)*N*n + (i%n)*N/n + (j/n)*N + (j%n)
				
				row_numbers.append(self.numbers[row_index])
				column_numbers.append(self.numbers[column_index])
				square_numbers.append(self.numbers[square_index])
			
			if (self.contains_duplicates(row_numbers) or
				self.contains_duplicates(column_numbers) or
				self.contains_duplicates(square_numbers)):
				return False
		
		return True

	def contains_duplicates(self, list):
		"""
		Checks a list for duplicates
		"""
		# Remove all '0's from the list
		list_copy = []
		for element in list:
			if element != '0':
				list_copy.append(element)
		
		# Turning the list to a set removes duplicates
		list_as_set = set(list_copy)
		
		if len(list_copy) == len(list_as_set):
			return False
		return True
	
	def try_solve(self):
		"""
		Solve the puzzle!
		"""
		# First, attempt a solution by logical methods
		self.logic_solve()
		# When we can't get any further, start backtracking
		self.backtrack_solve(Board(self.numbers, self.size))
	
	def was_solved(self):
		"""
		If the initial entries are nontrivially inconsistent, then it is
		not possible to tell that there is no solution until a solve is
		attempted. Thus, this method should be called after try_solve()
		to verify that a correct solution was produced.
		"""
		return not('0' in self.numbers)
	
	def logic_solve(self):
		"""
		Solve the puzzle as far as possible by logic - see if there are any
		positions where only one number is possible. If a pass of the entire
		board is made without changing a number, then we can proceed no further
		with this method.
		"""
		N = self.size
		# A search is "successful" if a position is modified in one pass
		# of the board
		successful_search = True	
		
		# Continue looping until a search is not successful
		while successful_search:
			successful_search = False
			
			# Loop through the entire board
			for i in range(N*N):
				# Don't look at nonempty positions
				if self.numbers[i] != "0":
					continue
				
				valid_numbers_list = list(self.get_valid_numbers(i))
				
				# If there is only one valid number, insert it
				if len(valid_numbers_list) == 1:
					successful_search = True
					self.numbers = self.numbers[:i] + \
					               valid_numbers_list[0] + self.numbers[i+1:]
	
	def backtrack_solve(self, board_copy):
		"""
		Solve the puzzle by backtracking - guessing a number from a list of
		available numbers and then continuing until a contradiction is reached
		(i.e. there is a position which has no valid numbers) or the puzzle
		is complete
		"""
		# Find the first unknown position on the board
		first_unknown = board_copy.numbers.find("0")
		# If there's no unknown position, the puzzle is solved!
		if first_unknown == -1:
			self.numbers = board_copy.numbers
			return
		
		valid_numbers = board_copy.get_valid_numbers(first_unknown)	
		for number in valid_numbers:
			# Insert the number at the correct index
			board_copy.numbers = board_copy.numbers[:first_unknown] + number + \
			                     board_copy.numbers[first_unknown+1:]
			# Call recursively with a copy of the board (the previous operation
			# essentially copied the string of numbers)
			self.backtrack_solve(Board(board_copy.numbers, self.size))
	
	def get_valid_numbers(self, current_index):
		"""
		Gets the set of all valid numbers that can be placed at the given
		postion
		"""
		N = self.size
		n = N/3
		row_number = current_index / N
		column_number = current_index % N
		# This is the location of the upper left position in the
		# current square
		square_index = (row_number / n)*N*n + (column_number / n)*N/n
		invalid_numbers = set()
		
		# Find all numbers that are not valid (the same number cannot
		# be repeated
		# in the row, column, or square)
		for i in xrange(N):
			# Find all invalid numbers in the same row
			invalid_numbers.add(self.numbers[N*row_number + i])
			# Find all invalid numbers in the same column
			invalid_numbers.add(self.numbers[column_number + N*i])
			# Find all invalid numbers in the same square
			invalid_numbers.add(self.numbers[square_index + i%n + i/n*N])
		
		all_numbers = set(str(i) for i in xrange(N+1))
		valid_numbers = all_numbers.difference(invalid_numbers)
		return valid_numbers
	
	def __repr__(self):
		"""
		Unambiguous representation
		"""
		return "Board('" + self.numbers + "', " + str(self.size) + ")"
	
	def __str__(self):
		"""
		A more readable representation
		"""
		N = self.size
		n = N/3
		output_string = ""
		
		for i in range(N*N):
			# Add the current number to the string
			output_string += self.numbers[i]
			
			# Don't add any markers after the final number
			if i != N*N-1:
				# Add a line break at the end of the row
				if (i+1) % N == 0:
					output_string += "\n"
				# Add a separator at every third column
				elif (i+1) % n == 0:
					output_string += " | "
				# Add a space at every other number
				else:
					output_string += " "
			
				# Add a horizontal rule at every third row
				if (i+1) % (N*3) == 0:
					output_string += "---------------------\n"
		
		return output_string

if __name__ == "__main__":
	"""
	Main method - if this module is run, this method can be used for a
	command-line interface
	"""
	# Initialize the board from a string
	board_numbers = raw_input("Enter numbers, as a single string (no spaces): ")
	board = Board(board_numbers)
	
	# Print the board
	print "\nHere is the board:\n"
	print str(board)
	# Solve the puzzle and print the solution
	if board.is_solvable():
		board.try_solve()
		if board.was_solved():
			print "\nAnd here is the solution:\n"
			print str(board)
		else:
			print "\nSorry, no unique solution exists."
	else:
		print "\nSorry, no unique solution exists."