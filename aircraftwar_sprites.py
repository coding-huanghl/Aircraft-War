import random
import pygame

# 屏幕尺寸常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 屏幕刷新帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    """
    飞机大战游戏精灵类
    image_name: 要显示的图像名称
    speed: 飞行速度
    """
    def __init__(self, image_name, speed=1):
        # 因为继承的父类不是object类，所以一定要先super()一下父类的__init__方法
        super().__init__()
        # 加载图像
        self.image = pygame.image.load(image_name)
        # 设置尺寸
        self.rect = self.image.get_rect()
        # 记录速度（缺省值1）
        self.speed = speed

    def update(self, *args):
        # 默认在垂直方向移动(模拟动态效果)
        self.rect.y += self.speed

    @staticmethod
    def image_names(prefix, count):
        # 获取所有图片，添加到列表中
        names = []
        for i in range(1, count + 1):
            names.append("./images/" + prefix + str(i) + ".png")

        return names


class Background(GameSprite):
    """背景精灵"""
    def __init__(self, is_alt=False):
        super().__init__("./images/background.png")

        # 如果is_alt是True表示的是第二张背景图，初始状态显示在屏幕正上方
        if is_alt:
            self.rect.bottom = 0

    def update(self, *args):
        super().update(args)

        if self.rect.top >= SCREEN_RECT.height:
            self.rect.bottom = 0


class PlaneSprite(GameSprite):
    """飞机精灵，包括敌机和英雄"""
    def __init__(self, image_names, destroy_names, life, speed):

        image_name = image_names[0]
        super().__init__(image_name, speed)

        # 生命值
        self.life = life

        # 正常图像列表
        self.__life_images = []
        for file_name in image_names:
            image = pygame.image.load(file_name)
            self.__life_images.append(image)

        # 被摧毁图像列表
        self.__destroy_images = []
        for file_name in destroy_names:
            image = pygame.image.load(file_name)
            self.__destroy_images.append(image)

        # 默认播放生存图片
        self.images = self.__life_images
        # 显示图像索引
        self.show_image_index = 0
        # 是否循环播放
        self.is_loop_show = True
        # 是否可以被删除
        self.can_destroy = False

    def update(self, *args):
        self.update_images()

        super().update(args)

    def update_images(self):
        """更新图像"""
        pre_index = int(self.show_image_index)
        self.show_image_index += 0.05
        count = len(self.images)

        # 判断是否循环播放
        if self.is_loop_show:
            self.show_image_index %= len(self.images)
        elif self.show_image_index > count - 1:
            self.show_image_index = count - 1
            self.can_destroy = True

        current_index = int(self.show_image_index)

        if pre_index != current_index:
            self.image = self.images[current_index]

    def destroy(self):
        """飞机被摧毁"""

        # 默认播放生存图片
        self.images = self.__destroy_images
        # 显示图像索引
        self.show_image_index = 0
        # 是否循环播放
        self.is_loop_show = False


class Enemy(PlaneSprite):
    """敌机精灵"""
    def __init__(self):
        image_names = ["./images/enemy1.png"]
        destroy_names = GameSprite.image_names("enemy1_down", 4)

        # 调用父类方法,创建敌机精灵,并且指定敌机的图像
        super().__init__(image_names, destroy_names, 2, 1)
        # 设置敌机的随机初始速度1-3
        self.speed = random.randint(1, 3)
        # 设置敌机的随机初始位置
        width = SCREEN_RECT.width - self.rect.width  # 敌机出现的水平位置最右边值
        self.rect.left = random.randint(0, width)
        self.rect.bottom = 0

    def update(self, *args):
        # 调用父类方法，让敌机在垂直方向运动
        super().update(args)

        # 判断是否飞出屏幕，如果是，需要将敌机从精灵组删除
        if self.rect.y >= SCREEN_RECT.height:
            # print("敌机飞出屏幕...")
            # 将精灵从所有组中删除
            self.kill()

        # 判断敌机是否已经被销毁
        if self.can_destroy:
            self.kill()


class Hero(PlaneSprite):
    """英雄精灵"""

    def __init__(self):
        image_names = GameSprite.image_names("me", 2)
        destroy_names = GameSprite.image_names("me_destroy_", 4)

        super().__init__(image_names, destroy_names, 0, 0)
        # 设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 80
        # 创建子弹组
        self.bullets = pygame.sprite.Group()

    def update(self, *args):
        self.update_images()

        # 飞机水平移动
        self.rect.left += self.speed

        # 超出屏幕检测
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        # print("发射子弹...")
        # 每次连续发射3枚
        for i in range(0, 3):
            # 创建子弹精灵
            bullet = Bullet()

            # 设置子弹位置
            bullet.rect.bottom = self.rect.top - i * 20
            bullet.rect.centerx = self.rect.centerx

            # 将子弹添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    """子弹精灵"""
    def __init__(self):
        image_name = "./images/bullet1.png"
        super().__init__(image_name, -2)

    def update(self):
        super().update()

        # 判断是否超出屏幕，如果是，从精灵组删除
        if self.rect.bottom < 0:
            self.kill()
