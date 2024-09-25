import numpy as np

# 四元数クラスを定義
class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = w  # 実部
        self.x = x  # 虚部
        self.y = y
        self.z = z

    # 四元数の積（ユニタリー変換の基本）
    def __mul__(self, other):
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)

    # 四元数をユニタリー変換として適用
    def rotate(self, vector):
        q_vector = Quaternion(0, *vector)
        q_conjugate = Quaternion(self.w, -self.x, -self.y, -self.z)
        rotated_vector = self * q_vector * q_conjugate
        return np.array([rotated_vector.x, rotated_vector.y, rotated_vector.z])

# 四元数による3次元ベクトルの回転例
q = Quaternion(0.707, 0.707, 0, 0)  # 45度回転を表す四元数
vector = np.array([1, 0, 0])  # 回転させるベクトル

rotated_vector = q.rotate(vector)
print("Rotated Vector:", rotated_vector)

# 複数次元のデータへの適用
def apply_unitary_operation(data, quaternions):
    """
    高次元データにユニタリー変換を適用
    data: 入力データ (N次元データ)
    quaternions: 各次元に対応する四元数リスト
    """
    transformed_data = []
    for i, vec in enumerate(data):
        q = quaternions[i % len(quaternions)]  # 各次元に異なる四元数を適用
        transformed_data.append(q.rotate(vec))
    return np.array(transformed_data)

# 高次元データに対して四元数を適用
data = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
quaternions = [Quaternion(0.707, 0.707, 0, 0), Quaternion(1, 0, 0, 0)]
transformed_data = apply_unitary_operation(data, quaternions)
print("Transformed Data:", transformed_data)

import numpy as np
from scipy.stats import multivariate_normal

# n次元ガウス関数の例
def n_dimensional_gaussian(x, mean, cov):
    """
    n次元ガウス関数を計算
    x: n次元ベクトル
    mean: 平均ベクトル (n次元)
    cov: 共分散行列 (n x n)
    """
    return multivariate_normal.pdf(x, mean=mean, cov=cov)

# 3次元のガウス分布の例
mean = np.array([0, 0, 0])  # 平均ベクトル
cov = np.eye(3)  # 単位行列 (共分散行列)

# サンプルデータ
x = np.array([1, 2, 3])  # 3次元ベクトル

# ガウス分布の値を計算
gaussian_value = n_dimensional_gaussian(x, mean, cov)
print(f"3次元ガウス関数の値: {gaussian_value}")

# --- ガウスフィルタの適用例 ---
from scipy.ndimage import gaussian_filter

# ランダムなn次元データの生成
data = np.random.rand(100, 100, 100)

# ガウスフィルタを適用 (3次元データの場合)
filtered_data = gaussian_filter(data, sigma=1)

# フィルタリング後のデータを確認
print("フィルタリング後のデータ形状:", filtered_data.shape)
