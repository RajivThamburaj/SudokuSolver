"""
GUI for the Sudoku Solver

Author: Rajiv Thamburaj
"""

from Tkinter import *
import tkFont
import board

class SolverGUI(Frame):
	"""
	GUI for the Sudoku Solver
	"""
	
	def __init__(self, parent):
		"""
		Initialize the instance
		"""
		Frame.__init__(self, parent, background="#222222")
		
		# Create and set the instance variables
		self.parent = parent
		self.board_string = "0"*81
		# Map each cell rectangle specifier to a text specifier
		self.text_specifiers = {}
		# Map each text specifier to a cell index
		self.cell_indices = {}
		self.selected_cell_specifier = None
		self.selected_text_specifier = None
		self.solved = False
		
		self.create_gui()
	
	def create_gui(self):
		"""
		Create and place the GUI elements
		"""
		self.parent.title("Sudoku Solver")
		self.pack(fill=BOTH, expand=1)
		
		# Create the canvas (the area where the board is displayed)
		board_canvas = Canvas(self, bg="#333333", highlightthickness=0)
		self.canvas = board_canvas
		board_canvas.place(x=20, y=20, width=360, height=360)
		board_canvas.bind("<Key>", self.key_pressed)
		board_canvas.focus_set()
		
		# Update the window and find the canvas width
		root.update()
		canvas_size = board_canvas.winfo_width()
		cell_size = canvas_size/9
		
		# Create the cells for the grid
		for i in xrange(9):
			for j in xrange(9):
				# Create the cell rectangle and add a callback for mouse
				# click events
				cell_specifier = board_canvas.create_rectangle(
					cell_size*j, cell_size*i, cell_size*(j+1), cell_size*(i+1),
					fill="#333333", width=0)
				board_canvas.tag_bind(cell_specifier, "<Button>",
									  self.cell_pressed)
				
				# Set the font and create the text field
				font = tkFont.Font(family='Arial', size=20)
				textSpecifier = board_canvas.create_text(
					cell_size*(j+0.5), cell_size*(i+0.5), fill="#CCCCCC",
					font=font, state=DISABLED)
				
				# Map each cell rectangle specifier to its corresponding
				# text specifier
				self.text_specifiers[cell_specifier] = textSpecifier
				# Map each text specifier to its cell's index
				self.cell_indices[textSpecifier] = i*9 + j
		
		# Keep track of which lines are bold (we need to move them to
		# the front)
		bold_line_specifiers = []
		
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
			horizontal_specifier = board_canvas.create_line(
				cell_size*i, 0, cell_size*i, canvas_size, fill=color,
				width=width)
			vertical_specifier = board_canvas.create_line(
				0, cell_size*i, canvas_size, cell_size*i, fill=color,
				width=width)
			
			if i % 3 == 0:
				bold_line_specifiers.append(horizontal_specifier)
				bold_line_specifiers.append(vertical_specifier)
		
		# Move all the bold lines to the front
		for s in bold_line_specifiers:
			board_canvas.tag_raise(s)
		
		# Create the status bar message field
		status_bar = Message(
			self,
			text="Click a cell and type a number! You'll need at least 17.",
			width=360, background="#444444", foreground="#CCCCCC")
		self.status_bar = status_bar
		status_bar.place(x=20, y=400, width=360, height=30)
		# Create the solve button
		solve_button = Button(
			self, text="Solve", command=self.solve_button_pressed,
			highlightbackground="#222222")
		self.solve_button = solve_button
		solve_button.place(x=20, y=450, width=170, height=20)
		# Create the reset button
		reset_button = Button(
			self, text="Reset", command=self.reset_button_pressed,
			highlightbackground="#222222")
		reset_button.place(x=210, y=450, width=170, height=20)
	
	def cell_pressed(self, event):
		"""
		Callback for mouse click events on one of the grid cells
		"""
		# Don't allow cells to be clicked when the grid is solved
		if self.solved:
			return
		# Deselect the selected cell
		if self.selected_cell_specifier is not None:
			self.canvas.itemconfig(self.selected_cell_specifier,
								    fill="#333333")
		
		# Select the new cell
		self.selected_cell_specifier = self.canvas.find_withtag("current")[0]
		self.selected_text_specifier = \
			self.text_specifiers[self.selected_cell_specifier]
		self.canvas.itemconfig(self.selected_cell_specifier, fill="#3355CC")
	
	def key_pressed(self, event):
		"""
		Callback for keyboard events
		"""
		# Make sure that a cell has been selected
		if self.selected_text_specifier is not None:
			# Make sure that the key pressed is a number
			if event.char in "123456789" and event.char != "":
				self.canvas.itemconfig(self.selected_text_specifier,
										text=event.char)
				index = self.cell_indices[self.selected_text_specifier]
				# Update the model to reflect the changes
				self.board_string = self.board_string[:index] + event.char + \
				                    self.board_string[index+1:]
			# Delete the text if the user pressed the backspace or delete keys
			elif event.char == "\x08" or event.char == "\x7f":
				self.canvas.itemconfig(self.selected_text_specifier, text="")
				index = self.cell_indices[self.selected_text_specifier]
				# Update the model to reflect the changes
				self.board_string = self.board_string[:index] + "0" + \
				                    self.board_string[index+1:]
	
	def solve_button_pressed(self):
		"""
		Callback for mouse events on the solve button
		"""	
		# Create the model
		board_model = board.Board(self.board_string, 9)
		# Make sure the puzzle can be solved
		if not(board_model.is_solvable()):
			self.status_bar.config(
				text="No solution. Do you have 17+ consistent numbers?")
			return
		# Attempt a solution
		board_model.try_solve()
		# Check for any inconsistencies
		if not(board_model.was_solved()):
			self.status_bar.config(
				text="Oops, looks like your numbers are inconsistent.")
			return
		
		# Deselect the selected cell
		self.canvas.itemconfig(self.selected_cell_specifier, fill="#333333")
		self.selected_cell_specifier = None
		self.selected_text_specifier = None
		
		# Assign each character of the model's string to a text object
		# on the canvas
		for key,value in self.cell_indices.items():
			self.canvas.itemconfig(key, text=board_model.numbers[value])
		
		# Disable the solve button
		self.solve_button.config(state=DISABLED)
		self.solved = True
		
		# Update the status bar
		self.status_bar.config(text="Puzzle solved!")
	
	def reset_button_pressed(self):
		"""
		Callback for mouse events on the reset button
		"""
		# Deselect the selected cell
		self.canvas.itemconfig(self.selected_cell_specifier, fill="#333333")
		self.selected_cell_specifier = None
		self.selected_text_specifier = None
		
		# Erase all numbers from the board
		for key, value in self.cell_indices.items():
			self.canvas.itemconfig(key, text="")
		
		# Reset the solve button and the model
		self.solve_button.config(state=NORMAL)
		self.board_string = "0"*81
		self.solved = False
		
		# Update the status bar
		self.status_bar.config(
			text="Click a cell and type a number! You'll need at least 17.")

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