import psutil, os, time, subprocess


def is_game_running(game_name): # проверяю есть ли игра в задачах
    for process in psutil.process_iter(['pid', 'name']):
        if game_name.lower() in process.info['name'].lower():
            return True
    return False


def start_game(): # это говно запускает маинкрафт заново
    usr_path = os.getlogin()
    game_path = fr"C:/Users/{usr_path}/AppData/Roaming/.minecraft/TLauncher.exe"
    subprocess.Popen(game_path)


if __name__ == "__main__":
    while True:
        if not is_game_running("java.exe"):  # Если игра не запущена
            start_game()
        time.sleep(5)
