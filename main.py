import game

# 　ゲームのタイトル
title = 'テトリス'
# 　画面の幅
width = 32 * 10
# 画面の高さ
height = 32 * 20

tetris = game.Game(title, width, height)
tetris.start()
