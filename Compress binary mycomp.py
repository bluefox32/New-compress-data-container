import re

# 圧縮処理関数
def binary_compression(data):
    binary_data = ''.join(format(byte, '08b') for byte in data)
    pattern = re.findall(r'(01+|00+)', binary_data)
    
    compressed_data = []
    position_data = []
    current_position = 0
    
    for p in pattern:
        if p.startswith('01'):
            symbol = 'X'
        elif p.startswith('00'):
            symbol = 'Y'
        n = len(p) // 2
        compressed_data.append(f"{symbol}^{n}")
        position_data.append((current_position, current_position + len(p)))
        current_position += len(p)
    
    return compressed_data, position_data

# 圧縮データをファイルに保存する関数
def save_compressed_data(filename, compressed_data, position_data):
    with open(f"{filename}.mycomp", 'w') as file:
        file.write("Compressed Data:\n")
        file.write(','.join(compressed_data) + "\n")
        file.write("Position Data:\n")
        file.write(','.join([f"({start},{end})" for start, end in position_data]) + "\n")

# テスト用バイナリデータ
binary_data = b'\xaa\xcc'
compressed_data, position_data = binary_compression(binary_data)

# 圧縮データをファイルに保存
save_compressed_data("example", compressed_data, position_data)

# 解凍処理関数
def binary_decompression(compressed_file):
    with open(compressed_file, 'r') as file:
        lines = file.readlines()

    compressed_data = lines[1].strip().split(',')
    position_data = [tuple(map(int, re.findall(r'\d+', pos))) for pos in lines[3].strip().split(',')]
    
    decompressed_data = ""
    for i, pattern in enumerate(compressed_data):
        symbol, n = pattern[0], int(pattern[2:])
        if symbol == 'X':
            decompressed_data += '01' * n
        elif symbol == 'Y':
            decompressed_data += '00' * n
    
    return decompressed_data

# 解凍処理を実行
decompressed_data = binary_decompression("example.mycomp")
print("解凍されたバイナリデータ:", decompressed_data)
