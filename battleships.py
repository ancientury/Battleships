import random
import sys


class Fleet:  # main class for fleet
    def __init__(self):
        self.ships = dict()  # location of ships
        if "pytest" not in sys.modules:  # only place ships in a non-testing environment
            self.randomly_place_all_ships()  # place all ships randomly in the sea
        self.sunk_ships = 0  # number of sunken ships
        self.shots = 0  # total number of shots
        self.hit_locations = set()  # location of hits initiated
        self.game_status = "CLICK ON A POINT TO SHOOT!"
        self.game_over = False

    def is_open_sea(self, row, column):  # check if its a ship, an adjacent ship or open sea
        for location in self.ships:  # loop through ship coordinates
            # check if given parameters are exact or adjacent to an existing ship
            if abs(row - location[0]) <= 1 and abs(column - location[1]) <= 1:
                return False  # return false if not open sea
        return True  # otherwise return true for open sea

    def randomly_place_all_ships(self):
        # initialise a list of ships to be placed in the fleet
        ships = [Battleship(),  # 1 battleship
                 Cruiser(), Cruiser(),  # 2 cruisers
                 Destroyer(), Destroyer(), Destroyer(),  # 3 destroyers
                 Submarine(), Submarine(), Submarine(), Submarine()]  # 4 submarines

        for ship in ships:  # attempt to place each ship
            placed = False  # flag to check whether ship has been placed successfully
            while not placed:  # attempt to place the ship using random coordinates
                row = random.randint(0, 9)  # random row
                column = random.randint(0, 9)  # random column
                horizontal = random.random() < 0.5  # random orientation
                if ship.ok_to_place_ship_at(row, column, horizontal, ship.length, self):  # check for legal coordinates
                    ship.place_ship_at(row, column, horizontal, ship.length, self)  # place the ship
                    placed = True

    def check_if_hits(self, row, column):
        shot_already = (row, column) in self.hit_locations  # check whether shot has been registered previously
        self.hit_locations.add((row, column))  # register the shot

        if (row, column) in self.ships:  # check if coordinates match any existing ship coordinates
            self.game_status = "Target hit!"
            ship = self.ships[(row, column)]
            ship.hit(row, column)  # add the shot to the ship

            # check if all locations are hit and shot hasn't been registered previously
            if ship.is_sunk() and not shot_already:
                self.sunk_ships += 1
                if self.are_unsunk_ships_left():
                    self.game_status = "A " + ship.ship_type + " has been sunk!"
                else:
                    self.game_over = True
                    self.game_status = "Game over!"

            return True  # return true if ship has been hit or sunk
        else:
            self.game_status = "Target missed!"

        return False  # no ship has been hit or sunk

    def are_unsunk_ships_left(self):
        return self.sunk_ships < 10  # returns true if unsunk ships are left


class Ship:  # main class for ships
    def __init__(self):
        self.locations = set()  # locations of the ship
        self.hits = set()  # received hit locations

    def get_locations(self, row, column, horizontal, length):  # function to test and register ship locations
        if horizontal:
            if column + length - 1 > 9:  # limiting boundaries for horizontal ships
                return None
        else:
            if row + length - 1 > 9:  # limiting boundaries for vertical ships
                return None

        locations = set()
        for i in range(0, length):  # row or column + i to length
            if horizontal:
                locations.add((row, column + i))  # register ship locations horizontally
            else:
                locations.add((row + i, column))  # register ship locations vertically

        return locations  # return locations

    def ok_to_place_ship_at(self, row, column, horizontal, length, fleet):  # location is valid before placing ship
        locations = self.get_locations(row, column, horizontal, length)
        if locations is None:
            return False  # invalid location - exceeds boundaries
        for location in locations:
            if not fleet.is_open_sea(location[0], location[1]):
                return False  # invalid location - not open sea
        return True  # valid location

    def place_ship_at(self, row, column, horizontal, length, fleet):  # place ship in the specified fleet
        self.locations = self.get_locations(row, column, horizontal, length)
        if self.locations is not None:
            for location in self.locations:
                fleet.ships[location] = self  # place ship object in designated location within the fleet
        return fleet

    def hit(self, row, column):
        if (row, column) in self.locations:  # check if coordinates are valid in relation to locations
            if (row, column) not in self.hits:  # eliminate duplicate hits
                self.hits.add((row, column))  # register a hit
            return True  # hit registered or already registered
        else:
            return False  # hit coordinates don't match

    def ship_type(self):
        return self.ship_type  # returns ship type

    def is_sunk(self):
        return self.hits == self.locations  # returns true if all ship coordinates are hit


class Battleship(Ship):  # subclass inherited from ship class

    def __init__(self):
        self.ship_type = "battleship"
        self.length = 4
        self.hits = set()


class Cruiser(Ship):  # subclass inherited from ship class

    def __init__(self):
        self.ship_type = "cruiser"
        self.length = 3
        self.hits = set()


class Destroyer(Ship):  # subclass inherited from ship class

    def __init__(self):
        self.ship_type = "destroyer"
        self.length = 2
        self.hits = set()


class Submarine(Ship):  # subclass inherited from ship class

    def __init__(self):
        self.ship_type = "submarine"
        self.length = 1
        self.hits = set()
