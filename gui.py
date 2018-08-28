import cocos
from cocos.director import director
from cocos.scenes import SlideInRTransition
from cocos.layer import ColorLayer

import pyglet
from pyglet.window import key, mouse

import sys

from hand_hm import HandHMLayer

"""
class AnimExample(cocos.layer.Layer):

    def __init__(self):
        super().__init__()
        img = pyglet.image.load('path/to/image.jpg')
        img_grid = pyglet.image.ImageGrid(img, rows=1, columns=1, item_width=100, item_height=100)
        anim = pyglet.image.Animation.from_image_sequence(img_grid[:], 0.1, loop=True)
        spr = cocos.sprite.Sprite(anim)
        spr.position = 100, 100
        spr.velocity = (0, 0)
        spr.do(MoverExample)
        self.add(spr)


class MoverExample(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.RIGHT] - keyboard[key.LEFT]) * 500
        vel_y = (keyboard[key.UP] - keyboard[key.DOWN]) * 500
        self.target.velocity = (vel_x, vel_y)
        scroller.set_focus(self.target.x, self.target.y)


class ScrollExample(cocos.layer.ScrollableLayer):
    def __init__(self):
        super().__init__()


"""


class SceneControlLayer(cocos.layer.Layer):
    is_event_handler = True
    active_scene = None

    def __init__(self):
        super().__init__()

    @staticmethod
    def on_mouse_press(x, y, button, modifiers):
        if button & mouse.LEFT:
            if SceneControlLayer.active_scene.name == 'Start':
                on_label = SceneControlLayer.active_scene.children[1][1].mouse_on_label(x, y)
                if on_label == 1:
                    SceneControlLayer.active_scene = ConfigScene()
                    director.replace(SlideInRTransition(SceneControlLayer.active_scene, duration=0.3))
                elif on_label == 2:
                    SceneControlLayer.active_scene = LoadScene()
                    director.replace(SlideInRTransition(SceneControlLayer.active_scene, duration=0.3))
            elif SceneControlLayer.active_scene.name == 'Config' or SceneControlLayer.active_scene.name == 'Load':
                SceneControlLayer.active_scene = GameScene()
                director.replace(SlideInRTransition(SceneControlLayer.active_scene, duration=0.3))
            # elif SceneControlLayer.active_scene.name == 'Game':
            #     SceneControlLayer.active_scene = StartScene()
            #     director.replace(SlideInRTransition(SceneControlLayer.active_scene, duration=0.3))
            else:
                pass


class StartScene(cocos.scene.Scene):
    name = 'Start'

    def __init__(self):
        super().__init__()
        self.add(StartPage())
        self.add(StartPageButtonLayer())
        self.add(SceneControlLayer())


class StartPage(cocos.layer.Layer):

    def __init__(self):
        super().__init__()

        self.bg = cocos.sprite.Sprite('images/startpage_800.png')
        wd_x, wd_y = director.get_window_size()
        self.bg.position = wd_x//2, wd_y//2
        self.add(self.bg)

        version = 0.4
        self.v_text = cocos.text.Label('v '+str(version)+' ', font_name='Times New Roman', font_size=14,
                                  x=0.68*wd_x, y=0.74*wd_y, anchor_x='left', anchor_y='bottom')
        self.add(self.v_text)


class StartPageButtonLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self):
        super().__init__()

        wd_x, wd_y = director.get_window_size()

        self.button1_off = pyglet.image.load('images/button/new_story.png')
        self.button1_on = pyglet.image.load('images/button/new_story_on.png')
        self.button2_off = pyglet.image.load('images/button/load_saves.png')
        self.button2_on = pyglet.image.load('images/button/load_saves_on.png')
        self.button3_off = pyglet.image.load('images/button/quit_game.png')
        self.button3_on = pyglet.image.load('images/button/quit_game_on.png')
        self.button1 = cocos.sprite.Sprite(self.button1_off)
        self.button1.position = wd_x//2, 0.4*wd_y
        self.button2 = cocos.sprite.Sprite(self.button2_off)
        self.button2.position = wd_x//2, 0.4*wd_y - self.button1.height
        self.button3 = cocos.sprite.Sprite(self.button3_off)
        self.button3.position = wd_x//2, 0.4*wd_y - 2* self.button1.height

        self.quit_confirm_off = pyglet.image.load('images/button/confirm.png')
        self.quit_sure_off = pyglet.image.load('images/button/sure.png')
        self.quit_sure_on = pyglet.image.load('images/button/sure_on.png')
        self.quit_cancel_off = pyglet.image.load('images/button/cancel.png')
        self.quit_cancel_on = pyglet.image.load('images/button/cancel_on.png')

        self.quit_confirm = cocos.sprite.Sprite(self.quit_confirm_off)
        self.quit_confirm.position = wd_x//2, 0.4*wd_y
        self.quit_confirm.visible = False
        self.quit_sure = cocos.sprite.Sprite(self.quit_sure_off)
        self.quit_sure.position = 0.45*wd_x, 0.4*wd_y - 54
        self.quit_sure.visible = False
        self.quit_cancel = cocos.sprite.Sprite(self.quit_cancel_off)
        self.quit_cancel.position = 0.55*wd_x, 0.4*wd_y - 54
        self.quit_cancel.visible = False

        self.add(self.button1)
        self.add(self.button2)
        self.add(self.button3)
        self.add(self.quit_confirm)
        self.add(self.quit_sure)
        self.add(self.quit_cancel)

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT:
            on_label = self.mouse_on_label(x, y)
            if on_label == 3:
                self.handle_exit()
            elif on_label == 4:
                sys.exit()
            elif on_label == 5:
                self.handle_exit()

    def on_mouse_motion(self, x, y, dx, dy):
        on_label = self.mouse_on_label(x, y)

        self.button1.image = self.button1_on if on_label == 1 else self.button1_off
        self.button2.image = self.button2_on if on_label == 2 else self.button2_off
        self.button3.image = self.button3_on if on_label == 3 else self.button3_off
        self.quit_sure.image = self.quit_sure_on if on_label == 4 else self.quit_sure_off
        self.quit_cancel.image = self.quit_cancel_on if on_label == 5 else self.quit_cancel_off

    def mouse_on_label(self, x, y):
        if self.button1.visible:
            if StartPageButtonLayer._on_button(x, y, self.button1):
                return 1
            elif StartPageButtonLayer._on_button(x, y, self.button2):
                return 2
            elif StartPageButtonLayer._on_button(x, y, self.button3):
                return 3
            else:
                return 0
        else:
            if StartPageButtonLayer._on_button(x, y, self.quit_sure):
                return 4
            elif StartPageButtonLayer._on_button(x, y, self.quit_cancel):
                return 5
            return 0

    def handle_exit(self):
        self.button1.visible = not self.button1.visible
        self.button2.visible = not self.button2.visible
        self.button3.visible = not self.button3.visible
        self.quit_confirm.visible = not self.quit_confirm.visible
        self.quit_sure.visible = not self.quit_sure.visible
        self.quit_cancel.visible = not self.quit_cancel.visible

    @staticmethod
    def _on_button(x, y, button):
        return abs(x-button.x) < 0.5*button.width and abs(y-button.y) < 0.5*button.height


class ConfigScene(cocos.scene.Scene):
    name = 'Config'

    def __init__(self):
        super().__init__()
        self.add(ColorLayer(204, 255, 204, 255, 800, 600))
        self.add(ConfigPage())
        self.add(SceneControlLayer())


class ConfigPage(cocos.layer.Layer):

    def __init__(self):
        super().__init__()

        self.pic = cocos.sprite.Sprite('images/construction.png')
        self.pic.position = 550, 150
        self.add(self.pic)

        self.text1 = cocos.text.Label('This page is for you to enter your name and configure game settings.',
                                      font_name='Times New Roman', color=(255, 102, 179, 255),
                                      anchor_x='center', font_size=18, x=400, y=350)
        self.text2 = cocos.text.Label('Click to continue.',
                                      font_name='Times New Roman', color=(255, 102, 179, 255),
                                      anchor_x='center', font_size=18, x=400, y=300)
        self.add(self.text1)
        self.add(self.text2)


class LoadScene(cocos.scene.Scene):
    name = 'Load'

    def __init__(self):
        super().__init__()
        self.add(ColorLayer(204, 255, 204, 255, 800, 600))
        self.add(LoadPage())
        self.add(SceneControlLayer())


class LoadPage(cocos.layer.Layer):

    def __init__(self):
        super().__init__()

        self.pic = cocos.sprite.Sprite('images/construction.png')
        self.pic.position = 550, 150
        self.add(self.pic)

        self.text1 = cocos.text.Label('This page is for you to choose a save to load from.',
                                      font_name='Times New Roman', color=(255, 102, 179, 255),
                                      anchor_x='center', font_size=18, x=400, y=350)
        self.text2 = cocos.text.Label('Click to continue.',
                                      font_name='Times New Roman', color=(255, 102, 179, 255),
                                      anchor_x='center', font_size=18, x=400, y=300)
        self.add(self.text1)
        self.add(self.text2)


class GameScene(cocos.scene.Scene):
    name = 'Game'

    def __init__(self):
        super().__init__()
        self.add(ColorLayer(204, 255, 204, 255, 800, 600))
        self.add(GamePage())
        self.add(SceneControlLayer())


class GamePage(cocos.layer.Layer):

    def __init__(self):
        super().__init__()

        self.avatar = cocos.sprite.Sprite('images/avatar.jpg', scale=0.25, anchor=(0, 0))

        # self.hand_hm = ColorLayer(255, 179, 255, 255, 400, 300)
        self.hand_hm = HandHMLayer()
        self.hand_hm.scale = 0.5
        self.hand_hm.anchor = (0, 0)
        self.hand_hm.position = 200, 0

        self.sets_hm = ColorLayer(255, 255, 179, 255, 200, 250)
        self.sets_hm.position = 600, 0

        self.table = ColorLayer(34, 177, 76, 255, 400, 200)
        self.table.position = 200, 300

        # self.buttons = ColorLayer(179, 179, 255, 255, 300, 50)
        # self.buttons.position = 250, 250

        self.settings = ColorLayer(255, 179, 179, 255, 800, 50)
        self.settings.position = 0, 550

        self.sets_cpt = ColorLayer(255, 255, 179, 255, 200, 250)
        self.sets_cpt.position = 0, 300

        self.hand_cpt = ColorLayer(255, 179, 255, 255, 400, 50)
        self.hand_cpt.position = 200, 500

        self.stella = cocos.sprite.Sprite('images/stella.jpg', position=(600, 350),
                                          scale=0.25, anchor=(0, 0))

        self.logs_hm = ColorLayer(255, 179, 179, 255, 200, 100)
        self.logs_hm.position = 0, 200

        self.logs_cpt = ColorLayer(255, 179, 179, 255, 200, 100)
        self.logs_cpt.position = 600, 250

        self.add(self.avatar)
        self.add(self.hand_hm)
        self.add(self.sets_hm)
        self.add(self.table)
        # self.add(self.buttons)
        self.add(self.settings)
        self.add(self.sets_cpt)
        self.add(self.hand_cpt)
        self.add(self.stella)
        self.add(self.logs_hm)
        self.add(self.logs_cpt)

        self.text_settings = BlackCenterLabel('存档 读档 悔棋 积分 音乐 音效 帮助 退出', 400, 575)
        self.text_hand_cpt = BlackCenterLabel('电脑手牌', 400, 525)
        self.text_table = BlackCenterLabel('牌桌', 400, 400)
        self.text_button = BlackCenterLabel('过 吃 碰 笑 掉 胡', 400, 280)
        self.text_logs_hm = BlackCenterLabel('回合信息', 100, 250)
        self.text_logs_cpt = BlackCenterLabel('回合信息', 700, 300)
        self.text_sets_hm = BlackCenterLabel('落地', 700, 125)
        self.text_sets_cpt = BlackCenterLabel('落地', 100, 425)

        self.add(self.text_settings)
        self.add(self.text_hand_cpt)
        self.add(self.text_table)
        self.add(self.text_button)
        self.add(self.text_logs_hm)
        self.add(self.text_logs_cpt)
        self.add(self.text_sets_hm)
        self.add(self.text_sets_cpt)


class BlackCenterLabel(cocos.text.Label):

    def __init__(self, text, x, y):
        super().__init__(text, (x, y), color=(0, 0, 0, 255), anchor_x='center', anchor_y='center', font_size=18)


if __name__ == "__main__":
    director.init(width=800, height=600, caption='Hengyang Zipai by Stella')

    image = pyglet.image.load('images/mouse/leaf.png')
    cursor = pyglet.window.ImageMouseCursor(image, 10, 28)
    director.window.set_mouse_cursor(cursor)

    # keyboard = key.KeyStateHandler()
    # director.window.push_handlers(keyboard)

    # scroller = cocos.layer.ScrollingManager()
    # scroller.add(bg_layer)

    SceneControlLayer.active_scene = StartScene()
    SceneControlLayer.active_scene_name = SceneControlLayer.active_scene.name

    director.run(SceneControlLayer.active_scene)