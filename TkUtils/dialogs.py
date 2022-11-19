from typing import Any, Mapping

import tkinter as tk
import tkinter.ttk as ttk

class KeyValDialog():
    def __init__(self, title: str, labels: Mapping[str, Any], master: tk.Tk | None = None) -> None:
        # If there is no master window, create one
        if master is not None:
            self.master = master
        else:
            self.master = tk.Tk()

        # Set the labels
        self.labels = labels

        # Set the wondow title
        self.master.title(title)

        # Set up the dialog
        self.body()

    def body(self) -> None:
        # Loop thorugh the label dict
        for count, (label, value) in enumerate(self.labels.items()):
            # Create the left frame for this row
            leftFrame = ttk.Frame(self.master)
            leftFrame.grid(row=count, column=0, padx=10, pady=3, sticky=tk.W)

            # Create the right frame for this row
            rightFrame = ttk.Frame(self.master)
            rightFrame.grid(row=count, column=1, padx=10, pady=3, sticky=tk.W)

            # Add the label to the left frame
            theLabel = ttk.Label(leftFrame, text=label)
            theLabel.pack()

            # Add the value to the right frame
            theValue = ttk.Label(rightFrame, text=value)
            theValue.pack()

            # Configure the row to auto expand
            self.master.rowconfigure(count, weight=1, minsize=26)

        # Create a frame for the Close button
        frame = ttk.Frame(self.master)
        frame.grid(row=len(self.labels), column=1, padx=10, pady=3, sticky=tk.E)

        # Create the Close button
        self.close = ttk.Button(frame, text='Close', command=self.onClose)
        self.close.pack()

        # Configure the button row
        self.master.rowconfigure(len(self.labels), weight=1, minsize=26)

        # Configure the left column to be fixed width
        self.master.columnconfigure(0, weight=0, minsize=150)

        # Configure the right column to expand
        self.master.columnconfigure(1, weight=1, minsize=150)

    def run(self) -> None:
        # Can be used to run the dialog if the script would otherwise quit
        self.master.mainloop()

    def onClose(self) -> None:
        # Destroy the window and all widgets
        self.master.destroy()

if __name__ == '__main__':
    # Test the dialog
    dlg = KeyValDialog('Key/Val Dialog', {'One': 'First', 'Two': 'Second', 'Three': 'Third', 'Four': 'Fourth', 'Five': 'Fifth'})
    dlg.run()
