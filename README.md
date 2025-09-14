# python‑chan  (ﾊﾟｲｿﾝﾁｬﾝ)

![Picture](https://github.com/YoutechA320U/python-chan/blob/master/python-chan.gif "イメージ") 

**リアルタイムにテキストファイルを監視し、VOICEVOX で音声合成しながら  
2D アバター（目・口）をリップシンク＆瞬きでアニメーションさせるアプリ**  

---  

## 📖 目次

1. [概要](#概要)  
2. [ディレクトリ構成](#ディレクトリ構成)  
3. [使い方](#使い方)  
4. [設定項目の説明](#設定項目の説明)  

---  

## 概要

`python‑chan` は、テキストファイル (`message.txt`) の生成を検知し、  
生成された文字列を **VOICEVOX** のローカルサーバーに投げて音声を合成します。  

合成した音声を再生しながら、  
事前に用意した顔画像・目画像・口形画像をリップシンクさせて表示します。  


- 目はランダムタイミングで瞬きし、無音状態が続くと **ジッター (jitter)** が発生して自然に揺れます。  
- ウィンドウはリサイズ可能です。  

> **デモ**: `python python-chan.py`を起動→ `python demo.py`で`message.txt`が生成されると、アバターが喋ります。  

---  

## ディレクトリ構成

```
python-chan/
│
├─ python-chan.py               # ﾊﾟｲｿﾝﾁｬﾝ本体
├─ demo.py               # 動作確認用デモ
├─ message.txt           # (自動生成/削除) 監視対象テキストファイル
│
├─ img_data/             # 画像リソース
│   ├─ avatar_base.png
│   ├─ eyes_open.png
│   ├─ eyes_closed.png
│   ├─ mouth_A.png
│   ├─ mouth_I.png
│   ├─ mouth_U.png
│   ├─ mouth_E.png
│   ├─ mouth_O.png
│   ├─ mouth_N.png
│   └─ mouth_closed.png
│
└─ README.md             # 本ファイル
```

---  

## 使い方

### 1️⃣ アプリ起動

```bash
python python-chan.py
```

- 起動直後はウィンドウにベース画像だけが表示されます。  
- この際`message.txt`がある場合は削除されます。
- 2️⃣に進む前にVOICEVOXを起動しておいてください。

### 2️⃣ テキストを送信

```bash
# 同梱のmessage.txt を作成するだけのスクリプト
python demo.py
```

- ファイルが生成されると自動的に内容がキューに入れられ、バックグラウンドで合成が走ります。  
- 合成が完了すると音声が再生され、リップシンク・瞬きが同期します。  
- 再生が終わると `message.txt` が削除され、次の入力待ち状態に戻ります。

### 3️⃣ 無音状態のジッター

- 音声が途切れ、**2 秒** 以上無音が続くと目と口が微小に揺れ始めます。  
- 再びテキストが来るとジッターはリセットされます。

### 4️⃣ ウィンドウのリサイズ

- ウィンドウは拡大／縮小できます。  
- ウインドウサイズに合わせてﾊﾟｲｿﾝﾁｬﾝもリサイズされます。

---  

## 設定項目の説明

コード冒頭の定数部を直接編集するとカスタマイズできます。

| 定数 | 説明 | 例 |
|------|------|----|
| `TEXT_FILE` | 監視対象テキストファイル名（相対/絶対パス） | `"message.txt"` |
| `VOICOVOX_URL` | VOICEVOX エンドポイント | `"http://127.0.0.1:50021"` |
| `IMG_PATH` | 画像フォルダへのパス（OS に合わせて `\\` か `/`） | `".\\img_data\\"` |
| `BASE_FACE` | アバターのベース画像 | `IMG_PATH+"avatar_base.png"` |
| `WINDOW_W`, `WINDOW_H` | 初期ウィンドウサイズ | `320, 240` |
| `FPS` | 描画フレームレート | `60` |
| `MOUTH_IMAGES` | 口形画像のマッピング（キーは `A I U E O N C`） | `{"A": IMG_PATH+"mouth_A.png", ...}` |
| `EYE_IMAGES` | 目画像のマッピング (`open` / `closed`) | `{"open": IMG_PATH+"eyes_open.png", ...}` |
| `JITTER_MAX_OFFSET` | ジッターの最大平行移動量（ピクセル） | `40` |
| `JITTER_MAX_ANGLE` | ジッターの最大回転角度（度） | `2` |
| `JITTER_PROB_MOVE` / `JITTER_PROB_ROT` | 1 フレームあたりの移動・回転確率 | `0.10`, `0.08` |
| `JITTER_DELAY_MS` | 無音状態が続くとジッター開始までの遅延 | `2000` |
| `SPEAKER_ID` | VOICEVOXの話者ID | `3` ※ずんだもん(ノーマル) |
| `SPEEDSCALE` | VOICEVOXの話速 | `1.0` |
| `PITCHSCALE` | VOICEVOXの音高 | `0.0` |
| `INTONATIONSCALE` | VOICEVOXの抑揚 | `1.0` |
| `VOLUMESCALE` | VOICEVOXの音量 | `1.0` |
| `PREPHONEMELENGTH` | VOICEVOXの開始無音 | `1.0` |
| `POSTPHONEMELENGTH` | VOICEVOXの終了無音 | `0.1` |
| `PAUSELENGTHSCALE` | VOICEVOXの間の長さ | `1.0` |
