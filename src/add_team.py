import customtkinter as ctk
import admin_interface
import pandas as pd
import os
import csv


def create_root_add_team_frame(frame, parent_frame):
        # Hide the parent frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a new frame
    add_team_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    add_team_main_frame.configure(fg_color="#202020")
    add_team_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    # Create a frame for the label and back button
    header_frame = ctk.CTkFrame(add_team_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    # Add a label in the header frame
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




    # Create a back button in the header frame
    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(add_team_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)




def save_team(entry):
    print("btn clicked")

    team_name = entry.get().strip()
    if not team_name:
        print("Team name cannot be empty.")
        return
    
    # Define the file path for the CSV file
    file_path = "teams.csv"
    # Check if the team already exists
    if os.path.isfile(file_path):  # Check if the file exists
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip the header row
            for row in reader:
                if row and row[0].strip().lower() == team_name.lower():
                    print(f"Team '{team_name}' already exists.")
                    return  # Exit the function if the team already exists

    # Open the file in append mode
    with open(file_path, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # If the file does not exist, write the header first
        if not os.path.isfile(file_path) or os.stat(file_path).st_size == 0:
            writer.writerow(["Team Name", "Score"])  # Write header row
        
        # Write the team name and initial score of 0
        writer.writerow([team_name, 0])
    
    # Clear the entry field and print a success message
    entry.delete(0, 'end')
    print(f"Team '{team_name}' saved successfully!")





def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    admin_interface.show_admin_frame(root=parent_frame)

