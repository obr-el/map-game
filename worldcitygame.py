import citygame


class WorldGame(citygame.CityGame):
    city_list = [
        "WASHINGTON DC US"
    ]
    population = {  # in thousands
        "WASHINGTON DC US": 690
    }
    latitude = {  # north of eq > 0 > south of eq
        "WASHINGTON DC US": 38.54
    }
    longitude = {  # west of prime meridian > 0 > east of prime meridian
        "WASHINGTON DC US": 77.00
    }

    def __init__(self):
        super().__init__()
        self.attempt = 0
        self.guess_left = 5
        self.wrongGuess = []
        self.min_val = {"pop": 8, "lat": 30.16, "long": 69.46}
        self.max_val = {"pop": 1597, "lat": 58.30, "long": 157.51}
        self.pop = ["-", "<", ">", "pop"]
        self.long = ["-", ">", "<", "long"]
        self.lat = ["-", "v", "^", "lat"]
        # hint_commands = ["POP", "LAT", "LONG", "EXIT"]
        self.hint_list = self.city_list
        # city_list = [state_cities,world_cities]

