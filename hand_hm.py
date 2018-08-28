import cocos
from cocos.director import director

import pyglet
from pyglet.window import mouse

import random


class HandHMLayer(cocos.layer.Layer):

    def __init__(self):
        super().__init__()
        self.add(cocos.sprite.Sprite('images/mag.png', (0, 0), anchor=(0,0)), -601)
        self.setup = HandHMLayer.sort_setup(HandHMLayer.deal())
        self.refresh(self.setup, True)

    @staticmethod
    def deal():
        deck = []
        for i in range(10):
            deck.extend([i + 1, i + 101] * 4)
        random.shuffle(deck)

        hand = []
        for slot in range(7):
            s = []
            for rank in range(3):
                s.append(deck[slot*3+rank])
            hand.append(s)
        return hand

    def refresh(self, setup, new=False):
        setup = HandHMLayer.sort_setup(setup)
        if not new:
            for i in range(len(self.setup)):
                for j in range(len(self.setup[i])):
                    self.remove(str(i*10+j))
        for i, slot in enumerate(setup):
            for j, num in enumerate(slot):
                card = CardLayer(num, i, j)
                self.add(card, -card.y, str(i*10+j))
        self.setup = setup
        # print(self.setup)

    @staticmethod
    def sort_setup(setup):
        return [sorted(x, reverse=True) for x in setup]


class CardLayer(cocos.layer.Layer):

    is_event_handler = True

    def __init__(self, order, slot, rank):
        super().__init__()
        self.slot = slot
        self.rank = rank
        self.name = str(slot*10+rank)
        self.order = order
        self.width = 100
        self.height = 192
        self.anchor = (0, 0)
        self.position = (self.slot*110+20, self.rank*100+20)

        self.pic = cocos.sprite.Sprite('images/card/{}.png'.format(order), anchor=(0, 0), scale=100/184)
        self.add(self.pic)

        self.clicked = False

    def mouse_on_me(self, x, y):
        x_, y_ = self.coord_trans(x, y)
        if self.rank == 0:
            return self.children[0][1].contains(x_-self.x, y_-self.y)
        else:
            return self.children[0][1].contains(x_-self.x, y_-self.y) and self.y+self.height-y_ < 100

    # def on_mouse_motion(self, x, y, dx, dy):
    #     if self.mouse_on_me(x, y):
    #         print(self.order)

    def on_mouse_press(self, x, y, button, modifiers):
        if button & mouse.LEFT and self.mouse_on_me(x, y):
            self.clicked = True

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.clicked:
            scale = self.parent.scale
            self.position = (self.x + dx/scale, self.y + dy/scale)

    def on_mouse_release(self, x, y, button, modifiers):
        if not self.clicked:
            return

        self.clicked = False

        new_slot = self._get_new_slot()
        if new_slot == self.slot:
            self.position = (self.slot * 110 + 20, self.rank * 100 + 20)
        else:
            i, j = int(self.name)//10, int(self.name)%10
            new_setup = [[x for x in s] for s in self.parent.setup]
            num = new_setup[i].pop(j)
            new_setup[new_slot].append(num)
            self.parent.refresh(new_setup)

    def _get_new_slot(self):
        dist = [[slot, abs(self.x-(slot*100+20))] for slot in range(7)]
        for i in range(7):
            if len(self.parent.setup[i]) == 4:
                dist[i][1] = 1000
        dist.sort(key=lambda x: x[1])
        return dist[0][0]

    def coord_trans(self, x, y):
        # transfer mouse coord from game window to hand area
        # px, py are the position of hand area, scale is the scale of this area in game window
        # area anchor is 0, 0
        scale = self.parent.scale
        px, py = self.parent.position
        return (x-px)/scale, (y-py)/scale


    # def set_z(self):
    #     if not self.parent:
    #         return
    #     for i in range(len(self.parent.children)):
    #         if self.parent.children[i][1] == self:
    #             self.parent.children.pop(i)
    #             self.parent.children.append((-self.y, self))
    #             break
    #     self.parent.children.sort(key=lambda x: x[0])
    #     return


class CardBackSprite(cocos.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__('images/card/back.png', position=(x, y), anchor=(0, 0))


if __name__ == "__main__":
    director.init(width=800, height=600, caption='Hengyang Zipai by Stella')

    image = pyglet.image.load('images/mouse/leaf.png')
    cursor = pyglet.window.ImageMouseCursor(image, 10, 28)
    director.window.set_mouse_cursor(cursor)

    card_scene = cocos.scene.Scene()
    hand_hm = HandHMLayer()

    card_scene.add(hand_hm)

    director.run(card_scene)
