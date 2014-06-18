"""
Models a Sudoku board - this file can be run for a command-line interface

Author: Rajiv Thamburaj
"""

class Board(object):
	"""
	Models a Sudoku board
	"""
	
	def __init__(self, boardNumbers, boardSize=9):
		"""
		Initialize the board
		"""
		self.numbers = boardNumbers
		self.size = boardSize
	
	def isSolvable(self):
		"""
		Returns a boolean that corresponds to the solvability of the puzzle
		"""
		# A Sudoku puzzle requires at least 17 entries to have a unique solution
		MINIMUM_ENTRIES = 17
		MAXIMUM_EMPTY_CELLS = self.size*self.size - MINIMUM_ENTRIES
		numEmptyCells = self.numbers.count('0')
		
		if numEmptyCells > MAXIMUM_EMPTY_CELLS:
			return False
		return True
	
	def solve(self):
		"""
		Solve the puzzle!
		"""
		# First, attempt a solution by logical methods
		self.logic_solve()
		# When we can't get any further, start backtracking
		self.backtrack_solve(Board(self.numbers, self.size))
	
	def logic_solve(self):
		"""
		Solve the puzzle as far as possible by logic - see if there are any positions where only
		one number is possible. If a pass of the entire board is made without changing a number,
		then we can proceed no further with this method.
		"""
		N = self.size
		# A search is "successful" if a position is modified in one pass of the board
		successfulSearch = True	
		
		# Continue looping until a search is not successful
		while successfulSearch:
			successfulSearch = False
			
			# Loop through the entire board
			for i in range(N*N):
				# Don't look at nonempty positions
				if self.numbers[i] != "0":
					continue
				
				validNumbersList = list(self.getValidNumbers(i))
				
				# If there is only one valid number, insert it
				if len(validNumbersList) == 1:
					successfulSearch = True
					self.numbers = self.numbers[:i] + validNumbersList[0] + self.numbers[i+1:]
	
	def backtrack_solve(self, boardCopy):
		"""
		Solve the puzzle by backtracking - guessing a number from a list of available numbers and then
		continuing until a contradiction is reached (i.e. there is a position which has no valid numbers)
		or the puzzle is complete
		"""
		# Find the first unknown position on the board
		firstUnknown = boardCopy.numbers.find("0")
		# If there's no unknown position, the puzzle is solved!
		if firstUnknown == -1:
			self.numbers = boardCopy.numbers
			return
		
		validNumbers = boardCopy.getValidNumbers(firstUnknown)	
		for number in validNumbers:
			# Insert the number at the correct index
			boardCopy.numbers = boardCopy.numbers[:firstUnknown] + number + boardCopy.numbers[firstUnknown+1:]
			# Call recursively with a copy of the board (the previous operation
			# essentially copied the string of numbers)
			self.backtrack_solve(Board(boardCopy.numbers, self.size))
		
		
	def getValidNumbers(self, currentIndex):
		"""
		Gets the set of all valid numbers that can be placed at the given postion
		"""
		N = self.size
		n = N/3
		rowNumber = currentIndex / N
		columnNumber = currentIndex % N
		# This is the location of the upper left position in the current square
		squareIndex = (rowNumber / n)*N*n + (columnNumber / n)*N/n
		invalidNumbers = set()
		
		# Find all numbers that are not valid (the same number cannot be repeated
		# in the row, column, or square)
		for i in xrange(N):
			# Find all invalid numbers in the same row
			invalidNumbers.add(self.numbers[N*rowNumber + i])
			# Find all invalid numbers in the same column
			invalidNumbers.add(self.numbers[columnNumber + N*i])
			# Find all invalid numbers in the same square
			invalidNumbers.add(self.numbers[squareIndex + i%n + i/n*N])
		
		allNumbers = set(str(i) for i in xrange(N+1))
		validNumbers = allNumbers.difference(invalidNumbers)
		return validNumbers
	
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
		outputString = ""
		
		for i in range(N*N):
			# Add the current number to the string
			outputString += self.numbers[i]
			
			# Don't add any markers after the final number
			if i != N*N-1:
				# Add a line break at the end of the row
				if (i+1) % N == 0:
					outputString += "\n"
				# Add a separator at every third column
				elif (i+1) % n == 0:
					outputString += " | "
				# Add a space at every other number
				else:
					outputString += " "
			
				# Add a horizontal rule at every third row
				if (i+1) % (N*3) == 0:
					outputString += "---------------------\n"
		
		return outputString

if __name__ == "__main__":
	"""
	Main method - if this module is run, this method can be used for a
	command-line interface
	"""
	
	# Initialize the board from a string
	boardNumbers = raw_input("Enter numbers, as a single string (no spaces): ")
	board = Board(boardNumbers)
	
	# Print the board
	print "\nHere is the board:\n"
	print str(board)
	# Solve the puzzle and print the solution
	
	if board.isSolvable():
		board.solve()
		print "\nAnd here is the solution:\n"
		print str(board)
	else:
		print "\nSorry, no unique solution exists."