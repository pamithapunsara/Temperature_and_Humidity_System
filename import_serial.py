import serial
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

arduino = serial.Serial('COM6', 9600)
window = tk.Tk()
window.title("Temperature Humidity Monitor")
window.geometry("800x600")

fig = Figure(figsize=(7, 4), dpi=100)
ax_temperature = fig.add_subplot(121)
ax_humidity = fig.add_subplot(122)

temperature_data = []
humidity_data = []
time_data = []

temperature_label = tk.Label(window, text="Temperature: - °C", font=("Arial", 12), fg="black")
temperature_label.pack(pady=10)

humidity_label = tk.Label(window, text="Humidity: - %", font=("Arial", 12), fg="black")
humidity_label.pack(pady=10)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(pady=10)




# Function to send command to Arduino
def send_command(command):
    arduino.write(command.encode())

# Function to turn LED on
def turn_on():
    send_command('H')
    btn_on.configure(bg='green')
    btn_off.configure(bg='SystemButtonFace')

# Function to turn LED off
def turn_off():
    send_command('L')
    btn_on.configure(bg='SystemButtonFace')
    btn_off.configure(bg='red')

# Create buttons
btn_on = tk.Button(window, text="Turn On FAN", command=turn_on, bg='SystemButtonFace', width=35, height=4)
btn_on.pack()

btn_off = tk.Button(window, text="Turn Off FAN", command=turn_off, bg='SystemButtonFace', width=35, height=4)
btn_off.pack()





def read_data():
    data = arduino.readline().decode().strip()
    data = data.replace('\x00', '')  # Remove null bytes from the data

    try:
        temperature, humidity = map(float, data.split(',')) if data else (None, None)


    except ValueError:
        temperature, humidity = None, None

    if temperature is not None and humidity is not None:
        temperature_data.append(temperature)
        humidity_data.append(humidity)
        time_data.append(len(time_data) + 1)
        
        temperature_label.configure(text=f"Temperature: {temperature:.2f} °C")
        humidity_label.configure(text=f"Humidity: {humidity:.2f} %")
        
        ax_temperature.clear()
        ax_temperature.plot(time_data, temperature_data, '-', markersize=2)
        ax_temperature.set_xlabel("Time")
        ax_temperature.set_ylabel("Temperature (°C)")
        ax_temperature.grid(True)
        
        ax_humidity.clear()
        ax_humidity.plot(time_data, humidity_data, '-', markersize=2)
        ax_humidity.set_xlabel("Time")
        ax_humidity.set_ylabel("Humidity (%)")
        ax_humidity.grid(True)
        
        canvas.draw()
        
        #control_led(temperature)  # Control LED based on temperature

    window.after(100, read_data) 

read_data()
window.mainloop()
