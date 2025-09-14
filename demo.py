# -*- coding: utf-8 -*-

# 書き出したい文字列を変数に格納
msg = "ﾊﾟｲｿﾝﾁｬﾝは、リアルタイムにテキストファイルを監視し、VOICEVOXで音声合成しながら、ツーディーアバターの目と口をリップシンクと瞬きでアニメーションさせるアプリです！"   # 例: 任意の文字列に置き換えてください

# message.txt に書き込み（上書きモード）
with open("message.txt", "w", encoding="utf-8") as f:
    f.write(msg)

print("message.txt に書き込みました。")