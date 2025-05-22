#A game where the user guesses a randomly generated number
#If file not found, it will create a new file
#The data is file is displayed in a sorted manner as per highest score
#Execution view can be seen automated in Help menu
import sys
import os
import random
import time 
import datetime
from operator import itemgetter

#File Handling
def load_file():
    print(f"FILE REFERENCE:")
    TASK_FILE = "NumGuessLB.txt"
    print(f"Looking for file at: {TASK_FILE}")
    print()
    if not os.path.exists(TASK_FILE):
        print("File does not exist : Creating a new file") 
        with open(TASK_FILE, "w") as f:
            pass   
        return []         
    with open(TASK_FILE, "r") as f:
        print("File does exist.")
        lines = f.readlines()
        records = [line.strip().split("-") for line in lines if line.strip()]
        # Sort by the 3rd field (score), descending, and convert to int for numeric sort
        try:
            records.sort(key=lambda x: int(x[1]), reverse=True)
        except ValueError:
            records.sort(key=itemgetter(2), reverse=True)
        print("Leaderboard Scores:")
        for record in records:
            print(" - ".join(record))
        return records  
    
def save_file(tasks):
    TASK_FILE = "NumGuessLB.txt"
    if not os.path.exists(TASK_FILE):
         print("File does not exist") 
         return []       
    with open(TASK_FILE, "w") as f:
        for player_name, player_score, play_time in tasks:
            f.write(f"{player_name}-{player_score}-{play_time}\n")

#Task Handling
def add_score(player_name, player_score, play_time):
    tasks = load_file()
    TASK_FILE = "NumGuessLB.txt"
    if not os.path.exists(TASK_FILE): 
        return []
    tasks.append([player_name, player_score, play_time])
    save_file(tasks)
    print(f"Score Added: {player_name} - {player_score} - {play_time}")

#Main Menu
def NumGuessMain():
    NumGuessWelcome() 
    first_input = NumGuessFirstInput()
    NumGuessFirstInputMenu(first_input)   

def NumGuessWelcome(): #1
    print()
    print("Welcome to the Random Number Guessing Game Application !")
    print("**The application will generate a random number based on the difficulty level you choose**" 
          "\n**You have to guess the right number within range of certain attempts [based on difficulty level you choose]**" 
          "\n**After certain attmpts you shall be given some clue**" 
          "\n**On successful finding, your score will be added to the leader board**")    
    print()
    print("Type 'Play' to Start the Game."
          "\nOr 'Help' to see how the Game works.")
    print()  

def NumGuessFirstInput(): #2
    first_input = input("Enter your choice (Play/Help/Exit) - [Not Case Sensitive] : ").strip().lower()  
    return(first_input)   

def NumGuessFirstInputMenu(first_input): #3
    if first_input == "play":
        NumGuessMainMenu()
    elif first_input == "help":
        NumGuessHelpMenu() 
        first_input = NumGuessFirstInput()
        NumGuessFirstInputMenu(first_input)
    elif first_input == "exit":
        NumGuessExitMenu()         
    else:
        print()
        print("Invalid input. Please try again.")
        print()
        first_input = NumGuessFirstInput()
        NumGuessFirstInputMenu(first_input)

def NumGuessMainMenu(): #3a
    print()
    print("The Number Guessing Game starts")
    print("Choose the Difficulty Level:")
    print("1. Easy (Range: 1-50, 20 attempts)")
    print("2. Medium (Range: 1-100, 10 attempts)")        
    print("3. Hard (Range: 1-1000, 5 attempts)")
    print("4. Exit")
    print()
    difficuty_choice = NumGuessOperInput()
    NumGuessMainOper(difficuty_choice) 
   
def NumGuessHelpMenu(): #3b
    print()
    print("Help Section:")
    NumGuessAutomatedHelp()
    print()

def NumGuessExitMenu(): #3c
    print()
    print("Thank you for visiting the Number Guess Game Application!")
    print("Goodbye!")   
    sys.exit()  
    
def NumGuessOperInput(): #3a1
    difficuty_choice = input("Enter your choice: ") 
    return(difficuty_choice) 

def NumGuessMainOper(difficuty_choice): #3a2
    if difficuty_choice == "1":
        print("You have selected Easy mode (Range: 1-50, 20 attempts)")
        min_val, max_val, max_attempt  = 1, 50, 20
        random_number = NumGuessRandomGen(min_val, max_val, max_attempt)
        validate_input = input("Enter your guess [attempt 1]: ")
        if validate_input.isdigit():
            user_guess = int(validate_input)
            NumGuessUserGuess(difficuty_choice, user_guess, random_number, max_attempt)
            NumGuessAgainAttempt()
        else:
            print("Invalid input! Please enter a valid number.")
            NumGuessMainMenu()
    elif difficuty_choice == "2":
        print("You have selected Medium mode (Range: 1-100, 10 attempts)")
        min_val, max_val, max_attempt  = 1, 100, 10
        random_number = NumGuessRandomGen(min_val, max_val, max_attempt)
        validate_input = input("Enter your guess [attempt 1]: ")
        if validate_input.isdigit():
            user_guess = int(validate_input)
            NumGuessUserGuess(difficuty_choice, user_guess, random_number, max_attempt)
            NumGuessAgainAttempt()
        else:
            print("Invalid input! Please enter a valid number.")
            NumGuessMainMenu()         
    elif difficuty_choice == "3":
        print("You have selected Hard mode (Range: 1-1000, 5 attempts)")
        min_val, max_val, max_attempt  = 1, 1000, 5
        random_number = NumGuessRandomGen(min_val, max_val, max_attempt)
        validate_input = input("Enter your guess [attempt 1]: ")
        if validate_input.isdigit():
            user_guess = int(validate_input)
            NumGuessUserGuess(difficuty_choice, user_guess, random_number, max_attempt)
            NumGuessAgainAttempt()
        else:
            print("Invalid input! Please enter a valid number.")
            NumGuessMainMenu()
    elif difficuty_choice == "4":
        NumGuessExitMenu()
    else:
        print()
        print("Invalid input. Please try again.")
        NumGuessMainMenu()

def NumGuessRandomGen(min_val, max_val, max_attempt): #3b1
        random_number = random.randint(min_val, max_val)        
#       print(f"Random number generated is: {random_number}")
        print(f"Guess the number between {min_val} and {max_val} within {max_attempt} attempts")
        return random_number  

def NumGuessUserGuess(difficuty_choice, user_guess, random_number, max_attempt): #3b2
    attempts = 1
    while attempts <= max_attempt: 
        if user_guess > random_number:
            print("Your Guess is Higher")
        elif user_guess < random_number:
            print("Your Guess is Lower")
        elif user_guess == random_number:
            print("You have Won !!!")
            print("The correct number is: ", random_number)
            NumGuessSaveLeaderboard(difficuty_choice, attempts)
            return
        else:
            print("Invalid input. Please try again.")
        if attempts == max_attempt:
            break
        else:   
            if difficuty_choice == "1":
                if attempts == 10:
                   NumGuessClue(random_number) 
            elif difficuty_choice == "2":
                if attempts == 5:
                     NumGuessClue(random_number)
            elif difficuty_choice == "3":
                if attempts == 3:
                    NumGuessClue(random_number)
                          
            validate_input = input(f"Enter your guess [attempt {attempts + 1}]: ")
            if validate_input.isdigit():
                user_guess = int(validate_input)
                attempts += 1
            else:
                print("Invalid input! Please enter a valid number.")
                NumGuessMainMenu()

    print(f"You have exceeded MAX Attempts: {max_attempt} !! You have lost the game !!! ")
    print("The correct number was: ", random_number)
    NumGuessAgainAttempt()
    NumGuessMainMenu()

def NumGuessAgainAttempt(): #3c1
    again_attempt = input("Do you want to play again? (Y/N)")    
    if again_attempt.lower() == "y":
        NumGuessMainMenu()
    elif again_attempt.lower() == "n":  
        print("Thanks for Playing the Game !!! Will Meet you Soon")
        NumGuessExitMenu()  
    else:
        print("Thanks for Playing the Game !!! Will Meet you Soon")
        NumGuessExitMenu()

def NumGuessSaveLeaderboard(difficuty_choice, attempts): #3c2
    player_name = input("Please enter your name for Leaderboard : ")
    if difficuty_choice == "1":
        player_score = 1000 - ((attempts - 1) * 50)
    elif difficuty_choice == "2":
        player_score = 1000 - ((attempts - 1) * 100)
    else:
        player_score = 1000 - ((attempts - 1) * 200)
  
    play_time = NumGuessCurrentTS()
    add_score(player_name, player_score, play_time)
    load_file()

def NumGuessClue(random_number): #3c3
    if random_number % 2 == 0:
        print(f"Clue: Random number is Even")
    else:
        print(f"Clue: Random number is Odd")
            
def NumGuessCurrentTS(): #3d1
    now = datetime.datetime.now()
    return now.strftime("%Y:%m:%d:%H:%M:%S")

def NumGuessAutomatedHelp(): #3d2
    print()
    print("The Number Guessing Game starts")
    print("Choose the Difficulty Level:")
    print("1. Easy (Range: 1-50, 20 attempts)")
    print("2. Medium (Range: 1-100, 10 attempts)")        
    print("3. Hard (Range: 1-1000, 5 attempts)")
    print("4. Exit")
    print()
    time.sleep(2)

    print("Enter your choice: ", end='', flush=True)
    time.sleep(1)
    print('\r' + ' ' * 30, end='', flush=True) 
    print('\rEnter your choice: 1', end='', flush=True)

    time.sleep(2)
    print("\nYou have selected Easy mode (Range: 1-50, 20 attempts)")
    print("\nGuess the number between 1 and 50 within 20 attempts")
    time.sleep(2)
    
    print()
    print("Enter your guess [attempt 1]: ", end='', flush=True)
    time.sleep(4)
    print('\r' + ' ' * 50, end='', flush=True) 
    print('\rEnter your guess [attempt 1]: 2', end='', flush=True)
    print("\nYour Guess is Lower")

    print()
    print("Enter your guess [attempt 2]: ", end='', flush=True)
    time.sleep(4)
    print('\r' + ' ' * 50, end='', flush=True) 
    print('\rEnter your guess [attempt 2]: 20', end='', flush=True)
    print("\nYour Guess is Higher")

    print()
    print("Enter your guess [attempt 3]: ", end='', flush=True)
    time.sleep(4)
    print('\r' + ' ' * 50, end='', flush=True) 
    print('\rEnter your guess [attempt 3]: 10', end='', flush=True)
    print("\nYour Guess is Higher")    

    print()
    print("Enter your guess [attempt 4]: ", end='', flush=True)
    time.sleep(4)
    print('\r' + ' ' * 50, end='', flush=True) 
    print('\rEnter your guess [attempt 4]: 5', end='', flush=True)
    print("\nYou have Won !!!") 
    print("\nThe correct number is:  5") 

    time.sleep(3)

    print()
    print("Please enter your name for Leaderboard :", end='', flush=True)
    time.sleep(4)
    print('\r' + ' ' * 70, end='', flush=True) 
    print('\rPlease enter your name for Leaderboard : Pep', end='', flush=True)
    print("\nScore Added: Pep - 850 - 2025:05:22:09:38:26") 
    print()

    time.sleep(3)
    print("Leaderboard Scores:") 
    print(" - Pep - 850 - 2025:05:22:09:38:26")
    print(" - Sara - 800 - 2025:05:22:09:38:26")
    print(" - Rahim - 750 - 2025:05:22:09:38:26")

    time.sleep(3)   

# Main function to start the game
NumGuessMain()
