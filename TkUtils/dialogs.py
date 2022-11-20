from typing import Any, Mapping
from abc import ABC, abstractmethod

import tkinter as tk
import tkinter.ttk as ttk

class DialogBase(ABC, ttk.Frame):
    def __init__(self, title: str, parent: tk.Tk | None) -> None:
        # If there is no parent window, create one
        if parent is not None:
            self.parent = parent
        else:
            self.parent = tk.Tk()

        # Set the wondow title
        self.parent.title(title)

        # Set up the dialog
        self.body()

    @abstractmethod
    def body(self) -> None:
        pass

    def run(self) -> None:
        # Can be used to run the dialog if the script would otherwise quit
        self.parent.mainloop()

    def onClose(self) -> None:
        # Destroy the window and all widgets
        self.parent.destroy()

class KeyValDialog(DialogBase):
    def __init__(self, title: str, labels: Mapping[str, Any], parent: tk.Tk | None = None) -> None:
        # Set the labels
        self.labels = labels

        # Call base class init
        super().__init__(title, parent)

    def body(self) -> None:
        # Loop thorugh the label dict
        for count, (label, value) in enumerate(self.labels.items()):
            # Create the left frame for this row
            leftFrame = ttk.Frame(self.parent)
            leftFrame.grid(row=count, column=0, padx=10, pady=3, sticky=tk.W)

            # Create the right frame for this row
            rightFrame = ttk.Frame(self.parent)
            rightFrame.grid(row=count, column=1, padx=10, pady=3, sticky=tk.W)

            # Add the label to the left frame
            theLabel = ttk.Label(leftFrame, text=label)
            theLabel.pack()

            # Add the value to the right frame
            theValue = ttk.Label(rightFrame, text=value)
            theValue.pack()

            # Configure the row to auto expand
            self.parent.rowconfigure(count, weight=1, minsize=26)

        # Create a frame for the Close button
        frame = ttk.Frame(self.parent)
        frame.grid(row=len(self.labels), column=1, padx=10, pady=3, sticky=tk.E)

        # Create the Close button
        self.close = ttk.Button(frame, text='Close', command=self.onClose)
        self.close.pack()

        # Configure the button row
        self.parent.rowconfigure(len(self.labels), weight=1, minsize=26)

        # Configure the left column to be fixed width
        self.parent.columnconfigure(0, weight=0, minsize=150)

        # Configure the right column to expand
        self.parent.columnconfigure(1, weight=1, minsize=150)

class TreeViewDialog(DialogBase):
    def __init__(self, title: str, headings: list[str], hierarchy: Mapping[str, Mapping[str, Any]], parent: tk.Tk | None = None) -> None:
        # Set the labels
        self.hierarchy = hierarchy

        # Set the headings
        self.headings = headings

        # Call base class init
        super().__init__(title, parent)

    def body(self) -> None:
        # Set the minimum size of the window
        self.parent.minsize(1024, 768)

        # Create a frame to contain the TreeView and Scrollbar

        tvFrame = ttk.Frame(self.parent)
        tvFrame.grid(row=0, column=0, padx=10, pady=3, sticky=tk.NSEW)

        # Configure this grid cell to stretch in both x and y
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        # Create the TreeView Scrollbar
        scrollbar = ttk.Scrollbar(tvFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the TreeView
        treeview = ttk.Treeview(tvFrame, columns=self.headings[1:], yscrollcommand=scrollbar.set)

        # Confirgure the Scrollbar to scroll the TreeView
        scrollbar.config(command=treeview.yview)

        # Set the Treeview headings
        for colCount, heading in enumerate(self.headings):
            treeview.heading(f'#{colCount}', text=heading)

        # Insert the rows
        for key, vals in self.hierarchy.items():
            # Insert the parent row
            parent = treeview.insert('', tk.END, None, text=key)

            # Insert the child rows
            for label, val in vals.items():
                treeview.insert(parent, tk.END, None, text=label, values=[val])

        # Pack the TreeView in the frame allowing it to expand to fill both x and y
        treeview.pack(fill=tk.BOTH, expand=tk.TRUE)

        # Create a frame for the Close button
        frame = ttk.Frame(self.parent)
        frame.grid(row=1, column=0, padx=10, pady=3, sticky=tk.E)

        # Create the Close button
        self.close = ttk.Button(frame, text='Close', command=self.onClose)
        self.close.pack()

        # Configure the button row
        self.parent.rowconfigure(1, weight=0, minsize=26)

if __name__ == '__main__':
    hierarchy: dict[str, dict[str, str]] = {
        'One' : {
            'FirstItem': '1st',
            'SecondItem': '2nd',
            'ThirdItem': '3rd',
        },
        'Two': {
            'FourthItem': '4th',
            'FifthItem': '5th',
        },
        'Three': {
        },
        'Four': {
            'SixthItem': '6th',
            'SeventhItem': '7th',
        },
    }

    # Test the Key/Val dialog
    dlg = KeyValDialog('Key/Val Dialog', {'One': 'First', 'Two': 'Second', 'Three': 'Third', 'Four': 'Fourth', 'Five': 'Fifth'})
    dlg.run()

    # Test the Treeview dialog
    dlg = TreeViewDialog('TreeView Dialog', ['Keys', 'Values'], hierarchy)
    dlg.run()
