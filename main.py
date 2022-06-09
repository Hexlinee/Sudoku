import random
import sys
import pygame
import numpy as np

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def message(screen,msg, color, size,):
    font = pygame.font.SysFont("comicsansms", size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect()
    text_rect.center = (screen.get_width() // 2, screen.get_height() )
    screen.blit(text, text_rect)

def generate_sudoku(mask_rate=0.75):
    while True:
        n = 9
        m = np.zeros((n, n), np.int)
        rg = np.arange(1, n + 1)
        m[0, :] = np.random.choice(rg, n, replace=False)
        try:
            for r in range(1, n):
                for c in range(n):
                    col_rest = np.setdiff1d(rg, m[:r, c])
                    row_rest = np.setdiff1d(rg, m[r, :c])
                    avb1 = np.intersect1d(col_rest, row_rest)
                    sub_r, sub_c = r//3, c//3
                    avb2 = np.setdiff1d(np.arange(0, n+1), m[sub_r*3:(sub_r+1)*3, sub_c*3:(sub_c+1)*3].ravel())
                    avb = np.intersect1d(avb1, avb2)
                    m[r, c] = np.random.choice(avb, size=1)
            break
        except ValueError:
            pass
    print("Answer:\n", m)
    mm = m.copy()
    mm[np.random.choice([True, False], size=m.shape, p=[mask_rate, 1 - mask_rate])] = 0
    print("\nMasked anwser:\n", mm)
    return m

def main():
    if len(sys.argv) > 1:
        board = []
        for i in range(9):
            board.append(list(map(int, sys.argv[1][i*9:(i+1)*9])))
        board = np.array(board)
        print("\nAnswer:\n", board)
        mm = board.copy()
        mm[np.random.choice([True, False], size=board.shape, p=[0.5, 0.5])] = 0
        print("\nMasked anwser:\n", mm)

    else:
        board= generate_sudoku()
        boardnew = board.copy()

    MainBoard = np.array(board)
    AnswerBoard = MainBoard.copy()
    FakeBoard = MainBoard.copy()
    FakeBoard[np.random.choice([True, False], size=MainBoard.shape, p=[0.5, 0.5])] = 0
    MaskBoard = FakeBoard.copy()
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Sudoku")
    font = pygame.font.SysFont("comicsans", 40)
    clock = pygame.time.Clock()
    run = True

    Real = []
    while run:
        MainBoard = FakeBoard.copy()
        pressed_button = None
        for event_ in pygame.event.get():
            if event_.type == pygame.QUIT:
                run = False
        screen.fill((255, 255, 255))
        a = -.5
        for i in range(9):
            for j in range(9):
                if FakeBoard[i][j] == 0:
                    pygame.draw.rect(screen, (200,200,200), (50 + j * 100, 50 + i * 100, 100, 100))
                    pygame.draw.rect(screen, (0,0,0), (50 + j * 100, 50 + i * 100, 100, 100), 1)



                    if a == -.5:
                        if 50 + j * 100 < pygame.mouse.get_pos()[0] < 50 + (j + 1) * 100 and 50 + i * 100 < \
                                pygame.mouse.get_pos()[1] < 50 + (i + 1) * 100:
                            pygame.draw.rect(screen, (0, 0, 0), (50 + j * 100, 50 + i * 100, 100, 100), 3)
                            a = i * 9 + j
                            if pygame.key.get_pressed()[pygame.K_1]:
                                FakeBoard[i][j] = 1
                            elif pygame.key.get_pressed()[pygame.K_2]:
                                FakeBoard[i][j] = 2
                            elif pygame.key.get_pressed()[pygame.K_3]:
                                FakeBoard[i][j] = 3
                            elif pygame.key.get_pressed()[pygame.K_4]:
                                FakeBoard[i][j] = 4
                            elif pygame.key.get_pressed()[pygame.K_5]:
                                FakeBoard[i][j] = 5
                            elif pygame.key.get_pressed()[pygame.K_6]:
                                FakeBoard[i][j] = 6
                            elif pygame.key.get_pressed()[pygame.K_7]:
                                FakeBoard[i][j] = 7
                            elif pygame.key.get_pressed()[pygame.K_8]:
                                FakeBoard[i][j] = 8
                            elif pygame.key.get_pressed()[pygame.K_9]:
                                FakeBoard[i][j] = 9
                            elif pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                                FakeBoard[i][j] = 0
                            pass
                else:
                    Actual_Number = AnswerBoard[i][j]
                    Fake_Number = MaskBoard[i][j]
                    if Actual_Number == Fake_Number:
                        pass
                    else:
                        pygame.draw.rect(screen, (255, 236, 130), (50 + j * 100, 50 + i * 100, 100, 100))
                        pygame.draw.rect(screen, (0, 0, 0), (50 + j * 100, 50 + i * 100, 100, 100), 1)
                        MainBoard[i][j] = FakeBoard[i][j]
                        if a == -.5:
                            if 50 + j * 100 < pygame.mouse.get_pos()[0] < 50 + (j + 1) * 100 and 50 + i * 100 < \
                                    pygame.mouse.get_pos()[1] < 50 + (i + 1) * 100:
                                pygame.draw.rect(screen, (0, 0, 0), (50 + j * 100, 50 + i * 100, 100, 100), 3)
                                a = i * 9 + j
                                if pygame.key.get_pressed()[pygame.K_1]:
                                    FakeBoard[i][j] = 1
                                elif pygame.key.get_pressed()[pygame.K_2]:
                                    FakeBoard[i][j] = 2
                                elif pygame.key.get_pressed()[pygame.K_3]:
                                    FakeBoard[i][j] = 3
                                elif pygame.key.get_pressed()[pygame.K_4]:
                                    FakeBoard[i][j] = 4
                                elif pygame.key.get_pressed()[pygame.K_5]:
                                    FakeBoard[i][j] = 5
                                elif pygame.key.get_pressed()[pygame.K_6]:
                                    FakeBoard[i][j] = 6
                                elif pygame.key.get_pressed()[pygame.K_7]:
                                    FakeBoard[i][j] = 7
                                elif pygame.key.get_pressed()[pygame.K_8]:
                                    FakeBoard[i][j] = 8
                                elif pygame.key.get_pressed()[pygame.K_9]:
                                    FakeBoard[i][j] = 9
                                elif pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                                    FakeBoard[i][j] = 0
                                elif pygame.key.get_pressed()[pygame.K_RETURN]:
                                    if 0 in FakeBoard:
                                        print("Please fill in all the numbers")
                                    else:
                                        for i in range(9):
                                            for j in range(9):
                                                CurrentNumber = MainBoard[i][j]
                                                CorrectNumber = AnswerBoard[i][j]
                                                if CurrentNumber == CorrectNumber:
                                                    pygame.draw.rect(screen, (106,255,87), (50 + j * 100, 50 + i * 100, 100, 100))
                                                    pygame.draw.rect(screen, (0, 0, 0), (50 + j * 100, 50 + i * 100, 100, 100), 1)
                                                    font = pygame.font.SysFont("comicsansms", 30)
                                                    text = font.render(str(CorrectNumber), 1, (106,255,87))
                                                    screen.blit(text, (50 + j * 100 + 20, 50 + i * 100 + 20))
                                                    textRect = text.get_rect()
                                                    textRect.center = (50 + j * 100 + 50, 50 + i * 100 + 50)
                                                    screen.blit(text, textRect)
                                                    text = font.render(str(CurrentNumber), 1, (10, 10, 10))
                                                    textRect = text.get_rect()
                                                    textRect.center = (50 + j * 100 + 50, 50 + i * 100 + 50)
                                                    screen.blit(text, textRect)
                                                else:
                                                    pygame.draw.rect(screen, (255, 114,111), (50 + j * 100, 50 + i * 100, 100, 100))
                                                    pygame.draw.rect(screen, (0, 0, 0), (50 + j * 100, 50 + i * 100, 100, 100), 1)
                                                    font = pygame.font.SysFont("comicsansms", 30)
                                                    text = font.render(str(CorrectNumber), 1, (255,114,111))
                                                    screen.blit(text, (50 + j * 100 + 20, 50 + i * 100 + 20))
                                                    textRect = text.get_rect()
                                                    textRect.center = (50 + j * 100 + 50, 50 + i * 100 + 50)
                                                    screen.blit(text, textRect)
                                                    text = font.render(str(CurrentNumber), 1, (10,10,10))
                                                    textRect = text.get_rect()
                                                    textRect.center = (50 + j * 100 + 50, 50 + i * 100 + 50)
                                                    screen.blit(text, textRect)
                                        message(screen, "Press space to continue", (0,0,0),25)
                                        pause()
                                pass
                    pygame.draw.rect(screen, (0, 0, 0), (50 + j * 100, 50 + i * 100, 100, 100), 2)
                    text = font.render(str(FakeBoard[i][j]), True, (0, 0, 0))
                    pygame.draw.rect(screen, (0, 0, 0), (50 + j * 100, 50 + i * 100, 100, 100), 2)
                    textRect = text.get_rect()
                    textRect.center = (50 + j * 100 + 50, 50 + i * 100 + 50)
                    screen.blit(text, textRect)

        pygame.display.update()





if __name__ == "__main__":
    main()

