import serial
import os
import time

# Configure serial connection
ser = serial.Serial(port="COM10", baudrate=115200, timeout=2)

file = None  # Initialize file to None
filename = None
while True:
    try:
        print("Begin ESP32 Polling...")
        ser.write(b"CHECK\n")  # Send CHECK command
        time.sleep(1)

        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if not line:
                continue  # Ignore empty lines

            if line.startswith("DATA_READY"):
                print("ESP32: Data is ready!")
                continue  # Wait for file transfer

            if line.startswith("NO_DATA"):
                print("ESP32: No new data available.")
                time.sleep(5)
                break  # Wait before polling again

            if "FILENAME:" in line:
                filename = os.path.basename(line.split("FILENAME:")[1].strip())
                print(f"Receiving file: {filename}")
                file = open(filename, "w", encoding="utf-8")  # Open new file
                continue

            if line == "START":
                print("File transfer starting...")
                continue

            if line == "END":
                print(f"File {filename} saved successfully!")
                if file:
                    file.close()  # Close the file properly
                file = None  # Reset file variable
                break  # Exit file transfer loop

            if file:
                file.write(line + "\n")  # Save file contents

        print("Waiting 30 seconds before next check...")
        time.sleep(5)  # Wait before next check

    except KeyboardInterrupt:
        print("Stopping reception...")
        break

ser.close()
print("Reception ended. Serial port closed.")
