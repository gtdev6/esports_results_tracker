import customtkinter as ctk
import pandas as pd
from tkinter import simpledialog, messagebox
import main
import view_all_teams
import add_team
import remove_team
import view_all_games
import add_game
import remove_game
import record_match




def load_data(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame()

def save_data(filename, data):
    data.to_csv(filename, index=False)

def show_admin_frame(root):
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new frame
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Title
    title_label = ctk.CTkLabel(frame, text="Admin Dashboard", font=("Arial", 24))
    title_label.pack(pady=10)


    menu_root_frame = ctk.CTkFrame(frame, corner_radius=10)
    menu_root_frame.pack(pady=10, padx=10, fill="both", expand=True)

    menu_frame = ctk.CTkFrame(menu_root_frame, corner_radius=10)
    menu_frame.pack(pady=10, padx=10, fill="both", expand=True)

    menu_row_one_frame = ctk.CTkFrame(menu_frame, corner_radius=10)
    menu_row_one_frame.pack(fill="none", pady=(100, 10), padx=40, side="top")

    menu_row_two_frame = ctk.CTkFrame(menu_frame, corner_radius=10)
    menu_row_two_frame.pack(fill="none", pady=10, padx=40, side="top")

    menu_row_three_frame = ctk.CTkFrame(menu_frame, corner_radius=10)
    menu_row_three_frame.pack(fill="none", pady=10, padx=40, side="top")

    # # Buttons
    view_teams_button = ctk.CTkButton(
        menu_row_one_frame, text="View All Teams", font=("Arial", 16),
        width=150,
        height=60,
        command=lambda: view_all_teams.create_root_all_teams_frame(frame, root)
    )
    view_teams_button.pack(side="left", pady=20, padx=20)

    add_team_button = ctk.CTkButton(
        menu_row_one_frame, text="Add New Team", font=("Arial", 16),
        width=150,
        height=60,
        command=lambda: add_team.create_root_add_team_frame(frame, root)
    )
    add_team_button.pack(side="left" ,pady=20, padx=20)

    remove_team_button = ctk.CTkButton(
        menu_row_one_frame, text="Remove Team", font=("Arial", 16), 
        width=150,
        height=60,
        command=lambda: remove_team.create_root_remove_team_frame(frame, root)
    )
    remove_team_button.pack(side="left", pady=20, padx=20)



    view_games_button = ctk.CTkButton(
        menu_row_two_frame, text="View All Games", font=("Arial", 16),
        width=150,
        height=60, 
        command=lambda: view_all_games.create_root_all_games_frame(frame, root)
    )
    view_games_button.pack(side="left", pady=20, padx=20)

    add_game_button = ctk.CTkButton(
        menu_row_two_frame, text="Add New Game", font=("Arial", 16), 
        width=150,
        height=60,command=lambda: add_game.create_root_add_game_frame(frame, root)
    )
    add_game_button.pack(side="left", pady=20, padx=20)

    remove_game_button = ctk.CTkButton(
        menu_row_two_frame, text="Remove Game", font=("Arial", 16), 
        width=150,
        height=60,
        command=lambda: remove_game.create_root_remove_game_frame(frame, root)
    )
    remove_game_button.pack(side="left", pady=20, padx=20)



    record_match_button = ctk.CTkButton(
        menu_row_three_frame, text="Record Match", font=("Arial", 16), 
        width=150,
        height=60,
        # command=lambda: record_match(frame)
    )
    record_match_button.pack(side="left", pady=20, padx=20)
    

    back_button = ctk.CTkButton(
        menu_row_three_frame, text="Back to Main Menu", font=("Arial", 16), 
        width=150,
        height=60,
        command=lambda: go_back_to_main_menu(frame, root)
    )
    back_button.pack(side="left", pady=20, padx=20)




    def go_back_to_main_menu(current_frame, parent_frame):
        current_frame.destroy()

        for widget in parent_frame.winfo_children():
            widget.destroy()


        main.create_main_menu(root=parent_frame)

