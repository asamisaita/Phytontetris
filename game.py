import sys
import tkinter

import pygame

import stage
import block


class Game:
    """
    ゲーム全体を管理するクラスです。
    このクラスを生成し、start()を呼び出すことで
    ゲームを開始させることが出来ます。
    """

    def __init__(self, title, width, height):
        """
        ゲームの各パラメータの状態を初期化し、
        ゲームを開始させる準備を整えます。

        title: ゲームのタイトル
        width: 画面の幅
        height: 画面の高さ
        """
        self.title = title
        self.width = width
        self.height = height
        self.root = tkinter.Tk()
        self.root.bind('<KeyPress>', self.__input)
        self.root.bind('<KeyPress>', self.sound)
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, bg='black')
        self.stage = stage.Stage()
        self.img_block = tkinter.PhotoImage(file='block.png')
        self.img_fix = tkinter.PhotoImage(file='fix.png')
        self.img_shadow = tkinter.PhotoImage(file='shadow.png')
        self.img_game_over = tkinter.PhotoImage(file='game_over.png')
        self.speed = 300

    def start(self):
        """
        ゲームを開始させるメソッドです。
        """
        self.__init()

    def __init(self):
        """
        ゲームの初期化を行うメソッドです。
        """
        pygame.init()
        try:
            self.bgm = pygame.mixer.music.load("bgm_maoudamashii_orchestra16.ogg")
            self.se = pygame.mixer.Sound("se_maoudamashii_system45.ogg")
        except:
            print("oggファイルが見当たらないか、audio機器が接続されてません")

        self.__make_window()
        self.__game_loop()
        self.root.mainloop()

    def __make_window(self):
        """
        ゲームの画面を作成するメソッドです。
        """
        self.root.title(self.title)
        self.canvas.pack()

    def __game_loop(self):
        """
        ゲームのメインロジックを定義するメソッドです。
        """
        self.__update()
        self.__render()
        if not self.stage.is_end():
            self.root.after(self.speed, self.__game_loop)
        else:
            self.__render(True)

    def __input(self, e):
        """
        ユーザからの入力処理を定義するメソッドです。
        """
        self.stage.input(e.keysym)

    def __update(self):
        """
        ゲーム全体の更新処理を定義するメソッドです。
        """
        self.stage.update()
        if self.stage.is_fix:
            # 速度を下げる
            self.speed -= 1

    def __render(self, is_end=False):
        """
        ゲームの描画処理を定義するメソッドです。
        """
        self.canvas.delete('block')

        for y in range(stage.Stage.HEIGHT):
            for x in range(stage.Stage.WIDTH):
                # ステージの各マスのデータを取得する
                cell_data = self.stage.data[y][x]

                if is_end:
                    # ゲームオーバーの画面を描画
                    if cell_data == stage.Stage.FIX:
                        # ゲームオーバーのブロックを描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,          # x座標
                            y * block.Block.SCALE,          # y座標
                            image=self.img_game_over,       # 描画画像
                            anchor='nw',                    # アンカー
                            tag='block'                     # タグ
                        )
                else:
                    # ゲームプレイ画面を描画
                    # 取得したマスのデータが空マスだった場合
                    """
                    if cell_data == stage.Stage.NONE:
                        # 黒色の32x32の四角を描画する
                        self.canvas.create_rectangle(
                            x * block.Block.SCALE,         # x0座標
                            y * block.Block.SCALE,         # y0座標
                            x * block.Block.SCALE + block.Block.SCALE,    # x1座標
                            y * block.Block.SCALE + block.Block.SCALE,    # y1座標
                            fill='black',   # 装飾色
                            tag='block'
                        )
                    """
                    # 取得したマスのデータがブロックだった場合
                    if cell_data == stage.Stage.BLOCK:
                        # ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,          # x座標
                            y * block.Block.SCALE,          # y座標
                            image=self.img_block,           # 描画画像
                            anchor='nw',                    # アンカー
                            tag='block'                     # タグ
                        )
                        """
                        # 白色の32x32の四角を描画する
                        self.canvas.create_rectangle(
                            x * block.Block.SCALE,         # x0座標
                            y * block.Block.SCALE,         # y0座標
                            x * block.Block.SCALE + block.Block.SCALE,    # x1座標
                            y * block.Block.SCALE + block.Block.SCALE,    # y1座標
                            fill='white',   # 装飾色
                            tag='block'
                        )
                        """
                    # 取得したマスのデータが固定されたブロックだった場合
                    if cell_data == stage.Stage.FIX:
                        # 固定ブロックの画像を描画する
                        self.canvas.create_image(
                            x * block.Block.SCALE,          # x座標
                            y * block.Block.SCALE,          # y座標
                            image=self.img_fix,             # 描画画像
                            anchor='nw',                    # アンカー
                            tag='block'                     # タグ
                        )
                        """
                        # 灰色の32x32の四角を描画する
                        self.canvas.create_rectangle(
                            x * block.Block.SCALE,         # x0座標
                            y * block.Block.SCALE,         # y0座標
                            x * block.Block.SCALE + block.Block.SCALE,    # x1座標
                            y * block.Block.SCALE + block.Block.SCALE,    # y1座標
                            fill='gray',    # 装飾色
                            tag='block'
                        )
                        """

        self.__render_shadow(is_end)

    def __render_shadow(self, is_end=False):
        """
        現在のテトリミノの影を描画するメソッドです。
        """
        type = self.stage.type
        rot = self.stage.rot
        x = self.stage.block.x
        # 影を描画するy座標を取得
        y = self.stage.shadow_position()

        if not is_end:
            for i in range(block.Block.SIZE):
                for j in range(block.Block.SIZE):
                    if self.stage.block.get_cell_data(type, rot, j, i) == stage.Stage.BLOCK:
                        # 影ブロックの画像を描画する
                        self.canvas.create_image(
                            (j + x) * block.Block.SCALE,          # x座標
                            (i + y) * block.Block.SCALE,          # y座標
                            image=self.img_shadow,             # 描画画像
                            anchor='nw',                    # アンカー
                            tag='block'                     # タグ
                        )
                        """
                        self.canvas.create_rectangle((j + x) * block.Block.SCALE,                       # x0座標
                                                     (i + y) * block.Block.SCALE,                       # y0座標
                                                     (j + x) * block.Block.SCALE + block.Block.SCALE,   # x1座標
                                                     (i + y) * block.Block.SCALE + block.Block.SCALE,   # y1座標
                                                     fill='black',                                      # 装飾色
                                                     outline='yellow',                                  # 枠線
                                                     tag='block')
                        """
    def sound(self, e):
        key = e.keysym

        if key == 'p':
            self.bgm.pygame.mixer.music.play(1)
        if key == 's':
            if pygame.mixer.music.get_busy() == True:
                pygame.mixer.music.stop()

        if key == 'space':
            self.se.play()
