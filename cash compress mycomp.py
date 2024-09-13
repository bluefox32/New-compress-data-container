import re
import io

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
        
        # z座標を更新し、10単位でy、x軸に切り替え（この基準は調整可能）
        z += 1
        if z >= 10:
            z = 0
            y += 1
        if y >= 10:
            y = 0
            x += 1
    
    return compressed_data

# バイナリデータを圧縮してキャッシュに保存
def compress_to_cache(data):
    compressed_data = binary_compression_with_coords(data)
    
    # メモリ上にキャッシュとして保存
    cache = io.BytesIO()
    cache.write(','.join(compressed_data).encode('utf-8'))
    cache.seek(0)  # キャッシュの読み取り位置を先頭に戻す
    
    return cache
    
# キャッシュから解凍して元のバイナリデータを復元
def decompress_from_cache(cache):
    cache.seek(0)  # キャッシュの読み取り位置を先頭に戻す
    compressed_data = cache.read().decode('utf-8').split(',')
    
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
