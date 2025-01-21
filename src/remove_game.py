import customtkinter as ctk
import admin_interface
import pandas as pd
import os

def create_root_remove_game_frame(frame, parent_frame):
        # Hide the parent frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a new frame
    remove_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    remove_main_frame.configure(fg_color="#202020")
    remove_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    # Create a frame for the label and back button
    header_frame = ctk.CTkFrame(remove_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    # Add a label in the header frame
    label = ctk.CTkLabel(header_frame, text="Remove Game", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")

    # Create a back button in the header frame
    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(remove_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)



def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    admin_interface.show_admin_frame(root=parent_frame)

