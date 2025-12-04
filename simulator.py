import abc
import random
import json
import os
import sys
import time


# ==========================================
# 1. UTILITY CLASS (File I/O & Helpers)
# ==========================================
class SystemAdmin:
    """
    Utility class for handling game state persistence and system operations.
    Stateless helper.
    """

    SAVE_FILE = "corporate_save.json"

    @staticmethod
    def save_game_state(player_obj):
        """Saves player data to a JSON file."""
        try:
            data = {
                "name": player_obj.name,
                "role": player_obj.__class__.__name__,
                "stress": player_obj.stress,
                "motivation": player_obj.motivation,
                "xp": player_obj.xp,
                "level": player_obj.level,
            }
            with open(SystemAdmin.SAVE_FILE, "w") as f:
                json.dump(data, f)
            print(f"\n[System]: Game saved successfully to {SystemAdmin.SAVE_FILE}.")
        except IOError as e:
            print(f"\n[Error]: Could not save game - {e}")

    @staticmethod
    def load_game_state():
        """Loads player data from JSON file."""
        if not os.path.exists(SystemAdmin.SAVE_FILE):
            print("\n[System]: No save file found.")
            return None

        try:
            with open(SystemAdmin.SAVE_FILE, "r") as f:
                data = json.load(f)
            return data
        except (IOError, json.JSONDecodeError) as e:
            print(f"\n[Error]: Corrupted save file - {e}")
            return None

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# 2. ABSTRACT BASE CLASS
# ==========================================
class CorporateEntity(abc.ABC):
    """
    Abstract base class for all entities in the office (Employees, Bosses, etc).
    """

    def __init__(self, name):
        self._name = name
        self._stress = 0  # 0 to 100

    @property
    def name(self):
        return self._name

    @property
    def stress(self):
        return self._stress

    @stress.setter
    def stress(self, value):
        self._stress = max(0, min(100, value))  # Clamp between 0-100

    @abc.abstractmethod
    def get_status(self):
        pass


# ==========================================
# 3. EMPLOYEE HIERARCHY
# ==========================================
class Employee(CorporateEntity):
    """
    Base class for the player characters.
    """

    def __init__(self, name, motivation=50):
        super().__init__(name)
        self._motivation = motivation  # 0 to 100
        self._xp = 0
        self._level = 1
        self.inventory = []

    @property
    def motivation(self):
        return self._motivation

    @motivation.setter
    def motivation(self, value):
        self._motivation = max(0, min(100, value))

    @property
    def xp(self):
        return self._xp

    @property
    def level(self):
        return self._level

    def get_status(self):
        return (
            f"--- {self.name} (Lvl {self.level} {self.__class__.__name__}) ---\n"
            f"Stress:     [{'#' * (self.stress // 10):<10}] {self.stress}/100\n"
            f"Motivation: [{'#' * (self.motivation // 10):<10}] {self.motivation}/100\n"
            f"XP: {self.xp}"
        )

    def gain_xp(self, amount):
        self._xp += amount
        print(f"   + {amount} XP gained!")
        if self._xp >= self._level * 100:
            self.level_up()

    def level_up(self):
        self._level += 1
        self._xp = 0
        self.motivation = 100
        self.stress = 0
        print(f"\n🎉 PROMOTION! {self.name} is now Level {self._level}! 🎉")
        print("Motivation restored. Stress cleared.")

    def take_break(self):
        recovery = random.randint(10, 25)
        self.motivation += recovery
        self.stress -= 5
        print(f"\n{self.name} takes a break... Motivation +{recovery}, Stress -5.")

    def is_burned_out(self):
        return self.stress >= 100

    def use_item(self, item):
        item.apply(self)
        if item in self.inventory:
            self.inventory.remove(item)


class Intern(Employee):
    """High stress gain, chaotic results."""

    def __init__(self, name):
        super().__init__(name, motivation=40)

    def gain_xp(self, amount):
        # Interns learn fast (bonus XP)
        super().gain_xp(int(amount * 1.2))


class Manager(Employee):
    """High authority, low coding skill."""

    def __init__(self, name):
        super().__init__(name, motivation=60)


class Developer(Employee):
    """High coding skill, hates meetings."""

    def __init__(self, name):
        super().__init__(name, motivation=50)


class HR(Employee):
    """Likes meetings, good at people tasks."""

    def __init__(self, name):
        super().__init__(name, motivation=70)


# ==========================================
# 4. TASK / BATTLE SYSTEM HIERARCHY
# ==========================================
class Task(abc.ABC):
    """
    Abstract base class for tasks (the 'Enemies' or 'Challenges').
    """

    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty  # 1-10
        self.stress_gain = difficulty * 5
        self.motivation_cost = difficulty * 3
        self.xp_reward = difficulty * 15

    @abc.abstractmethod
    def perform(self, employee):
        pass

    def calculate_base_chance(self, employee):
        # Base success formula: Motivation% + (Level * 5) - (Difficulty * 8)
        chance = employee.motivation + (employee.level * 5) - (self.difficulty * 8)
        # Random variance
        chance += random.randint(-10, 10)
        return max(5, min(95, chance))  # Clamp between 5% and 95%

    def apply_consequences(self, employee, success, success_msg, fail_msg):
        print(f"\nAttempting: {self.name} (Diff: {self.difficulty})...")
        time.sleep(1)

        employee.motivation -= self.motivation_cost

        if success:
            print(f"✅ SUCCESS: {success_msg}")
            employee.gain_xp(self.xp_reward)
            employee.stress += self.stress_gain // 2  # Little stress even on success
        else:
            print(f"❌ FAILURE: {fail_msg}")
            employee.stress += self.stress_gain
            print(f"   (Stress +{self.stress_gain})")


# --- Specific Task Types ---


class CodingTask(Task):
    def perform(self, employee):
        chance = self.calculate_base_chance(employee)

        # Unique Logic
        if isinstance(employee, Developer):
            chance += 30
        elif isinstance(employee, Intern):
            chance -= 10  # Bug risk
        elif isinstance(employee, Manager):
            # 2% chance to delete repo
            if random.random() < 0.02:
                print(
                    "💀 CATASTROPHE: Manager accidentally deleted the main repository!"
                )
                employee.stress += 50
                return
            chance -= 20

        success = random.randint(0, 100) < chance
        self.apply_consequences(
            employee,
            success,
            "Code compiled without errors! Git push successful.",
            "Syntax Error on line 432. The build failed.",
        )


class MeetingTask(Task):
    def perform(self, employee):
        chance = self.calculate_base_chance(employee)

        if isinstance(employee, Manager):
            chance += 40
            self.xp_reward += 10  # Managers love this
        elif isinstance(employee, Developer):
            employee.motivation -= 30  # Devs hate this
            chance -= 10
        elif isinstance(employee, HR):
            chance += 50
        elif isinstance(employee, Intern):
            print("😴 Intern fell asleep during the meeting...")
            employee.motivation += 10  # Nap bonus
            return  # No success or fail, just nap

        success = random.randint(0, 100) < chance
        self.apply_consequences(
            employee,
            success,
            "Synergy achieved! Action items delegated.",
            "This could have been an email. Everyone is annoyed.",
        )


class HRTask(Task):
    def perform(self, employee):
        chance = self.calculate_base_chance(employee)

        if isinstance(employee, HR):
            chance = 90
            stress_relief = 20
        else:
            chance -= 30
            stress_relief = 0

        success = random.randint(0, 100) < chance

        if success and isinstance(employee, HR):
            employee.stress -= stress_relief
            print(f"✨ HR Zen: Stress reduced by {stress_relief}.")

        self.apply_consequences(
            employee,
            success,
            "Conflict resolved. Peace restored.",
            "You accidentally forwarded the complaint to the whole company.",
        )


class SupportTicketTask(Task):
    def perform(self, employee):
        chance = self.calculate_base_chance(employee)

        if isinstance(employee, Intern):
            print("😱 Intern is panicking over angry customer!")
            employee.stress += 10
            chance -= 20
        elif isinstance(employee, Manager):
            print("Manager delegates the ticket...")
            chance += 10  # Delegation works usually
        elif isinstance(employee, HR):
            print("HR asks: 'Have you tried turning it off and on?'")
            # Random wild success or fail
            chance = 50

        success = random.randint(0, 100) < chance
        self.apply_consequences(
            employee,
            success,
            "Ticket closed. User is mildly satisfied.",
            "User is demanding to speak to your manager.",
        )


class DocumentationTask(Task):
    def perform(self, employee):
        # Everybody hates documentation
        chance = self.calculate_base_chance(employee)
        employee.motivation -= 10

        # Except Senior Devs (handled via high level Devs generically here)
        if isinstance(employee, Developer) and employee.level > 2:
            chance += 20
            print("Senior Dev grumbles but does it responsibly.")

        success = random.randint(0, 100) < chance
        self.apply_consequences(
            employee,
            success,
            "Docs updated. Wiki is readable.",
            "You wrote 500 lines of gibberish.",
        )


class CreativeTask(Task):
    def perform(self, employee):
        chance = self.calculate_base_chance(employee)

        if isinstance(employee, Intern):
            chance += 25  # Gen Z energy
        elif isinstance(employee, Manager):
            chance -= 10  # Thinks they are good, actually bad
        elif isinstance(employee, HR):
            # Irrelevant, neutral
            pass

        success = random.randint(0, 100) < chance
        self.apply_consequences(
            employee,
            success,
            "Brilliant pitch! The client loves it.",
            "The design looks like a 90s PowerPoint.",
        )


# ==========================================
# 5. ITEM SYSTEM (Operator Overloading)
# ==========================================
class Item:
    def __init__(self, name, effect_value):
        self.name = name
        self.effect_value = effect_value

    def apply(self, employee):
        raise NotImplementedError("Subclasses must implement apply")

    def __add__(self, other):
        """Operator Overloading: Combine two items into a Bundle."""
        if isinstance(other, Item):
            new_name = f"Bundle of {self.name} & {other.name}"
            new_effect = self.effect_value + other.effect_value
            # Return a generic item representing the bundle
            return Coffee(new_name, new_effect)  # Using Coffee class as generic wrapper
        return None

    def __str__(self):
        return f"{self.name} (Power: {self.effect_value})"


class Coffee(Item):
    def __init__(self, name="Espresso", effect_value=20):
        super().__init__(name, effect_value)

    def apply(self, employee):
        print(f"\n☕ {employee.name} consumes {self.name}!")
        employee.motivation += self.effect_value
        employee.stress -= self.effect_value // 2
        print(f"   Motivation +{self.effect_value}, Stress -{self.effect_value // 2}")

        if employee.motivation > 120:
            print("   ⚠️ JITTERS! Too much coffee. Health/Focus crash.")
            employee.stress += 15


# ==========================================
# 6. MAIN GAME LOOP
# ==========================================
def create_random_task():
    task_types = [
        CodingTask,
        MeetingTask,
        HRTask,
        SupportTicketTask,
        DocumentationTask,
        CreativeTask,
    ]
    t_cls = random.choice(task_types)

    # Generate fun names
    adjectives = ["Urgent", "Legacy", "Pointless", "Critical", "Boring"]
    nouns = [
        "API Update",
        "Sync",
        "Paperwork",
        "Client Complaint",
        "Wiki Edit",
        "Brainstorm",
    ]

    name = f"{random.choice(adjectives)} {random.choice(nouns)}"
    difficulty = random.randint(1, 8)

    return t_cls(name, difficulty)


def main():
    SystemAdmin.clear_screen()
    print("🏢 === CORPORATE BATTLE SIMULATOR === 🏢")

    player = None

    # --- Menu ---
    while True:
        print("\n1. New Game")
        print("2. Load Game")
        print("3. Exit")
        choice = input("Select: ")

        if choice == "1":
            name = input("Enter Name: ")
            print("Choose Class:\n1. Intern\n2. Developer\n3. Manager\n4. HR")
            r_choice = input("Role: ")

            if r_choice == "1":
                player = Intern(name)
            elif r_choice == "2":
                player = Developer(name)
            elif r_choice == "3":
                player = Manager(name)
            elif r_choice == "4":
                player = HR(name)
            else:
                player = Intern(name)  # Default

            # Starter Item
            player.inventory.append(Coffee("Instant Coffee", 10))
            break

        elif choice == "2":
            data = SystemAdmin.load_game_state()
            if data:
                # Reconstruct object
                p_cls_name = data["role"]
                if p_cls_name == "Intern":
                    player = Intern(data["name"])
                elif p_cls_name == "Developer":
                    player = Developer(data["name"])
                elif p_cls_name == "Manager":
                    player = Manager(data["name"])
                elif p_cls_name == "HR":
                    player = HR(data["name"])
                else:
                    player = Employee(data["name"])

                player.stress = data["stress"]
                player.motivation = data["motivation"]
                player._xp = data["xp"]
                player._level = data["level"]
                player.inventory.append(Coffee("Saved Coffee", 15))  # Bonus for loading
                print(f"Welcome back, {player.name}!")
                break

        elif choice == "3":
            sys.exit()

    # --- Game Loop ---
    while True:
        print("\n" + "=" * 30)
        print(player.get_status())
        print("=" * 30)

        if player.is_burned_out():
            print("\n🔥 BURNOUT! You have collapsed from stress.")
            print("GAME OVER.")
            break

        print("\nActions:")
        print("1. Find Work (Start Task)")
        print("2. Take a Break")
        print("3. Inventory")
        print("4. Save & Quit")

        action = input(">> ")

        if action == "1":
            task = create_random_task()
            # Logic check: Can player perform?
            if player.motivation < task.motivation_cost:
                print("\n❌ Too unmotivated to work! Drink coffee or take a break.")
                continue

            # Polymorphic call
            task.perform(player)

        elif action == "2":
            player.take_break()

        elif action == "3":
            if not player.inventory:
                print("\nEmpty Pockets.")
            else:
                print("\nInventory:")
                for i, item in enumerate(player.inventory):
                    print(f"{i+1}. {item}")
                print("C. Combine Items (Operator Overload Demo)")
                print("B. Back")

                inv_choice = input("Use item # or (C)ombine: ").upper()

                if inv_choice.isdigit():
                    idx = int(inv_choice) - 1
                    if 0 <= idx < len(player.inventory):
                        player.use_item(player.inventory[idx])

                elif inv_choice == "C" and len(player.inventory) >= 2:
                    # Demo of Operator Overloading
                    item1 = player.inventory.pop(0)
                    item2 = player.inventory.pop(0)
                    combined = item1 + item2  # Uses __add__
                    player.inventory.append(combined)
                    print(f"\n✨ Crafted: {combined.name}!")

        elif action == "4":
            SystemAdmin.save_game_state(player)
            print("Bye!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nForce Quit.")
    except Exception as e:
        print(f"Critical System Failure: {e}")
