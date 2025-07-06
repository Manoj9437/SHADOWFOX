# 8
class Avenger:
    def __init__(self, name, age, gender, power, weapon, is_leader=False):
        self.name = name
        self.age = age
        self.gender = gender
        self.power = power
        self.weapon = weapon
        self.is_leader_flag = is_leader
    def get_info(self):
        print("Name       :", self.name)
        print("Age        :", self.age)
        print("Gender     :", self.gender)
        print("Super Power:", self.power)
        print("Weapon     :", self.weapon)
    def is_leader(self):
        return self.is_leader_flag
team = [
    Avenger("Captain America", 100, "Male", "Super strength", "Shield", is_leader=True),
    Avenger("Iron Man", 48, "Male", "Technology", "Armor"),
    Avenger("Black Widow", 35, "Female", "Superhuman", "Batons"),
    Avenger("Hulk", 49, "Male", "Unlimited Strength", "No Weapon"),
    Avenger("Thor", 1500, "Male", "Super Energy", "Mjölnir"),
    Avenger("Hawkeye", 41, "Male", "Fighting skills", "Bow and Arrows")
]
for avenger in team:
    avenger.get_info()
    if avenger.is_leader():
        print(f"{avenger.name} is the leader of the Avengers.")
    else:
        print(f"{avenger.name} is not the leader.")
    print("-------------")