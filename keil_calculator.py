# main frame
import tkinter
from tkinter import *
import random
def timers_code():
    import tkinter as tk

    def calculate():
        try:
            frequency = float(entry_frequency.get())
            time_delay = float(entry_delay.get())

            # Calculate Control Word format
            control_word = 65536 - (time_delay * frequency)
            control_word = hex(int(control_word))[2:].upper()
            label_control_word.config(text="Control Word Format: " + control_word)

            # Calculate Delay
            delay = control_word / frequency
            label_delay.config(text="Delay (seconds): " + str(delay))

            # Calculate Count Value
            count_value = 256 - (time_delay * frequency)
            label_count_value.config(text="Count Value: " + str(int(count_value)))

        except ValueError:
            label_control_word.config(text="Invalid input!")
            label_delay.config(text="")
            label_count_value.config(text="")

    # Create main window
    root = tk.Tk()
    root.title("8051 Timer Calculator")

    # Frequency input
    label_frequency = tk.Label(root, text="Frequency (Hz):")
    label_frequency.grid(row=0, column=0)
    entry_frequency = tk.Entry(root)
    entry_frequency.grid(row=0, column=1)

    # Time delay input
    label_delay = tk.Label(root, text="Time Delay (seconds):")
    label_delay.grid(row=1, column=0)
    entry_delay = tk.Entry(root)
    entry_delay.grid(row=1, column=1)

    # Calculate button
    button_calculate = tk.Button(root, text="Calculate", command=calculate)
    button_calculate.grid(row=2, columnspan=2)

    # Result labels
    label_control_word = tk.Label(root, text="")
    label_control_word.grid(row=3, columnspan=2)

    label_delay = tk.Label(root, text="")
    label_delay.grid(row=4, columnspan=2)

    label_count_value = tk.Label(root, text="")
    label_count_value.grid(row=5, columnspan=2)

    root.mainloop()

def serial_communication():
    import tkinter as tk

    def calculate():
        oscillator_frequency = float(oscillator_entry.get())
        baud_rate = float(baud_rate_entry.get())
        mode = int(mode_entry.get())

        tmod = calculate_tmod(baud_rate, oscillator_frequency)
        scon = calculate_scon(mode, baud_rate)
        tmod_cwf = calculate_tmod_cwf(tmod)
        delay = calculate_delay(baud_rate)
        calculated_baud_rate = calculate_baud_rate(tmod, oscillator_frequency)

        results_label.config(text=f"TMOD: {hex(int(tmod))}\n"
                                  f"SCON: {hex(int(scon))}\n"
                                  f"TMOD CWF: {tmod_cwf}\n"
                                  f"Delay: {delay}\n"
                                  f"Calculated Baud Rate: {calculated_baud_rate}")

    def calculate_tmod(baud_rate, oscillator_frequency):
        reload_value = 256 - (oscillator_frequency / (32 * baud_rate))
        tmod = reload_value / 32
        return tmod

    def calculate_scon(mode, baud_rate):
        smod = 0  # Assuming SMOD is 0 for simplicity
        if mode == 0:  # Mode 0
            scon = 0x40 if baud_rate == 9600 else 0x00
        elif mode == 1:  # Mode 1
            scon = 0x50 if baud_rate == 9600 else 0x00
        else:
            raise ValueError("Invalid mode. Mode must be 0 or 1.")
        return scon | smod

    def calculate_tmod_cwf(tmod):
        tmod_cwf = ((int(tmod) & 0x01) << 6) | ((int(tmod) & 0x02) << 4) | ((int(tmod) & 0x04) << 2) | (
                    (int(tmod) & 0x08) << 0)
        return hex(tmod_cwf)

    def calculate_delay(baud_rate):
        return 1 / baud_rate

    def calculate_baud_rate(tmod, oscillator_frequency):
        reload_value = tmod * 32
        baud_rate = oscillator_frequency / (32 * (256 - reload_value))
        return baud_rate

    # GUI
    root = tk.Tk()
    root.title("Serial Communication Calculator")

    # Labels
    tk.Label(root, text="Oscillator Frequency (Hz):").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(root, text="Baud Rate:").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(root, text="Mode (0 or 1):").grid(row=2, column=0, padx=5, pady=5)
    tk.Label(root, text="Results:").grid(row=4, column=0, padx=5, pady=5)

    # Entry fields
    oscillator_entry = tk.Entry(root)
    oscillator_entry.grid(row=0, column=1, padx=5, pady=5)
    baud_rate_entry = tk.Entry(root)
    baud_rate_entry.grid(row=1, column=1, padx=5, pady=5)
    mode_entry = tk.Entry(root)
    mode_entry.grid(row=2, column=1, padx=5, pady=5)

    # Results label
    results_label = tk.Label(root, text="", justify="left")
    results_label.grid(row=4, column=1, padx=5, pady=5)

    # Calculate button
    calculate_button = tk.Button(root, text="Calculate", command=calculate)
    calculate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    root.mainloop()

def interrupt():
    import tkinter as tk
    from tkinter import messagebox

    def calculate():
        try:
            tmod = int(entry_tmod.get())
            scon = int(entry_scon.get(), 16)
            tmod_cwf = bin(tmod)[2:].zfill(8)
            delay = tmod * (1 / 11.0592) * 1000
            baud_rate = 11.0592 / (32 * (12 - (scon >> 4)))
            ie = scon & 0x02

            label_tmod_cwf.config(text=tmod_cwf)
            label_delay.config(text="{:.2f} ms".format(delay))
            label_baud_rate.config(text="{:.2f} baud".format(baud_rate))
            label_ie.config(text="Enabled" if ie else "Disabled")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values.")

    # Create main window
    root = tk.Tk()

    # Labels
    tk.Label(root, text="TMOD:").grid(row=0, column=0)
    tk.Label(root, text="SCON:").grid(row=1, column=0)
    tk.Label(root, text="TMOD CWF:").grid(row=2, column=0)
    tk.Label(root, text="Delay:").grid(row=3, column=0)
    tk.Label(root, text="Baud Rate:").grid(row=4, column=0)
    tk.Label(root, text="IE:").grid(row=5, column=0)

    # Entry fields
    entry_tmod = tk.Entry(root)
    entry_tmod.grid(row=0, column=1)
    entry_scon = tk.Entry(root)
    entry_scon.grid(row=1, column=1)

    # Result labels
    label_tmod_cwf = tk.Label(root, text="")
    label_tmod_cwf.grid(row=2, column=1)
    label_delay = tk.Label(root, text="")
    label_delay.grid(row=3, column=1)
    label_baud_rate = tk.Label(root, text="")
    label_baud_rate.grid(row=4, column=1)
    label_ie = tk.Label(root, text="")
    label_ie.grid(row=5, column=1)

    # Calculate button
    calculate_button = tk.Button(root, text="Calculate", command=calculate)
    calculate_button.grid(row=6, column=0, columnspan=2)

    root.mainloop()


def helpme():
    f = open("HELP.txt", "r")
    print(f.read())
root = Tk()
root.title("KEIL 8051 Calculator")
root.minsize(width=400, height=400)
root.geometry("900x700")

same = True
n = 0.25

# title card
headingFrame1 = Frame(root, bg="#FF006A", bd=5)
headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.10)
headingLabel = Label(headingFrame1, text="KEIL 8051 Calculator", bg='black', fg='white', font=('Times new roman', 45))
headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
# buttons
btn1 = Button(root, text="Timers and Counters", bg='white', fg='black', command=timers_code)
btn1.place(relx=0.38, rely=0.4, relwidth=0.25, relheight=0.05)

btn2 = Button(root, text="Serial Communication", bg='white', fg='black', command=serial_communication)
btn2.place(relx=0.38, rely=0.5, relwidth=0.25, relheight=0.05)

btn3 = Button(root, text="Interrupt Calculations", bg='white', fg='black', command=interrupt)
btn3.place(relx=0.38, rely=0.6, relwidth=0.25, relheight=0.05)

btn5 = Button(root, text="Help", bg='white', fg='black', command=helpme)
btn5.place(relx=0.38, rely=0.8, relwidth=0.25, relheight=0.05)

root.mainloop()