import winsound
import time

def play_alarm():
    base_path = os.environ.get("APPDATA")
    script_path = os.path.join(base_path, "mine")
    winsound.PlaySound(os.path.join(script_path, 'bu_ispugalsa.wav'), winsound.SND_FILENAME)

if __name__ == "__main__":
    while True:
        play_alarm()
        time.sleep(1)
