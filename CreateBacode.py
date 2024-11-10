import barcode
from barcode.writer import ImageWriter
import random

# 12桁のランダムな数字を生成
barcode_data = ''.join([str(random.randint(0, 9)) for _ in range(12)])

# バーコードの種類とイメージライターを指定
ean = barcode.get('ean13', barcode_data, writer=ImageWriter())

# 生成されたバーコードをPNG形式で保存
filename = ean.save("random_barcode_image")

print(f"ランダムバーコードが {filename}.png として保存されました")
input(" >> ")