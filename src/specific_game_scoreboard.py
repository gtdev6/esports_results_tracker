import customtkinter as ctk
import regular_user_interface
import pandas as pd
import os


def ensure_matches_file():
    # Define the path to the matches.csv file
    file_path = "matches.csv"

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create a new DataFrame with the required columns
        columns = ["Match ID", "Team A", "Team B", "Game", "Winning Team", "Score", "Date"]
        df = pd.DataFrame(columns=columns)
        
        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        print(f"Created {file_path} with columns {columns}")


def load_game_scores(game_name):
    try:
        ensure_matches_file()  # Ensure the matches file exists

        # Load matches from CSV
        matches = pd.read_csv("matches.csv")

        # Filter matches for the specific game
        game_matches = matches[matches["Game"].str.lower() == game_name.lower()]

        print(game_matches)

        # Group by Winning Team and sum their scores
        team_scores = (
            game_matches.groupby("Winning Team")["Score"]
            .sum()
            .reset_index()
            .rename(columns={"Winning Team": "Team Name"})
            .sort_values(by="Score", ascending=False)
            .reset_index(drop=True)
        )

        return team_scores
    except Exception as e:
        print(f"Error loading game scores: {e}")
        return pd.DataFrame(columns=["Team Name", "Score"])



def create_specific_score_root_frame(frame, parent_frame):
    # Hide the parent frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Create a new frame
    score_board_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    score_board_main_frame.configure(fg_color="#202020")
    score_board_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    # Create a frame for the label and back button
    header_frame = ctk.CTkFrame(score_board_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    # Add a label in the header frame
    label = ctk.CTkLabel(header_frame, text="Recent Matches", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")

    # Create a back button in the header frame
    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(score_board_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)

    create_game_specific_table(score_board_main_frame, "Fortnite")



def create_game_specific_table(frame, game_name):
    # Create a new frame for the game-specific scores
    game_frame = ctk.CTkFrame(frame, corner_radius=10)
    game_frame.configure(fg_color="#202020")
    game_frame.pack(pady=0, padx=0, fill="x", side="top")

    # Add a label for the game
    label = ctk.CTkLabel(game_frame, text=f"{game_name} Scores", font=("Arial", 20))
    label.pack(pady=20)

    # Create a scrollable frame for the table
    scrollable_frame = ctk.CTkScrollableFrame(game_frame, width=600, height=300)
    scrollable_frame.pack(pady=10, padx=20, fill="x")

   # Create the table header
    headers = ["Rank", "Team Name", "Score"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(scrollable_frame, text=header, font=("Arial", 14, "bold"), width=20, anchor="w")
        header_label.grid(row=0, column=col, padx=5, pady=5)

    # Load scores for the specific game


    # Function to refresh the table
    def refresh_game_table():
        scores = load_game_scores(game_name)
        # Clear the existing rows except for the header
        for widget in scrollable_frame.winfo_children()[len(headers):]:
            widget.destroy()

        # Populate the table with refreshed data
        for rank, row in enumerate(scores.itertuples(index=False), start=1):
            rank_label = ctk.CTkLabel(scrollable_frame, text=str(rank), font=("Arial", 12), width=20, anchor="w")
            rank_label.grid(row=rank, column=0, padx=5, pady=5)

            team_label = ctk.CTkLabel(scrollable_frame, text=row[0], font=("Arial", 12), width=20, anchor="w")
            team_label.grid(row=rank, column=1, padx=5, pady=5)

            score_label = ctk.CTkLabel(scrollable_frame, text=str(row[1]), font=("Arial", 12), width=20, anchor="w")
            score_label.grid(row=rank, column=2, padx=5, pady=5)

    # Refresh the table initially to show data
    refresh_game_table()
    # Add a refresh button
    refresh_button = ctk.CTkButton(game_frame, text="Refresh Scores", command=lambda: refresh_game_table)
    refresh_button.pack(pady=20)




def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()

    regular_user_interface.show_regular_user_frame(root=parent_frame)
