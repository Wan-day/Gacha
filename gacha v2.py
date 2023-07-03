import random
import sqlite3
import itertools

class Gacha:
    def __init__(self, weights, characters, db_out, roll_amount, counter, query, result, rarity, banner_rates):
        self.weights = weights
        self.characters = characters
        self.db_out = db_out
        self.roll_amount = roll_amount
        self.counter = counter
        self.query = query
        self.result = result
        self.rarity = rarity
        self.banner_rates = banner_rates

    def roll(roll_amount):
        # Connecting to a database and creating a cursor
        conn = sqlite3.connect('gachav1.db')
        cursor = conn.cursor()
        
        # Passing a query into the database that gives back character names and their respective weight
        query = """
                SELECT characters.Char_name AS "Character Name", rarity.Weight AS "Chance", characters.Char_rarity As "Rarity"
                FROM characters 
                INNER JOIN rarity ON characters.Char_rarity=rarity.Rarity
                """
        cursor.execute(query)
        db_out = cursor.fetchall()
        
        # Interpreting data from a dictionary to 2 lists and a dictionary
        characters_and_rarity = {}
        weights = []
        characters = []
        for row in db_out:
            characters.append(row[0])
            characters_and_rarity.update({row[0]: row[2]})
            weights.append(row[1])\
            
        # Making a weighted choice with 2 lists made from database and printing the result
        result = random.choices(characters, weights, k=roll_amount)
        for i in range(roll_amount):
            print(f"{i+1}. {result[i]} - {characters_and_rarity.get(result[i])}*")
            
        # Closing the cursor and closing the database
        cursor.close()
        conn.close()



    def banner_roll():
    
        # Connecting to a database and creating a cursor
        conn = sqlite3.connect('gachav1.db')
        cursor = conn.cursor()

        # Making a query that returns banner values: character name and their roll chance
        query = '''
                SELECT characters.Char_name, banner_standard.Banner_weight_6 AS Banner_Weight
                FROM characters
                INNER JOIN banner_standard ON characters.Char_name = banner_standard.Banner_main_6_name
                UNION
                SELECT characters.Char_name, banner_standard.Banner_weight_6
                FROM characters
                INNER JOIN banner_standard ON characters.Char_name = banner_standard.Banner_second_6_name
                UNION
                SELECT characters.Char_name, banner_standard.Banner_weight_5
                FROM characters
                INNER JOIN banner_standard ON characters.Char_name = banner_standard.Banner_main_5_name
                UNION
                SELECT characters.Char_name, banner_standard.Banner_weight_5
                FROM characters
                INNER JOIN banner_standard ON characters.Char_name = banner_standard.Banner_second_5_name
                UNION
                SELECT characters.Char_name, banner_standard.Banner_weight_5
                FROM characters
                INNER JOIN banner_standard ON characters.Char_name = banner_standard.Banner_third_5_name
                '''
        cursor.execute(query)
        
        # Breaking the output from the query into 2 lists: characters and rates
        banner_output = {}
        for row in cursor:
            banner_output.update({row[0] : row[1]})
        banner_characters = list(banner_output.keys())
        banner_rates = list(banner_output.values())
        
        # Making a query that returns amount of 5* and 6* units that are rate up on the banner
        query = "SELECT Banner_count_6, Banner_count_5 FROM banner_standard"
        cursor.execute(query)
        char_amount_minus = []
        
        # Returning the output from the query as a list with 2 values
        for row in cursor:
            for i in range(2):
                char_amount_minus.append(row[i])
        
        # Making a query that returns sum of all characters and full weight of a character on a banner
        query = '''
                SELECT COUNT(Char_name), rarity.Weight_full
                FROM characters
                INNER JOIN rarity ON characters.Char_rarity = rarity.Rarity
                WHERE Char_rarity = 3
                UNION
                SELECT COUNT(Char_name), rarity.Weight_full
                FROM characters
                INNER JOIN rarity ON characters.Char_rarity = rarity.Rarity
                WHERE Char_rarity = 4
                UNION
                SELECT COUNT(Char_name), rarity.Weight_full
                FROM characters
                INNER JOIN rarity ON characters.Char_rarity = rarity.Rarity
                WHERE Char_rarity = 5
                UNION
                SELECT COUNT(Char_name), rarity.Weight_full
                FROM characters
                INNER JOIN rarity ON characters.Char_rarity = rarity.Rarity
                WHERE Char_rarity = 6
                ORDER BY rarity.Weight_full
                '''
        cursor.execute(query)
        
        # Returning the values from the query in 3 lists:
        # char_amount is amount of characters in a selected rarity
        # char_full_weights is a full weight of a rarity without banner adjustments
        # char_weight is a weight of rarity after banner adjustments
        char_amount = []
        char_full_weight = []
        char_weight = []
        
        # Splitting the Output into 2 lists
        for row in cursor:
            char_amount.append(row[0])
            char_full_weight.append(row[1])
        
        # Adjusting the amount of characters to the banner
        for i in range(2):
            char_amount[i] = char_amount[i] - char_amount_minus[i]
        
        # Adjusting the weight of a rarity 
        for i in range(len(char_amount)):
            char_weight.append((char_full_weight[i]*0.5)/char_amount[i])
        
        # Making a query that returns all character names and their respective rarity
        query = '''
                SELECT characters.Char_name AS "Character Name", characters.Char_rarity As "Rarity"
                FROM characters 
                INNER JOIN rarity ON characters.Char_rarity=rarity.Rarity
                '''
        cursor.execute(query)
        
        # Returning the output from the query as a dictionary
        characters = {}
        for row in cursor:
            characters.update({row[0]:row[1]})
        
        # Changing weight values for all characters according to the true weights 
        char_weight_true = list(characters.values())
        for i in range(len(char_weight_true)):
            if char_weight_true[i] == 6:
                char_weight_true[i] = char_weight[0]
            elif char_weight_true[i] == 5:
                char_weight_true[i] = char_weight[1]
            elif char_weight_true[i] == 4:
                char_weight_true[i] = char_weight[2]
            elif char_weight_true[i] == 3:
                char_weight_true[i] = char_weight[3]
            else:
                print("Somehow you got this and you should not be happy")
                return
        
        # Changing weight values for banner characters 
        character_list = list(characters.keys())
        for i in range(len(characters)):
            for eggs in range(len(banner_characters)):
                if character_list[i] == banner_characters[eggs]:
                    char_weight_true[i] = banner_rates[eggs]
                else:
                    pass
        
        # Setting the amount of roll you want to make and finally making the weighted choice using true weight values for all units
        roll_amount = 10
        result = random.choices(character_list, char_weight_true, k=roll_amount)
        
        # Printing results
        for i in range(roll_amount):
            print(f"{i+1}. {result[i]} - {characters.get(result[i])}*")
        
        # Closing the cursor and closing the database
        cursor.close()
        conn.close()



Gacha.banner_roll()