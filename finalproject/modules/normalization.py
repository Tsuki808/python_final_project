# modules/normalization.py
import numpy as np

def min_max_normalize(data):
    """
    对传入的数值列表或numpy数组进行 min-max 归一化处理，返回归一化后的数据。
    公式：normalized = (x - min(x)) / (max(x) - min(x))
    """
    data = np.array(data, dtype=float)
    min_val = data.min()
    max_val = data.max()
    if max_val - min_val == 0:
        return np.zeros_like(data)  # 如果所有值都一样，返回全0数组
    normalized = (data - min_val) / (max_val - min_val)
    return normalized

# 简单测试
if __name__ == "__main__":
    sample_data = [10, 20, 30, 40, 50]
    print("原始数据：", sample_data)
    print("归一化结果：", min_max_normalize(sample_data))
