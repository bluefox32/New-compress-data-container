import re

# バイナリデータを Xn, Yn で圧縮し、座標を三次元で記録
def binary_compression_with_coords(data):
    binary_data = ''.join(format(byte, '08b') for byte in data)  # バイナリデータをビット列に変換
    
    pattern = re.findall(r'0+|1+', binary_data)  # 0と1の連続するパターンを抽出
    
    compressed_data = []
    x, y, z = 0, 0, 0  # 初期座標 (x', y', z')

    for p in pattern:
        n = len(p)  # 連続するビットの個数を取得
        if p.startswith('1'):
            symbol = 'X'
        else:
            symbol = 'Y'
        
        # 座標(x', y', z')を更新しながら記録
        compressed_data.append(f"{symbol}{n},({x},{y},{z})")
        
        # 座標を更新（シンプルに1次元移動とする）
        z += 1
        if z >= 10:  # 仮に10ごとにy軸を進めるとする（任意の基準に変更可能）
            z = 0
            y += 1
        if y >= 10:  # 仮にy軸が10を超えるとx軸を進めるとする（任意の基準に変更可能）
            y = 0
            x += 1
    
    return compressed_data

# 圧縮データをファイルに保存
def save_compressed_data_with_coords(filename, compressed_data):
    with open(f"{filename}.mycomp", 'w') as file:
        file.write("Compressed Data with Coordinates:\n")
        file.write(','.join(compressed_data) + "\n")

# テスト用バイナリデータ
binary_data = b'\xaa\xcc'  # 例: 1010101011001100
compressed_data = binary_compression_with_coords(binary_data)

# 圧縮データをファイルに保存
save_compressed_data_with_coords("example_coords", compressed_data)

print("圧縮結果:", compressed_data)

# 解凍処理関数
def binary_decompression_with_coords(compressed_file):
    with open(compressed_file, 'r') as file:
        lines = file.readlines()
    
    compressed_data = lines[1].strip().split(',')
    decompressed_data = []
    
    for i in range(0, len(compressed_data), 2):
        pattern = compressed_data[i]
        symbol = pattern[0]
        n = int(pattern[1:])
        
        # 圧縮データを元のビット列に戻す
        if symbol == 'X':
            decompressed_data.append('1' * n)
        elif symbol == 'Y':
            decompressed_data.append('0' * n)
    
    # ビット列をバイナリ形式に戻す
    decompressed_binary = ''.join(decompressed_data)
    byte_data = bytearray()
    
    for i in range(0, len(decompressed_binary), 8):
        byte_data.append(int(decompressed_binary[i:i+8], 2))
    
    return byte_data

# 解凍処理を実行
decompressed_data = binary_decompression_with_coords("example_coords.mycomp")
print("解凍されたバイナリデータ:", decompressed_data)

