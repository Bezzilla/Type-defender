import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Tracker import Tracker


class StatPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Statistics Visualization")
        self.root.geometry("1200x800")

        # Load data
        self.df = pd.DataFrame(Tracker.read_csv("statistics.csv"))

        # Convert numeric columns
        for col in self.df.columns:
            self.df[col] = pd.to_numeric(self.df[col])

        # Variables
        self.metric_var = tk.StringVar(value=self.df.columns[0])
        self.graph_type_var = tk.StringVar(value="Line Chart")
        self.second_metric_var = tk.StringVar(value="None")

        # Create UI
        self.create_controls()
        self.create_plot_frame()

        # Initial plot
        self.update_plot()

        self.root.mainloop()

    def create_controls(self):
        """Create control panel with dropdowns and buttons"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        # Metric selection
        tk.Label(control_frame, text="Primary Metric:").grid(row=0, column=0,
                                                             padx=5)
        metric_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.metric_var,
            values=list(self.df.columns),
            state="readonly",
            width=20
        )
        metric_dropdown.grid(row=0, column=1, padx=5)

        # Secondary metric
        tk.Label(control_frame, text="Secondary Metric:").grid(row=0, column=2,
                                                               padx=5)
        second_metric_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.second_metric_var,
            values=["None"] + list(self.df.columns),
            state="readonly",
            width=20
        )
        second_metric_dropdown.grid(row=0, column=3, padx=5)

        # Graph type selection
        tk.Label(control_frame, text="Graph Type:").grid(row=0, column=4,
                                                         padx=5)
        graph_type_dropdown = ttk.Combobox(
            control_frame,
            textvariable=self.graph_type_var,
            values=["Line Chart", "Bar Chart", "Scatter Plot",
                    "Histogram", "Box Plot", "Pie Chart"],
            state="readonly",
            width=15
        )
        graph_type_dropdown.grid(row=0, column=5, padx=5)

        # Update button
        update_btn = tk.Button(
            control_frame,
            text="Update Plot",
            command=self.update_plot,
            width=15
        )
        update_btn.grid(row=0, column=6, padx=10)

        # Quit button
        quit_btn = tk.Button(
            control_frame,
            text="Quit",
            command=self.root.destroy,
            width=10
        )
        quit_btn.grid(row=0, column=7, padx=5)

    def create_plot_frame(self):
        """Create frame for matplotlib plots"""
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas = None

    def update_plot(self):
        """Generate the selected plot type"""
        # Clear previous plot
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Get selected options
        metric = self.metric_var.get()
        graph_type = self.graph_type_var.get()
        second_metric = self.second_metric_var.get()

        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6))

        # Generate different plot types
        if graph_type == "Line Chart":
            ax.plot(self.df[metric], marker='o', linestyle='-', color='blue')
            if second_metric != "None":
                ax.plot(self.df[second_metric], marker='s', linestyle='--',
                        color='green')
                ax.legend([metric, second_metric])
            ax.set_title(f"{metric} Over Sessions")

        elif graph_type == "Bar Chart":
            ax.bar(self.df.index, self.df[metric], color='skyblue')
            if second_metric != "None":
                ax.bar(self.df.index, self.df[second_metric],
                       bottom=self.df[metric], color='lightgreen')
                ax.legend([metric, second_metric])
            ax.set_title(f"{metric} by Session")

        elif graph_type == "Scatter Plot":
            if second_metric != "None":
                ax.scatter(self.df[metric], self.df[second_metric],
                           color='red')
                ax.set_xlabel(metric)
                ax.set_ylabel(second_metric)
                ax.set_title(f"{metric} vs {second_metric}")
            else:
                ax.scatter(self.df.index, self.df[metric], color='red')
                ax.set_title(f"{metric} Distribution")
                ax.set_xlabel("Session")

        elif graph_type == "Histogram":
            ax.hist(self.df[metric], bins=10, color='purple',
                    edgecolor='black')
            ax.set_title(f"Distribution of {metric}")

        elif graph_type == "Box Plot":
            if second_metric != "None":
                data = [self.df[metric], self.df[second_metric]]
                ax.boxplot(data, labels=[metric, second_metric])
            else:
                ax.boxplot(self.df[metric])
            ax.set_title(f"Distribution Analysis of {metric}")

        elif graph_type == "Pie Chart":
            if len(self.df) > 10:
                ax.text(0.5, 0.5, "Too many sessions for pie chart",
                        ha='center', va='center')
                ax.set_title("Pie chart not suitable for >10 sessions")
            else:
                ax.pie(self.df[metric], labels=self.df.index,
                       autopct='%1.1f%%')
                ax.set_title(f"{metric} Distribution by Session")

        if graph_type not in ["Pie Chart", "Box Plot"]:
            ax.set_xlabel("Session")
            ax.set_ylabel(metric)
        ax.grid(True)

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


