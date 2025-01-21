import customtkinter as ctk
import admin_interface
import pandas as pd
import os
import csv


def create_root_add_team_frame(frame, parent_frame):
    global team_entry_lbl

    for widget in frame.winfo_children():
        widget.destroy()

    add_team_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    add_team_main_frame.configure(fg_color="#202020")
    add_team_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    header_frame = ctk.CTkFrame(add_team_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    label = ctk.CTkLabel(header_frame, text="Add Team", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")


    main_frame = ctk.CTkFrame(add_team_main_frame, corner_radius=10, fg_color="#212121")
    main_frame.pack(pady=(100, 40), padx=40, fill="none", side="top")

    entry = ctk.CTkEntry(main_frame, placeholder_text="Enter Team Name..", width=350, height=50, font=("Arial", 20))
    entry.pack(side="top", padx=20, pady=20)


    save_btn = ctk.CTkButton(main_frame, width=350, height=50, text="Save Team", font=("Arial", 16),
                command=lambda: save_team(entry))
    save_btn.pack(side="top", padx=20, pady=20)

    team_entry_lbl = ctk.CTkLabel(add_team_main_frame, text="", font=("Arial", 14), height=0)
    team_entry_lbl.configure(text_color="red")
    team_entry_lbl.pack(side="top")


    # Create a back button in the header frame
    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(add_team_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)




def save_team(entry):

    team_name = entry.get().strip()
    if not team_name:
        print("Team name cannot be empty.")
        team_entry_lbl.configure(text="Team name cannot be empty.", text_color="red")
        return

    file_path = "src/teams.csv"
    if os.path.isfile(file_path):
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row and row[0].strip().lower() == team_name.lower():
                    team_entry_lbl.configure(text=f"Team '{team_name}' already exists.", text_color="red")
                    return


    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
            writer.writerow(["Team Name", "Score"])

        writer.writerow([team_name, 0])

    entry.delete(0, 'end')
    team_entry_lbl.configure(text=f"Team '{team_name}' saved successfully!", text_color="green")





def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    admin_interface.show_admin_frame(root=parent_frame)

