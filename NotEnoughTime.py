from pwn import remote, context

context.log_level = "debug"
connect = remote("127.0.0.1", 49665)

expressionnull = connect.recvuntil("ones.")

while True:
    try:
        # 接收
        expression = connect.recvuntil(b"=").decode().strip()
        print(f"表达式: {expression}")
        expression = expression.replace("=", "").replace(" ", "").replace("/", "//")

        filtered_expression = "".join(
            filter(lambda c: c in "0123456789+*-()//\\", expression)
        )

        if filtered_expression:
            try:
                result = eval(filtered_expression)
                print(f"结果: {result}")
                connect.sendline(str(result).encode())
            except Exception as e:
                print(f"错误表达式: {e}")
                connect.sendline(b"Error")
        else:
            print("无效表达式")
            connect.sendline(b"null")

    except EOFError:
        print("EoFError.")
        break
    except Exception as e:
        print(f"错误: {e}")
        break

