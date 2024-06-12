import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog
import mplcursors

# Function to plot the data
def plot_data():
    global x_dropdown_vars, y_dropdown_vars, num_plots

    # Get the number of rows and columns for the subplots
    a = int(rows_entry.get())
    b = int(cols_entry.get())
    num_plots = a * b

    # Create subplots
    fig, axs = plt.subplots(nrows=a, ncols=b, figsize=(15, 10))

    # Adjust for single row/column cases
    if a == 1:
        axs = [axs]
    if b == 1:
        axs = [[ax] for ax in axs]

    # Plot the data
    index = 0
    for i in range(a):
        for j in range(b):
            if index >= num_plots:
                break
            x_column = x_dropdown_vars[index].get()
            y_column = y_dropdown_vars[index].get()
            print(f"Plotting {y_column} vs {x_column}")  # Debugging statement

            # Check if 'All Cells' is selected and compute the average
            if x_column == "All Cells":
                df['All Cells'] = df[[col for col in df.columns if 'Cell_' in col]].mean(axis=1)
                x_column = 'All Cells'
                x_unit = 'V'  # Assigning the unit 'V' when 'All Cells' is selected
            else:
                x_unit = units[df.columns.get_loc(x_column)]

            if y_column == "All Cells":
                df['All Cells'] = df[[col for col in df.columns if 'Cell_' in col]].mean(axis=1)
                y_column = 'All Cells'
                y_unit = 'V'  # Assigning the unit 'V' when 'All Cells' is selected
            else:
                y_unit = units[df.columns.get_loc(y_column)]

            # Check if the selected columns exist in the dataframe
            if x_column not in df.columns or y_column not in df.columns:
                print(f"Column not found: {x_column} or {y_column}")
                index += 1
                continue
            
            # Round the data to 3 decimal places
            df[x_column] = df[x_column].round(3)
            df[y_column] = df[y_column].round(3)

            axs[i][j].plot(df[x_column], df[y_column])
            axs[i][j].set_title(f'{y_column} vs {x_column}')
            axs[i][j].set_xlabel(f'{x_column} ({x_unit})')
            axs[i][j].set_ylabel(f'{y_column} ({y_unit})')
            axs[i][j].set_facecolor('black')

            # Grid
            axs[i][j].grid()

            index += 1

    # Adjust layout
    plt.tight_layout()
    mplcursors.cursor(hover=True)

    # Format hover text to 3 decimal places
    for ax_row in axs:
        for ax in ax_row:
            for line in ax.get_lines():
                mplcursors.cursor(line).connect("add", lambda sel: sel.annotation.set_text(f'x={sel.target[0]:.2f}, y={sel.target[1]:.2f}'))
    
    # Show the plot
    plt.show()

# Function to generate dropdowns based on the number of subplots
def generate_dropdowns():
    global x_dropdown_vars, y_dropdown_vars

    # Clear previous dropdowns
    for widget in root.grid_slaves():
        if int(widget.grid_info()["row"]) > 2:
            widget.grid_forget()

    x_dropdown_vars = []
    y_dropdown_vars = []

    a = int(rows_entry.get())
    b = int(cols_entry.get())
    num_plots = a * b

    columns_with_all_cells = ['All Cells'] + list(df.columns)

    for i in range(num_plots):
        tk.Label(root, text=f"Plot {i+1}: X axis").grid(row=i+3, column=0)
        x_var = tk.StringVar()
        x_dropdown = ttk.Combobox(root, textvariable=x_var, values=columns_with_all_cells)
        x_dropdown.grid(row=i+3, column=1)
        x_dropdown.current(0)
        x_dropdown_vars.append(x_var)
        
        tk.Label(root, text=f"Plot {i+1}: Y axis").grid(row=i+3, column=2)
        y_var = tk.StringVar()
        y_dropdown = ttk.Combobox(root, textvariable=y_var, values=columns_with_all_cells)
        y_dropdown.grid(row=i+3, column=3)
        y_dropdown.current(0)
        y_dropdown_vars.append(y_var)

    # Create the Plot Data button after generating the dropdowns
    plot_button = tk.Button(root, text="Plot Data", command=plot_data)
    plot_button.grid(row=num_plots + 4, column=0, columnspan=4)

# Function to load the CSV file
def load_file():
    global df, units

    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    # Load the CSV file, skipping the second line
    df = pd.read_csv(file_path, skiprows=[1])

    # Round the data to 3 decimal places
    df = df.round(2)

    # Load the second line to get the units
    with open(file_path, 'r') as file:
        lines = file.readlines()
        units_line = lines[1].strip().split(',')
        print("Units line:", units_line)

    # Extract units for labeling
    units = units_line  

    generate_button.grid(row=2, column=0, columnspan=2)  # Enable the Generate Dropdowns button

# Create the main window
root = tk.Tk()
root.title("Plot Data")

# Input for the number of rows and columns
tk.Label(root, text="Number of rows:").grid(row=0, column=0)
rows_entry = tk.Entry(root)
rows_entry.grid(row=0, column=1)

tk.Label(root, text="Number of columns:").grid(row=1, column=0)
cols_entry = tk.Entry(root)
cols_entry.grid(row=1, column=1)

# Button to load the CSV file
load_button = tk.Button(root, text="Load CSV File", command=load_file)
load_button.grid(row=0, column=2, columnspan=2)

# Button to generate dropdowns (initially disabled until a file is loaded)
generate_button = tk.Button(root, text="Generate Dropdowns", command=generate_dropdowns)
generate_button.grid(row=2, column=0, columnspan=2)
generate_button.grid_remove()  # Hide the button initially

# Start the Tkinter main loop
root.mainloop()
