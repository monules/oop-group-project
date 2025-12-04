import abc
import random
import json
import os
import sys
import time


# ==========================================
# FILE I/O AND HELPER STUFF
# ==========================================
class SystemAdmin:
    # handles saving and loading
    filename = "savefile.json"

    @staticmethod
    def save_game(p):
        try:
            # dumping stats to json
            data = {
                "name": p.name,
                "role": p.__class__.__name__,
                "stress": p.stress,
                "motivation": p.motivation,
                "xp": p.xp,
                "level": p.level,
            }
            with open(SystemAdmin.filename, "w") as f:
                json.dump(data, f)
            print("\n>> game saved. don't forget to push to git.")
        except Exception as e:
            print("err saving:", e)

    @staticmethod
    def load_game():
        if not os.path.exists(SystemAdmin.filename):
            print(">> no save file found.")
            return None

        try:
            with open(SystemAdmin.filename, "r") as f:
                return json.load(f)
        except:
            print(">> save file is corrupted or smth.")
            return None

    @staticmethod
    def cls():
        # clears terminal
        os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# BASE CLASSES
# ==========================================
class CorporateEntity(abc.ABC):
    def __init__(self, name):
        self._name = name
        self._stress = 0

    @property
    def name(self):
        return self._name

    # stress getter/setter encapsulation
    @property
    def stress(self):
        return self._stress

    @stress.setter
    def stress(self, val):
        # cap stress at 100
        if val > 100:
            self._stress = 100
        elif val < 0:
            self._stress = 0
        else:
            self._stress = val

    @abc.abstractmethod
    def get_status(self):
        pass


class Employee(CorporateEntity):
    def __init__(self, name, mot=50):
        super().__init__(name)
        self._motivation = mot
        self._xp = 0
        self._level = 1
        self.inventory = []  # list for items

    @property
    def motivation(self):
        return self._motivation

    @motivation.setter
    def motivation(self, val):
        self._motivation = max(0, min(100, val))

    @property
    def xp(self):
        return self._xp

    @property
    def level(self):
        return self._level

    def get_status(self):
        # messy string formatting but it works
        s_bar = "#" * (self.stress // 10)
        m_bar = "#" * (self.motivation // 10)
        return (
            f"--- {self.name} ({self.__class__.__name__}) ---\n"
            f"LVL: {self.level} | XP: {self.xp}\n"
            f"Stress:     [{s_bar:<10}] {self.stress}\n"
            f"Motivation: [{m_bar:<10}] {self.motivation}"
        )

    def add_xp(self, amount):
        self._xp += amount
        print(f"   > got {amount} xp")
        # level up logic
        if self._xp >= self._level * 100:
            self._level += 1
            self._xp = 0
            self.motivation = 100
            self.stress = 0
            print(f"\n!!! PROMOTION !!! {self.name} is now lvl {self._level}")

    def take_break(self):
        # randomization
        rec = random.randint(10, 25)
        self.motivation += rec
        self.stress -= 5
        print(f"\n{self.name} is scrolling tiktok... mot +{rec}, stress -5")

    def use_item(self, item):
        item.apply(self)
        if item in self.inventory:
            self.inventory.remove(item)


# ==========================================
# ROLES
# ==========================================
class Intern(Employee):
    def __init__(self, name):
        super().__init__(name, mot=40)

    def add_xp(self, amount):
        # interns learn faster
        super().add_xp(int(amount * 1.2))


class Manager(Employee):
    def __init__(self, name):
        super().__init__(name, mot=60)


class Developer(Employee):
    def __init__(self, name):
        super().__init__(name, mot=50)


class HR(Employee):
    def __init__(self, name):
        super().__init__(name, mot=70)


# ==========================================
# TASKS & LOGIC
# ==========================================
class Task(abc.ABC):
    def __init__(self, name, diff):
        self.name = name
        self.diff = diff
        self.stress_add = diff * 5
        self.mot_cost = diff * 3
        self.xp_gain = diff * 15

    @abc.abstractmethod
    def do_task(self, emp):
        pass

    def calc_odds(self, emp):
        # math for success chance
        base = emp.motivation + (emp.level * 5) - (self.diff * 8)
        rng = random.randint(-10, 10)
        return max(5, min(95, base + rng))

    def resolve(self, emp, success, win_msg, lose_msg):
        print(f"\nDoing: {self.name} (Diff: {self.diff})...")
        time.sleep(0.8)  # suspense

        emp.motivation -= self.mot_cost

        if success:
            print(f"OK: {win_msg}")
            emp.add_xp(self.xp_gain)
            emp.stress += self.stress_add // 2
        else:
            print(f"FAIL: {lose_msg}")
            emp.stress += self.stress_add


# subclass implementations
class CodingTask(Task):
    def do_task(self, emp):
        chance = self.calc_odds(emp)

        if isinstance(emp, Developer):
            chance += 30
        elif isinstance(emp, Intern):
            chance -= 10
        elif isinstance(emp, Manager):
            if random.random() < 0.02:
                print("BRUH. Manager deleted the repo.")
                emp.stress += 50
                return
            chance -= 20

        success = random.randint(0, 100) < chance
        self.resolve(emp, success, "It compiled!", "Syntax error on line 1.")


class MeetingTask(Task):
    def do_task(self, emp):
        chance = self.calc_odds(emp)

        if isinstance(emp, Manager):
            chance += 40
            self.xp_gain += 10
        elif isinstance(emp, Developer):
            emp.motivation -= 30
            chance -= 10
        elif isinstance(emp, HR):
            chance += 50
        elif isinstance(emp, Intern):
            print("Intern fell asleep lol")
            emp.motivation += 10
            return

        success = random.randint(0, 100) < chance
        self.resolve(emp, success, "Good meeting.", "Could have been an email.")


class HRTask(Task):
    def do_task(self, emp):
        chance = self.calc_odds(emp)
        if isinstance(emp, HR):
            chance = 90
            emp.stress -= 20
        else:
            chance -= 30

        success = random.randint(0, 100) < chance
        self.resolve(emp, success, "Peace restored.", "HR complaint filed against u.")


class SupportTicketTask(Task):
    def do_task(self, emp):
        chance = self.calc_odds(emp)
        if isinstance(emp, Intern):
            print("Intern is panicking!")
            emp.stress += 10
            chance -= 20
        elif isinstance(emp, Manager):
            print("Delegated it.")
            chance += 10
        elif isinstance(emp, HR):
            print("HR: 'Have you tried restarting?'")
            chance = 50

        success = random.randint(0, 100) < chance
        self.resolve(emp, success, "Ticket closed.", "User wants ur manager.")


class DocumentationTask(Task):
    def do_task(self, emp):
        chance = self.calc_odds(emp)
        emp.motivation -= 10
        if isinstance(emp, Developer) and emp.level > 2:
            chance += 20

        success = random.randint(0, 100) < chance
        self.resolve(emp, success, "Wiki updated.", "Nobody understands what u wrote.")


class CreativeTask(Task):
    def do_task(self, emp):
        chance = self.calc_odds(emp)
        if isinstance(emp, Intern):
            chance += 25
        elif isinstance(emp, Manager):
            chance -= 10

        success = random.randint(0, 100) < chance
        self.resolve(emp, success, "Client loves it.", "Looks ugly.")


# ==========================================
# ITEMS
# ==========================================
class Item:
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def apply(self, emp):
        pass  # override this

    # operator overloading requirement
    def __add__(self, other):
        if isinstance(other, Item):
            new_name = f"Bundle ({self.name} + {other.name})"
            return Coffee(new_name, self.val + other.val)
        return None

    def __str__(self):
        return f"{self.name} (+{self.val})"


class Coffee(Item):
    def __init__(self, name="Espresso", val=20):
        super().__init__(name, val)

    def apply(self, emp):
        print(f"\nDrinking {self.name}...")
        emp.motivation += self.val
        emp.stress -= self.val // 2
        if emp.motivation > 120:
            print("Too much caffeine -> crash imminent")
            emp.stress += 15


# ==========================================
# MAIN
# ==========================================
def get_random_task():
    types = [
        CodingTask,
        MeetingTask,
        HRTask,
        SupportTicketTask,
        DocumentationTask,
        CreativeTask,
    ]
    t = random.choice(types)
    return t(f"Task_{random.randint(100,999)}", random.randint(1, 8))


def main():
    SystemAdmin.cls()
    print("--- OFFICE RPG SIMULATOR ---")

    p = None

    while True:
        print("\n1. New Game\n2. Load\n3. Quit")
        c = input("> ")

        if c == "1":
            n = input("Name: ")
            print("1.Intern 2.Dev 3.Manager 4.HR")
            r = input("Role: ")
            if r == "1":
                p = Intern(n)
            elif r == "2":
                p = Developer(n)
            elif r == "3":
                p = Manager(n)
            elif r == "4":
                p = HR(n)
            else:
                p = Intern(n)
            p.inventory.append(Coffee("Instant Coffee", 10))
            break
        elif c == "2":
            d = SystemAdmin.load_game()
            if d:
                role = d["role"]
                if role == "Intern":
                    p = Intern(d["name"])
                elif role == "Developer":
                    p = Developer(d["name"])
                elif role == "Manager":
                    p = Manager(d["name"])
                elif role == "HR":
                    p = HR(d["name"])
                else:
                    p = Employee(d["name"])
                p.stress = d["stress"]
                p.motivation = d["motivation"]
                p._xp = d["xp"]
                p._level = d["level"]
                print("loaded save.")
                break
        elif c == "3":
            sys.exit()

    # game loop
    while True:
        print("\n" + "=" * 20)
        print(p.get_status())
        print("=" * 20)

        if p.stress >= 100:
            print("\nBURNOUT. Game Over.")
            break

        print("\n1. Work\n2. Break\n3. Items\n4. Save/Quit")
        act = input(">> ")

        if act == "1":
            t = get_random_task()
            if p.motivation < t.mot_cost:
                print("Too tired to work.")
                continue
            t.do_task(p)

        elif act == "2":
            p.take_break()

        elif act == "3":
            if not p.inventory:
                print("No items.")
            else:
                for i, x in enumerate(p.inventory):
                    print(f"{i+1}. {x}")
                print("Type 'C' to combine top 2 items")
                ch = input("Choice: ").upper()
                if ch.isdigit():
                    idx = int(ch) - 1
                    if 0 <= idx < len(p.inventory):
                        p.use_item(p.inventory[idx])
                elif ch == "C" and len(p.inventory) >= 2:
                    i1 = p.inventory.pop(0)
                    i2 = p.inventory.pop(0)
                    p.inventory.append(i1 + i2)
                    print("Crafted bundle!")

        elif act == "4":
            SystemAdmin.save_game(p)
            break


if __name__ == "__main__":
    main()
