import winsound, os, time


def play_alarm():
    usr_path = os.getlogin()
    winsound.PlaySound(f'C:/Users/{usr_path}/AppData/Roaming/mine/bu_ispugalsa.wav', winsound.SND_FILENAME)


if __name__ == "__main__":
    while True:
        play_alarm()
        time.sleep(1)
