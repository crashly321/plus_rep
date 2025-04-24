import subprocess, os
import time, psutil

def is_game_running(game_name): # проверяю есть ли игра в задачах
    for process in psutil.process_iter(['pid', 'name']):
        if game_name.lower() in process.info['name'].lower():
            return False
    return True


def start_process(script_path):
    subprocess.Popen(script_path)


if __name__ == "__main__":
    # Получаем путь к папке AppData/Roaming для текущего пользователя
    base_path = os.environ.get("APPDATA")
    script_path = os.path.join(base_path, "mine")

    # ждемс пока не появится нужный процесс
    while True:
        if not is_game_running("java.exe"):  # Если запустилась игра (в нашем случае — java.exe)
            print('123')
            start_process(os.path.join(script_path, "monitoring.exe"))
            start_process(os.path.join(script_path, "play_sound.exe"))
            start_process(os.path.join(script_path, "volume_up.exe"))
            break
        time.sleep(1)
