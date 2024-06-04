import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk

import yt_dlp


def main():
    # ウィンドウを作成
    window = tk.Tk()

    # 左上のアイコン変更（Windows用）
    # iconfile = './cat.ico'
    # window.iconbitmap(default=iconfile)

    # ウィンドウのタイトルを設定
    window.title("DownloaderX")

    # ウィンドウのサイズを設定
    window.geometry("500x360")

    # ラベル1 を作成して配置
    label1 = tk.Label(window, text="URL")
    # レイアウト調整
    label1.pack(pady=10, padx=10)

    # URLテキスト入力欄
    entry_url = tk.Entry(width=40)
    # レイアウト調整
    entry_url.pack(pady=10, padx=10)

    # ラベル2 を作成して配置
    label2 = tk.Label(window, text="Save Location")
    # レイアウト調整
    label2.pack(pady=10, padx=10)

    # PATHテキスト入力欄
    entry_path = tk.Entry(width=40)
    # レイアウト調整
    entry_path.pack(pady=10, padx=10)

    # ラジオボタンを配置
    choice = tk.IntVar()
    # 初期値に動画を設定
    choice.set(1)
    # ラジオボタンを横に配置
    frame = tk.Frame(window)
    frame.pack(pady=10)
    # mp4で出力
    radio_button_mp4 = tk.Radiobutton(frame, text="Movie", variable=choice, value=1)
    radio_button_mp4.pack(side=tk.LEFT, padx=10, pady=10)
    # mp3で出力
    radio_button_mp3 = tk.Radiobutton(frame, text="Music", variable=choice, value=2)
    radio_button_mp3.pack(side=tk.LEFT, padx=10, pady=10)

    # ボタンがクリックされたときの処理
    def download_button_clicked():
        # プログレスバー作成
        pb = progressbar_set(window)
        # プログレスバー開始
        pb.start(7)

        # URL取得
        url = entry_url.get()

        # ラジオボタン値取得
        flag = choice.get()

        # PATH取得
        path = entry_path.get()

        # PATH指定されない場合、OSごとのフォルダ配下にファルダ作成
        if path == "":
            if os.name == "nt":  # Windows
                path = os.path.join(
                    os.getenv("HOMEDRIVE"),
                    os.getenv("HOMEPATH"),
                    "Videos",
                    "DownloaderX",
                )
            elif os.name == "posix":  # macOS
                path = os.path.join(os.path.expanduser("~"), "Movies", "DownloaderX")
            else:
                raise OSError("Unsupported operating system")

        # 別スレッドで動画のダウンロードを実行
        thread_download = threading.Thread(
            target=download_video, args=(url, path, flag, pb)
        )
        # ダウンロードスレッド開始
        thread_download.start()

    # ボタンを作成して配置
    button = tk.Button(window, text="Download", command=download_button_clicked)
    # レイアウト調整
    button.pack(pady=10, padx=10)

    # イベントループを開始
    window.mainloop()


# プログレスバーを作成する関数
def progressbar_set(window):
    # プログレスバーのスタイルを設定
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "base.Horizontal.TProgressbar",
        thickness=17,  # プログレスバーの幅
        troughcolor="#d0d0d0",  # プログレスバーの背景色
        background="#008000",  # プログレスバーの色
    )

    # プログレスバーを作成
    bar = tk.IntVar()
    # 作成
    pb = ttk.Progressbar(
        window,
        style="base.Horizontal.TProgressbar",
        maximum=100,
        mode="indeterminate",
        variable=bar,
        length=200,
    )
    # 設置
    pb.pack(pady=10, padx=10)

    return pb


# 指定したURL上の動画をダウンロードする関数
def download_video(url, path, flag, pb):
    # オプション設定
    ydl_opts = {
        "outtmpl": os.path.join(path, f'%(title)s{"" if flag == 2 else ".mp4"}'),
        "format": "bestaudio"
        if flag == 2
        else "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
        if flag == 2
        else [],
    }

    # ダウンロード実行
    try:
        # ダウンロード
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # プログレスバー破壊
        pb.destroy()
        print("--- Download Completed ! ---")
    except Exception as e:
        # プログレスバー破壊
        pb.destroy()
        # エラー表示
        messagebox.showerror("Error", "Download failed.")


if __name__ == "__main__":
    main()
