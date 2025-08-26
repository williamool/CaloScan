import os

current_directory = os.getcwd()
print(current_directory)
if os.access(current_directory, os.W_OK):
    print("Current directory has write permission.")
else:
    print("Current directory does NOT have write permission.")
