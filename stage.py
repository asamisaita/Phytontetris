import block
import random


class Stage:
    """
   テトリスの盤面を管理するクラスです。
   """
    WIDTH = 10  # 盤面の幅
    HEIGHT = 20  # 盤面の高さ
    NONE = 0  # 空マス
    BLOCK = 1  # ブロックマス
    FIX = 2  # 固定ブロックマス

    def __init__(self):
        """
       盤面を生成させます。
       """

        self.data = [[Stage.NONE for i in range(Stage.WIDTH)] for j in range(Stage.HEIGHT)]
        self.block = block.Block()
        self.type = 0
        self.rot = 0
        self.can_drop = True
        self.remove_line = [False for i in range(Stage.HEIGHT)]
        self.is_fix = False
        self.__select_block()

    def update(self):
        """
       ステージの更新処理を行うメソッドです。
       """
        self.__marge_block()
        # もし下方向に衝突しない場合
        if not self.is_collision_bottom():
            self.is_fix = False
            if self.can_drop:
                self.__drop_block()
        # もし衝突する場合
        else:
            self.is_fix = True
            self.__fix_block()
            self.__check_remove_lines()
            self.__remove_lines()
            self.block.reset()
            self.__select_block()
        self.__marge_block()

    def input(self, key):
        """
        キー入力を受け付けるメソッドです。
        各キーの入力に対しての処理を記述してください。
        """
        if key == 'space':  # スペース
            self.can_drop = not self.can_drop
        # Wキー
        if key == 'w':
            self.__rotation_block()

        if key == 'a':
            if not self.is_collision_left():
                self.block.x -= 1

        if key == 's':
            self.hard_drop()
        # Dキー
        if key == 'd':
            if not self.is_collision_right():
                self.block.x += 1

    def __select_block(self):
        """
        ブロックの種類と角度をランダムに選びます。
        """
        # ランダムにブロックの種類を選ぶ
        self.type = random.randint(0, block.Block.TYPE_MAX - 1)
        # ランダムにブロックの角度を選ぶ
        self.rot = random.randint(0, block.Block.ROT_MAX - 1)

    def __rotation_block(self):
        """
        ブロックを回転させるメソッドです
        """
        if self.__can_rotation_block():
            self.rot += 1
            if self.rot == block.Block.ROT_MAX:
                self.rot = 0

    def __can_rotation_block(self):
        """
        現在のブロックが回転可能か判定するメソッドです。
        回転することができるのであればTrueを返却し、
        そうでなければ、Falseを返却します。
        """
        # 次の角度
        n_rot = (self.rot + 1) % block.Block.ROT_MAX
        # ブロックの座標
        b_x = self.block.x
        b_y = self.block.y
        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                #  次の角度のブロック情報を取得する
                if self.block.get_cell_data(self.type, n_rot, j, i) == Stage.BLOCK:
                    # 範囲外チェック
                    if self.is_out_of_stage(b_x + j, b_y + i):
                        return False
                    # 固定ブロックとの衝突チェック
                    if self.data[b_y + i][b_x + j] == Stage.FIX:
                        return False

        return True

    def __drop_block(self):
        """
        ブロックを１段下げるメソッドです。
        """

        self.block.y += 1

    def __marge_block(self):
        """
       ステージのデータにブロックのデータをマージするメソッドです。
       """
        b_t = self.type
        b_r = self.rot
        b_x = self.block.x
        b_y = self.block.y

        # ステージの状態を一度リセット
        for i in range(Stage.HEIGHT):
            for j in range(Stage.WIDTH):
                if self.data[i][j] == Stage.BLOCK:
                    self.data[i][j] = Stage.NONE

        # ブロックデータをステージに反映
        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    if not self.is_out_of_stage(b_x + j, b_y + i):
                        self.data[b_y + i][b_x + j] = Stage.BLOCK

    def __fix_block(self):
        """
       ブロックを固定するメソッドです。
       """
        b_t = self.type
        b_r = self.rot
        b_x = self.block.x
        b_y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    self.data[b_y + i][b_x + j] = Stage.FIX

    def is_out_of_stage(self, x, y):
        """
       指定されたステージの座標が範囲外かを調べるメソッドです。
       x: ステージセルのX軸
       y: ステージセルのY軸
       """

        return x < 0 or x >= Stage.WIDTH or y < 0 or y >= Stage.HEIGHT

    def is_collision_bottom(self, x=-1, y=-1):
        """
       下方向の衝突判定を行うメソッドです。
       衝突していればTrueが返却され、そうでなければFalseが返却されます。
       x: 対象のブロックのX軸座標
       y: 対象のブロックのY軸座標
       """
        b_t = self.type
        b_r = self.rot

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ下げたマスが
                    # 　ステージの範囲外だった場合
                    if self.is_out_of_stage(x + j, y + i + 1):
                        return True
                    # 　対象のブロックマスの位置から１つ下げたマスが
                    #   固定されたブロックのマス（２）だった場合
                    if self.data[y + i + 1][x + j] == Stage.FIX:
                        return True
                    # 　どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def is_collision_left(self, x=-1, y=-1):
        """
        下方向の衝突判定を行うメソッドです。
        衝突していればTrueが返却され、そうでなければFalseが返却されます。
        x: 対象のブロックのX軸座標
        y: 対象のブロックのY軸座標
        """
        b_t = self.type
        b_r = self.rot

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ左のマスが
                    # 　ステージの範囲外だった場合
                    if self.is_out_of_stage(x + j - 1, y + i + 1):
                        return True
                    # 　対象のブロックマスの位置から１つ左マスが
                    #   固定されたブロックのマス（２）だった場合
                    if self.data[y + i + 1][x + j - 1] == Stage.FIX:
                        return True
                    # 　どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def is_collision_right(self, x=-1, y=-1):
        """
       下方向の衝突判定を行うメソッドです。
       衝突していればTrueが返却され、そうでなければFalseが返却されます。
       x: 対象のブロックのX軸座標
       y: 対象のブロックのY軸座標
       """
        b_t = self.type
        b_r = self.rot

        if x == -1 and y == -1:
            x = self.block.x
            y = self.block.y

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                # 取得したブロックの１マスのデータがBLOCK(1)だった場合
                if self.block.get_cell_data(b_t, b_r, j, i) == Stage.BLOCK:
                    # 対象のブロックマスの位置から１つ右マスが
                    # 　ステージの範囲外だった場合
                    if self.is_out_of_stage(x + j + 1, y + i + 1):
                        return True
                    # 　対象のブロックマスの位置から１つ右マスが
                    #   固定されたブロックのマス（２）だった場合
                    if self.data[y + i + 1][x + j + 1] == Stage.FIX:
                        return True
                    # 　どの条件にも当てはまらない場合は常にどこにも衝突していない
        return False

    def hard_drop(self, x=-1, y=-1):
        while not self.is_collision_bottom():
            self.__drop_block()

    def __check_remove_lines(self):
        """
        消える例をチェックするメソッドです
        """

        for i in range(Stage.HEIGHT):
            flg = True
            for j in range(Stage.WIDTH):
                if self.data[i][j] != Stage.FIX:
                    flg = False
                    break
            self.remove_line[i] = flg

    def __remove_lines(self):
        # 置き換え先の列を参照するポインタ
        idx = Stage.HEIGHT - 1

        # そろっている列の削除（NONEにする）
        for i in range(Stage.HEIGHT):
            if self.remove_line[i]:
                for j in range(Stage.WIDTH):
                    self.data[i][j] = Stage.NONE

        # そろっていない列をしたの列から積み上げなおす
        for i in reversed(range(Stage.HEIGHT)):
            # 　もし、対象の列がそろっていなかった場合
            if not self.remove_line[i]:
                for j in range(Stage.WIDTH):
                    # 置き換え先の列にそろっていない列を代入する
                    self.data[idx][j] = self.data[i][j]
                # 置き換え先の列を参照するポインタを１列上げる
                idx -= 1

    def shadow_position(self):
        """
        テトリミノの影を作るｙ座標を計算してそのｙ座標を返却します。
        """
        # 現在のブロックの座標を退避
        tx = self.block.x
        ty = self.block.y

        while not self.is_collision_bottom(tx, ty):
            ty += 1

        return ty

    def is_end(self):
        """
        テトリスのゲームオーバー判定を行うメソッドです。
        ゲームオーバーであればTrueを返却し、
        そうでなければFalseを返却します。
        """
        x = self.block.x
        y = self.block.y
        t = self.type
        r = self.rot

        for i in range(block.Block.SIZE):
            for j in range(block.Block.SIZE):
                cell_data = self.block.get_cell_data(t, r, j, i)
                if cell_data == Stage.BLOCK:
                    # 範囲外チェック
                    if not self.is_out_of_stage(x + j, y + i):
                        # 衝突チェック
                        if self.data[y + i][x + j] == Stage.FIX:
                            return True

        return False
