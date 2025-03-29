import serial
import os

# Configure serial connection
ser = serial.Serial(port="COM10", baudrate=115200, timeout=1)

file = None  # File handler, initially None
filename = None  # To store the received filename

print("Waiting for filename and start marker...")

while True:
    try:
        line = ser.readline().decode("utf-8", errors="ignore").strip()  # Ignore decoding errors

        if line:
            # Skip debug messages that contain "Received:" or "file_transfer"
            if "Received:" in line or "file_transfer" in line:
                continue

            # If filename is received (Expected format: "FILENAME:sensor_1_date_3.csv")
            if line.startswith("FILENAME:"):
                filename = line.split("FILENAME:")[1].strip()  # Extract the actual filename
                filename = os.path.basename(filename)  # Ensure no path injection
                continue  # Move to the next line (Wait for START)

            # If we detect the start marker, begin saving data
            if line == "START":
                if filename:  # Ensure we have received a filename
                    file = open(filename, "w", encoding="utf-8")  # Open file with UTF-8 encoding
                    print(f"Data transmission started. Saving data to {filename}...")
                else:
                    print("⚠️ No filename received before START. Skipping save.")
                continue  # Skip the start marker itself

            # If we detect the end marker, close the current file and stop saving
            if line == "END":
                if file:  # Ensure there's an open file before closing
                    file.close()
                    print(f"Data transmission ended. {filename} saved.")
                file = None  # Reset file handler
                filename = None  # Reset filename
                
                # **Exit the script when all CSVs are received**
                print("All files received. Exiting...")
                break  # Exit while loop

            # Save data only if a file is currently open
            if file:
                print(f"Received: {line}")  # Optional: Print received line for debugging
                file.write(line + "\n")  # Write to file

    except KeyboardInterrupt:
        print("Stopping reception...")
        break

# Close serial port before exiting
ser.close()
print("Reception ended. Serial port closed.")


