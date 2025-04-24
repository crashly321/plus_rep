import psutil
import time
import subprocess

def is_game_running(game_name): # проверяю есть ли игра в задачах
    for process in psutil.process_iter(['pid', 'name']):
        if game_name.lower() in process.info['name'].lower():
            return True
    return False

def start_process(script_path):
    subprocess.Popen(script_path)

def start_game(): # это говно запускает маинкрафт заново
    base_path = os.environ.get("APPDATA")
    script_path = os.path.join(base_path, ".minecraft")
    start_process(os.path.join(script_path, "TLauncher.exe"))

if __name__ == "__main__":
    while True:
        if not is_game_running("java.exe"):  # Если игра не запущена
            start_game()
        time.sleep(5)
