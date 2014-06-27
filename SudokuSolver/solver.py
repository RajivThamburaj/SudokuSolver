"""
GUI for the Sudoku Solver

Author: Rajiv Thamburaj
"""

from Tkinter import *
import tkFont
import board

class SolverGUI(Frame):
	
	def __init__(self, parent):
		"""
		Initialize the instance
		"""
		Frame.__init__(self, parent, background="#222222")
		
		# Create and set the instance variables
		self.parent = parent
		self.boardString = "0"*81
		# Map each cell rectangle specifier to a text specifier
		self.textSpecifiers = {}
		# Map each text specifier to a cell index
		self.cellIndices = {}
		self.selectedCellSpecifier = None
		self.selectedTextSpecifier = None
		self.solved = False
		
		self.create_gui()
	
	def create_gui(self):
		"""
		Create and place the GUI elements
		"""
		self.parent.title("Sudoku Solver")
		self.pack(fill=BOTH, expand=1)
		
		# Create the canvas (the area where the board is displayed)
		boardCanvas = Canvas(self, bg="#333333", highlightthickness=0)
		self.canvas = boardCanvas
		boardCanvas.place(x=20, y=20, width=360, height=360)
		boardCanvas.bind("<Key>", self.key_pressed)
		boardCanvas.focus_set()
		
		# Update the window and find the canvas width
		root.update()
		canvasSize = boardCanvas.winfo_width()
		cellSize = canvasSize/9
		
		# Create the cells for the grid
		for i in xrange(9):
			for j in xrange(9):
				# Create the cell rectangle and add a callback for mouse click events
				cellSpecifier = boardCanvas.create_rectangle(cellSize*j, cellSize*i, cellSize*(j+1), cellSize*(i+1), fill="#333333", width=0)
				boardCanvas.tag_bind(cellSpecifier, "<Button>", self.cell_pressed)
				
				# Set the font and create the text field
				font = tkFont.Font(family='Arial', size=20)
				textSpecifier = boardCanvas.create_text(cellSize*(j+0.5), cellSize*(i+0.5), fill="#CCCCCC", font=font, state=DISABLED)
				
				# Map each cell rectangle specifier to its corresponding text specifier
				self.textSpecifiers[cellSpecifier] = textSpecifier
				# Map each text specifier to its cell's index
				self.cellIndices[textSpecifier] = i*9 + j
		
		# Keep track of which lines are bold (we need to move them to the front)
		boldLineSpecifiers = []
		
		# Create the grid lines
		for i in xrange(10):
			width = 1
			color = "#555555"
			
			# Every third line should be darker
			if i == 0 or i == 9:
				color = "#CCCCCC"
				width = 4
			elif i % 3 == 0:
				width = 2
				color = "#CCCCCC"
			
			# Draw the lines
			horizontalSpecifier = boardCanvas.create_line(cellSize*i, 0, cellSize*i, canvasSize, fill=color, width=width)
			verticalSpecifier = boardCanvas.create_line(0, cellSize*i, canvasSize, cellSize*i, fill=color, width=width)
			
			if i % 3 == 0:
				boldLineSpecifiers.append(horizontalSpecifier)
				boldLineSpecifiers.append(verticalSpecifier)
		
		# Move all the bold lines to the front
		for s in boldLineSpecifiers:
			boardCanvas.tag_raise(s)
		
		# Create the status bar message field
		statusBar = Message(self, text="Click a cell and type a number! You'll need at least 17.", width=360, background="#444444", foreground="#CCCCCC")
		self.statusBar = statusBar
		statusBar.place(x=20, y=400, width=360, height=30)
		# Create the solve button
		solveButton = Button(self, text="Solve", command=self.solve_button_pressed, highlightbackground="#222222")
		self.solveButton = solveButton
		solveButton.place(x=20, y=450, width=170, height=20)
		# Create the reset button
		resetButton = Button(self, text="Reset", command=self.reset_button_pressed, highlightbackground="#222222")
		resetButton.place(x=210, y=450, width=170, height=20)
	
	def cell_pressed(self, event):
		"""
		Callback for mouse click events on one of the grid cells
		"""
		# Don't allow cells to be clicked when the grid is solved
		if self.solved:
			return
		# Deselect the selected cell
		if self.selectedCellSpecifier is not None:
			self.canvas.itemconfig(self.selectedCellSpecifier, fill="#333333")
		
		# Select the new cell
		self.selectedCellSpecifier = self.canvas.find_withtag("current")[0]
		self.selectedTextSpecifier = self.textSpecifiers[self.selectedCellSpecifier]
		self.canvas.itemconfig(self.selectedCellSpecifier, fill="#3355CC")
	
	def key_pressed(self, event):
		"""
		Callback for keyboard events
		"""
		# Make sure that a cell has been selected
		if self.selectedTextSpecifier is not None:
			# Make sure that the key pressed is a number
			if event.char in "123456789" and event.char != "":
				self.canvas.itemconfig(self.selectedTextSpecifier, text=event.char)
				index = self.cellIndices[self.selectedTextSpecifier]
				# Update the model to reflect the changes
				self.boardString = self.boardString[:index] + event.char + self.boardString[index+1:]
			# Delete the text if the user pressed the backspace or delete keys
			elif event.char == "\x08" or event.char == "\x7f":
				self.canvas.itemconfig(self.selectedTextSpecifier, text="")
				index = self.cellIndices[self.selectedTextSpecifier]
				# Update the model to reflect the changes
				self.boardString = self.boardString[:index] + "0" + self.boardString[index+1:]
	
	def solve_button_pressed(self):
		"""
		Callback for mouse events on the solve button
		"""	
		# Create the model
		boardModel = board.Board(self.boardString, 9)
		# Make sure the puzzle can be solved
		if not(boardModel.is_solvable()):
			self.statusBar.config(text="No solution. Do you have 17+ consistent numbers?")
			return
		# Attempt a solution
		boardModel.try_solve()
		# Check for any inconsistencies
		if not(boardModel.was_solved()):
			self.statusBar.config(text="Oops, looks like your numbers are inconsistent.")
			return
		
		# Deselect the selected cell
		self.canvas.itemconfig(self.selectedCellSpecifier, fill="#333333")
		self.selectedCellSpecifier = None
		self.selectedTextSpecifier = None
		
		# Assign each character of the model's string to a text object on the canvas
		for key,value in self.cellIndices.items():
			self.canvas.itemconfig(key, text=boardModel.numbers[value])
		
		# Disable the solve button
		self.solveButton.config(state=DISABLED)
		self.solved = True
		
		# Update the status bar
		self.statusBar.config(text="Puzzle solved!")
	
	def reset_button_pressed(self):
		"""
		Callback for mouse events on the reset button
		"""
		# Deselect the selected cell
		self.canvas.itemconfig(self.selectedCellSpecifier, fill="#333333")
		self.selectedCellSpecifier = None
		self.selectedTextSpecifier = None
		
		# Erase all numbers from the board
		for key, value in self.cellIndices.items():
			self.canvas.itemconfig(key, text="")
		
		# Reset the solve button and the model
		self.solveButton.config(state=NORMAL)
		self.boardString = "0"*81
		self.solved = False
		
		# Update the status bar
		self.statusBar.config(text="Click a cell and type a number! You'll need at least 17.")

if __name__ == "__main__":
	"""
	Main method - instantiates the GUI
	"""
	root = Tk()
	root.geometry("400x490+500+200")
	# Prevent the window from being resized
	root.resizable(0,0)
	app = SolverGUI(root)
	root.mainloop()