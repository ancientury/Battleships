import random
from battleships import Fleet, Submarine, Battleship, Cruiser, Destroyer

# Test Driven Development
# Arrange
# Act
# Assert

f = Fleet()


class TestFleet:

    def test_place_ship_at(self):
        ships = [Battleship(),  # 1 battleship
                 Cruiser(), Cruiser(),  # 2 cruisers
                 Destroyer(), Destroyer(), Destroyer(),  # 3 destroyers
                 Submarine(), Submarine(), Submarine(), Submarine()]  # 4 submarines

        for ship in ships:
            placed = False

            while not placed:
                r = random.randint(0, 9)
                c = random.randint(0, 9)
                h = random.random() < 0.5

                if ship.ok_to_place_ship_at(r, c, h, ship.length, f):
                    ship.place_ship_at(r, c, h, ship.length, f)
                    assert (r, c) in f.ships  # check if coordinates are present in the fleet
                    placed = True

        # verify length of ship objects as such 1x4 + 2x3 + 3x2 + 4x1 = 20
        assert len(f.ships) == 20

    def test_ok_to_place_ship_at(self):

        ships = [Battleship(), Cruiser(), Destroyer(), Submarine()]
        s = ships[random.randint(0, 3)]  # pick a random ship

        # loop through all coordinates and check for adjacent or matching ships
        for row in range(0, 10):
            for column in range(0, 10):
                ok = True

                # adjacent ship locations
                for r in range(max(0, row - 1), min(10, row + 2)):
                    for c in range(max(0, column - 1), min(10, column + 2)):
                        if (r, c) in f.ships:
                            ok = False
                assert s.ok_to_place_ship_at(row, column, random.random() < 0.5, 1, f) == ok

    def test_ship_type(self):

        types = {
            'battleship': 4,
            'cruiser': 3,
            'destroyer': 2,
            'submarine': 1
        }

        #  check if ship types are valid
        for ship in f.ships.values():
            assert ship.ship_type in types.keys()  # ship type
            assert ship.length == types.get(ship.ship_type)  # ship length

    def open_sea(self, fleet, row, column):  # open sea function
        if (row, column) in fleet.ships:
            return False  # matching ship location
        for r in range(max(0, row - 1), min(10, row + 2)):
            for c in range(max(0, column - 1), min(10, column + 2)):
                if (r, c) in fleet.ships:
                    return False  # matching adjacent ship location
        return True  # open sea

    def test_is_open_sea(self):

        #  check if location is a ship, adjacent ship or open sea
        for row in range(0, 10):
            for column in range(0, 10):
                assert self.open_sea(f, row, column) == f.is_open_sea(row, column)

    def test_check_if_hits(self):
        s = random.choice(list(f.ships.values()))  # select a random ship
        for location in s.locations:
            r, c = location
            assert location not in s.hits  # no hits registered
            f.check_if_hits(r, c)
            assert location in s.hits and location in f.hit_locations  # hit registered

            # check game status when a hit is registered
            assert f.game_status == "Target hit!" or f.game_status == ("A " + s.ship_type + " has been sunk!")

    def test_hit(self):

        skip = None
        s = random.choice(list(f.ships.values()))  # randomly select a ship from the fleet

        for i in range(0, 3):  # randomly select upto 3 different ships from the fleet
            while skip == s:
                s = random.choice(list(f.ships))

            for location in s.locations:
                r, c = location
                s.hit(r, c)  # hit all locations of the ship
                assert (r, c) in s.hits  # check if ship has been hit

            if s.hits == s.locations:
                f.sunk_ships += 1  # should be a total of 4 sunk ships

    def test_is_sunk(self):
        checked_ships = set()  # ship blacklist for checking once only

        for s in f.ships.values():
            hits = 0  # registered hits

            if s not in checked_ships:
                checked_ships.add(s)

                for location in s.locations:
                    for hit in s.hits:
                        if hit == location:  # check if hit and location match
                            hits += 1

                if hits == len(s.locations):  # all locations match therefore ship has sunk
                    assert s.is_sunk() == True
                else:
                    assert s.is_sunk() == False

    def test_are_unsunk_ships_left(self):
        sunk_ships = 0  # sunk ships
        checked_ships = set()  # ship blacklist for checking once only

        for s in f.ships.values():
            if s not in checked_ships:
                checked_ships.add(s)

                if len(s.hits) == s.length:  # all ship locations match hits therefore ship has sunk
                    sunk_ships += 1

        if f.sunk_ships < 10 and sunk_ships > 0:  # unsunk ships availability confirmed by checking the variables
            assert f.are_unsunk_ships_left() == True
        else:
            assert f.are_unsunk_ships_left() == False
