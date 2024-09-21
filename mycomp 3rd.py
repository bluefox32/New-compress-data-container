class DataCompressor:
    def __init__(self):
        self.compressed_data = []
        self.position_info = []

    def compress(self, binary_data):
        count_0 = 0
        count_1 = 0
        current_bit = None

        for bit in binary_data:
            if bit == '0':
                if current_bit == '0':
                    count_0 += 1
                else:
                    if current_bit is not None:
                        self.compressed_data.append((current_bit, count_0, count_1))
                    current_bit = '0'
                    count_0 = 1
                    count_1 = 0
            elif bit == '1':
                if current_bit == '1':
                    count_1 += 1
                else:
                    if current_bit is not None:
                        self.compressed_data.append((current_bit, count_0, count_1))
                    current_bit = '1'
                    count_1 = 1
                    count_0 = 0
        
        # Add the last recorded bit
        if current_bit is not None:
            self.compressed_data.append((current_bit, count_0, count_1))

        self.record_position_info()

    def record_position_info(self):
        for index, (bit, count_0, count_1) in enumerate(self.compressed_data):
            self.position_info.append((bit, index))

    def decompress(self):
        original_data = ''
        for bit, count_0, count_1 in self.compressed_data:
            original_data += bit * (count_0 + count_1)
        return original_data

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for entry in self.compressed_data:
                file.write(f"{entry}\n")

# 使用例
compressor = DataCompressor()
compressor.compress("0011001110")
print(compressor.compressed_data)