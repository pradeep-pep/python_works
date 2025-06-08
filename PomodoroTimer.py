#Pomodoro technique timer
import sys
import os
import random
import time 
import datetime
import platform

POMODORO_TIME_DEFAULT = 25
POMODORO_SHORT_DEFAULT = 5
POMODORO_LONG_DEFAULT = 15
POMODORO_CYCLE_DEFAULT = 3
 
#File Handling
def load_all_tasks():
    TASK_FILE = "PomodoroTask.txt"
    print()
    if not os.path.exists(TASK_FILE):
        print("File does not exist") 
        return []      
    with open(TASK_FILE, "r") as f:
        print("File does exist.")
        lines = f.readlines()
        print(lines)
        return [line.strip().split("-") for line in lines if line.strip()]
    
def load_pend_tasks():
    TASK_FILE = "PomodoroTask.txt"
    print()
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w") as f:
            pass   
        return []         
    with open(TASK_FILE, "r") as f:
        lines = f.readlines()
        records = [line.strip().split("-") for line in lines if line.strip()]
        filtered_records = [rec for rec in records if len(rec) > 2 and rec[2].strip().lower() == "pending"]
        filtered_records = filtered_records[:5]
        for idx, record in enumerate(filtered_records, start=1):
            print(f"{idx}. {' - '.join(record[:2])}")
        return filtered_records
    
def save_file(tasks):
    TASK_FILE = "PomodoroTask.txt"
    if not os.path.exists(TASK_FILE):
        print("File does not exist") 
        return []       
    with open(TASK_FILE, "w") as f:
        for task_name, task_desc, status in tasks:
            f.write(f"{task_name}-{task_desc}-{status}\n")

def add_task(task_name, task_desc):
    tasks = load_all_tasks()
    TASK_FILE = "PomodoroTask.txt"
    if not os.path.exists(TASK_FILE): 
        return []
    tasks.append([task_name, task_desc, "pending"])
    save_file(tasks)
    print(f"Added: {task_name} - {task_desc} - pending")
      
#Main Menu
def PomodoroMain():
    PomodoroWelcome() 
    first_input = PomodoroFirstInput()
    PomodoroFirstInputMenu(first_input)   

def PomodoroWelcome(): #1
    print()
    print("Welcome to the Pomodoro Timer : https://pomofocus.io/ !")
    print("**The application will generate a timer cycle based on entries in minutes you choose**" 
          "\n**You have to access to start and stop the timer for the tasks you work**" 
          "\n**Privilage to set short & long break timer is also present**" 
          "\n**Thank you**")    
    print()
    print("Type 'Start' to Use the Pomodoro Timer.")
    print()  

def PomodoroFirstInput(): #2
    first_input = input("Enter your choice (Start/Exit) - [Not Case Sensitive] : ").strip().lower()  
    return(first_input)   

def PomodoroFirstInputMenu(first_input): #3
    if first_input == "start":
        PomodoroMainMenu()
    elif first_input == "exit":
        PomodoroExitMenu()         
    else:
        print()
        print("Invalid input. Please try again.")
        print()
        first_input = PomodoroFirstInput()
        PomodoroFirstInputMenu(first_input)

#Task for Timer Handling
def PomodoroMainMenu(): #3a
    print()
    print("Choose Task from your 'Pending Top 10 To-Do list' for which Timer to be set:")
    filtered_records = load_pend_tasks()  
    print("       OR      ")
    print("6. Add new task - [Format: Add Task_Name Task_Description]")
    print("7. Exit")
    print()
    task_choice = PomodoroOperInput()
    pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomodoroMainOper(task_choice, filtered_records) 
    time.sleep(4)
    clear_console()
    pomodoro_timer(pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles)
    

def PomodoroExitMenu(): #3b
    print()
    print("Thank you for using the Pomodoro Timer Application!")
    print("Goodbye!")   
    sys.exit()  
    
def PomodoroOperInput(): #3a1
    task_choice = input("Enter your choice: ") 
    return(task_choice) 

def PomodoroMainOper(task_choice, filtered_records): #3a2
    if task_choice == "1":
        task_name, task_desc = filtered_records[0][:2]  
        pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomorodoAssignTask(task_name,task_desc) 
        return  (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles)  
    elif task_choice == "2":    
        task_name, task_desc = filtered_records[1][:2]    
        pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomorodoAssignTask(task_name,task_desc) 
        return  (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles) 
    elif task_choice == "3":
        task_name, task_desc = filtered_records[2][:2]    
        pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomorodoAssignTask(task_name,task_desc) 
        return  (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles) 
    elif task_choice == "4":    
        task_name, task_desc = filtered_records[3][:2]    
        pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomorodoAssignTask(task_name,task_desc) 
        return  (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles) 
    elif task_choice == "5":
        task_name, task_desc = filtered_records[4][:2]    
        pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomorodoAssignTask(task_name,task_desc) 
        return  (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles) 
    elif task_choice == "6":
        print("You have selected to add a task.")
        task_input = input("Enter add task - [Format: Add Task_Name Task_Description] : ")
        oper_list = ToDoStrOperInput(task_input) 
        task_name,task_desc = ToDoAddTasks(oper_list)
        print()
        pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomorodoAssignTask(task_name,task_desc) 
        return  (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles)         
    elif task_choice == "7":
        PomodoroExitMenu()
    else:
        print()
        print("Invalid input. Please try again.")
        PomodoroMainMenu()

def ToDoStrOperInput(task_input): #3a2a
    oper_list = task_input.split() 
    print(oper_list)
    return(oper_list)

def ToDoAddTasks(oper_list): #3a2b
    if len(oper_list) < 3 or oper_list[0].lower() != "add":
        print("Wrong Input Format- [Please use: Add Task_Name Task_Description] : ")
        return   
    print(f"Task requested to add is: {oper_list[1]}-{oper_list[2:]}")
    task_name, task_desc = oper_list[1], " ".join(oper_list[2:])
    add_task(task_name, task_desc)
    return task_name, task_desc

def PomorodoAssignTask(task_name,task_desc): #3a2c
    print(f"You have selected Task: {task_name} - {task_desc}")
    pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomodoroTimerSetting()
    print()
    print("The new user set pomodoro timer settings are:")
    print(f"Pomodoro Time: {pomodoro_time} minutes")
    print(f"Short Break Time: {pomodoro_short} minutes")   
    print(f"Long Break Time: {pomodoro_long} minutes")
    print(f"Pomodoros before Long Break: {pomodoro_cycles}")
    print()    
    print(f"Pomodoro Timer set for {task_name} - {task_desc} with {pomodoro_time} minutes.")   

    return  (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles) 

def PomodoroTimerSetting(): #3a2c1
    print()
    print("The default pomodoro timer settings are:")
    print(f"Pomodoro Time: {POMODORO_TIME_DEFAULT} minutes")
    print(f"Short Break Time: {POMODORO_SHORT_DEFAULT} minutes")   
    print(f"Long Break Time: {POMODORO_LONG_DEFAULT} minutes")
    print(f"Pomodoros before Long Break: {POMODORO_CYCLE_DEFAULT}")
    print()
    user_settings = input("Do you want to change the default settings? (yes/no): ").strip().lower() 
    if user_settings == "yes":
        pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles = PomodoroUserSettings()
    elif user_settings == "no":
        pomodoro_time = POMODORO_TIME_DEFAULT
        pomodoro_short = POMODORO_SHORT_DEFAULT
        pomodoro_long = POMODORO_LONG_DEFAULT
        pomodoro_cycles = POMODORO_CYCLE_DEFAULT
    else:
        print("Invalid input. Using default settings.")
        pomodoro_time = POMODORO_TIME_DEFAULT
        pomodoro_short = POMODORO_SHORT_DEFAULT
        pomodoro_long = POMODORO_LONG_DEFAULT
        pomodoro_cycles = POMODORO_CYCLE_DEFAULT 

    return  (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles)

def PomodoroUserSettings(): #3a2c1a     
    try:
        pomodoro_time = int(input("Enter your pomodoro for choosen task: "))
        if pomodoro_time <= 0:
            raise ValueError("Pomodoro time must be a positive integer.")  
         
        pomodoro_short = int(input("Enter your short break time: ")) 
        if pomodoro_short <= 0: 
            raise ValueError("Short break time must be a positive integer.") 
           
        pomodoro_long = int(input("Enter your long break time: ")) 
        if pomodoro_long <= 0:
            raise ValueError("Long break time must be a positive integer.")
        
        pomodoro_cycles = int(input("Enter number of pomodoros before a long break: "))
        if pomodoro_cycles <= 0:
            raise ValueError("Number of cycles must be a positive integer.")
        
    except ValueError:
        print("Invalid input. Using default settings.")
        pomodoro_time = POMODORO_TIME_DEFAULT
        pomodoro_short = POMODORO_SHORT_DEFAULT
        pomodoro_long = POMODORO_LONG_DEFAULT
        pomodoro_cycles = POMODORO_CYCLE_DEFAULT
    
    return (pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles)

def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def PomodoroCurrentTS(): #3d1
    now = datetime.datetime.now()
    return now.strftime("%Y:%m:%d:%H:%M:%S")

def pomodoro_timer(pomodoro_time, pomodoro_short, pomodoro_long, pomodoro_cycles):
    print(f"Pomodoro Time: {pomodoro_time} minutes")
    print(f"Short Break Time: {pomodoro_short} minutes")   
    print(f"Long Break Time: {pomodoro_long} minutes")
    print(f"Pomodoros before Long Break: {pomodoro_cycles}")

    pomodoro_count = 0
    while True:
        clear_console()
        print(f"🍅 Pomodoro Session {pomodoro_count + 1}")
        countdown(pomodoro_time)
        pomodoro_count += 1
        notify("Work session complete!")

        if pomodoro_count % pomodoro_cycles == 0:
            print("🛌 Time for a long break!")
            countdown(pomodoro_long)
            notify("Long break over!")
        else:
            print("☕ Time for a short break!")
            countdown(pomodoro_short)
            notify("Short break over!")

        user_input = input("Start next Pomodoro? (y/n): ").strip().lower()
        if user_input != 'y':
            print("👋 Session ended. Great job!")
            break   

def countdown(minutes):
    total_seconds = minutes * 60
    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        time_format = f"{mins:02d}:{secs:02d}"
        print(f"\r⏳ {time_format}", end="")
        time.sleep(1)
        total_seconds -= 1
    print()

def notify(message):
    print(f"\n🔔 {message}")
    # For Windows, you can use winsound.Beep
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 500)
    else:
        print('\a')  # Beep for Unix-like systems

# Main function to start the timer
PomodoroMain()
