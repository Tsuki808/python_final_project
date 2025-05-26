# modules/hailstone.py

def hailstone_sequence(n):
    """
    输入正整数 n，返回冰雹猜想序列列表。
    算法：
      - 如果 n 为偶数，则 n = n / 2
      - 如果 n 为奇数，则 n = 3 * n + 1
      - 重复直到 n == 1
    """
    if n < 1:
        raise ValueError("请输入大于0的正整数")

    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence


# 简单测试函数（可选）
if __name__ == "__main__":
    num = int(input("请输入一个正整数: "))
    seq = hailstone_sequence(num)
    print("冰雹猜想序列：", seq)
