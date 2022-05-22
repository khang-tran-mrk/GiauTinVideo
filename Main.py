import os

# Checks if output Directory Exists, otherwise Create It
if not os.path.exists('output'):
    os.makedirs('output')

# Menu
print("\t1: Hide Data in Frames\n")
print("\t2: Recover Data in Frames\n")

# User Selection
while True:
    # Menu
    print("\t1: Hide Data in Frames\n")
    print("\t2: Recover Data in Frames\n")
    try:
        start_step = int(input("\nSelect the Program to Run: "))

        if start_step == 1:
            print("Starting Program...\n")
            print("=== Hide Data in Frames ===")
            os.system("python Encoder.py")

        elif start_step == 2:
            print("Starting Program...\n")
            print("=== Recover Data in Frames ===")
            os.system("python Decoder.py")

        else:
            print("\nInvalid Input! Exiting...\n")

    except ValueError:
        print("Non-Integer Input Entered. Exiting...\n")
    except KeyboardInterrupt:
        print("\nUser canceled, exiting...")


