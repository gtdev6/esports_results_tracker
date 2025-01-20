import customtkinter as ctk
import pandas as pd

from src import Recent_Matches
from src import Score_Board
from src import main
from src import specific_game_scoreboard



def load_data(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame()



def show_game_scores(frame, game):
    # Load match data
    matches = load_data("matches.csv")
    if matches.empty:
        label = ctk.CTkLabel(frame, text=f"No results for {game}.")
        label.pack(pady=10)
    else:
        game_matches = matches[matches["Game"] == game]
        if game_matches.empty:
            label = ctk.CTkLabel(frame, text=f"No results for {game}.")
            label.pack(pady=10)
        else:
            for index, match in game_matches.iterrows():
                game_label = ctk.CTkLabel(
                    frame,
                    text=f"{match['Team 1']} vs {match['Team 2']} - Winner: {match['Winner']}"
                )
                game_label.pack(pady=5)


def show_regular_user_frame(root):
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new frame
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=50, padx=50, fill="both", expand=True)


    header_frame = ctk.CTkFrame(frame, fg_color="#202020", corner_radius=10)
    header_frame.pack(fill="x", pady=40, padx=50)

    # Title
    title_label = ctk.CTkLabel(header_frame, text="Regular User Mode", font=("Arial", 24))
    title_label.pack(pady=20)

    title_label.place(relx=0.5, rely=0.5, anchor="center")

    back_button = ctk.CTkButton(header_frame, text="Back", command=lambda: go_back_to_main_menu(frame, root))
    back_button.pack(side="left", padx=10, pady=20)

    # Recent Matches
    recent_matches_button = ctk.CTkButton(
        frame,
        text="Recent Matches",
        font=("Arial", 16),
        command=lambda: Recent_Matches.show_recent_matches(frame, root)
    )
    recent_matches_button.pack(pady=10)

    # Scoreboard
    scoreboard_button = ctk.CTkButton(
        frame,
        text="Scoreboard",
        font=("Arial", 16),
        command=lambda: Score_Board.create_score_root_frame(frame, root)
    )
    scoreboard_button.pack(pady=10)

    # Specific Game Scores
    game_scores_button = ctk.CTkButton(
        frame,
        text="Specific Game Scores",
        font=("Arial", 16),
        command=lambda: specific_game_scoreboard.create_specific_score_root_frame(frame, root)  # Replace with selected game
    )
    game_scores_button.pack(pady=10)


def go_back_to_main_menu(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    main.create_main_menu(root=parent_frame)


