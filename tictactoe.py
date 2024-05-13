# This is a python program.
# By Giosuè Elia Dannenmann, Jan Rauber and Gian-Luca Thüler (& with some help from ChatGPT).
# Created in May, 2024.

# Here is a step-by-step guide on how to use this code for the "tic tac toe" game in python:
# 1. Download python
# 2. Copy and save the code
# 3. Open Terminal and execute the code with the command "python3 tictactoe.py"
# 4. Play the game, have fun and enjoy!


# Import modules
from tkinter import * # That way we can use all functions directely without tkinter.
import numpy as np

# Define the size of the game board
size_of_board = 600
# Calculate the size of each symbol (X or O) based on the size of the board
# symbol_size is calculated as half the distance between each grid line, minus an offset
# The offset is calculated to leave some space around the symbols
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
# Set the thickness of the symbol lines
symbol_thickness = 50
# Define color codes
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


# Create the TicTacToe class
class Tic_Tac_Toe():

    # Define magic method __init__
    def __init__(self):
        # Create a Tkinter window for the game
        self.window = Tk()
        # Set the title of the window
        self.window.title('Tic-Tac-Toe')
        # Create a canvas widget within the window to draw the game board
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        # Pack the canvas widget into the window
        self.canvas.pack()
        # Bind the left mouse button click event to the 'click' method
        self.window.bind('<Button-1>', self.click)

        # Initialize the game board
        self.initialize_board()
        # Set the flag to indicate it's player X's turn
        self.player_X_turns = True
        # Initialize the board status as a 3x3 numpy array filled with zeros
        self.board_status = np.zeros(shape=(3, 3))

        # Initialize variables to track game state
        self.player_X_starts = True  # Flag to indicate if player X starts the game
        self.reset_board = False  # Flag to indicate if the board needs to be reset for a new game
        self.gameover = False  # Flag to indicate if the game is over
        self.tie = False  # Flag to indicate if the game ended in a tie
        self.X_wins = False  # Flag to indicate if player X wins
        self.O_wins = False  # Flag to indicate if player O wins
        

    def mainloop(self):
        # Run the Tkinter main event loop to start the game
        self.window.mainloop()

    def initialize_board(self):
        # Function to initialize the game board by drawing grid lines on the canvas
        for i in range(2):
            # Draw vertical lines
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board)

        for i in range(2):
            # Draw horizontal lines 
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3)

    def play_again(self):
        # Function to reset the game board and start a new game
        # Initialize the board by redrawing grid lines
        self.initialize_board()
        # Toggle the starting player for the new game
        self.player_X_starts = not self.player_X_starts
        # Set the current player's turn to the starting player
        self.player_X_turns = self.player_X_starts
        # Reset the board status to all zeros (empty)
        self.board_status = np.zeros(shape=(3, 3))


    # Drawing functions

    def draw_O(self, logical_position):
        # Function to draw the 'O' symbol on the canvas at the specified logical position
        logical_position = np.array(logical_position)  # Convert logical position to numpy array
        # Calculate the actual pixel values of the center of the grid based on logical position
        grid_position = self.convert_logical_to_grid_position(logical_position)
        # Draw an oval (circle) representing the 'O' symbol centered at grid_position
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)  # Set outline color to symbol_O_color

    def draw_X(self, logical_position):
        # Function to draw the 'X' symbol on the canvas at the specified logical position
        # Calculate the actual pixel values of the center of the grid based on logical position
        grid_position = self.convert_logical_to_grid_position(logical_position)
        # Draw two lines intersecting each other to form the 'X' symbol centered at grid_position
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)  # Set fill color to symbol_X_color
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)  # Set fill color to symbol_X_color


    def display_gameover(self):
        # Function to display the game over message and update scores on the canvas

        # Determine the game outcome and update scores accordingly
        if self.X_wins:
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color  # Set color to symbol_X_color for Player 1
        elif self.O_wins:
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color  # Set color to symbol_O_color for Player 2
        else:
            text = 'Its a tie'
            color = 'gray'  # Set color to gray for a tie game

        # Clear the canvas and display the game outcome message at the center
        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        # Indicate that the board needs to be reset for a new game
        self.reset_board = True

        # Display a message prompting the user to click to play again
        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)


    # Logical Functions:
    # The modules required to carry out game logic

    def convert_logical_to_grid_position(self, logical_position):
        # Function to convert logical position to grid position on the canvas

        # Convert logical position to numpy array
        logical_position = np.array(logical_position, dtype=int)

        # Calculate grid position based on logical position
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        # Function to convert grid position on the canvas to logical position

        # Convert grid position to numpy array
        grid_position = np.array(grid_position)

        # Calculate logical position based on grid position
        return np.array(grid_position // (size_of_board / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        # Function to check if a grid position on the board is already occupied

        # Check if the grid position is occupied based on the board status
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False  # Grid position is not occupied
        else:
            return True  # Grid position is occupied


    def is_winner(self, player):
        # Function to check if a player has won the game

        # Convert player symbol to corresponding numeric value (-1 for 'X', 1 for 'O')
        player = -1 if player == 'X' else 1

        # Check for three in a row horizontally and vertically
        for i in range(3):
            # Three in a row horizontally
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            # Three in a row vertically
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True
            
        # Check for diagonals
        # Diagonal from top-left to bottom-right
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True
        # Diagonal from top-right to bottom-left
        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True
        
        # No winner found
        return False
        

    def is_tie(self):
        # Function to check if the game has ended in a tie
        
        # Find the positions where the board is empty (contains 0)
        r, c = np.where(self.board_status == 0)
        
        tie = False
        # If there are no empty positions, it's a tie
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Function to check if the game is over
        
        # Check if 'X' has won
        self.X_wins = self.is_winner('X')
        
        # If 'X' hasn't won, check if 'O' has won
        if not self.X_wins:
            self.O_wins = self.is_winner('O')
        
        # If neither 'X' nor 'O' has won, check for a tie
        if not self.O_wins:
            self.tie = self.is_tie()
        
        # Determine if the game is over based on whether 'X' has won, 'O' has won, or it's a tie
        gameover = self.X_wins or self.O_wins or self.tie

        # Print the outcome if 'X' or 'O' wins or if it's a tie
        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover


    def click(self, event):
        # Function to handle the click event when a player makes a move
        
        # Get the pixel coordinates of the clicked position
        grid_position = [event.x, event.y]
        
        # Convert the pixel coordinates to logical position (grid coordinates)
        logical_position = self.convert_grid_to_logical_position(grid_position)

        # Check if the board has been reset
        if not self.reset_board:
            # If it's X's turn and the clicked grid is not occupied
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    # Draw X symbol on the clicked grid
                    self.draw_X(logical_position)
                    
                    # Update the board status with X's move
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    
                    # Switch to O's turn
                    self.player_X_turns = not self.player_X_turns
            else:
                # If it's O's turn and the clicked grid is not occupied
                if not self.is_grid_occupied(logical_position):
                    # Draw O symbol on the clicked grid
                    self.draw_O(logical_position)
                    
                    # Update the board status with O's move
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    
                    # Switch to X's turn
                    self.player_X_turns = not self.player_X_turns

            # Check if the game is concluded after each move
            if self.is_gameover():
                # Display the gameover message
                self.display_gameover()
                # Reset the board for a new game
        else:  # Play Again
            # Clear the canvas to prepare for a new game
            self.canvas.delete("all")
            # Reset the board and game state
            self.play_again()
            self.reset_board = False


game_instance = Tic_Tac_Toe()  # Create an instance of the Tic_Tac_Toe class

# Call the mainloop method to start the Tkinter event loop, which handles user inputs and updates the GUI
game_instance.mainloop()
