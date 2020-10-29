import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
from aircraftwar_sprites import *


class AircraftWar(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("game initial...")
        pygame.init()
        # 创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 修改窗体显示名称
        pygame.display.set_caption('Aircraft War')
        # 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()

        AircraftWar.score = 0

        # 设置定时器事件 -
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)  # 创建敌机,每1s一架
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)   # 创建子弹,每500ms一次

    def __create_sprites(self):
        # 创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()
        # 创建销毁精灵组
        self.destroy_group = pygame.sprite.Group()
        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        """开始游戏"""
        print("game start...")

        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)

            # 2. 事件监听
            self.__event_handler()

            # 3. 碰撞检测
            self.__check_collide()

            # 4. 更新精灵组
            self.__update_sprites()

            # 5. 更新屏幕显示
            pygame.display.update()

    def __event_handler(self):
        """事件监听"""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                AircraftWar.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                # print("创建敌机...")
                # 创建敌机精灵
                enemy = Enemy()
                # 将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

            # 判断英雄是否已经被销毁，如果是，游戏结束！
            if self.hero.can_destroy:
                AircraftWar.__game_over()

            # 使用键盘提供的方法获取键盘按键 - 按键元组
            keys_pressed = pygame.key.get_pressed()
            # 判断元组中对应的按键索引值 1
            if keys_pressed[pygame.K_RIGHT]:
                self.hero.speed = 2
            elif keys_pressed[pygame.K_LEFT]:
                self.hero.speed = -2
            else:
                self.hero.speed = 0

    def __check_collide(self):
        """碰撞检测"""
        # 子弹摧毁敌机
        enemies = pygame.sprite.groupcollide(self.enemy_group,
                                             self.hero.bullets,
                                             False,
                                             True).keys()
        for enemy in enemies:
            enemy.life -= 1

            if enemy.life <= 0:
                enemy.add(self.destroy_group)
                enemy.remove(self.enemy_group)

                enemy.destroy()
                AircraftWar.score += 1

        # 敌机撞毁英雄
        for hero in pygame.sprite.spritecollide(self.hero,
                                                self.enemy_group,
                                                True):
            self.hero.destroy()

    def __update_sprites(self):
        """更新精灵组"""
        # self.back_group.update()
        # self.back_group.draw(self.screen)
        #
        # self.enemy_group.update()
        # self.enemy_group.draw(self.screen)
        #
        # self.hero_group.update()
        # self.hero_group.draw(self.screen)
        #
        # self.hero.bullets.update()
        # self.hero.bullets.draw(self.screen)
        #
        # self.destroy_group.update()
        # self.destroy_group.draw(self.screen)

        # 代码优化，通过循环遍历更新精灵组
        for group in [self.back_group, self.hero_group,
                      self.hero.bullets, self.enemy_group,
                      self.destroy_group]:
            group.update()
            group.draw(self.screen)

    @classmethod
    def __game_over(cls):
        """游戏结束"""
        print("game over...")
        print(f"Your Score is {cls.score}")
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    game = AircraftWar()

    # 开始游戏
    game.start_game()
