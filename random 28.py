import random
import time
from colorama import Fore, Style, init

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
    yellow_numbers = sorted(random.sample(range(1, num_range + 1), num_yellow))
    return blue_numbers, yellow_numbers

class Random28Game:
    def __init__(self):
        print(Fore.YELLOW + banner)  # Print banner
        self.num_range = 28
        self.num_blue = 7
        self.num_yellow = 5
        self.draw_main, self.draw_bonus = draw_numbers(self.num_blue, self.num_yellow, self.num_range)
    
    def input_numbers(self):
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

    def generate_draws(self):
        print(Fore.YELLOW + "Generating draw numbers, please wait...")
        time.sleep(2)
        print(Fore.BLUE + f"Drawn Blue Numbers: {self.draw_main}")
        print(Fore.YELLOW + f"Drawn Yellow Numbers: {self.draw_bonus}")
    
    def check_win(self):
        print(Fore.YELLOW + "Calculating your result, please wait...")
        time.sleep(2)
        
        main_matches = [num for num in self.user_numbers if num in self.draw_main]
        bonus_matches = [num for num in self.user_numbers if num in self.draw_bonus]
        
        total_matches = len(main_matches) + len(bonus_matches)
        is_win = len(main_matches) >= 4
        
        print(Fore.CYAN + f"Main Draw Matches: {sorted(main_matches)}")
        print(Fore.CYAN + f"Bonus Matches: {sorted(bonus_matches)}")
        print(Fore.CYAN + f"Total Matches: {total_matches}")

        if is_win:
            print(Fore.GREEN + "Congratulations! You win! :)")
        else:
            print(Fore.RED + "Sorry, you lose. :(")
        print(Fore.CYAN + f"Your final matched numbers: {sorted(main_matches + bonus_matches)}")

def main():
    game = Random28Game()
    game.input_numbers()
    game.generate_draws()
    game.check_win()

if __name__ == '__main__':
    main()
