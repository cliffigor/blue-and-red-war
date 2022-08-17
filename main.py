#!/usr/bin/python#-*-coding:utf-8-*-
import sys
import random

from PyQt5.QtWidgets import QApplication

from map import SetMap


class Game():
    """游戏主体"""

    def __init__(self):
        """初始化"""
        self.land = MapInit()
        self.init_extend_map()
        self.player = Player(2)
        self.listen()

    def init_extend_map(self):
        """
        扩展地图初始化
        """
        self.land.define_terrain()
        # 禁止通过地形
        self.disable = []
        self.chess = self.land.chess_name
        self.check(sign=1)

    def listen(self):
        """
        建立鼠标监听事件
        """
        for button in self.land.cache:
            button.clicked.connect(self.record)

    def record(self):
        """
        判断点击来源
        """
        send = self.land.sender()
        self.chess = send.text()
        self.check()

    def check(self, sign=0):
        """
        检查移动条件
        :param sign: 0->人类棋子; 1->高山
        """
        site = None
        permit = None
        for i in range(len(self.land.cache)):
            if self.land.cache[i].text() == self.chess:
                site = i
                # 遍历禁止地形
                for disable in self.disable:
                    if self.land.cache[i] == disable:
                        site = None
        # 安全检查通过，允许进军
        if site != None:
            # 检查为人类棋子
            if sign == 0:
                # permit控制，还没写
                if True:
                    self.march(site)
            # 检查为高山地形
            if sign == 1:
                self.flag(self.land.cache[site], 'green')
                self.disable.append(self.land.cache[site])

    def march(self, site):
        """
        棋子移动
        :param site: 
        """
        # 保证交替下棋
        color = self.player.flag[self.player.id[self.player.round_now]]
        if site != None:
            # 持续隐藏字体
            self.flag(self.land.cache[site], color)
        # 储存玩家下的棋子的位置
            self.player.chess_map[self.player.round_now].append(
                self.land.cache[site].text())
        self.player.player_round()

    def flag(self, chess, color):
        """
        棋子染色
        :param chess: 要染色的棋子
        :param color: 染后的颜色
        """
        chess.setStyleSheet("color : rgb(0,0,0,0);\n"
                            "background-color : {}".format(color))


class Player():
    """
    玩家信息
    """
    # 储存累计回合数
    round = 0
    round_now = None

    def __init__(self, player_number):
        # 储存身分组信息
        self.id = None
        self.flag = ['red', 'blue', 'yellow', 'black']
        self.chess_map = []
        self.player_chess(player_number)
        self.player_number = player_number
        self.player_round()

    def player_chess(self, player_number):
        """玩家的棋子信息"""
        id = []
        for i in range(player_number):
            id.append(i)

            self.chess_map = [[]
                              for x in range(player_number)]  # 创建储存玩家拥有棋子的位置
        self.id = id
        # print(self.chess_map)

    def player_round(self):
        """判断当前回合"""
        self.round_now = self.round % self.player_number  # 当前回合记录
        self.round += 1


class MapInit(SetMap):
    def __init__(self):
        """地图初始化"""
        super(MapInit, self).__init__()

    def extend_map(self):
        """扩展地图"""
        pass

    def define_terrain(self):
        """随机位置生成一座高山"""
        self.chess_name = str(
            (random.randint(0, self.size_x - 1), random.randint(0, self.size_y - 1)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Game()
    w.land.show()
    app.exec()
