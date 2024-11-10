import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os

class BarcodeEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("バーコード暗号化ツール")
        
        # バーコード入力エントリ1
        self.barcode_label1 = tk.Label(root, text="バーコード1を入力してください:")
        self.barcode_label1.pack()
        
        self.barcode_entry1 = tk.Entry(root, width=50)
        self.barcode_entry1.pack()
        
        # バーコード入力エントリ2
        self.barcode_label2 = tk.Label(root, text="パスフレーズ用バーコードを入力してください:")
        self.barcode_label2.pack()
        
        self.barcode_entry2 = tk.Entry(root, width=50)
        self.barcode_entry2.pack()
        
        # 暗号化ボタン
        self.encrypt_button = tk.Button(root, text="ファイルを暗号化", command=self.encrypt_file)
        self.encrypt_button.pack()
        
        # 復号化ボタン
        self.decrypt_button = tk.Button(root, text="ファイルを復号化", command=self.decrypt_file)
        self.decrypt_button.pack()
    
    def generate_key(self, barcode1, barcode2):
        combined_barcode = barcode1 + barcode2
        salt = combined_barcode.encode()
        return PBKDF2(combined_barcode, salt, dkLen=32, count=1000000)
    
    def encrypt_file(self):
        barcode1 = self.barcode_entry1.get()
        barcode2 = self.barcode_entry2.get()
        if not barcode1 or not barcode2:
            messagebox.showwarning("警告", "バーコード1とバーコード2を入力してください。")
            return
        
        key = self.generate_key(barcode1, barcode2)
        
        file_path = filedialog.askopenfilename(title="暗号化するファイルを選択")
        if not file_path:
            return
        
        with open(file_path, "rb") as f:
            data = f.read()
        
        cipher = AES.new(key, AES.MODE_GCM)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        
        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, "wb") as f:
            f.write(nonce + tag + ciphertext)
        
        messagebox.showinfo("完了", f"ファイルを暗号化しました: {encrypted_file_path}")
        os.remove(file_path)

    def decrypt_file(self):
        barcode1 = self.barcode_entry1.get()
        barcode2 = self.barcode_entry2.get()
        if not barcode1 or not barcode2:
            messagebox.showwarning("警告", "バーコード1とバーコード2を入力してください。")
            return
        
        key = self.generate_key(barcode1, barcode2)
        
        file_path = filedialog.askopenfilename(title="復号化するファイルを選択")
        if not file_path:
            return
        
        with open(file_path, "rb") as f:
            nonce, tag, ciphertext = f.read(16), f.read(16), f.read()
        
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        try:
            data = cipher.decrypt_and_verify(ciphertext, tag)
            decrypted_file_path = os.path.splitext(file_path)[0]
            with open(decrypted_file_path, "wb") as f:
                f.write(data)
            messagebox.showinfo("完了", f"ファイルを復号化しました: {decrypted_file_path}")
        except ValueError:
            messagebox.showerror("エラー", "復号化に失敗しました。バーコードが正しいか確認してください。")

root = tk.Tk()
app = BarcodeEncryptionApp(root)
root.mainloop()
