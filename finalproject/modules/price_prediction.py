# modules/price_prediction.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 在modules/price_prediction.py中新增
def generate_demo_data():
    """生成虚拟训练数据（与原demo一致）"""
    np.random.seed(42)
    sample_size = 100
    data = pd.DataFrame({
        'area': np.random.randint(50, 200, size=sample_size),
        'rooms': np.random.randint(1, 6, size=sample_size),
        'age': np.random.randint(0, 30, size=sample_size),
    })
    data['price'] = 1000 * data['area'] + 5000 * data['rooms'] - 300 * data['age'] + \
                    np.random.randint(-10000, 10000, size=sample_size)
    return data

def train_price_model(data):
    """
    data：pandas DataFrame，要求包含若干关键特征和房价目标列
    假设数据中有以下列：'area'（面积）, 'rooms'（房间数）, 'age'（房龄）, 'price'（房价）
    """
    features = ['area', 'rooms', 'age']
    target = 'price'

    X = data[features]
    y = data[target]

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"模型测试得分（R^2）：{score:.3f}")

    return model


def predict_price(model, area, rooms, age):
    """
    根据模型和输入的特征预测房价
    """
    features = np.array([[area, rooms, age]])
    predicted_price = model.predict(features)
    return predicted_price[0]


def demo_price_prediction():
    """
    演示一个完整的房价预测流程。
    这里使用随机生成的虚拟数据进行演示，实际应用中请替换为真实数据文件读取。
    """
    # 生成虚拟数据
    np.random.seed(42)
    sample_size = 100
    data = pd.DataFrame({
        'area': np.random.randint(50, 200, size=sample_size),  # 面积
        'rooms': np.random.randint(1, 6, size=sample_size),  # 房间数
        'age': np.random.randint(0, 30, size=sample_size),  # 房龄
    })
    # 假设房价 = 1000 * area + 5000 * rooms - 300 * age + 噪声
    data['price'] = 1000 * data['area'] + 5000 * data['rooms'] - 300 * data['age'] + np.random.randint(-10000, 10000,
                                                                                                       size=sample_size)

    print("开始训练房价预测模型...")
    model = train_price_model(data)

    # 从用户获取输入进行预测
    try:
        area = float(input("请输入房屋面积（单位：平方米）: "))
        rooms = int(input("请输入房间数: "))
        age = int(input("请输入房龄（年）: "))
    except Exception as e:
        print("输入有误，请输入正确的数值。")
        return

    predicted = predict_price(model, area, rooms, age)
    print(f"预测的房价为：{predicted:.2f}")


# 如果直接运行本模块，可调用演示函数
if __name__ == "__main__":
    demo_price_prediction()
