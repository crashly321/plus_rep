import winsound
import time

def play_alarm():
    winsound.PlaySound('C:/Users/malim/AppData/Roaming/mine/bu_ispugalsa.wav', winsound.SND_FILENAME)

if __name__ == "__main__":
    while True:
        play_alarm()
        time.sleep(1)
