###
#
# File: Main.py
# Version 1.0.2
# Date 2022-07-09
# Copyright (c) 2021 Sindre Andre Ditlefsen
# License: http://opensource.org/licenses/gpl-license.php GNU Public License
#
###

import pygame
import random

from Blank import Blank
from Cat import Cat
from Dog import Dog
from Monkey import Monkey
from Panda import Panda
from Sheep import Sheep
from SheepZombie import SheepZombie


class Main:
    pygame.init()
    pygame.font.init()

    def __init__(self):

        # Initialize the game engine
        self.fontArialH1 = pygame.font.SysFont('Arial', 40)
        self.fontArial = pygame.font.SysFont('Arial', 30)

        # Define the colors we will use in RGB format
        self.colorYellow = (224, 196, 126)

        # Set the height and width of the screen
        screenSizeX = int(1080)
        screenSizeY = int(720)
        size = [screenSizeX, screenSizeY]  # list
        self.screen = pygame.display.set_mode(size)

        # Title
        pygame.display.set_caption("Cat Attack!")

        # Loop until the user clicks the close button.
        self.done = False
        self.clock = pygame.time.Clock()

        # Create board
        self.bg = pygame.image.load("images/netherlands.jpg")

        # Game variables
        self.gameActivePieceName = "";
        self.gameWinner = "" # to print on the screen

        # Whos turn it is?
        randomNumber = random.randint(0, 2)
        if(randomNumber > 1):
            self.gameWhosTurn = "red"
        else:
            self.gameWhosTurn = "blue"
        self.changePlayersTurn() # switch it (for sound)


        # Game Board
        self.gameboard = {} # creates array that holds game
        self.cageBoardRed =  ["blank", "blank", "blank", "blank"]
        self.cageBoardBlue = ["blank", "blank", "blank", "blank"]
        self.placePieces() # call method

        # Texts
        self.statusText = "Game on!"

        # Start game
        self.main()

    #- Places pieces in array --------------------------------------------------------------------------------------- #
    def placePieces(self):

        # Blue
        self.gameboard[0, 0] = Monkey("blue", "monkey", "monkey_blue_128", 1, "a1");
        self.gameboard[0, 1] = Cat("blue", "cat", "cat_blue_128", 1, "b1");
        self.gameboard[0, 2] = Dog("blue", "dog", "dog_blue_128", 1, "c1");

        self.gameboard[1, 0] = Blank("blank", "blank", "blank", 0, "a2");
        self.gameboard[1, 1] = Sheep("blue", "sheep", "sheep_blue_128", 1, "b2");
        self.gameboard[1, 2] = Blank("blank", "blank", "blank", 0, "c2");

        # Red
        self.gameboard[2, 0] = Blank("blank", "blank", "blank", 0, "a3");
        self.gameboard[2, 1] = Sheep("red", "sheep", "sheep_red_128", -1, "b3")
        self.gameboard[2, 2] = Blank("blank", "blank", "blank", 0, "c3");

        self.gameboard[3, 0] = Dog("red", "dog", "dog_red_128", -1, "a4")
        self.gameboard[3, 1] = Cat("red", "cat", "cat_red_128", -1, "b4")
        self.gameboard[3, 2] = Monkey("red", "monkey", "monkey_red_128", -1, "c4");

    #- The game it self --------------------------------------------------------------------------------------------- #
    def main(self):

        while not self.done:
            # This limits the while loop to a max of 10 times per second.
            # Leave this out and we will use all CPU we can.
            self.clock.tick(5)

            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop

                if event.type == pygame.MOUSEBUTTONUP:
                    clickPositionPixelX, clickPositionPixelY = event.pos

                    clickedOnPositionBoard = self.clickPositionPixelToPositionBoard(clickPositionPixelX,
                                                                                    clickPositionPixelY)

                    # Check that Y is not out of range
                    y = clickedOnPositionBoard[0]
                    if(self.gameWinner == "" and y != "Z"):
                        self.selectOrMovePiece(clickedOnPositionBoard)

                    break



            # Clear the screen and set the screen background
            self.screen.fill((255, 255, 255))

            # INSIDE OF THE GAME LOOP
            self.screen.blit(self.bg, (0, 0))

            # Draw Board Xstart Ystart, Xstop, Ystop (diff is always 150 px)
            pygame.draw.rect(self.screen, self.colorYellow, [250, 200, 150, 150], 2)  # A1
            pygame.draw.rect(self.screen, self.colorYellow, [250, 350, 150, 150], 2)  # B1
            pygame.draw.rect(self.screen, self.colorYellow, [250, 500, 150, 150], 2)  # C1

            pygame.draw.rect(self.screen, self.colorYellow, [400, 200, 150, 150], 2)  # A2
            pygame.draw.rect(self.screen, self.colorYellow, [400, 350, 150, 150], 2)  # B2
            pygame.draw.rect(self.screen, self.colorYellow, [400, 500, 150, 150], 2)  # C2

            pygame.draw.rect(self.screen, self.colorYellow, [550, 200, 150, 150], 2)  # A3
            pygame.draw.rect(self.screen, self.colorYellow, [550, 350, 150, 150], 2)  # B3
            pygame.draw.rect(self.screen, self.colorYellow, [550, 500, 150, 150], 2)  # C3

            pygame.draw.rect(self.screen, self.colorYellow, [700, 200, 150, 150], 2)  # A4
            pygame.draw.rect(self.screen, self.colorYellow, [700, 350, 150, 150], 2)  # B4
            pygame.draw.rect(self.screen, self.colorYellow, [700, 500, 150, 150], 2)  # C4

            textsurface = self.fontArial.render('A', False, (0, 0, 0))
            self.screen.blit(textsurface, (220, 275))

            textsurface = self.fontArial.render('B', False, (0, 0, 0))
            self.screen.blit(textsurface, (220, 425))

            textsurface = self.fontArial.render('C', False, (0, 0, 0))
            self.screen.blit(textsurface, (220, 575))

            textsurface = self.fontArial.render('1', False, (0, 0, 0))
            self.screen.blit(textsurface, (325, 160))

            textsurface = self.fontArial.render('2', False, (0, 0, 0))
            self.screen.blit(textsurface, (475, 160))

            textsurface = self.fontArial.render('3', False, (0, 0, 0))
            self.screen.blit(textsurface, (625, 160))

            textsurface = self.fontArial.render('4', False, (0, 0, 0))
            self.screen.blit(textsurface, (775, 160))

            # Draw whos turn it is
            if (self.gameWhosTurn == "red"):
                textsurface = self.fontArialH1.render('Reds turn!', True, (0, 0, 0))
                self.screen.blit(textsurface, (400, 60))
            else:
                textsurface = self.fontArialH1.render('Blues turn!', False, (0, 0, 0))
                self.screen.blit(textsurface, (400, 60))

            # Status text
            textsurface = self.fontArial.render(self.statusText, False, (0, 0, 0))
            self.screen.blit(textsurface, (400, 110))


            # Print board
            # Can also printBoardToConsole for debug
            self.printBoardToGraphics()
            self.printCageToGraphics()

            # Print winner
            if(self.gameWinner == "red" or self.gameWinner == "blue"):
                filename = "animals/cat_" + self.gameWinner + "_512.png"
                imagePiece = pygame.image.load(filename)
                self.screen.blit(imagePiece, (300, 150))


            # Draw
            pygame.display.flip()

        # Be IDLE friendly
        pygame.quit()


    #- This method first prints the board to console, then print it to the board ------------------------------------ #
    def printBoardToConsole(self):

        # a) Print to console
        print("\n\n ")
        print("[0] 1 | [1] 2 | [2] 3 | [3] 4 ")

        itemA1 = self.gameboard.get((0, 0))
        itemA2 = self.gameboard.get((1, 0))
        itemA3 = self.gameboard.get((2, 0))
        itemA4 = self.gameboard.get((3, 0))
        print("[0] A", itemA1.getColor() + " " + itemA1.getName() + " | ", itemA2.getColor() + " " + itemA2.getName(), " | ", itemA3.getColor() + " " + itemA3.getName(), " | ", itemA4.getColor() + " " + itemA4.getName(), " ")


        itemB1 = self.gameboard.get((0, 1))
        itemB2 = self.gameboard.get((1, 1))
        itemB3 = self.gameboard.get((2, 1))
        itemB4 = self.gameboard.get((3, 1))
        print("[1] B", itemB1.getColor() + " " + itemB1.getName() + " | ", itemB2.getColor() + " " + itemB2.getName(), " | ", itemB3.getColor() + " " + itemB3.getName(), " | ", itemB4.getColor() + " " + itemB4.getName(), " ")

        itemC1 = self.gameboard.get((0, 2))
        itemC2 = self.gameboard.get((1, 2))
        itemC3 = self.gameboard.get((2, 2))
        itemC4 = self.gameboard.get((3, 2))
        print("[2] C", itemC1.getColor() + " " + itemC1.getName() + " | ", itemC2.getColor() + " " + itemC2.getName(), " | ", itemC3.getColor() + " " + itemC3.getName(), " | ", itemC4.getColor() + " " + itemC4.getName(), " ")

    def printBoardToGraphics(self):
        # b) Print to board
        for position,piece in self.gameboard.items():
            # print(type(piece), " ", piece.color, " ",  piece.name, " ",  piece.direction)
            # prints <class 'Sheep.Sheep'>   blue   sheep_blue_128   -1

            # Image
            if(piece.isActive == "true"):
                filename = "animals/" + piece.icon + "_active.png"
            else:
                filename = "animals/" + piece.icon + ".png"

            imagePiece = pygame.image.load(filename)

            # Position is pixel
            positionInPixels = self.getPositionInPixels(piece.position)  # list

            self.screen.blit(imagePiece, positionInPixels)

    def printCageToGraphics(self):

        # Print blue cage
        for i in range(len(self.cageBoardBlue)):
            if (self.cageBoardBlue[i] != "blank"):

                # Is it active?
                checkIfActiveName = "cage_" + "blue" + "_" + self.cageBoardBlue[i]
                if(checkIfActiveName == self.gameActivePieceName):
                    filename = "animals/" + self.cageBoardBlue[i] + "_blue_64_active.png"
                    self.statusText = "Free blue " + self.cageBoardBlue[i] + " <3"
                else:
                    filename = "animals/" + self.cageBoardBlue[i] + "_blue_64.png"

                imagePiece = pygame.image.load(filename)
                positionInPixels = (100, 200+(i*70))  # list
                self.screen.blit(imagePiece, positionInPixels)

        # Print red cage
        for i in range(len(self.cageBoardRed)):
            if (self.cageBoardRed[i] != "blank"):


                # Is it active?
                checkIfActiveName = "cage_" + "red" + "_" + self.cageBoardRed[i]
                if(checkIfActiveName == self.gameActivePieceName):
                    filename = "animals/" + self.cageBoardRed[i] + "_red_64_active.png"
                    self.statusText = "Free red " + self.cageBoardRed[i] + " <3"
                else:
                    filename = "animals/" + self.cageBoardRed[i] + "_red_64.png"
                imagePiece = pygame.image.load(filename)
                positionInPixels = (930, 200+(i*70))  # list
                self.screen.blit(imagePiece, positionInPixels)



    #- Positions, X, Y ---------------------------------------------------------------------------------------------- #
    # Takes in a position as "a1", "a2", etc and gives pixels back
    def getPositionInPixels(self, pos):
        position = {
            "a1": (260, 210),
            "b1": (260, 360),
            "c1": (260, 510),

            "a2": (410, 210),
            "b2": (410, 360),
            "c2": (410, 510),

            "a3": (560, 210),
            "b3": (560, 360),
            "c3": (560, 510),

            "a4": (710, 210),
            "b4": (710, 360),
            "c4": (710, 510),
        }
        return position.get(pos)

    #- Positions, X, Y ---------------------------------------------------------------------------------------------- #
    # Takes in a position as "a1", "a2", etc and gives array back
    def getPositionInArray(self, pos):
        position = {
            "a1": (0, 0),
            "b1": (0, 1),
            "c1": (0, 2),

            "a2": (1, 0),
            "b2": (1, 1),
            "c2": (1, 2),

            "a3": (2, 0),
            "b3": (2, 1),
            "c3": (2, 2),

            "a4": (3, 0),
            "b4": (3, 1),
            "c4": (3, 2),
        }
        return position.get(pos)

    # - Take some random position clicked and return the square (example a1) ------------------------------------------#
    # input = 100, 200,
    def clickPositionPixelToPositionBoard(self, clickPositionPixelX, clickPositionPixelY):
        boardPositionX = ""
        boardPositionY = ""

        # X
        if (clickPositionPixelX > 100 and clickPositionPixelX < 164):
            boardPositionX = "0" # blue cage
        elif (clickPositionPixelX > 250 and clickPositionPixelX < 400):
            boardPositionX = "1"
        elif (clickPositionPixelX > 400 and clickPositionPixelX < 550):
            boardPositionX = "2"
        elif (clickPositionPixelX > 550 and clickPositionPixelX < 700):
            boardPositionX = "3"
        elif (clickPositionPixelX > 700 and clickPositionPixelX < 850):
            boardPositionX = "4"
        elif (clickPositionPixelX > 930 and clickPositionPixelX < 994):
            boardPositionX = "5" # red cage
        else:
            boardPositionX = "-1"

        # Y
        # Cage?
        if(boardPositionX == "0" or boardPositionX == "5"):
            if (clickPositionPixelY > 200 and clickPositionPixelY < 264):
                boardPositionY = "a"
            elif (clickPositionPixelY > 270 and clickPositionPixelY < 334):
                boardPositionY = "b"
            elif (clickPositionPixelY > 340 and clickPositionPixelY < 404):
                boardPositionY = "c"
            elif (clickPositionPixelY > 410 and clickPositionPixelY < 474):
                boardPositionY = "d"
            else:
                boardPositionY = "Z"
        else:
            if (clickPositionPixelY > 200 and clickPositionPixelY < 350):
                boardPositionY = "a"
            elif (clickPositionPixelY > 350 and clickPositionPixelY < 500):
                boardPositionY = "b"
            elif (clickPositionPixelY > 500 and clickPositionPixelY < 650):
                boardPositionY = "c"
            elif (clickPositionPixelY > 650 and clickPositionPixelY < 800):
                boardPositionY = "d"
            else:
                boardPositionY = "Z"

        # print(str(clickPositionPixelX) + " = " + str(boardPositionX) + " " + str(clickPositionPixelY) + " = " + str(boardPositionY))

        xy = str(boardPositionY) + boardPositionX

        return xy


    # - Take some random square and give back what piece is in that square -------------------------------------------#
    # input = a1, a2, a3, b1, etc
    def selectOrMovePiece(self, clickedOnPositionBoard):

        # Find the animal located at that position
        mode = ""

        # Do I have an active animal selected, and now is selecting the place where I want to put it?
        if(self.gameActivePieceName == "cage_red_cat" or self.gameActivePieceName == "cage_red_dog" or self.gameActivePieceName == "cage_red_monkey"):
            self.freeAnimalFromCage(clickedOnPositionBoard)
        elif(self.gameActivePieceName == "cage_red_panda" or self.gameActivePieceName == "cage_red_sheep"):
            self.freeAnimalFromCage(clickedOnPositionBoard)
        elif(self.gameActivePieceName == "cage_blue_cat" or self.gameActivePieceName == "cage_blue_dog" or self.gameActivePieceName == "cage_blue_monkey"):
            self.freeAnimalFromCage(clickedOnPositionBoard)
        elif(self.gameActivePieceName == "cage_blue_panda" or self.gameActivePieceName == "cage_blue_sheep"):
            self.freeAnimalFromCage(clickedOnPositionBoard)

        # Look in cage first
        if(clickedOnPositionBoard == "a0" or clickedOnPositionBoard == "b0" or clickedOnPositionBoard == "c0" or clickedOnPositionBoard == "d0"):
            mode = "free_animal_from_blue_cage"
            self.selectAnimalInCage(clickedOnPositionBoard, "blue")
        elif(clickedOnPositionBoard == "a5" or clickedOnPositionBoard == "b5" or clickedOnPositionBoard == "c5" or clickedOnPositionBoard == "d5"):
            mode = "free_animal_from_red_cage"
            self.selectAnimalInCage(clickedOnPositionBoard, "red")

        # Look on board
        for position,piece in self.gameboard.items():
            # print(type(piece), " ", piece.color, " ",  piece.name, " ",  piece.direction)
            # prints <class 'Sheep.Sheep'>   blue   sheep_blue_128   -1

            if(piece.color == self.gameWhosTurn):


                if(piece.position == clickedOnPositionBoard):
                    # piece.name = cat
                    # piece.color = red

                    # is the icon already active? Then we are on a move,
                    # if the icon is NOT active, then set it active, next click is move

                    # Change icon to active state
                    piece.isActive = "true"
                    mode = "setActiveAPiece"
                    self.gameActivePieceName = piece.name

                    # Play sound
                    soundName = "sound/" + piece.name + ".mp3"
                    pygame.mixer.music.load(soundName)
                    pygame.mixer.music.play(0)

                    #status Text

                    if (self.gameWhosTurn == "red"):
                        self.statusText = "Red chooses " + piece.name
                    else:
                        self.statusText = "Blue chooses " + piece.name

                else:
                    piece.isActive = "false"



        if(mode == ""):
            for position,piece in self.gameboard.items():

                if (piece.color == self.gameWhosTurn and piece.name == self.gameActivePieceName):

                    if(clickedOnPositionBoard != "a-1" and clickedOnPositionBoard != "b-1" and clickedOnPositionBoard != "c-1" and clickedOnPositionBoard != "d-1"):

                        print("\n\n")
                        print("I want to move " + piece.color + " " + piece.name + " at position " + clickedOnPositionBoard)

                        toArray = self.getPositionInArray(clickedOnPositionBoard)
                        toX = toArray[0]
                        toY = toArray[1]

                        fromArray = self.getPositionInArray(piece.position)
                        fromX = fromArray[0]
                        fromY = fromArray[1]




                        print("from " + piece.position + " " + str(self.getPositionInArray(piece.position)) + " " + str(fromX) + " " + str(fromY))
                        print("to " + clickedOnPositionBoard + " " + str(self.getPositionInArray(clickedOnPositionBoard)) + " " + str(toX) + " " + str(toY))


                        # Move OK?
                        isTheMoveOk = piece.availableMoves(self.getPositionInArray(piece.position), self.getPositionInArray(clickedOnPositionBoard))

                        if (isTheMoveOk):
                            print("Move is ok" + " for " + piece.color + " " + piece.name)

                            # Check crash
                            pieceTo = self.gameboard[toX, toY]
                            if (pieceTo.getName() != "blank"):
                                if (self.gameWhosTurn == "red"):
                                    self.statusText = "Blue " + pieceTo.getName() + " got killed!"

                                    # Capture the piece
                                    for i in range(len(self.cageBoardRed)):
                                        if(self.cageBoardRed[i] == "blank"):
                                            if(pieceTo.getName() == "sheepzonbie"):
                                                self.cageBoardRed[i] = "sheep"
                                            else:
                                                self.cageBoardRed[i] = pieceTo.getName()
                                            break


                                else:
                                    self.statusText = "Red " + pieceTo.getName() + " got killed!"

                                    # Capture the piece
                                    for i in range(len(self.cageBoardBlue)):
                                        if(self.cageBoardBlue[i] == "blank"):
                                            if(pieceTo.getName() == "sheepzonbie"):
                                                self.cageBoardBlue[i] = "sheep"
                                            else:
                                                self.cageBoardBlue[i] = pieceTo.getName()
                                            break
                            else:
                                    self.statusText = ""


                            # Move it
                            self.gameboard[toX, toY] = self.gameboard[fromX, fromY]

                            # Move the piece
                            piece.position = clickedOnPositionBoard

                            # Fill old placement with blank
                            self.gameboard[fromX, fromY] = Blank("blank", "blank", "blank", 0, "a2");

                            # Switch turn
                            self.changePlayersTurn()

                            break
                        else:
                            print("Move is not ok" + " for " + piece.color + " " + piece.name)
                    else:
                        print("Move out of range")


        self.checkIfIHaveWon()
        self.checkIfLambCanBeUpgradedToSheep()



    def changePlayersTurn(self):
        if(self.gameWhosTurn == "red"):
            self.gameWhosTurn = "blue"
        else:
            self.gameWhosTurn = "red"

        soundName = "sound/" + self.gameWhosTurn + ".mp3"
        pygame.mixer.music.load(soundName)
        pygame.mixer.music.play(0)


    def checkIfIHaveWon(self):

        # Check if I have won?
        redHasPiecesLeft = "false"
        blueHasPiecesLeft = "false"

        # Check if Cat is at the other side of the board
        redCatEscaped = "false"
        blueCatEscaped = "false"

        # Check if blue cat or red cat is dead
        redCatDead = "true"
        blueCatDead = "true"

        for position, piece in self.gameboard.items():

            # Pieces left
            if (piece.color == "red"):
                redHasPiecesLeft = "true"
            elif (piece.color == "blue"):
                blueHasPiecesLeft = "true"


            # Cat escaped
            if (piece.color == "red" and piece.name == "cat"):
                if(piece.position == "a1" or piece.position == "b1" or piece.position == "c1"):
                    redCatEscaped = "true"
            elif (piece.color == "blue" and piece.name == "cat"):
                if(piece.position == "a4" or piece.position == "b4" or piece.position == "c4"):
                    blueCatEscaped = "true"

            # Cat dead
            if (piece.color == "red" and piece.name == "cat"):
                redCatDead = "false"
            elif (piece.color == "blue" and piece.name == "cat"):
                blueCatDead = "false"


        # Print message and sound
        if(redHasPiecesLeft == "false" or blueCatEscaped == "true" or redCatDead == "true"):
            self.statusText = "Blue won!!!"

            if(blueCatEscaped == "true"):
                self.statusText = "Blue cat escaped!!"

            if (redCatDead == "true"):
                self.statusText = "Red cat dead!!"

            soundName = "sound/blue_won.mp3"
            pygame.mixer.music.load(soundName)
            pygame.mixer.music.play(0)


            # Winner
            self.gameWinner = "blue"

        if (blueHasPiecesLeft == "false" or redCatEscaped == "true" or blueCatDead == "true"):
            self.statusText = "Red won!!!"

            if(redCatEscaped == "true"):
                self.statusText = "Red cat escaped!!"

            if (blueCatDead == "true"):
                self.statusText = "Blue cat dead!!"

            soundName = "sound/red_won.mp3"
            pygame.mixer.music.load(soundName)
            pygame.mixer.music.play(0)

            # Winner
            self.gameWinner = "red"



        self.printBoardToConsole()
        self.printBoardToGraphics()

        # check If

    def checkIfLambCanBeUpgradedToSheep(self):
        for position, piece in self.gameboard.items():
            if (piece.color == "red" and piece.name == "sheep"):
                if(piece.position == "a1" or piece.position == "b1" or piece.position == "c1"):
                    self.statusText = "Red lamb became a sheep!"

                    array = self.getPositionInArray(piece.position)
                    x = array[0]
                    y = array[1]

                    self.gameboard[x, y] = Panda(piece.color, "panda", "panda_red_128", -1, piece.position);


            elif (piece.color == "blue" and piece.name == "sheep"):
                if(piece.position == "a4" or piece.position == "b4" or piece.position == "c4"):
                    self.statusText = "Blue lamb became a sheep!"

                    array = self.getPositionInArray(piece.position)
                    x = array[0]
                    y = array[1]

                    self.gameboard[x, y] = Panda(piece.color, "panda", "panda_blue_128", 1, piece.position);


    def selectAnimalInCage(self, clickedOnPositionBoard, color):
        # Cant set it out with cat

        if(self.gameWhosTurn == "blue" and clickedOnPositionBoard == "a0"):
            self.gameActivePieceName = "cage_" + color + "_" + self.cageBoardBlue[0];
        elif(self.gameWhosTurn == "blue" and clickedOnPositionBoard == "b0"):
            self.gameActivePieceName = "cage_" + color + "_" + self.cageBoardBlue[1];
        elif(self.gameWhosTurn == "blue" and clickedOnPositionBoard == "c0"):
            self.gameActivePieceName = "cage_" + color + "_" + self.cageBoardBlue[2];
        elif(self.gameWhosTurn == "blue" and clickedOnPositionBoard == "d0"):
            self.gameActivePieceName = "cage_" + color + "_" + self.cageBoardBlue[3];
        elif(self.gameWhosTurn == "red" and clickedOnPositionBoard == "a5"):
            self.gameActivePieceName = "cage_" + color + "_" + self.cageBoardRed[0];
        elif(self.gameWhosTurn == "red" and clickedOnPositionBoard == "b5"):
            self.gameActivePieceName = "cage_" + color + "_" + self.cageBoardRed[1];
        elif(self.gameWhosTurn == "red" and clickedOnPositionBoard == "c5"):
            self.gameActivePieceName = "cage_" + color + "_" + self.cageBoardRed[2];
        elif(self.gameWhosTurn == "red" and clickedOnPositionBoard == "d5"):
            self.gameActivePieceName = "cage_" + color + "_" + self.cageBoardRed[3];

        # Next click will be the same, but with the placement for the animal
        print("Freeing from position " + clickedOnPositionBoard + " color " + color + ". gameActivePieceName = " + self.gameActivePieceName)

    def freeAnimalFromCage(self, clickedOnPositionBoard):
            print("Now i selected where to place the caged animal " + self.gameActivePieceName + " to position " + clickedOnPositionBoard)

            toArray = self.getPositionInArray(clickedOnPositionBoard)
            toX = toArray[0]
            toY = toArray[1]


            # Check that I dont have any other animal there
            checkForCrash = self.gameboard[toX, toY]
            if(checkForCrash.getName() == "blank"):

                if (self.gameActivePieceName == "cage_red_cat"):
                    self.gameboard[toX, toY] = Cat("red", "cat", "cat_red_128", 1, clickedOnPositionBoard);
                elif(self.gameActivePieceName == "cage_red_dog"):
                    self.gameboard[toX, toY] = Dog("red", "dog", "dog_red_128", 1, clickedOnPositionBoard);
                elif (self.gameActivePieceName == "cage_red_monkey"):
                    self.gameboard[toX, toY] = Monkey("red", "monkey", "monkey_red_128", 1, clickedOnPositionBoard);
                elif (self.gameActivePieceName == "cage_red_panda" or self.gameActivePieceName == "cage_red_sheep" or self.gameActivePieceName == "cage_red_sheepzombie"):
                    self.gameboard[toX, toY] = SheepZombie("red", "sheepzombie", "sheep_red_128", 1, clickedOnPositionBoard);
                elif(self.gameActivePieceName == "cage_blue_cat"):
                    self.gameboard[toX, toY] = Cat("blue", "cat", "cat_blue_128", -1, clickedOnPositionBoard);
                elif(self.gameActivePieceName == "cage_blue_dog"):
                    self.gameboard[toX, toY] = Dog("red", "dog", "dog_blue128", 1, clickedOnPositionBoard);
                elif(self.gameActivePieceName == "cage_blue_monkey"):
                    self.gameboard[toX, toY] = Monkey("blue", "monkey", "monkey_blue_128", 1, clickedOnPositionBoard);
                elif (self.gameActivePieceName == "cage_blue_panda" or self.gameActivePieceName == "cage_blue_sheep" or self.gameActivePieceName == "cage_blue_sheepzombie"):
                    self.gameboard[toX, toY] = SheepZombie("blue", "sheepzombie", "sheep_blue_128", 1, clickedOnPositionBoard);

                self.gameActivePieceName = ""

                # Switch turn
                self.changePlayersTurn()

# ------------------ Main entry point ------------------
if __name__ == "__main__":
    Main()



