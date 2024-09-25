from pwn import remote
import re

connect = remote("127.0.0.1", 49538)

while True:
    try:
        # 接收并解码表达式
        expression = connect.recvline().decode().strip()
        print(f"表达式: {expression}")

        # 去掉等号和空格，并且替换除法符号
        expression = expression.replace("=", "").replace(" ", "").replace("/", "//")

        # 检查是否是有效的数学表达式
        if re.match(r"^[\d\+\-\*//()]+$", expression):
            try:
                # 计算表达式
                result = eval(expression)
                print(f"结果: {result}")
            except Exception as e:
                print(f"错误表达式: {e}")
                result = "Error"
        else:
            result = "无效表达式"

        # 发送计算结果
        connect.send(str(result).encode())

    except EOFError:
        print("EoFError.")
        break
    except Exception as e:
        print(f"错误: {e}")
        break
