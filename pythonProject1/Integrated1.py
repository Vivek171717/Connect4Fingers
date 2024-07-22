import pygame
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import sys
from button import Button

#Initialize
pygame.init()
#Create window
width1, height1 = 1280, 700
window = pygame.display.set_mode((width1, height1))
pygame.display.set_caption("Connect4Fingers")
#Initialize clock for fps
fps = 60
clock = pygame.time.Clock()

#OpenCV
cap = cv2.VideoCapture(0)
cap.set(3, width1)
cap.set(4, height1)
#Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

#object Rect
yellow_rect1 = pygame.Rect(160, 0, 100, 50) #(x,y,width,height)
yellow_rect2 = pygame.Rect(320, 0, 100, 50)
yellow_rect3 = pygame.Rect(480, 0, 100, 50)
red_rect1 = pygame.Rect(640, 0, 100, 50)
red_rect2 = pygame.Rect(800, 0, 100, 50)
red_rect3 = pygame.Rect(960, 0, 100, 50)

BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)

                                ################## GAME FUNCTIONS ###################
ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(window, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(window, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(window, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(window, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


                                      ################## CREATING MENU ####################

#Background
BG1 = pygame.image.load(r"C:\Users\saroj\OneDrive\Documents\Project\Background2.jpg")

def get_font(size):
    return pygame.font.Font(r"C:\Users\saroj\OneDrive\Documents\Project\font.ttf", size)
def main_menu():

        window.blit(BG1, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("Connect4Fingers", True, (182, 143, 64))
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load(r"C:\Users\saroj\OneDrive\Documents\Project\Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="WHITE", hovering_color="GREEN")
        HELP_BUTTON = Button(image=pygame.image.load(r"C:\Users\saroj\OneDrive\Documents\Project\Play Rect.png"), pos=(640, 400),
                                text_input="HELP", font=get_font(75), base_color="WHITE", hovering_color="GREEN")
        QUIT_BUTTON = Button(image=pygame.image.load(r"C:\Users\saroj\OneDrive\Documents\Project\Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="WHITE", hovering_color="GREEN")

        window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, HELP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(window)

        pygame.display.update()



board = create_board()   #matrix
print_board(board)       #flip
game_over = False
turn = 0


#Game Variables
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
RADIUS = int(SQUARESIZE/2 - 5)
myfont = pygame.font.SysFont("monospace", 75)
myfont2 = pygame.font.SysFont(None, 40)
wait_time = 1000

#Game Sounds
drop = pygame.mixer.Sound(r"C:\Users\saroj\OneDrive\Documents\Project\drop.mp3")
VictoryForRed = pygame.mixer.Sound(r"C:\Users\saroj\OneDrive\Documents\Project\VictoryForRed.mp3")
VictoryForYellow = pygame.mixer.Sound(r"C:\Users\saroj\OneDrive\Documents\Project\VictoryForYellow.mp3")

# Define game states
MENU = 0
GAME = 1
HELP = 2
# Initial game state
current_state = MENU

#Main loop
while not game_over:
    MENU_MOUSE_POS = pygame.mouse.get_pos()
    PLAY_BUTTON = Button(image=pygame.image.load(r"C:\Users\saroj\OneDrive\Documents\Project\Play Rect.png"),
                         pos=(640, 250), text_input="PLAY", font=get_font(75), base_color="WHITE", hovering_color="GREEN")
    HELP_BUTTON = Button(image=pygame.image.load(r"C:\Users\saroj\OneDrive\Documents\Project\Play Rect.png"),
                            pos=(640, 400), text_input="HELP", font=get_font(75), base_color="WHITE", hovering_color="GREEN")
    QUIT_BUTTON = Button(image=pygame.image.load(r"C:\Users\saroj\OneDrive\Documents\Project\Quit Rect.png"),
                         pos=(640, 550), text_input="QUIT", font=get_font(75), base_color="WHITE", hovering_color="GREEN")
    BACK_BUTTON = Button(image=None, pos=(60, 30), text_input="< BACK", font=get_font(20), base_color="Black", hovering_color="RED")

    #Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            #pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                if current_state == MENU:
                    current_state = GAME  # Start the game
            elif HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                if current_state == MENU:
                    current_state = HELP
            elif BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                if current_state == HELP:
                    current_state = MENU
            elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                pygame.quit()
                sys.exit()

    # Update based on the current game state
    if current_state == MENU:
        # Draw the menu
        main_menu()

    elif current_state == HELP:
        window.fill(WHITE)

        # Define text instructions
        help_font1 = pygame.font.Font((r"C:\Users\saroj\OneDrive\Documents\Project\font.ttf"), 20)
        help_font2 = pygame.font.Font((r"C:\Users\saroj\OneDrive\Documents\Project\font.ttf"), 13)
        help_font3 = pygame.font.Font((r"C:\Users\saroj\OneDrive\Documents\Project\font.ttf"), 55)
        Hand_img = pygame.image.load(r"C:\Users\saroj\OneDrive\Documents\Project\Hand.jpg")

        #Hand Image
        window.blit(Hand_img, (860, 90))

        #Title
        Title_text1 = help_font3.render("Connect4Fingers", True, (182, 143, 64))
        window.blit(Title_text1, (30, 100))
        Title_text2 = help_font3.render("ABOUT", True, BLUE)
        window.blit(Title_text2, (270, 230))

        # Hand Gestures Text
        hand_gestures_text = help_font1.render("Hand Gestures:", True, BLUE)
        window.blit(hand_gestures_text, (20, 400))

        # Define hand gestures instructions
        hand_gestures_instructions = [
            "-> Use your thumb to drop a token in the 1st, 4th, and 5th columns.",
            "-> Utilize your index finger to drop a token in the 2nd and 6th columns.",
            "-> Deploy your little finger to drop a piece in the 3rd and 7th columns."
        ]

        # Render hand gestures instructions
        y_offset = 450
        for instruction in hand_gestures_instructions:
            text = help_font2.render(instruction, True, (0,0,0))
            text_rect = text.get_rect(left=20, top=y_offset)
            window.blit(text, text_rect)
            y_offset += text_rect.height + 5  # Adjust vertical spacing

        # Game Rules Text
        game_rules_text = help_font1.render("Game Rules:", True, BLUE)
        window.blit(game_rules_text, (20, 570))

        # Define game rules instructions
        game_rules_instructions = [
            "-> Players take turns to drop one game piece at a time into any of the seven columns.",
            "-> Connect four of your token vertically, horizontally, or diagonally on the game board to win."
        ]

        # Render game rules instructions
        y_offset = 620
        for instruction in game_rules_instructions:
            text = help_font2.render(instruction, True, (0,0,0))
            text_rect = text.get_rect(left=20, top=y_offset)
            window.blit(text, text_rect)
            y_offset += text_rect.height + 5  # Adjust vertical spacing



        BACK_MOUSE_POS = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=None, pos=(60, 30), text_input="< BACK", font=get_font(20), base_color="Black", hovering_color="RED")
        BACK_BUTTON.changeColor(BACK_MOUSE_POS)
        BACK_BUTTON.update(window)
        pygame.display.update()


    elif current_state == GAME:

        # Apply Logic

        # window.fill((255, 255, 255)) #instead filling color integrate window with opencv
        # OpenCV-pygame integration
        success, img = cap.read()
        hands, img = detector.findHands(img)  # HandDetection

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgRGB = np.rot90(imgRGB)
        frame = pygame.surfarray.make_surface(imgRGB).convert()
        window.blit(frame, (0, 0))


        #Game board
        draw_board(board)
        #pygame.display.update()

        #Reactive coordinates
        pygame.draw.rect(window,(255,255,0),red_rect1)
        pygame.draw.rect(window,(255,255,0),red_rect2)
        pygame.draw.rect(window,(255,255,0),red_rect3)
        pygame.draw.rect(window, (255,0,0),yellow_rect1)
        pygame.draw.rect(window, (255,0,0), yellow_rect2)
        pygame.draw.rect(window, (255,0,0), yellow_rect3)


        #Indicaton
        text = myfont2.render("1-2-3", True, GREEN)
        window.blit(text, (175, 10))
        text = myfont2.render("4", True, GREEN)
        window.blit(text, (360, 10))
        text = myfont2.render("5-6-7", True, GREEN)
        window.blit(text, (495, 10))
        text = myfont2.render("1-2-3", True, GREEN)
        window.blit(text, (655, 10))
        text = myfont2.render("4", True, GREEN)
        window.blit(text, (840, 10))
        text = myfont2.render("5-6-7", True, GREEN)
        window.blit(text, (975, 10))
        pygame.display.update()


        if hands:
            hand = hands[0]
            a, b = hand['lmList'][4]
            x, y = hand['lmList'][20]
            c, d = hand['lmList'][8]

            if turn == 0:
                if red_rect3.collidepoint(a, b):   #1
                    col = 0
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 1):
                            label = myfont.render("RED WINS!!", 1, RED)
                            window.blit(label, (780, 300))
                            pygame.display.update()
                            VictoryForRed.play()
                            game_over = True


                elif red_rect3.collidepoint(c, d):  #2
                    col = 1
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 1):
                            label = myfont.render("RED WINS!!", 1, RED)
                            window.blit(label, (780, 300))
                            pygame.display.update()
                            VictoryForRed.play()
                            game_over = True

                elif red_rect3.collidepoint(x, y):  #3
                    col = 2
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 1):
                            label = myfont.render("RED WINS!!", 1, RED)
                            window.blit(label, (780, 300))
                            pygame.display.update()
                            VictoryForRed.play()
                            game_over = True

                elif red_rect2.collidepoint(a, b): #4
                    col = 3
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 1):
                            label = myfont.render("RED WINS!!", 1, RED)
                            window.blit(label, (780, 300))
                            pygame.display.update()
                            VictoryForRed.play()
                            game_over = True

                elif red_rect1.collidepoint(a, b):  #5
                    col = 4
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 1):
                            label = myfont.render("RED WINS!!", 1, RED)
                            window.blit(label, (780, 300))
                            pygame.display.update()
                            VictoryForRed.play()
                            game_over = True

                elif red_rect1.collidepoint(c, d):  #6
                    col = 5
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 1):
                            label = myfont.render("RED WINS!!", 1, RED)
                            window.blit(label, (780, 300))
                            pygame.display.update()
                            VictoryForRed.play()
                            game_over = True

                elif red_rect1.collidepoint(x, y):  #7
                    col = 6
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 1):
                            label = myfont.render("RED WINS!!", 1, RED)
                            window.blit(label, (780, 300))
                            pygame.display.update()
                            VictoryForRed.play()
                            game_over = True

            elif turn == 1:
                if yellow_rect3.collidepoint(a, b):  # 1
                    col = 0
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 2):
                            label = myfont.render("YELLOW WINS!!", 1, YELLOW)
                            window.blit(label, (710, 300))
                            pygame.display.update()
                            VictoryForYellow.play()
                            game_over = True

                elif yellow_rect3.collidepoint(c, d):  # 2
                    col = 1
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 2):
                            label = myfont.render("YELLOW WINS!!", 1, YELLOW)
                            window.blit(label, (710, 300))
                            pygame.display.update()
                            VictoryForYellow.play()
                            game_over = True

                elif yellow_rect3.collidepoint(x, y):  # 3
                    col = 2
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 2):
                            label = myfont.render("YELLOW WINS!!", 1, YELLOW)
                            window.blit(label, (710, 300))
                            pygame.display.update()
                            VictoryForYellow.play()
                            game_over = True

                elif yellow_rect2.collidepoint(a, b):  # 4
                    col = 3
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 2):
                            label = myfont.render("YELLOW WINS!!", 1, YELLOW)
                            window.blit(label, (710, 300))
                            pygame.display.update()
                            VictoryForYellow.play()
                            game_over = True

                elif yellow_rect1.collidepoint(a, b):  # 5
                    col = 4

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 2):
                            label = myfont.render("YELLOW WINS!!", 1, YELLOW)
                            window.blit(label, (710, 300))
                            pygame.display.update()
                            VictoryForYellow.play()
                            game_over = True

                elif yellow_rect1.collidepoint(c, d):  # 6
                    col = 5
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 2):
                            label = myfont.render("YELLOW WINS!!", 1, YELLOW)
                            window.blit(label, (710, 300))
                            pygame.display.update()
                            VictoryForYellow.play()
                            game_over = True

                elif yellow_rect1.collidepoint(x, y):  # 7
                    col = 6
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
                        print_board(board)
                        draw_board(board)
                        drop.play()
                        pygame.time.wait(wait_time)

                        if winning_move(board, 2):
                            label = myfont.render("YELLOW WINS!!", 1, YELLOW)
                            window.blit(label, (710, 300))
                            pygame.display.update()
                            VictoryForYellow.play()
                            game_over = True



        #print_board(board)
        #draw_board(board)


            #turn += 1
            #turn = turn % 2

            #pygame.time.wait(2000)

        if game_over:
            pygame.time.wait(5000)


    #Update window
    pygame.display.update()

    #Set fps
    clock.tick(fps)

    turn += 1
    turn = turn % 2

