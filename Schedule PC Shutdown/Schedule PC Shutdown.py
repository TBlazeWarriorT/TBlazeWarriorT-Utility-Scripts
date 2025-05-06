import os
import time
from datetime import datetime, timedelta
#import pyuac
#if __name__ == "__main__" and not pyuac.isUserAdmin():
#    print("Re-launching as admin!")
#    pyuac.runAsAdmin()

def check_wt_vs():
    if "WT_SESSION" in os.environ: return True # Windows Terminal (wt.exe)
    elif os.environ.get("TERM_PROGRAM") == "vscode": return True # VSCode terminal
    return False
rich_terminal = check_wt_vs()

if rich_terminal:
    secs = int(float(input("Schedule PC shutdown in x minutes: \033[31m")) * 60)
    print("\033[0m")
else:
    secs = int(float(input("Schedule PC shutdown in x minutes: ")) * 60)

shutdown_time = datetime.now() + timedelta(seconds=secs)
shutdown_time_str = shutdown_time.strftime("%H:%M")
if rich_terminal:
    print(f"Scheduled shutdown for \033[31m{shutdown_time_str}\033[0m")
else:
    print(f"Scheduled shutdown for {shutdown_time_str}")

def wait_and_msg(wait_until_min):
    global secs #tell Py to use the mins above and not create a new variable
    wait_until_sec = wait_until_min * 60
    if secs <= wait_until_sec: return
    time.sleep(secs - wait_until_sec)
    secs = wait_until_sec
    if rich_terminal:
        print(f"\033[31m{wait_until_min}\033[0m minute{"s" if secs > 0 else ""} left until PC shutdown. {"\N{CLOCK FACE ONE OCLOCK}" * wait_until_min}")
    else:
        print(f"{wait_until_min} minute{"s" if secs > 0 else ""} left until PC shutdown.")

# Wait until X mins and send a message telling X minutes left
wait_and_msg(15)
wait_and_msg(5)
wait_and_msg(1)

for i in range(0, secs): # Sleep for the remaining time until shutdown
    if rich_terminal:
        print(f"Shutting down in \033[31m{secs-i}\033[0ms.","\r",end="")
    else:
        print(f"Shutting down in {secs-i}s.","\r",end="")
    time.sleep(1)

if rich_terminal:
    print(f"\r\n\033[31mGood night\033[0m!")
else:
    print(f"\r\nGood night!")

os.system("shutdown /s /t 0")