import os
import shutil
import subprocess
import getpass
import time
import sys
import ctypes

# === Настройки ===
FLAG_FILENAME = "metka.flag"
JAVA_INSTALLER_REL = "jre-8u451-windows-x64.exe"
GAME_SRC_REL = ".minecraft"
SCRIPTS_SRC_REL = "mine"

JAVA_DST = r"C:\Program Files\Java"
USER_NAME = getpass.getuser()
APPDATA_DIR = os.path.join("C:\\Users", USER_NAME, "AppData", "Roaming")
GAME_DST = os.path.join(APPDATA_DIR, ".minecraft")
SCRIPTS_DST = os.path.join(APPDATA_DIR, "mine")


def print_status(message, status="info"):
    symbols = {"info": "[→]", "ok": "[✔]", "error": "[✘]", "warn": "[!]" }
    print(f"{symbols.get(status, '[→]')} {message}")


def find_drive_with_flag():
    print_status("Ищу флешку с меткой...")
    for drive_letter in "DEFGHIJKLMNOPQRSTUVWXYZ":
        drive_path = f"{drive_letter}:\\"
        if os.path.exists(os.path.join(drive_path, FLAG_FILENAME)):
            print_status(f"Найдена флешка: {drive_path}", "ok")
            return drive_path
    return None


def is_java_installed():
    try:
        subprocess.run(["java", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False


def install_java(installer_path):
    print_status("Устанавливаю Java в тихом режиме...")
    time.sleep(1)
    subprocess.run([installer_path, "/s"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print_status("Java установка завершена", "ok")


def copy_item(src, dst):
    if os.path.isdir(src):
        print_status(f"Копирование папки: {src} → {dst}")
        shutil.copytree(src, dst, dirs_exist_ok=True)
    elif os.path.isfile(src):
        print_status(f"Копирование файла: {src} → {dst}")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    else:
        print_status(f"Не найдено: {src}", "error")


def check_and_copy(drive_path):
    java_installed = is_java_installed()
    minecraft_exists = os.path.exists(GAME_DST)
    scripts_exist = os.path.exists(SCRIPTS_DST)

    if java_installed and minecraft_exists and scripts_exist:
        print_status("Заражение уже выполнено. Действий не требуется.", "ok")
        return

    if not java_installed:
        java_installer_path = os.path.join(drive_path, JAVA_INSTALLER_REL)
        if os.path.exists(java_installer_path):
            install_java(java_installer_path)
        else:
            print_status("Установщик Java не найден на флешке!", "error")
        fake_progress_bar("Проверка Java", 2)

    if not minecraft_exists:
        game_src_path = os.path.join(drive_path, GAME_SRC_REL)
        if os.path.exists(game_src_path):
            print_status("Копирую папку с игрой...")
            copy_item(game_src_path, GAME_DST)
        else:
            print_status("Папка с игрой не найдена на флешке!", "error")
        fake_progress_bar("Копирование игры", 3)

    if not scripts_exist:
        scripts_src_path = os.path.join(drive_path, SCRIPTS_SRC_REL)
        if os.path.exists(scripts_src_path):
            print_status("Копирую папку со скриптами...")
            copy_item(scripts_src_path, SCRIPTS_DST)
        else:
            print_status("Папка скриптов не найдена на флешке!", "error")
        fake_progress_bar("Копирование скриптов", 3)


def fake_progress_bar(task_name, seconds):
    print(f"[→] {task_name}: ", end="", flush=True)
    for i in range(seconds):
        print("█", end="", flush=True)
        time.sleep(1)
    print(" [✔]")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def main():
    if not is_admin():
        print_status("Перезапуск от имени администратора...", "warn")
        try:
            script = os.path.abspath(sys.argv[0])
            params = " ".join([script] + sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        except Exception as e:
            print_status(f"Ошибка перезапуска: {e}", "error")
        sys.exit()

    drive_path = find_drive_with_flag()
    if drive_path is None:
        user_input = input("[?] Флешка не найдена. Введите букву диска вручную (без двоеточия): ").upper()
        drive_path = f"{user_input}:\\"

    if not os.path.exists(drive_path):
        print_status("Диск не существует! Завершение работы.", "error")
        return

    print_status(f"Работаем с диском: {drive_path}")
    fake_progress_bar("Инициализация", 2)
    check_and_copy(drive_path)

    print_status("Работа завершена.", "ok")
    time.sleep(5)


if __name__ == "__main__":
    main()
