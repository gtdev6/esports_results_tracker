import customtkinter as ctk
import regular_user_interface
import pandas as pd
import os


def ensure_matches_file():
    file_path = "src/matches.csv"

    if not os.path.exists(file_path):
        columns = ["Match ID", "Team A", "Team B", "Game", "Winning Team", "Score", "Date"]
        df = pd.DataFrame(columns=columns)

        df.to_csv(file_path, index=False)
        print(f"Created {file_path} with columns {columns}")



def load_game_names():
    file_path = "src/games.csv"
    if not os.path.isfile(file_path):
        return []

    try:
        df = pd.read_csv(file_path)
        if "Game Name" in df.columns:
            return df["Game Name"].tolist()
        else:
            return []
    except Exception as e:
        print(f"Error loading games.csv: {e}")
        return []


def create_specific_score_root_frame(frame, parent_frame):
    for widget in frame.winfo_children():
        widget.destroy()

    score_board_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    score_board_main_frame.configure(fg_color="#202020")
    score_board_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    header_frame = ctk.CTkFrame(score_board_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    label = ctk.CTkLabel(header_frame, text="Specific Game Scoreboards", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")

    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(score_board_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)

    game_names = load_game_names()

    if game_names:
        combobox_values = game_names
    else:
        combobox_values = ["No games exist"]

    combobox_var = ctk.StringVar(value=combobox_values[0])
    combobox = ctk.CTkComboBox(
        score_board_main_frame,
        values=combobox_values,
        variable=combobox_var,
        width=350,
        height=50,
        font=("Arial", 20),
        command=lambda choice: create_game_specific_table(score_board_main_frame, choice)
    )
    combobox.pack(side="top", padx=20, pady=20)

    create_game_specific_table(score_board_main_frame, combobox_var.get())



def create_game_specific_table(frame, game_name):
    # Remove any previous game frames
    for widget in frame.winfo_children():
        if isinstance(widget, ctk.CTkFrame) and widget not in frame.winfo_children()[:2]:
            widget.destroy()

    game_frame = ctk.CTkFrame(frame, corner_radius=10)
    game_frame.configure(fg_color="#202020")
    game_frame.pack(pady=0, padx=0, fill="x", side="top")

    scrollable_frame = ctk.CTkScrollableFrame(game_frame, width=600, height=300)
    scrollable_frame.pack(pady=10, padx=20, fill="x")

    headers = ["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(scrollable_frame, text=header, font=("Arial", 14, "bold"), width=200, anchor="w")
        header_label.grid(row=0, column=col, padx=5, pady=5)

    def refresh_game_table():
        # Load match data for the selected game
        matches = load_game_matches(game_name)

        # Clear previous data rows
        for widget in scrollable_frame.winfo_children()[len(headers):]:
            widget.destroy()

        # Populate the table with match data
        for row_index, row in matches.iterrows():
            for col_index, value in enumerate(row):
                cell_label = ctk.CTkLabel(scrollable_frame, text=str(value), font=("Arial", 12), width=200, anchor="w")
                cell_label.grid(row=row_index + 1, column=col_index, padx=5, pady=5)

    refresh_game_table()

    refresh_button = ctk.CTkButton(
        game_frame,
        text="Refresh Matches",
        command=refresh_game_table
    )
    refresh_button.pack(pady=20)


def load_game_matches(game_name):
    file_path = "src/matches.csv"
    ensure_matches_file()

    try:
        matches = pd.read_csv(file_path)
        filtered_matches = matches[matches["Game"].str.lower() == game_name.lower()]
        return filtered_matches.sort_values(by="Date", ascending=False).reset_index(drop=True)
    except Exception as e:
        print(f"Error loading matches for game '{game_name}': {e}")
        return pd.DataFrame(columns=["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"])




def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()

    regular_user_interface.show_regular_user_frame(root=parent_frame)
