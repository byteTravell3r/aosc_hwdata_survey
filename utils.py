from colorama import Fore, Style


def print_warn(text: str) -> None:
    print(Fore.RED + text + Style.RESET_ALL)


def print_info(text: str) -> None:
    print(Fore.BLUE + text + Style.RESET_ALL)


def print_data(text: str) -> None:
    print(Fore.MAGENTA + text + Style.RESET_ALL)


import sys
import os
import platform, os, subprocess

def open_file(filename: str) -> None:
    # 打开电子表格软件
    if platform.system() == "Windows":
        os.startfile(filename)
    elif platform.system() == "Darwin":
        subprocess.call(["open", filename])
    else:
        subprocess.call(["xdg-open", filename])

def wait_for_q() -> None:
    """阻塞式等待用户按下 q 键，按下 x 或 Esc 退出程序"""
    if os.name == 'nt':
        # Windows 系统
        import msvcrt
        while True:
            key = msvcrt.getch()
            if key in (b'q', b'Q'):
                return
            elif key in (b'x', b'X', b'\x1b'):
                print("退出程序...")
                sys.exit(0)
    else:
        # Unix 系统（Linux/Mac）
        import tty
        import termios
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while True:
                key = sys.stdin.read(1)
                if key in ('q', 'Q'):
                    return
                elif key in ('x', 'X', '\x1b'):
                    print("退出程序...")
                    sys.exit(0)
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

