# This sets up the board and works with game.py to adjust the coordinates for each step taken
# Author: Jessica Truong

class Board:
    def __init__(self):
        # j = 0 is to determine when an exception is applied
        j = 0
        # try and except to determine if the files are valid
        try:
            maps = "map.txt"
            filehandler_m = open(maps)
            filehandler_m.read()
        # j = 1 is used for the conditional at the bottom for when there is an error, then only empty map is produced
        except:
            print("File Error")
            j = 1
        try:
            players = "players.txt"
            filehandler_p = open(players)
            filehandler_p.read()
        except:
            print("File Error")
            j = 1
        try:
            exit = "exit.txt"
            filehandler_e = open(exit)
            filehandler_e.read()
        except:
            print("File Error")
            j = 1
        # lists for each element of the game
        self.map_draw = []
        self.door = []
        self.coordinates = []
        # when j == 0 then the rest of the code run, otherwise it prints am empty board to indicate an error
        if j == 0:
            maps = "map.txt"
            filehandler_m = open(maps)
            # Creating the map based on the map.txt file
            for line in filehandler_m:

                line = line.strip("\n")
                print(line)
                row = []
                for i in line:
                    if i == " " or i == "#":
                        row.append(i)
                    else:
                        row.append(" ")
                self.map_draw.append(row)

            players = "players.txt"
            filehandler_p = open(players)
            self.original_players = []

            # Compiling the players' coordinates based on the players.txt file
            for line in filehandler_p:
                line = line.strip()
                s = line
                x = s.split(" ")
                player = []
                for i in x:
                    j = int(i)
                    player.append(j)
                self.coordinates.append(player)
                self.original_players.append(player)
            # Adding the players  based on the coordinates
            for i in self.coordinates:
                list = i
                self.map_draw[list[0]][list[1]] = "P"

            # Adding the exit based on the coordinates from exit.txt
            exit = "exit.txt"
            filehandler_e = open(exit)
            for line in filehandler_e:
                line = line.strip()
                for i in line:
                    if i != " ":
                        j = int(i)
                        self.door.append(j)
            self.map_draw[self.door[0]][self.door[1]] = "E"

            # setting up the dead/alive/won numbers for the get state method
            self.number = len(self.original_players)
            self.dead = 0
            self.won = 0
            self.steps = 0
        # Used to create an empty map for when the files have an error
        else:
            for i in range(12):
                t = []
                for j in range(16):
                    t.append(" ")
                self.map_draw.append(t)

    def get_board(self):
        return self.map_draw

    def update(self, direction):
    #creating if statements for each direction, where the code within each statement is the same for all
        if direction == "U":
            #Adds one step each time
            self.steps += 1
            remove = []
            # Sorts the player so if they align with each other, then this does not cause any problems
            self.coordinates.sort()
            # Remapping the coordinates of the players
            for i in self.coordinates:
                spot = i
                j = spot[0] - 1
                num = self.coordinates.index(i)
                new_coordinates = []
                new_coordinates.append(j)
                new_coordinates.append(spot[1])
                # If statement for when it goes past the board (ie. the coordinate -1), then it stays at the same spot
                if j == -1:
                    self.map_draw[i[0]][i[1]] = "P"
                # elif the next move is a space then it will add the player
                elif self.map_draw[j][spot[1]] == " ":
                    self.coordinates.insert(num, new_coordinates)
                    self.coordinates.remove(i)
                    self.map_draw[i[0]][i[1]] = " "
                    self.map_draw[j][i[1]] = "P"
                # elif there is a player at the next position then it will stay in place
                elif self.map_draw[j][spot[1]] == "P":
                    self.map_draw[spot[0]][spot[1]] = "P"
                # elif there is a wall at the next position, then the player dies (removed) and self.dead += 1
                elif self.map_draw[j][spot[1]] == "#":
                    self.map_draw[spot[0]][spot[1]] = " "
                    remove.append(i)
                    self.dead += 1
                # elif the door is at the next position, then the player wins and self.won +=1
                elif new_coordinates == self.door:
                    self.map_draw[spot[0]][spot[1]] = " "
                    remove.append(i)
                    self.won = self.won + 1

            #removes the old coordinates of the players
            for i in remove:
                self.coordinates.remove(i)

        if direction == "D":
            remove = []
            self.coordinates.sort(reverse=True)

            for i in self.coordinates:
                num = self.coordinates.index(i)
                spot = i
                j = spot[0] + 1
                new_coordinates = []
                new_coordinates.append(j)
                new_coordinates.append(spot[1])
                # If statement for when it goes past the board (ie. the coordinate 12), then it stays at the same spot
                if j == 12:
                    self.map_draw[i[0]][i[1]] = "P"

                elif self.map_draw[j][spot[1]] == " ":
                    self.coordinates.insert(num, new_coordinates)
                    self.coordinates.remove(i)
                    self.map_draw[spot[0]][spot[1]] = " "
                    self.map_draw[j][spot[1]] = "P"

                elif self.map_draw[j][spot[1]] == "P":
                    self.map_draw[i[0]][i[1]] = "P"

                elif self.map_draw[j][spot[1]] == "#":
                    self.map_draw[spot[0]][spot[1]] = " "
                    self.dead = self.dead + 1
                    remove.append(i)

                elif new_coordinates == self.door:
                    self.map_draw[spot[0]][spot[1]] = " "
                    remove.append(i)
                    self.won = self.won + 1

            self.steps += 1
            for i in remove:
                self.coordinates.remove(i)

        if direction == "L":
            remove = []
            #sorting in ascending order based on the second element, learned this from https://www.freecodecamp.org/news/lambda-sort-list-in-python/#howtosortalistinpython
            self.coordinates.sort(key=lambda list: list[1])
            for i in self.coordinates:
                num = self.coordinates.index(i)
                spot = i
                j = spot[1] - 1
                new_coordinates = []
                new_coordinates.append(spot[0])
                new_coordinates.append(j)
                # If statement for when it goes past the board (ie. the coordinate -1), then it stays at the same spot
                if j == -1:
                    self.map_draw[i[0]][i[1]] = "P"

                elif self.map_draw[i[0]][j] == " ":
                    self.coordinates.insert(num, new_coordinates)
                    self.coordinates.remove(i)
                    self.map_draw[spot[0]][spot[1]] = " "
                    self.map_draw[spot[0]][j] = "P"

                elif self.map_draw[i[0]][j] == "P":
                    self.map_draw[spot[0]][spot[1]] = "P"

                elif self.map_draw[i[0]][j] == "#":
                    self.map_draw[spot[0]][spot[1]] = " "
                    self.dead = self.dead + 1
                    remove.append(i)

                elif new_coordinates == self.door:
                    self.map_draw[spot[0]][spot[1]] = " "
                    remove.append(i)
                    self.won = self.won + 1
            self.steps += 1
            for i in remove:
                self.coordinates.remove(i)

        if direction == "R":
            remove = []
            #sorting in descending order based on the second element, learned this from https://www.freecodecamp.org/news/lambda-sort-list-in-python/#howtosortalistinpython
            self.coordinates.sort(key=lambda list: list[1], reverse=True)
            for i in self.coordinates:
                num = self.coordinates.index(i)
                spot = i
                j = spot[1] + 1
                new_coordinates = []
                new_coordinates.append(spot[0])
                new_coordinates.append(j)
                # If statement for when it goes past the board, then it stays at the same spot
                if j == 16:
                    self.map_draw[i[0]][i[1]] = "P"

                elif self.map_draw[spot[0]][j] == " ":
                    self.coordinates.insert(num, new_coordinates)
                    self.coordinates.remove(i)
                    self.map_draw[spot[0]][spot[1]] = " "
                    self.map_draw[spot[0]][j] = "P"

                elif self.map_draw[i[0]][j] == "P":
                    self.map_draw[spot[0]][spot[1]] = "P"

                elif self.map_draw[i[0]][j] == "#":
                    self.map_draw[spot[0]][spot[1]] = " "
                    self.dead = self.dead + 1
                    remove.append(i)

                elif new_coordinates == self.door:
                    self.map_draw[spot[0]][spot[1]] = " "
                    remove.append(i)
                    self.won = self.won + 1
            self.steps += 1
            for i in remove:
                self.coordinates.remove(i)

    def get_state(self):
        # if statement to see if there are any players left, if they have won or not based on the total amount of
        # players that won and the ones that did not or died compared to the original amount of players
        if self.won == self.number:
            self.steps = 0
            return 1
        elif self.dead == self.number:
            self.steps = 0
            return 2
        elif (self.dead + self.won) == self.number:
            self.steps = 0
            return 3
        else:
            return 0

    def save_game(self):
        j = 0
        # Creates a new file, clearing the previous stuff on this file and using try and except to catch errors
        try:
            gamefile = open("Game.txt", "w")
            playercoordinates = open("members.txt", "w")
            exitcoordinates = open("door.txt", "w")
            steps = open("steps.txt", "w")
        except:
            print("File Error")
            # if there is an error, j = 1, then it wont execute the rest of the code
            j = 1
        # if statement for if there was an exception error, if there was then an empty map will be shown
        if j == 0:
            # writes the current map into the file
            for i in self.map_draw:
                for j in i:
                    if j == "#" or j == " ":
                        gamefile.write(j)
                    else:
                        gamefile.write(" ")
                gamefile.write("\n")
            # closes the file to ensure it was saved
            gamefile.close()

            # Creates a new file for members' coordinates
            for i in self.coordinates:
                for j in i:
                    j = str(j)
                    playercoordinates.write(j + " ")
                playercoordinates.write("\n")
            playercoordinates.close()

            # used a new file for the exit coordinates
            for i in self.door:
                i = str(i)
                exitcoordinates.write(i +" ")
            exitcoordinates.close()

            # used a new file called steps for the steps taken so far and the amount of robots dead and won as well as the original number of players
            step = str(self.steps)
            live = str(self.won)
            dead = str(self.dead)
            o = str(self.number)
            # separated the different data by starting on another line
            steps.write(step+"\n")
            steps.write(live+"\n")
            steps.write(dead+"\n")
            steps.write(o+"\n")
            steps.close()

        else:
            for i in range(12):
                l = []
                for j in range(16):
                    l.append(" ")
                self.map_draw.append(l)

    def load_game(self):
        #used for if conditional in case there is any file error, then it will show a blank screen
        t = 0
        # clearing all previous data for these lists
        self.map_draw = []
        self.door = []
        self.coordinates = []
        self.steps = 0
        # try and except for each file in case it was moved to a different directory or deleted
        try:
            filehandler_m = open("Game.txt")
        except:
            print("File Error")
            t = 1
        try:
            players = "members.txt"
            filehandler_p = open(players)
        except:
            print("File Error")
            t = 1
        try:
            exit = "door.txt"
            filehandler_e = open(exit)

        except:
            print("File Error")
            t = 1

        try:
            stage = "steps.txt"
            filehandler_s = open(stage)
        except:
            print("File Error")
            t = 1

        # if statement to creates the saved map otherwise, if there was an error indicated by the value of t, then empty map shows
        if t == 0:
            for line in filehandler_m:
                line = line.strip("\n")
                row = []
                for i in line:
                    if i == " " or i == "#":
                        row.append(i)
                    else:
                        row.append(" ")
                self.map_draw.append(row)
        else:
            for i in range(12):
                l = []
                for j in range(16):
                    l.append(" ")
                self.map_draw.append(l)
        # adds the saved players based on saved coordinates if no exception error occured
        if t == 0:
            for line in filehandler_p:
                line = line.strip()
                player = []
                s = line
                x = s.split(" ")
                for i in x:
                    j = int(i)
                    player.append(j)
                self.coordinates.append(player)
                self.original_players.append(player)

            for i in self.coordinates:
                list = i
                self.map_draw[list[0]][list[1]] = "P"
        # adds the saved door if no exception error occured
        if t == 0:
            for line in filehandler_e:
                line = line.strip()
                for i in line:
                    if i != " ":
                        j = int(i)
                        self.door.append(j)

            self.map_draw[self.door[0]][self.door[1]] = "E"
        # updates variables (steps, won, dead, original number) based on the saved data
        if t == 0:
            self.steps = int(filehandler_s.readline())
            self.won = int(filehandler_s.readline())
            self.dead = int(filehandler_s.readline())
            self.number = int(filehandler_s.readline())
    #indicates the number of steps taken
    def get_steps(self):
        return self.steps
