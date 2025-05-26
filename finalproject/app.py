from flask import Flask, render_template, request, session, flash, redirect, url_for
import json
import os
import numpy as np
import pandas as pd
from modules.hailstone import hailstone_sequence
from modules.normalization import min_max_normalize
from modules.price_prediction import train_price_model, predict_price
from modules.data_processing import load_and_process_data

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 务必替换为安全的随机密钥
USER_FILE = 'users.json'


# 房价预测模型初始化（使用虚拟数据训练）
def init_price_model():
    """启动时训练房价预测模型（示例用虚拟数据）"""
    np.random.seed(42)
    sample_size = 1000
    data = pd.DataFrame({
        'area': np.random.randint(50, 200, size=sample_size),
        'rooms': np.random.randint(1, 6, size=sample_size),
        'age': np.random.randint(0, 30, size=sample_size),
    })
    # 生成虚拟房价（实际应用替换为真实数据）
    data['price'] = 1000 * data['area'] + 5000 * data['rooms'] - 300 * data['age'] + np.random.randint(-10000, 10000,
                                                                                                       size=sample_size)
    return train_price_model(data)


# 全局变量存储模型（实际生产环境建议用更可靠的方式管理）
price_model = init_price_model()


# 辅助函数：加载用户数据
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# 辅助函数：保存用户数据
def save_users(users):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


# 登录检查装饰器
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            flash('请先登录', 'danger')
            return redirect(url_for('login_page'))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


# 路由：登录页面
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash('登录成功', 'success')
            return redirect(url_for('index_page'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('login.html')


# 路由：注册页面
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            flash('用户名已存在', 'danger')
            return redirect(url_for('register_page'))

        users[username] = {'password': password}
        save_users(users)
        flash('注册成功，请登录', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html')


# 路由：退出登录
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('已退出登录', 'info')
    return redirect(url_for('login_page'))


# 路由：主菜单（需要登录）
@app.route('/')
@login_required
def index_page():
    return render_template('index.html')


# 路由：冰雹序列
@app.route('/hailstone', methods=['GET', 'POST'])
@login_required
def hailstone_page():
    error = None
    sequence = None

    if request.method == 'POST':
        try:
            num = int(request.form['num'])
            if num < 1:
                raise ValueError("请输入正整数")
            sequence = hailstone_sequence(num)
        except Exception as e:
            error = f"输入错误：{str(e)}"

    return render_template('hailstone.html', error=error, sequence=sequence)


# 路由：数据统计
@app.route('/data_stats', methods=['GET', 'POST'])
@login_required
def data_stats_page():
    error = None
    stats_html = None

    if request.method == 'POST':
        file = request.files.get('file')
        if not file or not file.filename.endswith('.csv'):
            error = "请上传有效的CSV文件"
        else:
            try:
                df = pd.read_csv(file)
                stats = df.describe().round(2)  # 保留两位小数
                stats_html = stats.to_html(classes='table table-striped table-hover', border=0)
            except Exception as e:
                error = f"处理文件失败：{str(e)}"

    return render_template('data_stats.html', error=error, stats_html=stats_html)


# 路由：数据归一化
@app.route('/normalization', methods=['GET', 'POST'])
@login_required
def normalization_page():
    error = None
    result = None

    if request.method == 'POST':
        try:
            data_str = request.form['data']
            data = [float(x.strip()) for x in data_str.split(',') if x.strip()]
            normalized = min_max_normalize(data)
            result = [round(x, 4) for x in normalized.tolist()]  # 保留4位小数
        except Exception as e:
            error = f"输入错误：{str(e)}"

    return render_template('normalization.html', error=error, result=result)


# 路由：房价预测
@app.route('/price_prediction', methods=['GET', 'POST'])
@login_required
def price_prediction_page():
    error = None
    predicted_price = None

    if request.method == 'POST':
        try:
            area = float(request.form['area'])
            rooms = int(request.form['rooms'])
            age = int(request.form['age'])

            if area < 10 or rooms < 1 or age < 0:
                raise ValueError("输入值需符合要求（面积≥10，房间数≥1，房龄≥0）")

            predicted_price = predict_price(price_model, area, rooms, age)
            predicted_price = round(predicted_price, 2)  # 保留两位小数
        except Exception as e:
            error = f"预测失败：{str(e)}"

    return render_template('price_prediction.html', error=error, predicted_price=predicted_price)


if __name__ == '__main__':
    app.run(debug=True)