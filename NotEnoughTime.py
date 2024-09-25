from pwn import remote
import re

connect = remote("127.0.0.1", 50976)

while True:
    try:
        expression = connect.recvuntil(b"=").decode().strip()
        print(f"表达式: {expression}")

        expression = expression.replace("/", "//")

        if re.match(r"^[\d\+\-\*//() ]+$", expression):
            try:
                result = eval(expression)
                print(f"结果: {result}")
            except Exception as e:
                print(f"错误表达式: {e}")
                result = "Error"
        else:
            result = "无效"

        connect.sendline(str(result).encode())

    except EOFError:
        print("EoFError.")
        break
    except Exception as e:
        print(f"EoFError: {e}")
        break
