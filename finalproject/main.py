# main.py
from modules import login_module, hailstone, data_processing, normalization, price_prediction

def main_menu():
    """
    主菜单，用户选择不同功能
    """
    while True:
        print("\n============================")
        print("请选择功能:")
        print("1. 冰雹猜想（Collatz 序列）")
        print("2. 数据处理（CSV数据统计）")
        print("3. 数据归一化（Min-Max归一化）")
        print("4. 房价预测")
        print("5. 退出")
        choice = input("请输入对应的选项编号: ")

        if choice == "1":
            try:
                num = int(input("请输入一个正整数: "))
                seq = hailstone.hailstone_sequence(num)
                print("冰雹猜想序列：", seq)
            except Exception as e:
                print(f"出错了：{e}")
        elif choice == "2":
            file_path = input("请输入CSV数据文件的路径: ")
            stats = data_processing.load_and_process_data(file_path)
            if stats is not None:
                print("数据统计信息：")
                print(stats)
        elif choice == "3":
            raw_data = input("请输入一组数字，用逗号分隔: ")
            try:
                data_list = [float(item) for item in raw_data.split(',')]
                norm_data = normalization.min_max_normalize(data_list)
                print("归一化结果：", norm_data)
            except Exception as e:
                print(f"转换数据时出错：{e}")
        elif choice == "4":
            price_prediction.demo_price_prediction()
        elif choice == "5":
            print("退出系统，再见！")
            break
        else:
            print("无效的选项，请重新输入。")

def main():
    """
    主程序入口，处理登录和注册逻辑
    """
    print("欢迎使用系统！")
    while True:
        print("\n请选择操作:")
        print("1. 登录")
        print("2. 注册")
        print("3. 退出")
        choice = input("请输入选项编号: ")

        if choice == "1":
            if login_module.login():
                print("进入主菜单...")
                main_menu()
                break  # 登录成功后退出循环
        elif choice == "2":
            login_module.register()
        elif choice == "3":
            print("退出系统，再见！")
            break
        else:
            print("无效选项，请重新输入。")

if __name__ == "__main__":
    main()