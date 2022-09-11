import shutil  # for CopyFile
import os  # for  GetFileSize and Check If File exist
import sys  # for CLI Arguments

if (len(sys.argv) < 4):
    print("Missing arguments !")
    exit(1)

file_name = sys.argv[1]
limit_size = sys.argv[2]
logs_number = sys.argv[3]

if os.path.isfile(file_name):  # Check if MAIN logfile file exist
    logfile_size = os.stat(file_name).st_size  # Get Filesize in BYTES
    logfile_size = logfile_size / 1024  # Convert from BYTES to KILOBYTES

    if logfile_size >= limit_size:
        if logs_number > 0:
            for current_file_num in range(logs_number, 1, -1):
                src = file_name + " " + str(current_file_num - 1)
                dst = file_name + " " + str(current_file_num)

                if os.path.isfile(src):
                    shutil.copyfile(src, dst)
                    print(f"Copied: {src} to {dst}")

            shutil.copyfile(file_name, file_name + "_1")
            print(f"Copied: {file_name} to {file_name}_1")
        my_file = open(file_name, 'w')
        my_file.close()
