import subprocess
import os
import platform
import sys
import shutil
import uuid
import time
usrdir = os.path.expanduser("~")
print("Note: we recommend running this as root because tshark may not work somehow.")
print("Checks")
if platform.system() == "Linux":
	print("Ok")
else:
	print("Err: unsupported platform")
	sys.exit(1)
swd = os.path.join(usrdir, "captures")
if os.path.isdir(swd):
	print("Ok")
else:
	if input(f"Err: didn't find 'captures' directory in '{usrdir}'. Do you want to make one? (y/n): ") == "y":
		print(f"Making the 'captures' directory in '{usrdir}'...")
		os.mkdir(swd)
		print("Ok")
	else:
		print("User disagreed or couldn't read input.")
		print("Stopping...")
		sys.exit(1)
if shutil.which("tshark"):
	print("Ok")
else:
	if input("Err: didn't find 'tshark'. Do you want to install it right now? (y/n): ") == "y":
		print("Detecting package manager...")
		if shutil.which("apt"):
			subprocess.run(["sudo", "apt", "install", "-y", "tshark"])
			print("Ok")
		elif shutil.which("zypper"):
			subprocess.run(["sudo", "zypper", "install", "y", "tshark"])
			print("Ok")
		elif shutil.which("dnf"):
			subprocess.run(["sudo", "dnf", "install", "-y", "tshark"])
			print("Ok")
		elif shutil.which("pacman"):
			subprocess.run(["sudo", "pacman", "-S", "--no-confirm", "tshark"])
			print("Ok")
		else:
			print("Err: couldn't install tshark for you. Try installing it manually.")
			sys.exit(1)
	else:
		print("User disagreed or couldn't read input.")
		print("Stopping...")
		sys.exit(1)
print("Checks complete.")
# -------------------------
print("Making .pcap file...")
filename = f"{uuid.uuid4().hex}.pcap"
os.chdir(swd)
if os.getcwd() != swd:
	print("Unexpected error, try restarting...")
	sys.exit(1)
else:
	print("Ok")
subprocess.run(["touch", filename])
if os.path.isfile(filename):
	print("Ok")
else:
	print("Unexpected error, try restarting...")
	sys.exit(1)
# -------------------------
print("Running tshark...")
print("(Stopping at 100 packets...)")
subprocess.run(["sudo", "tshark", "-i", "any", "-p", "-c", "100", "-w", filename])
print("Reading the full file in 10 seconds...")
time.sleep(10)
result = subprocess.run(["sudo", "tshark", "-r", filename, "-V"], capture_output=True, text=True)
print(result.stdout)
