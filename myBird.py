import pygame
import sys

class Bird():
    def __init__(self):
        self.posWidth = 200
        self.posHeight = 400
        self.birdImage = pygame.image.load("assets/1.png")
        self.dead = False 
        self.outBound = False
        self.gravity= 5

    def getRealTimeWidth(self):
        return self.posWidth

    def getRealTimeHeight(self):
        if self.dead:
            self.gravity +=  3 
        if self.posHeight <= 600:
            self.posHeight += self.gravity
        else:
            self.outBound = True
        return self.posHeight

    def jump(self):
        if not self.dead:
            self.posHeight -= 50
        if self.posHeight<0:
            self.outBound = True

    def setDead(self):
        self.dead = True
        self.birdImage = pygame.image.load("assets/dead.png")

class Pipeline():
    def __init__(self, w,h):
        self.posWidth = w
        self.posHeight = h

    def getRealTimeWidth(self):
        birdW =  globalData.bird.posWidth-globalData.bird.birdImage.get_width() 
        pipelineW =  globalData.topPipeline.posWidth + globalData.topImage.get_width()/2

        if birdW > pipelineW:
            if globalData.score_flag == 0:
                globalData.score += 1
                globalData.score_flag = 1

        self.posWidth -= 10
        if self.posWidth < -10:
            self.posWidth = 300
            globalData.score_flag = 0 
        return self.posWidth

    def getRealTimeHeight(self):
        return self.posHeight

def checkDead():
    if globalData.bird.dead:
        return True
    birdRect = pygame.Rect(globalData.bird.posWidth,globalData.bird.posHeight,
                           globalData.bird.birdImage.get_width(),
                          globalData.bird.birdImage.get_height())
    upPipeRect = pygame.Rect(globalData.topPipeline .posWidth,
                             globalData.topPipeline.posHeight,
                             globalData.topImage.get_width(),
                             globalData.topImage.get_height()
                            )
    downPipeRect = pygame.Rect(globalData.bottomPipeline.posWidth,
                               globalData.bottomPipeline.posHeight,
                               globalData.bottomImage.get_width(),
                              globalData.bottomImage.get_height())
    if birdRect.colliderect(upPipeRect) or birdRect.colliderect(downPipeRect):
        return True

    if globalData.bird.outBound:
        return True
    return False

def  show_gameover():
    size = [400,700]
    screen = pygame.display.set_mode(size)
    screen.blit(globalData.backImage,[0,0])
    fontPath="assets/SimSun.ttf"
    font = pygame.font.Font(fontPath, 50)  # 设置字体和大小


    final_text1 = "游戏结束!!"
    ft1_surf = font.render(final_text1, 1, (242, 3, 36))                             # 设置第一行文字颜色
    ft2_surf = font.render("Score:%s"%(globalData.score), 1, (242, 3, 36))                             # 设置第一行文字颜色
    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
    screen.blit(ft2_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 200])  # 设置第一行文字显示位置
    pygame.display.flip()


def  show_startgame():
    size = [400,700]
    screen = pygame.display.set_mode(size)
    screen.blit(globalData.backImage,[0,0])
    fontPath="assets/SimSun.ttf"
    font1 = pygame.font.Font(fontPath, 50)  # 设置字体和大小
    font2 = pygame.font.Font(fontPath, 20)  # 设置字体和大小


    final_text1 = "开始游戏"
    ft1_surf = font1.render(final_text1, 1, (242, 3, 36))                             # 设置第一行文字颜色
    ft2_surf = font2.render("按空格跳跃", 2, (242, 3, 36))
    ft3_surf = font2.render("按q退出", 3, (242, 3, 36))
    ft4_surf = font2.render("按a开始游戏", 4, (242, 3, 36))

    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
    screen.blit(ft2_surf, [screen.get_width() / 2 - ft2_surf.get_width() / 2, 200])  # 设置第一行文字显示位置
    screen.blit(ft3_surf, [screen.get_width() / 2 - ft3_surf.get_width() / 2, 230])  # 设置第一行文字显示位置
    screen.blit(ft4_surf, [screen.get_width() / 2 - ft4_surf.get_width() / 2, 260])  # 设置第一行文字显示位置
    pygame.display.flip()


def  show_rungame():
    size = [400,700]
    screen = pygame.display.set_mode(size)
    screen.blit(globalData.backImage,[0,0])

    screen.blit(globalData.topImage,[globalData.topPipeline.getRealTimeWidth()
                          ,globalData.topPipeline.getRealTimeHeight()])

    screen.blit(globalData.bottomImage,[globalData.bottomPipeline.getRealTimeWidth()
                             ,globalData.bottomPipeline.getRealTimeHeight()])

    if checkDead():
        globalData.bird.setDead()


    if globalData.bird.outBound:
        globalData.game_status = 2

    screen.blit(globalData.bird.birdImage,[globalData.bird.getRealTimeWidth(),globalData.bird.getRealTimeHeight()])

    fontPath="assets/SimSun.ttf"
    font = pygame.font.Font(fontPath, 50)  # 设置字体和大小


    final_text1 = "Score:%s"%(globalData.score)
    ft1_surf = font.render(final_text1, 1, (242, 3, 36))                             # 设置第一行文字颜色
    screen.blit(ft1_surf, [screen.get_width() / 2 - ft1_surf.get_width() / 2, 100])  # 设置第一行文字显示位置
    pygame.display.flip()


def  create_maps():
    game_status = globalData.game_status
    if  game_status == 1:
        return show_rungame()
    if game_status == 2:
        return show_gameover()
    return show_startgame()


def  main_loop():
    clock = pygame.time.Clock()              # 设置时钟
    globalData.game_status = 0
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if globalData.game_status ==  2:
                        globalData.reset()
                    globalData.game_status = 1
                if event.key == pygame.K_q:
                    sys.exit()
                if globalData.game_status != 2:
                    if event.key == pygame.K_SPACE:
                        globalData.bird.jump()
                    if event.key == pygame.K_b:
                        globalData.game_status = 2
        create_maps()

class GlobalData:
    def __init__(self):
        self.backImage = pygame.image.load("assets/background.png")
        self.topImage = pygame.image.load("assets/top.png")
        self.bottomImage = pygame.image.load("assets/bottom.png")
        self.bird  =  Bird()
        self.topPipeline = Pipeline(200,-300)
        self.bottomPipeline = Pipeline(200,500)
        self.game_status = 0
        self.score = 0
        self.score_flag = 0

    def reset(self):
        self.backImage = pygame.image.load("assets/background.png")
        self.topImage = pygame.image.load("assets/top.png")
        self.bottomImage = pygame.image.load("assets/bottom.png")
        self.bird  =  Bird()
        self.topPipeline = Pipeline(200,-300)
        self.bottomPipeline = Pipeline(200,500)
        self.game_status = 0
        self.score = 0
        self.score_flag = 0

if __name__ == '__main__':
    pygame.init()
    globalData = GlobalData()
    main_loop()
