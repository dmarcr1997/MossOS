from tkinter import font, ttk

#Theme colors
colors = {
    "background": "#f3e5ab",
    "primary": "#a5c48e",
    "accent": "#d1bfa3",
    "highlight": "#ffeb99",
    "text": "#2e472e",
    "light": "#fffaf0",
    "panel": "#e0d8b0"
}

def apply_theme(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    # Global font
    custom_font = font.Font(family="Segoe UI", size=9)
    root.option_add("*Font", custom_font)

    # Global Styles
    style.configure(".",
        background=colors["background"],
        foreground=colors["text"]
    )

    # Button styles
    style.configure("TButton",
        background=colors["primary"],
        foreground=colors["text"],
        padding=6,
        relief="flat"
    )
    style.map("TButton",
        background=[("active", colors["accent"])]
    )

    # Entry Styles
    style.configure("TEntry",
        fieldbackground=colors["light"],
        foreground=colors["text"],
        padding=4,
        font=("Segoe UI", 9)
    )

    # Label Styles
    style.configure("TLabel",
        background=colors["background"],
        foreground=colors["text"]
    )

    # Root background color
    root.configure(bg=colors["background"])