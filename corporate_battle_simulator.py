from abc import ABC, abstractmethod
import json
import os
import random

### Base classes ###
### employee is the player & associated attributes, contract is the main quest, task is like side-quest to up xp & gain skills ###
### some getter & setter methods might be missing ###

### list of possible skills in the game :
## Organisation : reduce stress impact, reduce coffee consumption
## Adaptability : reduce stress impact
## Teamwork : increase motivation
## Problem Solving : increase chance of success
## Communication : increase chance of success
## Leadership : increase motivation, increase stress_level
## Creativity : increase chance of success
## Critical Thinking : increase chance of success
## Negotiation : increase chance of success


class Employee(ABC):
    def __init__(self,name,role,xp,motivation_level,stress_level,coffee_level,skills):
        self.name = name
        self.role = role
        self.xp = xp
        self.motivation_level = motivation_level
        self.stress_level = stress_level
        self.coffee_level = coffee_level
        self.skills = skills
    
    @abstractmethod
    def work_contract(self,contract):
        pass
    
    @abstractmethod
    def work_task(self,task):
        pass
    
    # reduction/increase values being dependant on current levels adds an intelligent mechanic
    @abstractmethod
    def healing_break(self):
        if self.stress_level <= 25:
            stress_reduction = 5
        elif self.stress_level <= 50:
            stress_reduction = 10
        elif self.stress_level <= 75:
            stress_reduction = 20
        else:
            stress_reduction = 25
        
        if self.motivation_level <= 25:
            motivation_increase = 5
        elif self.motivation_level <= 50:
            motivation_increase = 10
        elif self.motivation_level <= 75:
            motivation_increase = 20
        else:
            motivation_increase = 25
        
        if self.coffee_level <= 25:
            coffee_increase = 5
        elif self.coffee_level <= 50:
            coffee_increase = 10
        elif self.coffee_level <= 75:
            coffee_increase = 20
        else:
            coffee_increase = 25
        
        self.stress_level = max(0,self.stress_level-stress_reduction)
        self.motivation_level = min(100,self.motivation_level+motivation_increase)
        self.coffee_level = min(100,self.coffee_level+coffee_increase)

        return f"\n{self.name} took a healing break!\nStress Level: {self.stress_level}\nMotivation Level: {self.motivation_level}\nCoffee Level: {self.coffee_level}"

    # this method is for checking the player's current status at any time of the game 
    @abstractmethod
    def check_status(self):
        status = f"""\n------- PLAYER STATUS -------
        \nEmployee Name: {self.name}\nRole: {self.role}\nExperience Points (XP): {self.xp}\nStress Level: {self.stress_level}\nMotivation Level: {self.motivation_level}\nCoffee Level: {self.coffee_level}\nSkills: {', '.join(self.skills)}"""
        return status

    ## getter and setter methods
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
    
    def get_role(self):
        return self.role
    
    def set_role(self, role):
        self.role = role
    
    def get_xp(self):
        return self.xp
    
    def set_xp(self, xp):
        self.xp = xp
    
    def get_motivation_level(self):
        return self.motivation_level
    
    def set_motivation_level(self, level):
        self.motivation_level = max(0,min(100, level))
    
    def get_stress_level(self):
        return self.stress_level
    
    def set_stress_level(self, level):
        self.stress_level = max(0,min(100, level))
    
    def get_coffee_level(self):
        return self.coffee_level
    
    def set_coffee_level(self, level):
        self.coffee_level = max(0,min(100, level))
    
    def get_skills(self):
        return self.skills.copy()
    
    def add_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)
            return f"Learned new skill: {skill}!"
        return "Skill already known."

    def __str__(self):
        return f"{self.name} - {self.role} (XP: {self.xp})"


class Contract(ABC):
    def __init__(self,name,xp,required_skills,stress_tool):
        self.name = name
        self.xp = xp
        self.required_skills = required_skills
        self.stress_tool = stress_tool
        self.success = False
    
    @abstractmethod
    def complete(self):
        pass

    ## getter methods
    def get_name(self):
        return self.name
    
    def get_xp(self):
        return self.xp
    
    def get_required_skills(self):
        return self.required_skills.copy()
    
    def get_stress_tool(self):
        return self.stress_tool
    
    def is_successful(self):
        return self.success
    
    def __str__(self):
        return f"{self.name} XP: {self.xp}"


class Task(ABC):
    def __init__(self,name,xp,required_skills,stress_tool):
        self.name = name
        self.xp = xp
        self.required_skills = required_skills
        self.stress_tool = stress_tool
        self.success = False
    
    @abstractmethod
    def complete(self):
        pass

    ## getter methods
    def get_name(self):
        return self.name
    
    def get_xp(self):
        return self.xp
    
    def get_required_skills(self):
        return self.required_skills.copy()
    
    def is_successful(self):
        return self.success
    
    def __str__(self):
        return f"{self.name} XP: {self.xp}"


### Classes inheriting from Employee ###
### they are kinda the basic positions in every company ###
    
class Intern(Employee):
    def __init__(self,name,role,xp,motivation_level,stress_level,coffee_level,skills):
        if skills is None:
            skills = []
        super().__init__(name,"Intern",xp,motivation_level,stress_level,coffee_level,skills)
        self.promotion_xp = 100

    def work_contract(self,contract):
        return super().work_contract(contract)
    
    def work_task(self,task):
        return super().work_task(task)
    
    def healing_break(self):
        return super().healing_break()
    
    def check_status(self):
        return super().check_status()
    
    

class Junior(Employee):
    def __init__(self,name,role,xp,motivation_level,stress_level,coffee_level,skills):
        super().__init__(name,role,xp,motivation_level,stress_level,coffee_level,skills)

        
class Associate(Employee):
    def __init__(self,name,role,xp,motivation_level,stress_level,coffee_level,skills):
        super().__init__(name,role,xp,motivation_level,stress_level,coffee_level,skills)

        
class Senior(Employee):
    def __init__(self,name,role,xp,motivation_level,stress_level,coffee_level,skills):
        super().__init__(name,role,xp,motivation_level,stress_level,coffee_level,skills)

                
class Manager(Employee):
    def __init__(self,name,role,xp,motivation_level,stress_level,coffee_level,skills):
        super().__init__(name,role,xp,motivation_level,stress_level,coffee_level,skills)

        
class President(Employee):
    def __init__(self,name,role,xp,motivation_level,stress_level,coffee_level,skills):
        super().__init__(name,role,xp,motivation_level,stress_level,coffee_level,skills)


### Classes inheriting from Contract ###

class SmallContract(Contract):
    def __init__(self,name,xp,required_skills,stress_tool):
        super().__init__(name,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_contract(self)

class MediumContract(Contract):
    def __init__(self,name,xp,required_skills,stress_tool):
        super().__init__(name,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_contract(self)

class LargeContract(Contract):
    def __init__(self,name,xp,required_skills,stress_tool):
        super().__init__(name,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_contract(self)

class CriticalContract(Contract):
    def __init__(self,name,xp,required_skills,stress_tool):
        super().__init__(name,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_contract(self)


### Classes inheriting from Task ###

class InitiationTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)

class MailSendingTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)

class ReportFilingTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)

class PresentationTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)

class ClientMeetingTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)

class ProjectManagementTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)

class ForecastingTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)

class StrategicPlanningTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)

class SchedulingTask(Task):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        super().__init__(name,description,xp,required_skills,stress_tool)
    
    def complete(self,employee):
        return employee.work_task(self)


### Game controller ###

class GameController:
    def __init__(self):
        self.player = None
        self.contracts = []
        self.tasks = []
        self.initialize_content()
    
    def initialize_content(self):
        self.contracts = []  # Load or define initial contracts
        self.tasks = []      # Load or define initial tasks
    
    def create_player(self, name):
        self.player = Intern(f"{name}","Intern",0,50,20,50,[])
        return self.player
    
    ## add the loading thing for the game pls
    #def load_game(self, filepath):
    #    pass

    ## add the saving thing for the game pls
    #def save_game(self, filepath):
    #    pass

    def is_game_victory(self):
        return self.player.role == "President"
    
    def is_game_over(self):
        if self.player.stress_level >= 100:
            return "Your stress level is over 100, you are burnout!"
        if self.player.motivation_level <= 0:
            return "Your motivation level is 0, you are quitting!"


### Main game stuff ###

def main():
    game = GameController()

    print("\n=================================================")
    print("Welcome to Corporate Battle Simulator!")
    print("=================================================")
    print("\nIn this game, you will navigate the corporate world, taking on contracts and tasks to climb the corporate hierarchy.")
    print("The goal is to reach the position of President of the company.\n")
    print("Mind your stress, motivation, and coffee levels as you progress as they have an impact on bonus (or malus) you will get during your journey! :)\n")
    
    # if there is a saved game, possibility to load it, else start new game logic pls
    player_name = input("Enter your employee name: ")
    player = game.create_player(player_name)
    print(f"\nHello, {player.get_name()}! You have been hired as an Intern at BattleCORP.")
    
    ## game loop
    while True:
        if game.is_game_victory():
            print("\n------- VICTORY -------\n")
            print("Congratulations! You have reached the position of President and won the game!")
            print("\n------- VICTORY -------")
            break
        
        game_over_message = game.is_game_over()
        if game_over_message:
            print("\n------- GAME OVER -------\n")
            print(game_over_message)
            print("\n------- GAME OVER -------")
            break
    
        try:
            print("\n------- MENU -------")
            print("\nWhat would you like to do?")
            print("1. Take on a contract")
            print("2. Take on a task")
            print("3. Take a healing break")
            print("4. View status")
            print("5. Save and quit")
            try:
                choice = int(input("\nEnter the number of your choice: "))
                if choice == 1:
                    pass
                elif choice == 2:
                    pass
                elif choice == 3:
                    heal = player.healing_break()
                    print(heal)
                elif choice == 4:
                    status = player.check_status()
                    print(status)
                elif choice == 5:
                    pass
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")
    
if __name__ == "__main__":
    main()