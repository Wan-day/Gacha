import numpy as np # help me
# The class "Gacha" is the main game class where all the game functions are implemented.
class Gacha: # The game class, everything works form here
    def __init__(self):
        self.rates = None
        self.title = None
        self.server = None
        self.banner = None
        self.counter = 0
        
    def info(self): # Outputs info about the game
        print("{}%, {}%, {}%, {}, {}".format(self.rates[0],self.rates[1],self.rates[2],self.title, self.server))
        
    def test(self): # Tests whether the game is playable or not
        info_var = "Playable" if (self.rates[0] > 1) else "Unplayable"
        print(info_var)
        
    def pull(self): # Makes a pull of your choosing
        choice = int(input("How many pull do you wanna make? "))
        index = 0
        roll_ten = np.random.default_rng()
        pull_ten = roll_ten.random(choice)
        pull_ten = pull_ten.tolist()
        while index < choice:
            pull_ten.append(pull_ten[0] * 100)
            pull_ten.pop(0)
            index += 1
        pull_num = 0
        choice = choice - 1
        while not(choice < 0):
            if (pull_ten[choice] > self.rates[1]):
                outcome = "No luck for you today"
            elif (pull_ten[choice] > self.rates[0] and pull_ten[choice] <= self.rates[1]):
                outcome = "You got a decent unit"
            elif (pull_ten[choice] <= self.rates[0]):
                outcome = "You got lucky"
            pull_num += 1
            print("{}: {}".format(pull_num, outcome))
            choice = int(choice) - 1
            
Gacha_ak = Gacha()
Gacha_ak.rates = [2, 5, 93]
Gacha_ak.title = "Arknights"
Gacha_ak.server = "Global"
Gacha_Genshit = Gacha()
Gacha_Genshit.rates = [0.3, 10, 89.7]
Gacha_Genshit.title = "Genshin Impact"
Gacha_Genshit.server = "Global"
Gacha_ak.pull()