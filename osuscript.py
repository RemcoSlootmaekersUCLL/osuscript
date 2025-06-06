import time
import shutil
import psutil
import subprocess
from datetime import datetime

open_tablet_driver = r'c:\Users\User\OneDrive\Bureaublad\osu!\OpenTabletDriver.lnk'
stream_companion = r'c:\Users\User\OneDrive\Bureaublad\osu!\StreamCompanion.lnk'
key_overlay = r'c:\Users\User\OneDrive\Bureaublad\osu!\KeyOverlay.lnk'
obs = r'c:\ProgramData\Microsoft\Windows\Start Menu\Programs\OBS Studio\OBS Studio (64bit).lnk'

applications = [open_tablet_driver, stream_companion, key_overlay, obs]
process_names = ['osu!StreamCompanion.exe', 'KeyOverlay.exe', 'OpenTabletDriver.UX.Wpf.exe', 'obs64.exe']

log_file_path = r'C:\Users\User\OneDrive\Documenten\coding_challenges\osuscript\log.txt'

def create_clean_log_file():
    with open(log_file_path, 'w') as log_file:
        log_file.write("")

def log(message):
    print(message)
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'{datetime.now()} --- {message}\n')

def copy_files(file, destination, amount):
    src = file
    dest = destination

    log(f'Copying files {amount} times...')
    for i in range(amount):
        shutil.copy(src, dest + f"-{i}.png")
    log('Copied files')


def run_stream_tools():
    log('Starting tools...')

    for app in applications:
        log(f'Starting {app}')
        subprocess.Popen(['explorer', app])
        time.sleep(1)
    
    log('Stream tools running.')

def close_stream_tools():
    if not process_names:
        log('There are no stream tools running: aborting.')
        return
    
    for process in psutil.process_iter(['name']):
        try:
            if process.info['name'] in process_names:
                log(f'Closing {process.info['name']}')
                process.terminate()
                process.wait(timeout=1)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            log(f"[Error: Couldn't close process. {process.info['name']} is either not running or access has been denied.")
    
    log('Closed all processes')


def main():
    # create or clean log file for new session
    create_clean_log_file()
    print('Script running~~')

    run = True
    while run:
        print("1. Copy files")
        print("2. Run osu!stream tools")
        print("3. Close osu!stream tools")
        print("0. Quit\n")
        choice = int(input("What operation do you want to do?\n"))

        if choice == 0:
            log('Quitting script~~')
            run = False
            
        elif choice == 1:
            src = input("File that needs to be copied [Full path]\n")
            dest = input("Location & file base name [Full path]\n")
            amount = int(input("Amount of copies\n"))

            copy_files(src, dest, amount)
            time.sleep(2)

        elif choice == 2:
            run_stream_tools()
            time.sleep(2)

        elif choice == 3:
            close_stream_tools()
            time.sleep(2)

        else:
            print("Invalid choice. Please try again.")

main()
