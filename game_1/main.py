import pygame
from player import Player
from enemy import Enemy
from items import Triangle
from game import Game


def main():

    hight = 800
    width = 600

    game = Game(hight,width)
    player = Player(game.screen, 35, [300,765], 30)
    game.player = player
    tri = Triangle(game.screen, 40, 5)

    while not game.gameOver:

        game.gameMenu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.LEFT()
                elif event.key == pygame.K_RIGHT:
                    player.RIGHT()
                elif event.key == pygame.K_UP:
                    player.UP()
                elif event.key == pygame.K_DOWN:
                    player.DOWN()

        game.refresh()
        player.drawSelf()

        if len(game.enemyList) < 15:
            game.wave += 1
            game.createWave()
            
        
        game.dropWave()    

        if tri.ACTIVE:
            tri.dropTriangle()
            transform = tri.detectCollision(player)
            if transform is True:
                player.shape = 'triangle'
        elif game.score%10 == 0:
            tri = Triangle(game.screen, 40, 5)

        game.scoreText()
        game.clock.tick(50)
        pygame.display.flip()


if __name__ == "__main__":
    
    main()


