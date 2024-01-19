# City Guesser: state capital edition
import citygame


class StateGame(citygame.CityGame):
    city_list = [
        "MONTGOMERY AL", "JUNEAU AK", "LITTLE ROCK AR", "PHOENIX AZ"
        , "SACRAMENTO CA", "DENVER CO", "HARTFORD CT"
        , "WASHINGTON DC", "DOVER DE"
        , "TALLAHASSEE FL", "ATLANTA GA", "HONOLULU HI"
        , "INDIANAPOLIS IN", "BOISE ID", "SPRINGFIELD IL", "DES MOINES IA"
        , "TOPEKA KS", "FRANKFORT KY", "BATON ROUGE LA"
        , "BOSTON MA", "ANNAPOLIS MD", "AUGUSTA ME", "LANSING MI", "SAINT PAUL MN"
        , "JEFFERSON CITY MO", "JACKSON MS", "HELENA MT"
        , "LINCOLN NA", "RALEIGH NC", "BISMARCK ND", "CONCORD NH", "TRENTON NJ"
        , "SANTA FE NM", "CARSON CITY NV", "ALBANY NY"
        , "COLUMBUS OH", "OKLAHOMA CITY OK", "SALEM OR"
        , "HARRISBURG PA", "PROVIDENCE RI", "COLUMBIA SC", "PIERRE SD"
        , "AUSTIN TX", "NASHVILLE TN", "SALT LAKE CITY UT"
        , "RICHMOND VA", "MONTPELIER VT"
        , "OLYMPIA WA", "MADISON WI", "CHARLESTON WV", "CHEYENNE WY"]
    hint_list = city_list
    population = {  # in thousands
        "SANTA FE NM": 85, "ABQ NM": 565
        , "MONTGOMERY AL": 199, "JUNEAU AK": 32, "LITTLE ROCK AR": 206, "PHOENIX AZ": 1597
        , "SACRAMENTO CA": 516, "DENVER CO": 722, "HARTFORD CT": 116
        , "WASHINGTON DC": 690, "DOVER DE": 36
        , "TALLAHASSEE FL": 201, "ATLANTA GA": 503, "HONOLULU HI": 345
        , "INDIANAPOLIS IN": 893, "BOISE ID": 240, "SPRINGFIELD IL": 107, "DES MOINES IA": 213
        , "TOPEKA KS": 123, "FRANKFORT KY": 29, "BATON ROUGE LA": 223
        , "BOSTON MA": 617, "ANNAPOLIS MD": 46, "AUGUSTA ME": 19, "LANSING MI": 106, "SAINT PAUL MN": 312
        , "JEFFERSON CITY MO": 42, "JACKSON MS": 159, "HELENA MT": 32
        , "LINCOLN NA": 287, "RALEIGH NC": 474, "BISMARCK ND": 69, "CONCORD NH": 48
        , "TRENTON NJ": 96, "CARSON CITY NV": 54, "ALBANY NY": 103
        , "COLUMBUS OH": 910, "OKLAHOMA CITY OK": 666, "SALEM OR": 168
        , "HARRISBURG PA": 46, "PROVIDENCE RI": 203, "COLUMBIA SC": 142, "PIERRE SD": 14
        , "AUSTIN TX": 948, "NASHVILLE TN": 695, "SALT LAKE CITY UT": 204
        , "RICHMOND VA": 230, "MONTPELIER VT": 8
        , "OLYMPIA WA": 48, "MADISON WI": 262, "CHARLESTON WV": 41, "CHEYENNE WY": 57
    }
    latitude = {  # how far north
        "SANTA FE NM": 35.40, "ABQ NM": 35.06
        , "MONTGOMERY AL": 31.21, "JUNEAU AK": 58.30, "LITTLE ROCK AR": 34.44, "PHOENIX AZ": 33.26
        , "SACRAMENTO CA": 38.34, "DENVER CO": 39.74, "HARTFORD CT": 41.45
        , "WASHINGTON DC": 38.54, "DOVER DE": 39.09
        , "TALLAHASSEE FL": 30.27, "ATLANTA GA": 33.44, "HONOLULU HI": 21.18
        , "INDIANAPOLIS IN": 39.46, "BOISE ID": 43.36, "SPRINGFIELD IL": 39.47, "DES MOINES IA": 41.35
        , "TOPEKA KS": 39.03, "FRANKFORT KY": 38.12, "BATON ROUGE LA": 30.26
        , "BOSTON MA": 42.21, "ANNAPOLIS MD": 38.58, "AUGUSTA ME": 44.18, "LANSING MI": 42.44, "SAINT PAUL MN": 44.56
        , "JEFFERSON CITY MO": 38.34, "JACKSON MS": 32.17, "HELENA MT": 46.35
        , "LINCOLN NA": 40.48, "RALEIGH NC": 35.46, "BISMARCK ND": 46.48, "CONCORD NH": 43.12
        , "TRENTON NJ": 40.22, "CARSON CITY NV": 39.9, "ALBANY NY": 42.39
        , "COLUMBUS OH": 39.57, "OKLAHOMA CITY OK": 35.28, "SALEM OR": 44.56
        , "HARRISBURG PA": 46, "PROVIDENCE RI": 41.49, "COLUMBIA SC": 34.0, "PIERRE SD": 44.22
        , "AUSTIN TX": 30.16, "NASHVILLE TN": 36.09, "SALT LAKE CITY UT": 40.45
        , "RICHMOND VA": 37.32, "MONTPELIER VT": 44.15
        , "OLYMPIA WA": 47.2, "MADISON WI": 43.04, "CHARLESTON WV": 38.20, "CHEYENNE WY": 41.8
    }
    longitude = {  # how far west
        "SANTA FE NM": 105.57, "ABQ NM": 106.36
        , "MONTGOMERY AL": 86.16, "JUNEAU AK": 134.42, "LITTLE ROCK AR": 92.19, "PHOENIX AZ": 112.04
        , "SACRAMENTO CA": 121.29, "DENVER CO": 104.99, "HARTFORD CT": 72.40
        , "WASHINGTON DC": 77.00, "DOVER DE": 75.31
        , "TALLAHASSEE FL": 84.15, "ATLANTA GA": 84.23, "HONOLULU HI": 157.51
        , "INDIANAPOLIS IN": 86.09, "BOISE ID": 116.12, "SPRINGFIELD IL": 89.39, "DES MOINES IA": 93.37
        , "TOPEKA KS": 95.41, "FRANKFORT KY": 84.52, "BATON ROUGE LA": 91.10
        , "BOSTON MA": 71.03, "ANNAPOLIS MD": 76.30, "AUGUSTA ME": 69.46, "LANSING MI": 84.32, "SAINT PAUL MN": 93.5
        , "JEFFERSON CITY MO": 92.10, "JACKSON MS": 90.11, "HELENA MT": 112.1
        , "LINCOLN NA": 96.40, "RALEIGH NC": 78.38, "BISMARCK ND": 100.47, "CONCORD NH": 71.32
        , "TRENTON NJ": 74.76, "CARSON CITY NV": 119.46, "ALBANY NY": 73.45
        , "COLUMBUS OH": 83.0, "OKLAHOMA CITY OK": 97.31, "SALEM OR": 123.2
        , "HARRISBURG PA": 76.52, "PROVIDENCE RI": 71.25, "COLUMBIA SC": 81.2, "PIERRE SD": 100.19
        , "AUSTIN TX": 97.44, "NASHVILLE TN": 86.46, "SALT LAKE CITY UT": 111.53
        , "RICHMOND VA": 77.28, "MONTPELIER VT": 72.34
        , "OLYMPIA WA": 122.54, "MADISON WI": 89.23, "CHARLESTON WV": 81.38, "CHEYENNE WY": 104.49
    }

    def __init__(self):
        super().__init__()
        self.wrongGuess = []
        self.guess_left = 5
        self.min_val = {"pop": 8, "lat": 30.16, "long": 69.46}
        self.max_val = {"pop": 1597, "lat": 58.30, "long": 157.51}
        # hint_commands = ["POP", "LAT", "LONG", "EXIT"]
