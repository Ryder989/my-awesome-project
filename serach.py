import os # 用來操作系統(走訪資料夾、模組路徑)
import threading # 執行緒模組，避免GUI卡住
import tkinter as tk # Python 內建GUI 工具包
from tkinter import ttk, filedialog, messagebox
# ttk tkinter進階元件(美化版)
# filedialog 開啟資料夾選擇視窗
# messagebox 顯示提示訊息
import psutil # psutil 取得系統持碟機資訊 (跨平台)

stop_flag = False # 全域變數，控制是否中斷搜尋

# 🔍 動態取得磁碟機清單，過濾沒有檔案系統的裝置 (如虛擬磁碟)
def get_drives():
    return [part.device for part in psutil.disk_partitions() if part.fstype != ""]

# 🔍 搜尋檔案（執行緒中）
def search_files(keyword, path):
    global stop_flag
    stop_flag = False

    result_list.delete(0, tk.END)
    progress_bar.start() #顯示搜尋進度開始

    for folder, _, files in os.walk(path):
        if stop_flag:
            break
        for file in files:
            if stop_flag:
                break
            if keyword.lower() in file.lower():
                full_path = os.path.join(folder, file)
                result_list.insert(tk.END, full_path)

    progress_bar.stop() #顯示搜尋進度停止
    if stop_flag:
        messagebox.showinfo("完成", "搜尋停止！")
    else:
        messagebox.showinfo("完成", "搜尋完成！")

# 🧵 包裝搜尋為執行緒
def threaded_search():
    keyword = entry.get()
    path = path_var.get()
    if not keyword or not path:
        messagebox.showwarning("警告", "請輸入關鍵字並選擇路徑")
        return
    threading.Thread(target=search_files, args=(keyword, path), daemon=True).start()

# 停止搜尋
def stop_search():
    global stop_flag
    stop_flag = True

# 📂 選擇資料夾
def choose_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)

# 📂 快速選擇磁碟機
def select_drive(event):
    path_var.set(drive_combo.get())

# 📁 開啟檔案
def open_file(event):
    selected = result_list.get(result_list.curselection())
    os.startfile(selected)

# 🖼️ GUI 主視窗
root = tk.Tk()
root.title("檔案搜尋工具")
root.geometry("600x400")
root.config(background="skyblue")
#root.iconbitmap("D:\公司資料\公司資料\RYDER\碩益\常用軟體\搜尋工具\lhxmn-85zgf-001.ico")

# 🔤 關鍵字輸入
entry = tk.Entry(root)
entry.insert(0,"請輸入檔案名稱關鍵字")
entry.pack(fill="x", padx=10, pady=5)

# 📁 路徑選擇區
path_frame = tk.Frame(root)
path_frame.pack(fill="x", padx=10)

path_var = tk.StringVar()
path_entry = tk.Entry(path_frame, textvariable=path_var)
path_entry.pack(side="left", fill="x", expand=True)

choose_btn = tk.Button(path_frame, text="選擇資料夾", command=choose_folder)
choose_btn.pack(side="right", padx=5)

# 💽 磁碟機下拉選單
drive_combo = ttk.Combobox(root, values=get_drives(), state="readonly")
drive_combo.set("選擇磁碟機")
drive_combo.pack(fill="x", padx=10, pady=5)
drive_combo.bind("<<ComboboxSelected>>", select_drive)

# 🔘 搜尋按鈕
search_btn = tk.Button(root, text="開始搜尋", command=threaded_search)
search_btn.pack(pady=5)

# 停止搜尋按紐
stop_btn = tk.Button(root,text="停止搜尋",command=stop_search)
stop_btn.pack()

# 📊 進度條
progress_bar = ttk.Progressbar(root, mode="indeterminate")
progress_bar.pack(fill="x", padx=10, pady=5)

# 📋 結果列表
result_list = tk.Listbox(root)
scrollbar = tk.Scrollbar(root,command=result_list.yview)
result_list.config(yscrollcommand=scrollbar.set) # 雙向綁定
result_list.pack(side="left",fill="both", expand=True, padx=10, pady=5)
scrollbar.pack(side="right",fill="y")
result_list.bind("<Double-Button-1>", open_file)

root.mainloop()