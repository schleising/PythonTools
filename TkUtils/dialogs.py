"""##Custom Dialogs Created from a Common Dialog Base
- `KeyValueDialog` - Creates a key/value dialog from a Mapping
- `TreeViewDialog` - Creates a Tree View dialog from a two level hierarchy
"""

from typing import Any
from abc import ABC, abstractmethod
from collections.abc import Mapping

import tkinter as tk
import tkinter.ttk as ttk

class DialogBase(ttk.Frame, ABC):
    """Abstract base class for all dialogs inherited from ttk::Frame

    Allows the user to create a standalone dialog or a widget to be added to another, larger app by inheriting from this class

    Args:
        title (str): Title that the dialog will have if standalone
        parent (tk.Tk | None, optional): Parent if any, None if this is a standalone dialog. Defaults to None.
        row (int | None, optional): If this is in a parent, the grid row it will be in. Defaults to None.
        column (int | None, optional): If this is in a parent, the grid column it will be in. Defaults to None.
    """
    def __init__(self, title: str, parent: tk.Tk | None = None, row: int | None = None, column: int | None = None) -> None:
        # If there is no parent window, create one
        if parent is not None and row is not None and column is not None:
            # This is not a standalone widget
            self.standalone = False

            # The parent for all widgets in this frame is self
            self.parent = parent

            # Initialise the base class with the parent of this frame
            super().__init__(parent)

            # Lay this frame out in the grid
            self.grid(row=row, column=column, padx=5, pady=5, sticky=tk.NSEW)

            # Configure the row and column being added
            self.parent.columnconfigure(column, weight=1)
            self.parent.rowconfigure(row, weight=1)

        else:
            # This widget is standalone
            self.standalone = True

            # Create a Tk app as the parent
            self.parent = tk.Tk()

            # Initialise the base class with the Tk app as parent
            super().__init__(self.parent)
            
            # Set the window title
            self.parent.title(title)

            # Set the minimium size of the widget
            self.parent.minsize(1024, 768)

            # Lay this frame out in the grid
            self.grid(row=0, column=0, padx=10, pady=3, sticky=tk.NSEW)

            # Configure the row and column being added
            self.parent.columnconfigure(0, weight=1)
            self.parent.rowconfigure(0, weight=1)

        # Set up the dialog
        self.body()

    # This method must  be overridden
    @abstractmethod
    def body(self) -> None:
        """Abstract method, must be overridden by classes inheriting from DialogBase
        """
        pass

    def run(self) -> None:
        """Can be used to run the dialog if the script would otherwise quit
        """
        self.parent.mainloop()

    def onClose(self) -> None:
        """Called when the dialog is closed, destroys the window and all widgets
        """
        self.parent.destroy()

class KeyValDialog(DialogBase):
    """Creates a Key/Value dialog

    This allows the user to create a simple dialog to show label/value pairs

    Args:
        title (str): Title of the dialog if standalone
        labels (Mapping[str, Any]): The label/value pair data to be displayed in the dialog
        parent (tk.Tk | None, optional): Parent window, if any. Defaults to None.
        row (int | None, optional): If this is in a parent, the grid row it will be in. Defaults to None.
        column (int | None, optional): If this is in a parent, the grid column it will be in. Defaults to None.
    """
    def __init__(self, title: str, labels: Mapping[str, Any], parent: tk.Tk | None = None, row: int | None = None, column: int | None = None) -> None:
        # Set the labels
        self.labels = labels

        # Call base class init
        super().__init__(title, parent, row, column)

    def body(self) -> None:
        """Generates and lays out the dialog widgets, called by the base class on initialisation
        """
        # Loop thorugh the label dict
        for count, (label, value) in enumerate(self.labels.items()):
            # Create the left frame for this row
            leftFrame = ttk.Frame(self)
            leftFrame.grid(row=count, column=0, padx=10, pady=3, sticky=tk.W)

            # Create the right frame for this row
            rightFrame = ttk.Frame(self)
            rightFrame.grid(row=count, column=1, padx=10, pady=3, sticky=tk.W)

            # Add the label to the left frame
            theLabel = ttk.Label(leftFrame, text=label)
            theLabel.pack()

            # Add the value to the right frame
            theValue = ttk.Label(rightFrame, text=value)
            theValue.pack()

            # Configure the row to auto expand
            self.rowconfigure(count, weight=1, minsize=26)

        # Configure the left column to be fixed width
        self.columnconfigure(0, weight=0, minsize=150)

        # Configure the right column to expand
        self.columnconfigure(1, weight=1, minsize=150)

        # Only create the Close button if this is a standalone widget
        if self.standalone:
            # Create a frame for the Close button
            frame = ttk.Frame(self)
            frame.grid(row=len(self.labels), column=1, padx=10, pady=3, sticky=tk.E)

            # Create the Close button
            self.close = ttk.Button(frame, text='Close', command=self.onClose)
            self.close.pack()

            # Configure the button row
            self.rowconfigure(len(self.labels), weight=1, minsize=26)

class TreeViewDialog(DialogBase):
    """Creates a TreeViewDialog

    Args:
        title (str): Title of the dialog if standalone
        headings (list[str]): The column headings for the Tree View
        hierarchy (Mapping[str, Mapping[str, Any]]): The two level mapping for the Tree View data
        parent (tk.Tk | None, optional): Parent window, if any. Defaults to None.
        row (int | None, optional): If this is in a parent, the grid row it will be in. Defaults to None.
        column (int | None, optional): If this is in a parent, the grid column it will be in. Defaults to None.
    """
    def __init__(self, title: str, headings: list[str], hierarchy: Mapping[str, Mapping[str, Any]], parent: tk.Tk | None = None, row: int | None = None, column: int | None = None) -> None:
        # Set the headings
        self.headings = headings

        # Call base class init
        super().__init__(title, parent, row, column)

        # Set the labels
        self.hierarchy = hierarchy

    @property
    def hierarchy(self) -> None:
        """Used to update the hierarchy after initialisation, write only

        Args:
            newHierarchy (Mapping[str, Mapping[str, Any]]): The two level mapping for the Tree View data

        Raises:
            ValueError: Raised if the user tries to get the hierarchy
        """
        raise ValueError

    @hierarchy.setter
    def hierarchy(self, newHierarchy: Mapping[str, Mapping[str, Any]]) -> None:
        # Delete all items in the TreeView
        self.treeview.delete(*self.treeview.get_children())

        # Insert the rows
        for key, vals in newHierarchy.items():
            # If there is only one item open it at startup
            if len(newHierarchy) == 1:
                openNode = True
            else:
                openNode = False

            # Insert the parent row
            parent = self.treeview.insert('', tk.END, None, text=key, open=openNode)

            # Insert the child rows
            for label, val in vals.items():
                self.treeview.insert(parent, tk.END, None, text=label, values=[val])

    def body(self) -> None:
        """Generates and lays out the dialog widgets, called by the base class on initialisation
        """
        # Create the TreeView Scrollbar
        scrollbar = ttk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create the TreeView
        self.treeview = ttk.Treeview(self, columns=self.headings[1:], yscrollcommand=scrollbar.set)

        # Confirgure the Scrollbar to scroll the TreeView
        scrollbar.config(command=self.treeview.yview)

        # Set the Treeview headings
        for colCount, heading in enumerate(self.headings):
            self.treeview.heading(f'#{colCount}', text=heading)

        # Pack the TreeView in the frame allowing it to expand to fill both x and y
        self.treeview.pack(fill=tk.BOTH, expand=tk.TRUE)

        # Only create the Close button if this is a standalone widget
        if self.standalone:
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

    # Create the root window
    root = tk.Tk()

    # Test the Key/Val dialog
    widget1 = KeyValDialog('Key/Val Dialog', {'One': 'First', 'Two': 'Second', 'Three': 'Third', 'Four': 'Fourth', 'Five': 'Fifth'}, parent=root, row=0, column=0)

    # Test the Treeview dialog
    widget2 = TreeViewDialog('TreeView Dialog', ['Keys', 'Values'], hierarchy, parent=root, row=1, column=0)

    # Start the main loop
    root.mainloop()
