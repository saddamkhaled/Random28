import csv
from datetime import datetime, timedelta
import os
import random
import time
import pandas as pd
import tkinter as tk
from tkinter import filedialog, scrolledtext
from colorama import Fore, Style, init
import threading

# Initialize Colorama
init(autoreset=True)

# Banner for Random28
banner = f"""
{Fore.CYAN + Style.BRIGHT}
 _______  _______  _        ______   _______  _______    _______   _____  
(  ____ )(  ___  )( (    /|(  __  \ (  ___  )(       )  / ___   ) / ___ \ 
| (    )|| (   ) ||  \  ( || (  \  )| (   ) || () () |  \/   )  |( (___) )
| (____)|| (___) ||   \ | || |   ) || |   | || || || |      /   ) \     / 
|     __)|  ___  || (\ \) || |   | || |   | || |(_)| |    _/   /  / ___ \ 
| (\ (   | (   ) || | \   || |   ) || |   | || |   | |   /   _/  ( (   ) )
| ) \ \__| )   ( || )  \  || (__/  )| (___) || )   ( |  (   (__/\( (___) )
|/   \__/|/     \||/    )_)(______/ (_______)|/     \|  \_______/ \_____/ 
          
                     ~Author: Ben Khaled Saddam~                                                                 
"""

def draw_numbers(num_blue, num_yellow, num_range):
    """Draws a specified number of unique random numbers from a given range."""
    blue_numbers = sorted(random.sample(range(1, num_range + 1), num_blue))
    remaining_numbers = list(set(range(1, num_range + 1)) - set(blue_numbers))
    yellow_numbers = sorted(random.sample(remaining_numbers, num_yellow))
    return blue_numbers, yellow_numbers

def predict_next_numbers(blue_frequency, yellow_frequency, num_blue=7, num_yellow=5):
    """Predict the next set of blue and yellow numbers based on frequency data."""
    try:
        # Select the most common blue and yellow numbers
        blue_predictions = sorted(blue_frequency.nlargest(num_blue).index.tolist())
        yellow_predictions = sorted(yellow_frequency.nlargest(num_yellow).index.tolist())

        print(f"Predicted next blue numbers: {blue_predictions}")
        print(f"Predicted next yellow numbers: {yellow_predictions}")

        return blue_predictions, yellow_predictions
    except Exception as e:
        print(f"Error predicting numbers: {e}")
        return [], []


class Random28Game:
    def __init__(self):
        print(Fore.YELLOW + banner)  # Print banner
        self.num_range = 28
        self.num_blue = 7
        self.num_yellow = 5
        self.history = []  # To store game history for frequency analysis
        self.bet_per_draw = 0  # Initialize bet_per_draw here
        self.num_draws = 1  # Initialize num_draws here
        self.total_bet = 0  # Initialize total_bet here
        self.draws_results = []  # To store results of multiple draws
        self.total_gain = 0  # Initialize total_gain here1
        self.total_loss = 0  # Initialize total_loss here




    def start(self):
        """Main method to start the game or predict from CSV."""
        while True:
            print(Fore.GREEN + "Welcome to Random28!")
            print("1: Play the game")
            print("2: Predict numbers from a CSV file")
            print("3: Show total gain and loss")  # New option
            choice = input("Enter your choice (1, 2, or 3: ").strip()
            
            if choice == '1':
                self.play_game()
            elif choice == '2':
                self.show_prediction_window()
            elif choice == '3':
                self.show_total_gain_loss()  

            else:
                print(Fore.RED + "Invalid choice. Please try again.")
            if not self.ask_replay():
                print("Thank you for playing! Goodbye.")
                break

    def ask_replay(self):
        """Ask the user if they want to play or predict again."""
        while True:
            replay_choice = input(Fore.YELLOW + "Do you want to play or predict again? (y/n): ").strip().lower()
            if replay_choice == 'y':
                return True
            elif replay_choice == 'n':
                return False
            else:
                print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.")
    def show_total_gain_loss(self):
        """Display the total gain and total loss."""
        print(Fore.GREEN + f"Total Gain: {self.total_gain} €")
        print(Fore.RED + f"Total Loss: {self.total_loss} €")
            # Calculate profit or loss
        profit_or_loss = self.total_gain - self.total_loss
        if profit_or_loss > 0:
            print(Fore.BLUE + f"Profit: {profit_or_loss} €")
        elif profit_or_loss < 0:
            print(Fore.YELLOW + f"Loss: {abs(profit_or_loss)} €")
        else:
            print(Fore.MAGENTA + "No Profit, No Loss.")

    def play_game(self):
        """Handle the gameplay functionality."""
        self.input_bet()  # Ask the user for the bet
        self.input_numbers()
        self.generate_draws()
        self.check_win()
    def input_bet(self):
        """Prompt the user to input their bet per draw and number of draws."""
        while True:
            try:
                # Prompt user for bet per draw
                self.bet_per_draw = int(input(f"{Fore.GREEN}Choose your bet per draw (2, 4, 6, or 8 €): ").strip())
                if self.bet_per_draw not in [2, 4, 6, 8]:
                    raise ValueError("Bet must be 2, 4, 6, or 8 €.")
                
                # Prompt user for number of draws
                self.num_draws = int(input(f"{Fore.GREEN}How many draws would you like to play (1 to 10): ").strip())
                if self.num_draws < 1 or self.num_draws > 10:
                    raise ValueError("You must choose between 1 and 10 draws.")
                
                # Calculate the total bet for all draws
                self.total_bet = self.bet_per_draw * self.num_draws
                print(Fore.CYAN + f"Your total bet is: {self.total_bet} € ({self.bet_per_draw} € per draw for {self.num_draws} draws).")
                break
            except ValueError as e:
                print(Fore.RED + str(e))
                continue

    def input_numbers(self):
        """Prompt the user to input their numbers."""
        while True:
            try:
                self.user_numbers = [int(x) for x in input(f"{Fore.GREEN}Enter your 7 numbers (1-{self.num_range}) separated by space: ").split()]
                if len(self.user_numbers) != 7:
                    raise ValueError("You must enter exactly 7 numbers.")
                if any(num < 1 or num > self.num_range for num in self.user_numbers):
                    raise ValueError(f"Numbers must be between 1 and {self.num_range}.")
                print(Fore.CYAN + f"Your chosen numbers: {sorted(self.user_numbers)}")
                break
            except ValueError as e:
                print(Fore.RED + str(e))
                continue

    import csv

    def generate_draws(self):
        """Generate and display random draw numbers for multiple draws."""
        self.draws_results = []
        print(Fore.YELLOW + "Generating draw numbers, please wait...")
        time.sleep(2)

        for _ in range(self.num_draws):
            draw_main, draw_bonus = draw_numbers(self.num_blue, self.num_yellow, self.num_range)
            self.draws_results.append((draw_main, draw_bonus))
            print(Fore.BLUE + f"Drawn Blue Numbers: {draw_main}")
            print(Fore.YELLOW + f"Drawn Yellow Numbers: {draw_bonus}")
        
        # Add the drawn numbers to history
        self.history.extend({
            'blue': draw_main,
            'yellow': draw_bonus
        } for draw_main, draw_bonus in self.draws_results)
        
        # Save the current history to a CSV file
        self.save_draw_history_to_csv()



    def save_draw_history_to_csv(self):
        """Save the draw history to a CSV file with the specified format."""
        try:
            # Get the current directory path and specify a file path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "draw_history.csv")
            
            # Set headers according to the requested format
            headers = [
                'N_du_tirage', 'Date', 'Heure', 'Date_de_forclusion', 
                'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7',
                'NJAUNES 1', 'NJAUNES 2', 'NJAUNES 3', 'NJAUNES 4', 'NJAUNES 5'
            ]

            # Open CSV file for writing
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  # Write the headers

                # Write each draw's history
                for i, draw in enumerate(self.history, 1):
                    # Extract blue and yellow numbers
                    blue_numbers = draw['blue']
                    yellow_numbers = draw['yellow']

                    # Get the current date and time for the draw
                    current_datetime = datetime.now()
                    date_str = current_datetime.strftime("%Y-%m-%d")  # Format as 'YYYY-MM-DD'
                    time_str = current_datetime.strftime("%H:%M:%S")  # Format as 'HH:MM:SS'
                    
                    # Set a future date for Date_de_forclusion (e.g., 1 day after draw)
                    date_de_forclusion = (current_datetime + timedelta(days=1)).strftime("%Y-%m-%d")

                    # Write the row with the required format
                    writer.writerow([
                        i,  # N_du_tirage (draw number)
                        date_str,  # Date of the draw
                        time_str,  # Time of the draw
                        date_de_forclusion,  # Date_de_forclusion
                        *blue_numbers,  # N1 to N7 (blue numbers)
                        *yellow_numbers  # NJAUNES 1 to NJAUNES 5 (yellow numbers)
                    ])

            print(Fore.CYAN + f"Draw history saved to {file_path}")
        
        except Exception as e:
            print(Fore.RED + f"Error saving draw history to CSV: {str(e)}")



    def check_win(self):
        """Check if the user's numbers match the drawn numbers for each draw."""
        print(Fore.YELLOW + "Calculating your results, please wait...")
        time.sleep(2)

        for index, (draw_main, draw_bonus) in enumerate(self.draws_results, start=1):
            main_matches = len([num for num in self.user_numbers if num in draw_main])
            bonus_matches = len([num for num in self.user_numbers if num in draw_bonus])
            print(Fore.GREEN + f"\nDraw {index}:")
            print(Fore.BLUE + f"Drawn Blue Numbers: {draw_main}")
            print(Fore.YELLOW + f"Drawn Yellow Numbers: {draw_bonus}")
            print(Fore.CYAN + f"Your Numbers: {self.user_numbers}")
            print(Fore.GREEN + f"Main number matches: {main_matches}")
            print(Fore.YELLOW + f"Bonus number matches: {bonus_matches}")
        
            winnings = self.calculate_winnings(main_matches, bonus_matches)
            if winnings > 0:
                print(Fore.GREEN + f"Congratulations! You win {winnings} €!")
            else:
                print(Fore.RED + "Sorry, you lose. :("  )



            

    def calculate_winnings(self, main_matches, bonus_matches):
        """Calculate winnings based on the number of main and bonus matches."""
        
        amigo_prizes = {
            (7, 0): {2: 25000, 4: 50000, 6: 75000, 8: 100000},
            (6, 1): {2: 500, 4: 1000, 6: 1500, 8: 2000},
            (5, 2): {2: 120, 4: 240, 6: 360, 8: 480},
            (4, 3): {2: 100, 4: 200, 6: 300, 8: 400},
            (3, 4): {2: 100, 4: 200, 6: 300, 8: 400},
            (2, 5): {2: 100, 4: 200, 6: 300, 8: 400},
            (6, 0): {2: 250, 4: 500, 6: 750, 8: 1000},
            (5, 1): {2: 55, 4: 110, 6: 165, 8: 220},
            (4, 2): {2: 20, 4: 40, 6: 60, 8: 80},
            (3, 3): {2: 15, 4: 30, 6: 45, 8: 60},
            (2, 4): {2: 15, 4: 30, 6: 45, 8: 60},
            (1, 5): {2: 15, 4: 30, 6: 45, 8: 60},
            (5, 0): {2: 50, 4: 100, 6: 150, 8: 200},
            (4, 1): {2: 8, 4: 16, 6: 24, 8: 32},
            (3, 2): {2: 3, 4: 6, 6: 9, 8: 12},
            (2, 3): {2: 3, 4: 6, 6: 9, 8: 12},
            (1, 4): {2: 3, 4: 6, 6: 9, 8: 12},
            (0, 5): {2: 3, 4: 6, 6: 9, 8: 12},
            (4, 0): {2: 5, 4: 10, 6: 15, 8: 20},
            (3, 1): {2: 2, 4: 4, 6: 6, 8: 8},
            (2, 2): {2: 2, 4: 4, 6: 6, 8: 8},
            (1, 3): {2: 2, 4: 4, 6: 6, 8: 8},
            (0, 4): {2: 2, 4: 4, 6: 6, 8: 8},
            # (main_matches, bonus_matches): {bet_amount: prize_amount, ...}
            (7, 0): {2: 25000, 4: 50000, 6: 75000, 8: 100000},
            (6, 1): {2: 500, 4: 1000, 6: 1500, 8: 2000},
            (5, 2): {2: 120, 4: 240, 6: 360, 8: 480},
        }
        winnings_info = amigo_prizes.get((main_matches, bonus_matches))
    
       
        # Check if winnings_info exists; if not, return 0 (no prize)
        if winnings_info is None:
            winnings = 0
        else:
            winnings = winnings_info.get(self.bet_per_draw, 0)

        # Update total gain and loss
        if winnings > 0:
            self.total_gain += winnings
        else:
            self.total_loss += self.bet_per_draw

        return winnings

    def analyze_frequencies(self):
        """Analyze the frequency of blue and yellow numbers in the history."""
        try:
            # Extract blue and yellow numbers from the history
            blue_numbers = [num for draw in self.history for num in draw['blue']]
            yellow_numbers = [num for draw in self.history for num in draw['yellow']]
            
            # Calculate frequency counts for blue and yellow numbers
            blue_frequency = pd.Series(blue_numbers).value_counts().sort_index()
            yellow_frequency = pd.Series(yellow_numbers).value_counts().sort_index()

            # Display frequency results for analysis
            print(f"Blue number frequencies:\n{blue_frequency}")
            print(f"Yellow number frequencies:\n{yellow_frequency}")

            return blue_frequency, yellow_frequency
        except Exception as e:
            print(f"Error analyzing frequencies: {e}")
            return pd.Series(), pd.Series()


    def predict_from_csv(self, file_path):
        """Predict the next sets of blue and yellow numbers based on CSV data."""
        try:
            df = pd.read_csv(file_path)
            
            # Extract number columns
            blue_columns = [f'N{i}' for i in range(1, 8)]
            yellow_columns = [f'NJAUNES {i}' for i in range(1, 6)]
            
            # Check if all expected columns are present
            missing_columns = [col for col in blue_columns + yellow_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing columns in the CSV file: {missing_columns}")
            
            # Extract blue and yellow numbers from the CSV
            all_blue_numbers = df[blue_columns].values.flatten()
            all_yellow_numbers = df[yellow_columns].values.flatten()
            
            # Remove duplicates and convert to sorted lists
            unique_blue_numbers = sorted(set(all_blue_numbers))
            unique_yellow_numbers = sorted(set(all_yellow_numbers))
            
            if len(unique_blue_numbers) < 7 or len(unique_yellow_numbers) < 5:
                raise ValueError("Not enough unique numbers in CSV data to generate predictions.")
            
            # Strategy: Select 4 unique combinations of blue and yellow numbers from the data
            predictions = []
            for _ in range(4):  # Predict 4 sets based on strategy
                # Generate blue numbers from the pool of unique blue numbers
                blue_pred = sorted(random.sample(unique_blue_numbers, 7))
                remaining_numbers = list(set(range(1, 29)) - set(blue_pred))
                
                # Ensure yellow numbers are different from blue numbers
                yellow_pred = sorted(random.sample(sorted(set(remaining_numbers).union(unique_yellow_numbers)), 5))
                
                # Convert numpy int64 to regular int
                blue_pred = [int(num) for num in blue_pred]
                yellow_pred = [int(num) for num in yellow_pred]
                
                predictions.append((blue_pred, yellow_pred))

            return predictions
        except Exception as e:
            return [f"Error: {str(e)}"]

    def show_prediction_window(self):
        """Create a tkinter window to show prediction options and results."""
        window = tk.Tk()
        window.title("Prediction Window")
        window.geometry("1024x1024")
        window.configure(bg="black")

        def generate_predictions():
            """Generate predictions based on game history."""
            def worker():
                blue_frequency, yellow_frequency = self.analyze_frequencies()  # Get both frequencies
                predictions = predict_next_numbers(blue_frequency, yellow_frequency)  # Pass both to the prediction function
                code_box.delete(1.0, tk.END)
                if predictions:
                    code_box.insert(tk.END, f"Predicted next 7 blue numbers: {predictions[0]}\n")
                    code_box.insert(tk.END, f"Predicted next 5 yellow numbers: {predictions[1]}\n")
                else:
                    code_box.insert(tk.END, "No predictions available.\n")
            
            # Run in a separate thread to avoid blocking UI
            threading.Thread(target=worker).start()


        def upload_csv():
            """Upload CSV file and generate predictions from it."""
            def worker():
                file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
                if file_path:
                    try:
                        predictions = self.predict_from_csv(file_path)
                        code_box.delete(1.0, tk.END)
                        if isinstance(predictions, list) and all(isinstance(pred, tuple) and len(pred) == 2 for pred in predictions):
                            code_box.insert(tk.END, "Predictions based on CSV data:\n")
                            for i, (blue, yellow) in enumerate(predictions, start=1):
                                code_box.insert(tk.END, f"Prediction {i}: Blue: {blue}, Yellow: {yellow}\n")
                        else:
                            code_box.insert(tk.END, f"Error: {predictions[0]}\n")
                    except Exception as e:
                        code_box.insert(tk.END, f"Error: {str(e)}\n")
            
            # Run in separate thread to avoid blocking UI
            threading.Thread(target=worker).start()
  


  

        # Label
        label = tk.Label(window, text="Click the button to upload CSV and generate predictions:", bg="black", fg="green", font=("Consolas", 14))
        label.pack(pady=10)

        # Upload Button
        upload_button = tk.Button(window, text="Upload CSV File", command=upload_csv, bg="green", fg="black", font=("Consolas", 12))
        upload_button.pack(pady=10)

        # Button to generate predictions based on game history
        generate_button = tk.Button(window, text="Generate Predictions", command=generate_predictions, bg="green", fg="black", font=("Consolas", 12))
        generate_button.pack(pady=10)

        # Text box for displaying the predictions
        code_box = scrolledtext.ScrolledText(window, height=30, width=100, bg="black", fg="green", insertbackground="green", font=("Consolas", 12))
        code_box.pack(pady=10)

        window.mainloop()

if __name__ == "__main__":
    game = Random28Game()
    game.start()
