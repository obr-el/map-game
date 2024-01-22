"""
Ellen's City Guesser
"""


def verify(user_input, answer_list):
    """
    Check to see if the guess is a valid answer
    :param user_input: the user's input
    :param answer_list: the list of possible answers
    :return: True if the guess is in the list, False if not
    """
    in_list = False
    for possible in answer_list:
        in_list = (user_input == possible)
        if in_list:
            break
    return in_list


def in_range(lower, upper, value):
    is_in_range = False
    if upper >= value >= lower:
        is_in_range = True
    return is_in_range

# sort the list by dictionary key ref alphabetically

def convert(number, is_long):
    """
    Convert long/lat into degrees and minutes
    :param number:
    :return:
    """
    direction = "N"
    if is_long:
        if number < 0:
            direction = "E"
            number = number * (-1)
        else:
            direction = "W"
    else:
        if number < 0: direction = "S"
    number = int(number * 100)
    minutes = number % 100
    degrees = int((number - minutes) / 100)
    converted = str(degrees) + "°" + str(minutes) + "' " + direction
    return converted


class CityGame:
    """
    :type city_list (List[str])
    """
    attempt = 0
    guess_left = 10
    wrongGuess = []
    min_val = {"pop": 8, "lat": 30.16, "long": 69.46}
    max_val = {"pop": 1597, "lat": 58.30, "long": 157.51}
    # symbols to be used to show the relation of a guess's values to the answer's
    pop = ["-", "<", ">", "pop"]
    long = ["-", ">", "<", "long"]
    lat = ["-", "v", "^", "lat"]
    hint_commands = ["POP", "LAT", "LONG", "EXIT"]
    city_list = []
    hint_list = []
    population = {}
    latitude = {}
    longitude = {}
    city = ""

    def __init__(self):
        pass

    def get_answer(self):
        return self.city

    def get_list(self):
        return self.city_list

    def playgame(self, in_guess):
        """
        Take a guess and check it against the city's attributes
        :return: N/A
        """
        guess = in_guess
        if guess is None:
            return "No guess input. Try again."
        else:
            self.attempt = self.attempt + 1
            self.guess_left = self.guess_left - 1
            # compare the population of the user's guess to the actual city
            pop_check = self.check(self,guess, self.population, self.pop)
            popcompare = ("\n... Population: " + pop_check)
            # compare the latitude of the user's guess to the actual city
            lat_check = self.check(self,guess, self.latitude, self.lat)
            latcompare = ("\n... Latitude: " + lat_check)
            # compare the longitude of the user's guess to the actual city
            long_check = self.check(self,guess, self.longitude, self.long)
            longcompare = ("\n... Longitude: " + long_check)
            # guess matches the answer
            returnstring = guess + popcompare + latcompare + longcompare
            if long_check != '-' or lat_check != '-' or pop_check != '-':
                if self.attempt > 0:
                    if self.attempt % 5 == 0:
                        self.wrongGuess.append("\n     ")
                    else:
                        self.wrongGuess.append(", ")
                self.wrongGuess.append(guess)
            return returnstring

    def instruct(self):
        return ("Select your guess from the list or search a city to find it faster."
                + "\nTo change the order of the cities, select a sorting method from the drop-down menu."
                + "\nDouble click a listed city for information about it."
                + "\n'<' means the correct city is LESS populated than your guess"
                + "\n'>' means the correct city is MORE populated than your guess"
                + "\n'>', '<', 'v', and '^' show which cardinal direction the correct city is from your guess."
                + "\nClick QUIT to end the game early."
                + "\nClick RULES to see these instructions again. Click HINT for a hint.")

    def info(self,instr):
        """
        :param: instr :type: String
        Give the user information about the selected city
        :return: (String)
        """
        info_text = ""
        is_long = True  # keep track of if the coordinate data is for longitude or latitude
        city = instr
        info_text = info_text + city
        out_pop = str(self.population[city] * 1000)
        # Population data
        info_text = info_text + "\n Population of " + city + " is " + out_pop  # concat population data to info_text
        # Coordinate data
        # latitude
        out_lat = convert(self.latitude[city], not is_long)  # convert latitude to degrees minutes format
        info_text = info_text + "\n Latitude of " + city + " is " + out_lat  # concat converted lati data to info_text
        # longitude
        out_long = convert(self.longitude[city], is_long)  # convert longitude to degrees minutes format
        info_text = info_text + "\n Longitude of " + city + " is " + out_long  # concat converted longi data to info_text
        return info_text

    def hint(self):
        """
        Print useful hints
        :return: (String)
        """
        is_long = True
        hint_string = ""
        hint_string = hint_string + ("Population is between " + str(self.min_val["pop"] * 1000) +
                                     " and " + str(self.max_val["pop"] * 100))
        hint_string = hint_string + ("\nLatitude is between " + convert(self.min_val["lat"], not is_long) + " and "
                                     + convert(self.max_val["lat"], not is_long))
        hint_string = hint_string + ("\nLongitude is between " + convert(self.min_val["long"], is_long) + " and "
                                     + convert(self.max_val["long"], is_long))
        hint_string = hint_string + "\nUsable cities: "
        self.update_hint_list(self)  # the hint list currently has all entries in the full possible answer list
        for guessed in self.wrongGuess:
            for answer in self.hint_list:
                if guessed == answer:  # if a previous guess is found...
                    self.hint_list.remove(answer)  # remove it from the list of hints
        for x in self.hint_list:
            if self.hint_list.index(x) > 0:
                if self.hint_list.index(x) % 5 == 0:  # add a line break every fifth entry
                    hint_string = hint_string + "\n  "
                else:  # separate entries with commas
                    hint_string = hint_string + ", "
            hint_string = hint_string + x
        return hint_string

    def update_hint_list(self):
        """
        Generate a list of all possible answers based on info from previous incorrect guesses
        :return:
        """
        temp = []
        for x in self.hint_list:
            pop_valid = in_range(self.min_val["pop"], self.max_val["pop"], self.population[x])
            lat_valid = in_range(self.min_val["lat"], self.max_val["lat"], self.latitude[x])
            long_valid = in_range(self.min_val["long"], self.max_val["long"], self.longitude[x])
            if pop_valid and lat_valid and long_valid:
                temp.append(x)
        self.hint_list = temp

    def check(self, guess, dictionary, field):
        """
        Compare the numerical value of two entries in the same dictionary
        :param field: list) population, longitude, or latitude
        :param dictionary: dict) the name of the dictionary being accessed
        :param guess: String) the user's input
        :return: Array with if
        """
        maximum = self.max_val[field[3]]
        minimum = self.min_val[field[3]]
        compare = dictionary[guess]  # the city to be compared
        check_is = None
        returnsign = ""
        if compare == dictionary[self.city]:  # same as answer
            returnsign = field[0]
            check_is = True
        elif compare > dictionary[self.city]:  # value needs to be decreased
            returnsign = field[1]
            if compare < maximum:
                maximum = compare
                self.max_val[field[3]] = compare
            check_is = False
        elif compare < dictionary[self.city]:  # value needs to be increased
            returnsign = field[2]
            if compare > minimum:
                minimum = compare
                self.min_val[field[3]] = compare
            check_is = False
        # print("Minimum " + field[3] + " " + str(minimum))
        # print("Maximum " + field[3] + " " + str(maximum))
        return returnsign
