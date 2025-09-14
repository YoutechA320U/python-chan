import os, io, random, bisect, queue
import pygame
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor

# -------------------------------------------------
# 監視するテキストファイルと設定
# -------------------------------------------------
TEXT_FILE = "message.txt"          # 監視対象ファイル（相対パスでも絶対パスでも可）
VOICOVOX_URL = "http://127.0.0.1:50021"
IMG_PATH =  ".\\img_data\\"
BASE_FACE = IMG_PATH+"avatar_base.png"
WINDOW_W, WINDOW_H = 320, 240
FPS = 60
try:
 os.remove(TEXT_FILE)
except:
    pass
# 口形画像
MOUTH_IMAGES = {
    "A": IMG_PATH+"mouth_A.png", "I": IMG_PATH+"mouth_I.png", "U": IMG_PATH+"mouth_U.png",
    "E": IMG_PATH+"mouth_E.png", "O": IMG_PATH+"mouth_O.png", "N": IMG_PATH+"mouth_N.png",
    "C": IMG_PATH+"mouth_closed.png",
}

# 目画像
EYE_IMAGES = {
    "open":   IMG_PATH+"eyes_open.png",
    "closed": IMG_PATH+"eyes_closed.png",
}

# -------------------------------------------------
# VOICEVOX設定
# -------------------------------------------------
SPEAKER_ID = 3  #話者ID。3はずんだもん（ノーマル）
SPEEDSCALE=1.0  #話速
PITCHSCALE=0.0  #音高
INTONATIONSCALE=1.0 #抑揚
VOLUMESCALE=1.0 #音量
PREPHONEMELENGTH=0.1    #開始無音
POSTPHONEMELENGTH=0.1   #終了無音
PAUSELENGTHSCALE=1.0    #間の長さ

#※話者ID一覧
#四国めたん, ノーマル id: 2
#四国めたん, あまあま id: 0
#四国めたん, ツンツン id: 6
#四国めたん, セクシー id: 4
#四国めたん, ささやき id: 36
#四国めたん, ヒソヒソ id: 37
#ずんだもん, ノーマル id: 3
#ずんだもん, あまあま id: 1
#ずんだもん, ツンツン id: 7
#ずんだもん, セクシー id: 5
#ずんだもん, ささやき id: 22
#ずんだもん, ヒソヒソ id: 38
#ずんだもん, ヘロヘロ id: 75
#ずんだもん, なみだめ id: 76
#春日部つむぎ, ノーマル id: 8
#雨晴はう, ノーマル id: 10
#波音リツ, ノーマル id: 9
#波音リツ, クイーン id: 65
#玄野武宏, ノーマル id: 11
#玄野武宏, 喜び id: 39
#玄野武宏, ツンギレ id: 40
#玄野武宏, 悲しみ id: 41
#白上虎太郎, ふつう id: 12
#白上虎太郎, わーい id: 32
#白上虎太郎, びくびく id: 33
#白上虎太郎, おこ id: 34
#白上虎太郎, びえーん id: 35
#青山龍星, ノーマル id: 13
#青山龍星, 熱血 id: 81
#青山龍星, 不機嫌 id: 82
#青山龍星, 喜び id: 83
#青山龍星, しっとり id: 84
#青山龍星, かなしみ id: 85
#青山龍星, 囁き id: 86
#冥鳴ひまり, ノーマル id: 14
#九州そら, ノーマル id: 16
#九州そら, あまあま id: 15
#九州そら, ツンツン id: 18
#九州そら, セクシー id: 17
#九州そら, ささやき id: 19
#もち子さん, ノーマル id: 20
#もち子さん, セクシー／あん子 id: 66
#もち子さん, 泣き id: 77
#もち子さん, 怒り id: 78
#もち子さん, 喜び id: 79
#もち子さん, のんびり id: 80
#剣崎雌雄, ノーマル id: 21
#WhiteCUL, ノーマル id: 23
#WhiteCUL, たのしい id: 24
#WhiteCUL, かなしい id: 25
#WhiteCUL, びえーん id: 26
#後鬼, 人間ver. id: 27
#後鬼, ぬいぐるみver. id: 28
#後鬼, 人間（怒り）ver. id: 87
#後鬼, 鬼ver. id: 88
#No.7, ノーマル id: 29
#No.7, アナウンス id: 30
#No.7, 読み聞かせ id: 31
#ちび式じい, ノーマル id: 42
#櫻歌ミコ, ノーマル id: 43
#櫻歌ミコ, 第二形態 id: 44
#櫻歌ミコ, ロリ id: 45
#小夜/SAYO, ノーマル id: 46
#ナースロボ＿タイプＴ, ノーマル id: 47
#ナースロボ＿タイプＴ, 楽々 id: 48
#ナースロボ＿タイプＴ, 恐怖 id: 49
#ナースロボ＿タイプＴ, 内緒話 id: 50
#†聖騎士 紅桜†, ノーマル id: 51
#雀松朱司, ノーマル id: 52
#麒ヶ島宗麟, ノーマル id: 53
#春歌ナナ, ノーマル id: 54
#猫使アル, ノーマル id: 55
#猫使アル, おちつき id: 56
#猫使アル, うきうき id: 57
#猫使アル, つよつよ id: 110
#猫使アル, へろへろ id: 111
#猫使ビィ, ノーマル id: 58
#猫使ビィ, おちつき id: 59
#猫使ビィ, 人見知り id: 60
#猫使ビィ, つよつよ id: 112
#中国うさぎ, ノーマル id: 61
#中国うさぎ, おどろき id: 62
#中国うさぎ, こわがり id: 63
#中国うさぎ, へろへろ id: 64
#栗田まろん, ノーマル id: 67
#あいえるたん, ノーマル id: 68
#満別花丸, ノーマル id: 69
#満別花丸, 元気 id: 70
#満別花丸, ささやき id: 71
#満別花丸, ぶりっ子 id: 72
#満別花丸, ボーイ id: 73
#琴詠ニア, ノーマル id: 74
#Voidoll, ノーマル id: 89
#ぞん子, ノーマル id: 90
#ぞん子, 低血圧 id: 91
#ぞん子, 覚醒 id: 92
#ぞん子, 実況風 id: 93
#中部つるぎ, ノーマル id: 94
#中部つるぎ, 怒り id: 95
#中部つるぎ, ヒソヒソ id: 96
#中部つるぎ, おどおど id: 97
#中部つるぎ, 絶望と敗北 id: 98
#離途, ノーマル id: 99
#離途, シリアス id: 101
#黒沢冴白, ノーマル id: 100
#ユーレイちゃん, ノーマル id: 102
#ユーレイちゃん, 甘々 id: 103
#ユーレイちゃん, 哀しみ id: 104
#ユーレイちゃん, ささやき id: 105
#ユーレイちゃん, ツクモちゃん id: 106
#東北ずん子, ノーマル id: 107
#東北きりたん, ノーマル id: 108
#東北イタコ, ノーマル id: 109

# -------------------------------------------------
# 画像キャッシュ（起動時に一括ロード）
# -------------------------------------------------
def load_images():
    base_img   = pygame.image.load(BASE_FACE).convert_alpha()
    mouth_imgs = {k: pygame.image.load(v).convert_alpha()
                  for k, v in MOUTH_IMAGES.items()}
    eye_imgs   = {"open":   pygame.image.load(EYE_IMAGES["open"]).convert_alpha(),
                  "closed": pygame.image.load(EYE_IMAGES["closed"]).convert_alpha()}
    return base_img, mouth_imgs, eye_imgs

# -------------------------------------------------
# VOICEVOX 合成（バックグラウンドで実行）
# -------------------------------------------------
def synthesize(text):
    aq = requests.post(
        f"{VOICOVOX_URL}/audio_query",
        params={"text": text, "speaker": SPEAKER_ID}
    ).json()
    aq['speedScale'] = SPEEDSCALE
    aq['pitchScale'] = PITCHSCALE
    aq['intonationScale'] = INTONATIONSCALE
    aq['volumeScale'] = VOLUMESCALE
    aq['prePhonemeLength'] = PREPHONEMELENGTH
    aq['postPhonemeLength'] =  POSTPHONEMELENGTH
    aq['pauseLengthScale'] =   PAUSELENGTHSCALE

    wav = requests.post(
        f"{VOICOVOX_URL}/synthesis",
        params={"speaker": SPEAKER_ID, "output_sampling_rate": 24000},
        json=aq
    ).content
    return wav, aq

# -------------------------------------------------
# 口形テーブル作成（ms → key）※ O(1) で取得できるようにする
# -------------------------------------------------
def build_lip_sync_table(aq, insert_closed_ms=50):
    speed = aq["speedScale"]
    table = []               # [(end_time_ms, key), ...]
    cur_ms = 0
    prev_vowel = None        # 直前に出力した母音（大文字）

    for phrase in aq["accent_phrases"]:
        moras = phrase["moras"]
        for i, mora in enumerate(moras):
            # 1. 文字情報 → キー取得
            key = (
                "C"
                if mora["consonant"] and not mora["vowel"]
                else mora["vowel"].upper()
            )
            key = key if key in MOUTH_IMAGES else "C"

            # 2. 長さ計算（consonant + vowel） → ms
            cons_len = mora["consonant_length"] or 0.0
            vowel_len = mora["vowel_length"]
            length_ms = int(round((cons_len + vowel_len) / speed * 1000))

            # 3. **同じ母音が続く場合**、閉じ口を先に入れる
            if prev_vowel is not None and key == prev_vowel:
                # 　閉じ口 (C) を挿入
                cur_ms += insert_closed_ms
                table.append((cur_ms, "C"))
                # 　残りの時間は元の長さから差し引く
                length_ms = max(0, length_ms - insert_closed_ms)

            # 4. 現在のモーラをテーブルへ
            cur_ms += length_ms
            table.append((cur_ms, key))

            # 5. 次の比較用に保存
            prev_vowel = key if key != "C" else None   # C のときはリセット

        # -------------------------------------------------
        # ポーズがあれば（pause_mora は必ず C にする）
        # -------------------------------------------------
        if phrase.get("pause_mora"):
            pause_ms = int(round(
                phrase["pause_mora"]["vowel_length"] / speed * 1000))
            cur_ms += pause_ms
            table.append((cur_ms, "C"))
            prev_vowel = None     # ポーズの後はリセット

    # 末尾に必ず閉じた口を入れる（安全策）
    table.append((cur_ms, "C"))
    return table

def lookup_mouth_key(table, elapsed_ms):
    idx = bisect.bisect_right(table, (elapsed_ms, ""))
    if idx == 0:
        return "C"
    return table[idx-1][1]

# -------------------------------------------------
# ファイル監視ハンドラ（watchdog）
# -------------------------------------------------
class TextFileHandler(FileSystemEventHandler):
    def __init__(self, q):
        super().__init__()
        self.q = q                 # 合成結果を入れる queue.Queue

    def on_created(self, event):
        if event.src_path.endswith(TEXT_FILE):
            # ファイルが出来たら内容を読むだけでキューに入れる
            try:
                with open(event.src_path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                #os.remove(event.src_path)    # すぐ削除（二重処理防止）
                self.q.put_nowait(text)
            except Exception as e:
                print("ファイル読み取りエラー:", e)
                
# -------------------------------------------------
# 乱れ（jitter）ロジック
# -------------------------------------------------
JITTER_MAX_OFFSET = 40      # ピクセル
JITTER_MAX_ANGLE  = 2       # 度
JITTER_PROB_MOVE  = 0.10    # 1 フレームで動く確率
JITTER_PROB_ROT   = 0.08    # 1 フレームで回転する確率
JITTER_DELAY_MS   = 2000    # 「無音状態」から揺れを始めるまでの遅延

def _clamp(v, lo, hi):
    return max(lo, min(hi, v))

def update_jitter(offset, angle):
    # --- 位置 ---
    if random.random() < JITTER_PROB_MOVE:
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        offset[0] = _clamp(offset[0] + dx, -JITTER_MAX_OFFSET, JITTER_MAX_OFFSET)
        offset[1] = _clamp(offset[1] + dy, -JITTER_MAX_OFFSET, JITTER_MAX_OFFSET)

    # --- 回転 ---
    if random.random() < JITTER_PROB_ROT:
        dθ = random.choice([-1, 0, 1])
        angle = _clamp(angle + dθ, -JITTER_MAX_ANGLE, JITTER_MAX_ANGLE)

    return offset, angle

# -------------------------------------------------
# メインループ（高速・高精度版）
# -------------------------------------------------
talking=False
def main():
    global talking
    pygame.init()
    pygame.mixer.init(frequency=24000)

    # 初期サイズは定数だが、RESIZABLE フラグでサイズ変更可能にする
    win_w, win_h = WINDOW_W, WINDOW_H
    screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
    pygame.display.set_caption("ﾊﾟｲｿﾝﾁｬﾝ")
    clock = pygame.time.Clock()

    # 画像は一括ロードしてキャッシュ（オリジナルサイズで保持）
    base_img, mouth_imgs, eye_imgs = load_images()

    # 合成タスク用スレッドプール
    executor = ThreadPoolExecutor(max_workers=1)

    # テキスト受信用キュー（watchdog → メインスレッドへ）
    txt_queue = queue.Queue()
    event_handler = TextFileHandler(txt_queue)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()

    # 瞬きタイマー（pygame のカスタムイベントを使う）
    BLINK_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BLINK_EVENT, random.randint(1000, 3000))

    # 再生中情報
    channel = None
    lip_table = []          # (end_ms, key) のリスト
    start_tick = 0          # pygame.time.get_ticks()（ms）

    # 乱れ用状態（目・口それぞれ）
    eye_offset   = [0, 0]
    eye_angle    = 0.0
    mouth_offset = [0, 0]
    mouth_angle  = 0.0

    silent_start_tick = None   # 「無音」開始時刻
    jitter_active     = False  # 揺れが有効か

    running = True
    while running:
        # -------------------------------------------------
        # ① イベント処理（ウインドウリサイズを含む）
        # -------------------------------------------------
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.VIDEORESIZE:
                # ウインドウサイズが変わったら再設定
                win_w, win_h = ev.w, ev.h
                screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
            elif ev.type == BLINK_EVENT:
                blink_start_tick = pygame.time.get_ticks()
                blink_end_tick   = blink_start_tick + 150   # 150ms 瞬き
                pygame.time.set_timer(BLINK_EVENT, 0)       # 今回は停止

        # -------------------------------------------------
        # ② テキストが来たら非同期で合成開始
        # -------------------------------------------------
        try:
            txt = txt_queue.get_nowait()
        except queue.Empty:
            txt = None

        if txt is not None:
            future = executor.submit(synthesize, txt)

        # -------------------------------------------------
        # ③ 合成完了待ち（非ブロッキング）
        # -------------------------------------------------
        if 'future' in locals() and future.done():
            try:
                wav_bytes, aq = future.result()
                # 再生
                sound = pygame.mixer.Sound(io.BytesIO(wav_bytes))
                channel = sound.play()
                start_tick = pygame.time.get_ticks()

                # 口形テーブル作成
                lip_table = build_lip_sync_table(aq)

                # 瞬きタイマーリセット
                pygame.time.set_timer(BLINK_EVENT, random.randint(1000, 3000))
            except Exception as e:
                print("合成エラー:", e)
            finally:
                del future   # もう使わない

        # -------------------------------------------------
        # ④ 再生状態の判定
        # -------------------------------------------------
        speaking = channel is not None and channel.get_busy()
        if not speaking:
            # しゃべっていない → 無音状態開始タイマーを走らせる
            if silent_start_tick is None:
                silent_start_tick = pygame.time.get_ticks()
            else:
                if (pygame.time.get_ticks() - silent_start_tick) >= JITTER_DELAY_MS:
                    jitter_active = True
            try:
                future
                talking = True
            except:
                if not speaking and talking is True:
                    os.remove(TEXT_FILE)    # しゃべり終わったら削除（二重処理防止）
                    talking = False
        else:
            # しゃべり始めたらすべてリセット
            silent_start_tick = None
            jitter_active = False
            eye_offset   = [0, 0]
            eye_angle    = 0.0
            mouth_offset = [0, 0]
            mouth_angle  = 0.0

        # -------------------------------------------------
        # ⑤ 乱れ（jitter）更新
        # -------------------------------------------------
        if jitter_active:
            eye_offset,   eye_angle   = update_jitter(eye_offset,   eye_angle)
            mouth_offset, mouth_angle = eye_offset,   eye_angle   # 口も同様に

        # -------------------------------------------------
        # ⑥ 口形決定（ms タイマーで高精度）
        # -------------------------------------------------
        if speaking:
            elapsed_ms = pygame.time.get_ticks() - start_tick
            mouth_key = lookup_mouth_key(lip_table, elapsed_ms)
        else:
            mouth_key = "C"

        # -------------------------------------------------
        # ⑦ 瞬き状態決定
        # -------------------------------------------------
        now_tick = pygame.time.get_ticks()
        if 'blink_start_tick' in locals() and now_tick < blink_end_tick:
            eye_state = "closed"
        else:
            eye_state = "open"
            if 'blink_start_tick' in locals():
                pygame.time.set_timer(BLINK_EVENT, random.randint(1000, 3000))
                del blink_start_tick, blink_end_tick

        # -------------------------------------------------
        # ⑧ 描画（ウインドウサイズに合わせてスケール）
        # -------------------------------------------------
        # 1) 背景（ベース）を現在のウインドウサイズへスケール
        base_scaled = pygame.transform.smoothscale(base_img, (win_w, win_h))
        screen.blit(base_scaled, (0, 0))

        # スケール係数（幅基準）を算出（高さも同様に扱えるが、比率が同じ前提）
        scale_x = win_w / WINDOW_W
        scale_y = win_h / WINDOW_H

        # 2) 目（回転 + オフセット）※オフセットはスケール適用
        eye_surf = pygame.transform.rotate(eye_imgs[eye_state], eye_angle)
        eye_surf = pygame.transform.smoothscale(
            eye_surf,
            (int(eye_surf.get_width() * scale_x),
             int(eye_surf.get_height() * scale_y))
        )
        eye_rect = eye_surf.get_rect()
        eye_rect.topleft = (int(eye_offset[0] * scale_x),
                            int(eye_offset[1] * scale_y))
        screen.blit(eye_surf, eye_rect)

        # 3) 口（回転 + オフセット）※同様にスケール
        mouth_surf = pygame.transform.rotate(mouth_imgs[mouth_key], mouth_angle)
        mouth_surf = pygame.transform.smoothscale(
            mouth_surf,
            (int(mouth_surf.get_width() * scale_x),
             int(mouth_surf.get_height() * scale_y))
        )
        mouth_rect = mouth_surf.get_rect()
        mouth_rect.topleft = (int(mouth_offset[0] * scale_x),
                              int(mouth_offset[1] * scale_y))
        screen.blit(mouth_surf, mouth_rect)

        pygame.display.flip()
        clock.tick(FPS)

    # -------------------------------------------------
    # 後処理
    # -------------------------------------------------
    observer.stop()
    observer.join()
    executor.shutdown(wait=False)
    pygame.quit()

if __name__ == "__main__":
    main()