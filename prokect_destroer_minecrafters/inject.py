import os
import shutil
import subprocess
import sys
import win32api
import win32file
import win32com.client

def check_java():
    """Проверка наличия Java на системе."""
    try:
        subprocess.check_output("java -version", stderr=subprocess.STDOUT)
        print("Java уже установлена.")
    except subprocess.CalledProcessError:
        print("Java не найдена. Установка Java...")
        install_java()

def install_java():
    """Установка Java с указанного пути."""
    JAVA_INSTALLER_PATH = "D:\\jre-8u451-windows-x64.exe"  # Путь к установщику Java на флешке
    if os.path.exists(JAVA_INSTALLER_PATH):
        subprocess.run([JAVA_INSTALLER_PATH, "/s", "/v", "/quiet"], check=True)
        print("Java установлена успешно.")
    else:
        print("Не удалось найти установщик Java.")
        sys.exit(1)

def find_drive_with_flag(flag):
    """Поиск флешки с файлом flag."""
    drives = win32api.GetLogicalDriveStrings().split("\000")[:-1]
    for drive in drives:
        try:
            drive_letter = drive[0]
            drive_path = f"{drive_letter}:\\{flag}"
            if os.path.exists(drive_path):
                print(f"Найдено устройство с флагом: {drive_letter}")
                return drive_letter
        except Exception as e:
            print(f"Ошибка при проверке тома {drive}: {e}")
    return None

def copy_files(src, dest):
    """Копирование файлов из src в dest."""
    try:
        if os.path.exists(src):
            if not os.path.exists(dest):
                os.makedirs(dest)
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dest, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
            print(f"Файлы успешно скопированы из {src} в {dest}.")
        else:
            print(f"Источник {src} не существует.")
    except Exception as e:
        print(f"Ошибка при копировании файлов: {e}")

def main():
    FLAG = "metka.flag"  # Имя флага
    print("Программа установки и копирования Minecraft и скриптов.")
    
    # Запрос метки тома
    drive_letter = find_drive_with_flag(FLAG)
    if not drive_letter:
        print(f"Не удалось найти флешку с меткой {FLAG}.")
        drive_letter = input("Пожалуйста, введите букву диска флешки: ").strip()

    # Убедимся, что Java установлена
    check_java()

    # Папки для копирования
    GAME_SRC = f"{drive_letter}:\\.minecraft"
    GAME_DIR = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', '.minecraft')
    SCRIPT_SRC = f"{drive_letter}:\\mine"
    SCRIPT_DIR = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Roaming', 'mine')

    # Копирование файлов
    print("Копирование файлов игры...")
    copy_files(GAME_SRC, GAME_DIR)

    print("Копирование скриптов...")
    copy_files(SCRIPT_SRC, SCRIPT_DIR)

    print("Процесс завершён успешно.")

if __name__ == "__main__":
    main()
