# modules/data_processing.py
import pandas as pd

def load_and_process_data(file_path):
    """
    读取 CSV 数据文件，并进行简单的数据处理。
    这里的示例仅计算数值型数据的描述性统计信息。
    """
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        print(f"读取数据文件失败: {e}")
        return None

    # 计算描述性统计
    stats = data.describe()
    return stats

# 可选测试
if __name__ == "__main__":
    file = input("请输入数据文件的路径（CSV格式）: ")
    result = load_and_process_data(file)
    if result is not None:
        print("数据统计信息：")
        print(result)
