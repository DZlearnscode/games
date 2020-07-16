import pygame, json, random, time
from player import Player
from enemy import Enemy
from items import Triangle

class Game():
    def __init__(self, hight, width, player = None):
        # initiating pygame
        pygame.init()
        pygame.display.set_caption("DZ's first Game!")
        pygame.font.init()

        self.font = pygame.font.SysFont('Comic Sans MS',30)
        self.hight = hight
        self.width = width 
        self.screen = pygame.display.set_mode((self.width, self.hight))
        # self.screen_rect[2] is the x - horizontal dimantion, self.screen_rect[3] is y - the vertival dimantion
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()

        self.click = False

        self.tri = Triangle(self.screen, 40, 5)
        self.player = player 
        self.gameOver = False
        self.wave = 0
        self.score = 0
        self.enemyList = [] 

        # setting up score board

        try: 
            with open('highscore.json', 'r') as highscores:
              self.highscores = json.load(highscores)
        except:
            self.highscores = [['name', 0, 0] for i in range(10)]

        # colours
        self.PURPLE = (125,75,150)
        self.BLUE = (000,000,255)
        self.GREEN = (000,255,000)
        self.BLACK = (000,000,000)
        self.WHITE = (255,255,255)
        self.GOLD = (255,215,000)

    def createWave(self):
        if self.score >= 0:
            for i in range(15):
                self.enemyList.append(Enemy(self.screen, random.randint(55,75), random.randint(2,6), self.player))
        elif self.score > 30:
            for i in range(10):
                self.enemyList.append(Enemy(self.screen, random.randint(55,75), random.randint(2,5), self.player))
        elif self.score > 50:
            for i in range(10):
                self.enemyList.append(Enemy(self.screen, random.randint(55,75), random.randint(3,5), self.player))
            for i in range(5):
                self.enemyList.append(Enemy(self.screen, random.randint(55,75), random.randint(2,6), self.player))
        elif self.score > 75:
            for i in range(10):
                self.enemyList.append(Enemy(self.screen, random.randint(45,75), random.randint(3,6), self.player))
            for i in range(6):
                self.enemyList.append(Enemy(self.screen, random.randint(55,75), random.randint(2,5), self.player))

    def dropWave(self):
        for i, enemy in enumerate(self.enemyList):
            enemy.dropEnemy()
            if enemy.detectCollision(enemy.player):
                self.scoreText()
                self.GameOver()        
            if enemy.DEACTIVE is True:
                self.score += 1
                self.enemyList.pop(i)
        if self.player.shape == 'triangle':
            if self.player.transformCounter > 150:
                self.player.shape = 'rect'
                self.player.transformCounter = 0
            else:
                self.player.transformCounter += 1

    def refresh(self):
        self.screen.fill(self.PURPLE)

    def scoreText(self):
        text = f'wave: {self.wave}, score: {self.score}'
        scoreTextSurface = self.font.render(text, False, self.WHITE)
        self.screen.blit(scoreTextSurface, (330,10))
        pygame.display.flip()
        
    def GameOver(self):
        gameOverText = self.font.render('GAME OVER', False, self.WHITE)
        self.screen.blit(gameOverText, (200,300))
        pygame.display.flip()
        if self.score > self.highscores[-1][2]:
            self.newHighscore()
        self.gameOver = True
        # reset game 
        self.enemyList = []
        self.player.position = [300,765]
        self.player.shape = 'rect'
        self.wave = 0
        self.score = 0
        self.refresh()
        time.sleep(3)
        pygame.display.flip()
        self.gameMenu()
    
    def gameMenu(self):
        while True:
            self.click = False
            self.refresh()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('highscore.json', 'w') as highscores:
                        json.dump(self.highscores, highscores)
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        with open('highscore.json', 'w') as highscores:
                            json.dump(self.highscores, highscores)
                        pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True

            mx,my = pygame.mouse.get_pos()

            newGameText = self.font.render('New Game', False, self.WHITE)
            newGameRect = pygame.Rect(200,300,200,60)
            self.screen.blit(newGameText, (225,310))
            pygame.draw.rect(self.screen, self.WHITE, newGameRect, width = 4)

            highScoreText = self.font.render('High Scores', False, self.WHITE)
            highScoreRect = pygame.Rect(200,400,200,60)
            self.screen.blit(highScoreText, (215,410))
            pygame.draw.rect(self.screen, self.WHITE, highScoreRect, width= 4) 
 
            if newGameRect.collidepoint((mx,my)):
                if self.click == True:
                    self.gameOver = False
                    self.gameLoop()
            if highScoreRect.collidepoint((mx,my)):
                if self.click == True:
                    self.highScoreBoard()

            pygame.display.flip()

    def highScoreBoard(self):
        self.highscores = self.sort(self.highscores)
        highscoresFonts = []
        if len(self.highscores) > 9:
            self.highscores.pop()
        for score in self.highscores:
            text = f'{score[0]}    wave: {score[1]}    score: {score[2]}'
            highscoreFont = self.font.render(text, False, self.WHITE)
            highscoresFonts.append(highscoreFont)

        heading = self.font.render("Hall Of Fame", False, self.WHITE)
        
        running = True
        while running:
            renderLoc = [50,250]
            self.refresh()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            self.screen.blit(heading, (200,100))
            for score in highscoresFonts:
                self.screen.blit(score, renderLoc)
                renderLoc[1] += 35

            self.clock.tick(50)
            pygame.display.flip()

    def newHighscore(self):
        userName = self.textInput()
        self.highscores.append([userName, self.wave, self.score])

    def sort(self, array):
        if len(array) <= 1:
            return array
        mid = len(array) // 2
        left, right = self.sort(array[:mid]), self.sort(array[mid:])
        # merge lists
        return self.merge(left,right)
        
    def merge(self,left,right):
        result = []
        l_pointer = r_pointer = 0
        while l_pointer < len(left) and r_pointer < len(right):
            if left[l_pointer][2] >= right[r_pointer][2]:
                result.append(left[l_pointer])
                l_pointer += 1 
            else:
                result.append(right[r_pointer])
                r_pointer += 1
        
        result.extend(left[l_pointer:])
        result.extend(right[r_pointer:])

        return result

    def gameLoop(self):
        
        while not self.gameOver:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.LEFT()
                    elif event.key == pygame.K_RIGHT:
                        self.player.RIGHT()
                    elif event.key == pygame.K_UP:
                        self.player.UP()
                    elif event.key == pygame.K_DOWN:
                        self.player.DOWN()

            self.refresh()
            self.player.drawSelf()

            if len(self.enemyList) < 15:
                self.wave += 1
                self.createWave()
                
            
            self.dropWave()    

            if self.tri.ACTIVE:
                self.tri.dropTriangle()
                transform = self.tri.detectCollision(self.player)
                if transform is True:
                    self.player.shape = 'triangle'
            elif self.score%10 == 0:
                self.tri = Triangle(self.screen, 40, 5)

            self.scoreText()
            self.clock.tick(50)
            pygame.display.flip()
        
    def textInput(self):
        validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
        shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
        inputing = True
        shift = False
        userStr = ''
        while inputing:
            self.refresh()
            prompt = self.font.render('Enter your name below', False, self.WHITE)
            self.screen.blit(prompt, (150,300))
            userStrFont = self.font.render(userStr, False, self.WHITE)
            self.screen.blit(userStrFont, (165,450))
            userInputRect = pygame.Rect(150,425,300,100)
            pygame.draw.rect(self.screen, self.WHITE, userInputRect, width=4)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        shift = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(userStr) < 1:
                            userStr = 'ChAmP'
                        inputing = False
                        return userStr
                    if event.key == pygame.K_ESCAPE:
                        inputing = False
                    if event.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                        shift = True
                    if pygame.key.name(event.key) in validChars and not shift and len(userStr) <= 25:
                        userStr += pygame.key.name(event.key)
                    elif pygame.key.name(event.key) in validChars and shift and len(userStr) <= 25:
                        userStr += shiftChars[validChars.index(pygame.key.name(event.key))]
                    if event.key == pygame.K_SPACE and len(userStr) <= 25:
                        userStr += " "
                    if event.key == pygame.K_BACKSPACE:
                        userStr = userStr[:-1]
            pygame.display.flip()

        return userStr

    
        


