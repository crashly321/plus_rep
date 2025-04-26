import subprocess, os, time, psutil


def is_game_running(game_name): # проверяю есть ли игра в задачах
    for process in psutil.process_iter(['pid', 'name']):
        if game_name.lower() in process.info['name'].lower():
            return False
    return True


def start_process(script_path):
    subprocess.Popen(script_path)


if __name__ == "__main__":
    # Циклом жду пока запустится игра и выключаю цикл при включении
    while True:
        if not is_game_running("java.exe"):  # Если запустилась игра(в нашем случае игра это джава)
            print('123')
            usr_path = os.getlogin()
            start_process(f"C:/Users/{usr_path}/AppData/Roaming/mine/monitoring.exe") # какой я тупой пиздец
            start_process(f"C:/Users/{usr_path}/AppData/Roaming/mine/play_sound.exe")
            start_process(f"C:/Users/{usr_path}/AppData/Roaming/mine/volume_up.exe")
            break
        time.sleep(1)  # Система будет работать бесконечно
