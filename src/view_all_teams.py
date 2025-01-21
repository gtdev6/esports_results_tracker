import customtkinter as ctk
import admin_interface
import pandas as pd
import os



def create_root_all_teams_frame(frame, parent_frame):
    for widget in frame.winfo_children():
        widget.destroy()

    view_all_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    view_all_main_frame.configure(fg_color="#202020")
    view_all_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    header_frame = ctk.CTkFrame(view_all_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    label = ctk.CTkLabel(header_frame, text="View All Teams", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")


    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(view_all_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)

    main_frame = ctk.CTkFrame(view_all_main_frame, corner_radius=10, fg_color="#212121")
    main_frame.pack(pady=(100, 40), padx=40, fill="none", side="top")

    scrollable_frame = ctk.CTkScrollableFrame(main_frame, width=500, height=300, corner_radius=10)
    scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

    refresh_button = ctk.CTkButton(
        main_frame, text="Refresh", font=("Arial", 16),
        command=lambda: load_table_data(scrollable_frame)
    )
    refresh_button.pack(pady=10)

    load_table_data(scrollable_frame)

def create_teams_file():
    file_path = "teams.csv"
    if not os.path.isfile(file_path):
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                file.write("Team Name,Score\n")
            print("teams.csv file created successfully.")
        except Exception as e:
            print(f"Error creating teams.csv: {e}")

def load_table_data(scrollable_frame):
    create_teams_file()

    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    file_path = "teams.csv"
    try:
        df = pd.read_csv(file_path)

        if df.empty or "Team Name" not in df.columns:
            no_data_label = ctk.CTkLabel(scrollable_frame, text="No teams found.", font=("Arial", 16))
            no_data_label.pack(pady=20)
            return

        header_label = ctk.CTkLabel(scrollable_frame, text="Team Name - Score", font=("Arial", 16, "bold"))
        header_label.pack(pady=10)

        for index, row in df.iterrows():
            team_label = ctk.CTkLabel(scrollable_frame, text=f"{row['Team Name']} - {row['Score']}", font=("Arial", 14))
            team_label.pack(pady=5)

    except Exception as e:
        error_label = ctk.CTkLabel(scrollable_frame, text=f"Error loading teams: {e}", font=("Arial", 14))
        error_label.pack(pady=20)


def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    admin_interface.show_admin_frame(root=parent_frame)



