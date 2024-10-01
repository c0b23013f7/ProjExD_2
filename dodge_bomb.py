import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),pg.K_DOWN: (0, +5), pg.K_LEFT: (-5, 0), pg.K_RIGHT: (+5, 0),}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def game_over(screen, txt, fonto):
    """
    ゲームオーバーと表示させるリストを作成
    """
    black = pg.Surface(screen.get_size())  # 画面サイズのSurfaceを作成
    black.fill((0, 0, 0))  # 黒く塗りつぶす
    black.set_alpha(150)  # 半透明に
    
    screen.blit(black, (0, 0))  # 画面に描画
    screen.blit(txt, (530, 150))  # 泣いているこうかとんの画像を表示
    
    # Game Overの文字列を表示
    txt = fonto.render("Game Over", True, (255, 255, 255))  # 白い文字で表示
    screen.blit(txt, (400, 300))  # 文字の場所指定
    pg.display.update()  # 表示の更新

    time.sleep(5)



def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとん、または、爆弾のRect
    戻り値:真理数タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面内ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate   


def bombtime():
    """
    爆弾のサイズと加速度を段階的に変化させるリストを作成
    """
    bb_imgs = []
    bb_accs = [a for a in range(1, 11)]  # 加速度のリスト 
    
    for r in range(1, 11):  # 爆弾のサイズを1倍から10倍まで作成
        bb_img = pg.Surface((20*r, 20*r))  # サイズに応じたSurface作成
        bb_img.set_colorkey((0, 0, 0))  
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤い円
        bb_imgs.append(bb_img)
    
    return bb_imgs, bb_accs


def roto_zoom(kk_img):
    """
    キーの方向に応じて、こうかとん画像を回転させた辞書関数
    """
    roto= {
        (0, -5): pg.transform.rotozoom(kk_img, 90, 1.0),     # 上
        (0, +5): pg.transform.rotozoom(kk_img, -90, 1.0),    # 下
        (-5, 0): pg.transform.rotozoom(kk_img, 180, 1.0),    # 左
        (+5, 0): pg.transform.rotozoom(kk_img, 0, 1.0),      # 右
        (-5, -5): pg.transform.rotozoom(kk_img, 135, 1.0),   # 左上
        (-5, +5): pg.transform.rotozoom(kk_img, -135, 1.0),  # 左下
        (+5, -5): pg.transform.rotozoom(kk_img, 45, 1.0),    # 右上
        (+5, +5): pg.transform.rotozoom(kk_img, -45, 1.0)    # 右下
    }
    return roto

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # こうかとんの画像を読み込み、回転・拡大縮小する
    kk_rct = kk_img.get_rect()  # こうかとんのRectを取得
    kk_rct.center = 300, 200  # 初期位置を設定

    roto = roto_zoom(kk_img)  # こうかとんの画像を回転・拡大縮小する関数を呼び出す
    bb_imgs, bb_accs = bombtime()   # 爆弾の画像リストと加速度リストを取得する関数を呼び出す

    #bb_img = pg.Surface((20, 20))  # 空のSurface
    #bb_img.set_colorkey((0, 0, 0))  # 爆弾の四隅を透過させる
    #pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_imgs[0].get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾の速度


    clock = pg.time.Clock()
    tmr = 0
    fonto = pg.font.Font(None, 80)  # 任意のフォントとサイズを指定
    
    txt = pg.image.load("fig/8.png")  # 泣いているこうかとん画像
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なっていたら
            game_over(screen, txt, fonto)
            #print("GameOver")
            return
           
        avx = vx * bb_accs[min(tmr // 500, 9) ]  
        avy = vy * bb_accs[min(tmr // 500, 9) ]     
        bb_img = bb_imgs[min(tmr // 500, 9) ]  

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  #横座標 縦座標
        #if key_lst[pg.K_UP]:
            #sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
            #sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
            #sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
            #sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
