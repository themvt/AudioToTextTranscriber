import tkinter as tk

def create_button(root, text, command, bg=None, fg=None):
    """
    Creates a styled button.

    :param root: Parent widget
    :param text: Button text
    :param command: Command to execute when the button is clicked
    :param bg: Background color (optional)
    :param fg: Foreground color (optional)
    :return: The created button
    """
    button = tk.Button(root, text=text, command=command, bg=bg, fg=fg, padx=10, pady=5)
    button.pack(pady=5)
    return button

def create_text_area(root):
    """
    Creates a scrollable text area for displaying logs.

    :param root: Parent widget
    :return: The created text widget
    """
    text_area = tk.Text(root, height=15, width=60, state=tk.NORMAL)
    text_area.pack(pady=5)
    
    scroll_bar = tk.Scrollbar(root)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_area.config(yscrollcommand=scroll_bar.set)
    scroll_bar.config(command=text_area.yview)
    
    return text_area
