from abc import ABC, abstractmethod
import json
import os
import random

### Base classes ###
### employee is the player & associated attributes, contract is the main quest, task is like side-quest to up xp & gain skills ###
### some getter & setter methods are missing ###

### list of skills in the game :
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
    
    # reduction/increase values being dependant on current levels adds an intelligent mechaanic
    @abstractmethod
    def healing_break(self,player):
        if player.stress_level <= 25:
            stress_reduction = 5
        elif player.stres_level <= 50:
            stress_reduction = 10
        elif player.stress_level <= 75:
            stress_reduction = 20
        else:
            stress_reduction = 25
        
        if player.motivation_level <= 25:
            motivation_increase = 5
        elif player.motivation_level <= 50:
            motivation_increase = 10
        elif player.motivation_level <= 75:
            motivation_increase = 20
        else:
            motivation_increase = 25
        
        if player.coffee_level <= 25:
            coffee_increase = 5
        elif player.coffee_level <= 50:
            coffee_increase = 10
        elif player.coffee_level <= 75:
            coffee_increase = 20
        else:
            coffee_increase = 25
        
        self._stress_level = max(0, self._stress_level - stress_reduction)
        self._motivation_level = min(100, self._motivation_level + motivation_increase)
        self._coffee_level = min(100, self._coffee_level + coffee_increase)

        return f"{self._name} took a healing break!\nCurrent Stress Level: {self._stress_level}\n Motivation Level: {self._motivation_level}\n Coffee Level: {self._coffee_level}"

    # this method is for checking the player's current status at any time of the game 
    # like xp, stress, motivation, coffee levels, acquired skills etc
    @abstractmethod
    def check_status(self):
        status = f""" ------- PLAYER STATUS ------- \n
        Employee Name: {self._name}\n
        Role: {self._role}\n
        Experience Points (XP): {self._xp}\n
        Motivation Level: {self._motivation_level}\n
        Stress Level: {self._stress_level}\n
        Coffee Level: {self._coffee_level}\n
        Skills: {', '.join(self._skills)}"""
        return status

    ## getter and setter methods
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        self._name = name
    
    def get_role(self):
        return self._role
    
    def set_role(self, role):
        self._role = role
    
    def get_xp(self):
        return self._xp
    
    def set_xp(self, xp):
        self._xp = xp
    
    def get_motivation_level(self):
        return self._motivation_level
    
    def set_motivation_level(self, level):
        self._motivation_level = max(0, min(100, level))
    
    def get_stress_level(self):
        return self._stress_level
    
    def set_stress_level(self, level):
        self._stress_level = max(0, min(100, level))
    
    def get_coffee_level(self):
        return self._coffee_level
    
    def set_coffee_level(self, level):
        self._coffee_level = max(0, min(100, level))
    
    def get_skills(self):
        return self._skills.copy()
    
    def add_skill(self, skill):
        if skill not in self._skills:
            self._skills.append(skill)
            return f"Learned new skill: {skill}!"
        return "Skill already known."

    def __str__(self):
        return f"{self._name} - {self._role} (XP: {self._xp})"


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
        return self._name
    
    def get_description(self):
        return self._description
    
    def get_xp(self):
        return self._xp
    
    def get_required_skills(self):
        return self._required_skills.copy()
    
    def get_stress_impact(self):
        return self._stress_impact
    
    def is_successful(self):
        return self._success
    
    def __str__(self):
        return f"{self._name}: {self._description} (XP: {self._xp})"


class Task(ABC):
    def __init__(self,name,description,xp,required_skills,stress_tool):
        self.name = name
        self.description = description
        self.xp = xp
        self.required_skills = required_skills
        self.stress_tool = stress_tool
        self.success = False
    
    @abstractmethod
    def complete(self):
        pass

    ## getter methods
    def get_name(self):
        return self._name
    
    def get_xp(self):
        return self._xp
    
    def get_contractor(self):
        return self._contractor
    
    def get_required_skills(self):
        return self._required_skills.copy()
    
    def get_difficulty(self):
        return self._difficulty
    
    def is_successful(self):
        return self._success
    
    def __str__(self):
        return f"{self._name}: {self._description} (XP: {self._xp})"


### Classes inheriting from Employee ###
### they are kinda the basic positions in every company ###
    
class Intern(Employee):
    def __init__(self,name,role,xp,motivation_level,stress_level,coffee_level,skills):
        if skills is None:
            skills = []
        super().__init__(name, "Intern", xp, motivation_level, stress_level, coffee_level, skills)
        self._promotion_xp = 100

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
        self._initialize_content()
    
    def _initialize_content(self):
        self.contracts = []  # Load or define initial contracts
        self.tasks = []      # Load or define initial tasks
    
    def create_player(self, name):
        self.player = Intern(f"{name}", "Intern", 0, 50, 20, 50, [])
        return self.player
    
    ## add a saving thing for the game pls


### Main game stuff ###

def main():
    game = GameController()

    print("Welcome to Corporate Battle Simulator!")
    print("In this game, you will navigate the corporate world, taking on contracts and tasks to climb the corporate hierarchy.")
    print("The goal is to reach the position of President of the company.")
    print("Mind your stress, motivation, and coffee levels as you progress as they have an impact on bonus (or malus) you will get during your journey! :)")
    player_name = input("Enter your employee name: ")
    player = game.create_player(player_name)
    print(f"Hello, {player.get_name()}! You are starting as an Intern.")
    
    ## Menu stuff
    print("\nWhat would you like to do?")
    print("1. Take on a contract")
    print("2. Take on a task")
    print("3. Take a healing break")
    print("4. View status")
    print("5. Save and quit")
    try:
        choice = int(input("Enter the number of your choice: "))
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
    

if __name__ == "__main__":
    main()