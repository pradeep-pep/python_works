#ToDo List Application fetching user data via Input() & Not via sys.argv
#If file not found, it will NOT create a new file
import sys
import os

#File Handling
def load_file():
    print(f"FILE REFERENCE:")
    TASK_FILE = "todotask.txt"
    print(f"Looking for file at: {TASK_FILE}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Absolute path of the script: {os.path.abspath(__file__)}")
    print()
    if not os.path.exists(TASK_FILE):
        print("File does not exist") 
        return []      
    with open(TASK_FILE, "r") as f:
        print("File does exist.")
        lines = f.readlines()
        print(lines)
        return [line.strip().split("-") for line in lines if line.strip()]

def save_file(tasks):
    TASK_FILE = "todotask.txt"
    if not os.path.exists(TASK_FILE):
        print("File does not exist") 
        return []       
    with open(TASK_FILE, "w") as f:
        for task_name, task_desc, status in tasks:
            f.write(f"{task_name}-{task_desc}-{status}\n")

#Task Handling
def add_task(task_name, task_desc):
    tasks = load_file()
    TASK_FILE = "todotask.txt"
    if not os.path.exists(TASK_FILE): 
        return []
    tasks.append([task_name, task_desc, "pending"])
    save_file(tasks)
    print(f"Added: {task_name} - {task_desc} - pending")

def upd_task(task_num, status):
    tasks = load_file()
    TASK_FILE = "todotask.txt"
    if not os.path.exists(TASK_FILE): 
        return []    
    tasks[task_num - 1][2] = status
    save_file(tasks)
    print(f"Updated: {tasks[task_num - 1][0]} - {tasks[task_num - 1][1]} - {status}")

def rem_task(remove_Item):
    tasks = load_file()
    if not tasks:
        print("Your To-Do list is empty to attempt any remove item.")
        return
    removed = tasks.pop(remove_Item)
    save_file(tasks)
    print(f"Deleted: {removed[0]} - {removed[1]} - {removed[2]}")

#Main Menu
def ToDoMain():
    ToDoWelcome() 
    first_input = ToDoFirstInput()
    ToDoFirstInputMenu(first_input)   
    if first_input != "menu":
        ToDoSecondTryMenu() 

def ToDoWelcome(): #1
    print()
    print("Welcome to the To-Do List Application!")
    print("You will be able to maintain a list of tasks where you can " \
          "\n'Add a new itenary, Update the status & Remove them from list'" \
          " as per need.")
    print()
    print("Type 'Menu' to view the list of available actions."
          "\nOr 'Help' to view the help section.")
    print()  

def ToDoFirstInput(): #2
    first_input = input("Enter your choice (Menu/Help) - [Not Case Sensitive] : ").strip().lower()  
    return(first_input)   

def ToDoFirstInputMenu(first_input): #3
    if first_input == "menu":
        ToDoMainMenu()
    elif first_input == "help":
        ToDoHelpMenu() 
    else:
        print()
        print("Invalid input. Please try again.")

def ToDoSecondTryMenu(): #4
    secondTry_input = input("Enter your choice (Menu/Help/Exit) - [Not Case Sensitive] : ").strip().lower()  
    if secondTry_input == "menu":
        ToDoMainMenu()
    elif secondTry_input == "help":
        ToDoHelpMenu()
        ToDoSecondTryMenu() 
    elif secondTry_input == "exit":
        ToDoExitMenu()    
    else:
        print()
        print("Invalid input. Please try again.")
        ToDoSecondTryMenu()   

def ToDoMainMenu(): #4a
    print()
    print("Main Menu:")
    print("1. View Tasks")
    print("2. Add Task")        
    print("3. Update Task")
    print("4. Remove Task")
    print("5. Exit")
    print()
    oper_choice = ToDoOperInput()
    ToDoMainOper(oper_choice) 
   
def ToDoHelpMenu(): #4b
    print()
    print("Help Section:")
    print("You will have to enter the Action 'View, Add, Update, Remove' " \
          "followed by the Task Name & Task Description:'optional'")
    print()
    print("Samples: You can choose to enter any of the following methods:")
    print("*\t1 [OR] View")
    print("*\t2 [AND then] Add Study Python Programming")
    print("*\t2 [AND then] Add Finish Training Program")
    print("*\t3 [AND then] Update 2 Done [OR] Update 1 Cancelled [OR] Update 3 In Progress")
    print("*\t4 [AND then] Remove 2")
    print("*\t5 [OR] Exit")
    print()

def ToDoExitMenu(): #4c
    print()
    print("Thank you for using the To-Do List Application!")
    print("Goodbye!")   
    sys.exit()  
    
def ToDoOperInput(): #4a1
    oper_choice = input("Enter your choice: ") 
    return(oper_choice) 

def ToDoMainOper(oper_choice): #4a2
    if oper_choice == "1" or oper_choice.lower() == "view":
        print("You have selected to view the tasks.")
        ToDoListTasks()
        print()
        ToDoSecondTryMenu()
    elif oper_choice == "2":
        print("You have selected to add a task.")
        task_input = input("Enter add task - [Format: Add Task_Name Task_Description] : ")
        oper_list = ToDoStrOperInput(task_input) 
        ToDoAddTasks(oper_list)
        print()
        ToDoListTasks()
        print()
        ToDoSecondTryMenu()         
    elif oper_choice == "3":
        print("You have selected to update a task.")
        task_input = input("Enter update task - [Format: Update Task_Number Task_Status] : ")
        oper_list = ToDoStrOperInput(task_input)
        ToDoUpdTasks(oper_list)
        print()     
        ToDoListTasks()
        print()
        ToDoSecondTryMenu()  
    elif oper_choice == "4":
        print("You have selected to remove a task.")
        ToDoListTasks()
        task_input = input("Enter remove task - [Format: Remove Task_Number] : ")
        oper_list = ToDoStrOperInput(task_input) 
        ToDoRemoveTasks(oper_list)
        print()
        ToDoListTasks()
        print()
        ToDoSecondTryMenu()        
    elif oper_choice == "5"  or oper_choice.lower() == "exit":
        ToDoExitMenu()
    else:
        print()
        print("Invalid input. Please try again.")
        ToDoMainMenu()
        
def ToDoStrOperInput(task_input): #4b0
    oper_list = task_input.split() 
    print(oper_list)
    return(oper_list)

def ToDoListTasks(): #4b1
    tasks = load_file()
    if not tasks:
        print("Your To-Do list is empty.")
        return
    for i, (task_name, task_desc, status) in enumerate(tasks, 1):
        if status.lower() == "done":
           mark = "✔️"
           print(f"{i}. [{mark} ] {task_name} {task_desc}") 
        elif status.lower() == "in progress":
              mark = "⏳"
              print(f"{i}. [{mark}] {task_name} {task_desc}") 
        elif status.lower() == "cancelled":
              mark = "❌"
              print(f"{i}. [{mark}] {task_name} {task_desc}") 
        elif status.lower() == "pending":
              mark = "❌❌"
              print(f"{i}. [{mark}] {task_name} {task_desc}") 
        else:
              print(f"{i}. Status of this item in To-Do list is any other than permitted.")

def ToDoAddTasks(oper_list): #4b2
    tasks = load_file()
    if len(oper_list) < 3 or oper_list[0].lower() != "add":
        print("Wrong Input Format- [Please use: Add Task_Name Task_Description] : ")
        return   
    print(f"Task requested to add is: {oper_list[1]}-{oper_list[2:]}")
    task_name, task_desc = oper_list[1], " ".join(oper_list[2:])
    add_task(task_name, task_desc)

def ToDoUpdTasks(oper_list): #4b3
    tasks = load_file()

    if len(oper_list) < 3 or oper_list[0].lower() != "update" or oper_list[1].isdigit() == False:
        print("Wrong Input Format- [Please use: Update Task_Number Task_Status] : ")       
        return  
    if int(oper_list[1]) < 1 or int(oper_list[1]) > len(tasks):
        print("Invalid task number.")
        return
    print(f"Task requested to update is: {oper_list[1]}") 
    task_num, status = int(oper_list[1]), " ".join(oper_list[2:])
    print(task_num, status)
    upd_task(task_num, status)
   
def ToDoRemoveTasks(oper_list): #4b4
    tasks = load_file()
    if not tasks:
        print("Your To-Do list is empty to attempt any remove item.")
        return
    if len(oper_list) != 2 or oper_list[0].lower() != "remove" or oper_list[1].isdigit() == False:
        print("Wrong Input Format- [Please use: Remove Task_Number] : ")
        return   
    if int(oper_list[1]) < 1 or int(oper_list[1]) > len(tasks):
        print("Invalid Task number to remove.")
        return
    print(f"Task requested to remove is: {oper_list[1]}")
    remove_Item = int(oper_list[1]) - 1
    rem_task(remove_Item)
 
ToDoMain()
