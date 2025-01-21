import customtkinter as ctk
import admin_interface
import pandas as pd
import os

def create_root_remove_team_frame(frame, parent_frame):
    global combobox, remove_btn, team_entry_lbl
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
    label = ctk.CTkLabel(header_frame, text="Remove Team", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")

    # Create a back button in the header frame
    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(remove_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)


    main_frame = ctk.CTkFrame(remove_main_frame, corner_radius=10, fg_color="#212121")
    main_frame.pack(pady=(100, 40), padx=40, fill="none", side="top")

    team_names = load_team_names()
    
    # Set up combobox
    if team_names:
        combobox_values = team_names
        remove_btn_state = "normal"
    else:
        combobox_values = ["No teams exist"]
        remove_btn_state = "disabled"

    combobox_var = ctk.StringVar(value=combobox_values[0])
    combobox = ctk.CTkComboBox(
        main_frame,
        values=combobox_values,
        variable=combobox_var,
        width=350,
        height=50,
        font=("Arial", 20)
    )
    combobox.pack(side="top", padx=20, pady=20)

    team_entry_lbl = ctk.CTkLabel(main_frame, text="", font=("Arial", 14), height=0)
    team_entry_lbl.configure(text_color="red")
    team_entry_lbl.pack(side="top")

# Remove Team Button
    remove_btn = ctk.CTkButton(
        main_frame,
        width=350,
        height=50,
        text="Remove Team",
        font=("Arial", 16),
        state=remove_btn_state,
        command=lambda: remove_team(combobox_var.get())
    )
    remove_btn.pack(side="top", padx=20, pady=20)

def load_team_names():
    file_path = "src/teams.csv"
    if not os.path.isfile(file_path):
        return []

    try:
        df = pd.read_csv(file_path)
        if "Team Name" in df.columns:
            return df["Team Name"].tolist()
        else:
            return []
    except Exception as e:
        print(f"Error loading teams.csv: {e}")
        return []

def remove_team(team_name):
    file_path = "src/teams.csv"
    if not os.path.isfile(file_path):
        print("No teams file found.")
        return

    try:
        df = pd.read_csv(file_path)
        if "Team Name" not in df.columns:
            print("Invalid file format.")
            return

        # Filter out the selected team
        df = df[df["Team Name"] != team_name]

        # Save the updated file
        df.to_csv(file_path, index=False)
        print(f"Team '{team_name}' removed successfully!")
        team_entry_lbl.configure(text=f"Team '{team_name}' removed successfully!", text_color="green")


        refresh_ui()
    except Exception as e:
        print(f"Error removing team: {e}")



def refresh_ui():
    """Refresh the combobox and remove button state."""
    # Reload team names
    team_names = load_team_names()
    
    # Update the combobox values
    if team_names:
        combobox.configure(values=team_names)
        combobox.set(team_names[0])  # Set the first value as selected
        remove_btn.configure(state="normal")  # Enable the remove button
    else:
        combobox.configure(values=["No teams exist"])
        combobox.set("No teams exist")
        remove_btn.configure(state="disabled")  # Disable the remove button



def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    admin_interface.show_admin_frame(root=parent_frame)

