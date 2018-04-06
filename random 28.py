import random
import time


print("""
 _______  _______  _        ______   _______  _______    _______   _____  
(  ____ )(  ___  )( (    /|(  __  \ (  ___  )(       )  / ___   ) / ___ \ 
| (    )|| (   ) ||  \  ( || (  \  )| (   ) || () () |  \/   )  |( (___) )
| (____)|| (___) ||   \ | || |   ) || |   | || || || |      /   ) \     / 
|     __)|  ___  || (\ \) || |   | || |   | || |(_)| |    _/   /  / ___ \ 
| (\ (   | (   ) || | \   || |   ) || |   | || |   | |   /   _/  ( (   ) )
| ) \ \__| )   ( || )  \  || (__/  )| (___) || )   ( |  (   (__/\( (___) )
|/   \__/|/     \||/    )_)(______/ (_______)|/     \|  \_______/ \_____/ 
          
                     ~Author:Ben Khaled Saddam~                                                                 
""")
print("~" * 80)
print( "       RANDOM 28:\n*you have to choose 7 numbers from 1 to 28. \n*you have 5 bonus numbers."
          "\n*once you get 4 correct numbers you win!")
print("~"*80)

num = list(range(1,29))
print(num)
a = random.sample(range(1, 29), 7)
b = random.sample(range(1, 29), 5)

class game:
    def inputNumber(self):
        while True:
            try:
                self.numbers = [int(x) for x in input("Enter your list of 7 numbers separated by space please :").split()]
                print("Your chosen numbers : ", self.numbers)
            except ValueError:
                print("Not an integer! Try again.")
                continue
            else:
                return input
                break
    def generation(self):

            print("Generating playing list,please wait...")
            time.sleep(5)
            print(a)
            print("Generating Bonus list,please wait...")
            time.sleep(5)
            print(b)
    def winLoose(self):

            print("Your result is loading...")
            time.sleep(2)
            numFinal = list()
            isWin = False
            for number in self.numbers:
                if number in a or number in b:
                    numFinal.insert(numFinal.__len__(), number)
                    print(number, "Correct !")
                if (numFinal.__len__() == 4):
                    isWin = True
            if isWin:
                print('You win ! :)')
            else:
                print('Sorry, you loose :(')
                print("your final list :", numFinal)
def main():
     yourgame=game()
     yourgame.inputNumber()
     yourgame.generation()
     yourgame.winLoose()



if __name__ == '__main__':main()
