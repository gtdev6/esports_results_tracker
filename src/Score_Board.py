import customtkinter as ctk
import regular_user_interface
import pandas as pd
import os

def ensure_teams_file():
    # Define the path to the teams.csv file
    file_path = "teams.csv"

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create a new DataFrame with the required columns
        columns = ["Team Name", "Score"]
        df = pd.DataFrame(columns=columns)
        
        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        print(f"Created {file_path} with columns {columns}")

def load_team_scores():
    try:
        ensure_teams_file()  # Ensure the teams file exists

        # Load team scores from CSV
        teams = pd.read_csv("teams.csv")

        # Ensure "Score" is numeric
        teams["Score"] = pd.to_numeric(teams["Score"], errors="coerce").fillna(0)

        # Sort teams by score in descending order
        sorted_teams = teams.sort_values(by="Score", ascending=False).reset_index(drop=True)
        
        return sorted_teams
    except Exception as e:
        print(f"Error loading team scores: {e}")
        return pd.DataFrame(columns=["Team Name", "Score"])


def create_score_root_frame(frame, parent_frame):
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

    create_scoreboard(score_board_main_frame)


def create_scoreboard(frame):
    # Create a new frame for the scoreboard
    scoreboard_frame = ctk.CTkFrame(frame, corner_radius=10)
    scoreboard_frame.configure(fg_color="#202020")
    scoreboard_frame.pack(pady=0, padx=0, fill="x", side="top")

    # Create a scrollable frame for the table
    table_frame = ctk.CTkScrollableFrame(scoreboard_frame, width=600, height=300)
    table_frame.pack(pady=10, padx=20, fill="x")

    # Create a frame for the table
    # table_frame = ctk.CTkFrame(scrollable_frame)
    # table_frame.pack(pady=10, padx=20, fill="x")

# Create the table header
    headers = ["Rank", "Team Name", "Score"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), width=20, anchor="w")
        header_label.grid(row=0, column=col, padx=5, pady=5)

    # Function to refresh table
    def refresh_scoreboard():
    # Load team scores from CSV
        team_scores = load_team_scores()

        # Clear existing data rows except for the headers
        for widget in table_frame.winfo_children()[len(headers):]:
            widget.destroy()

        # Add refreshed data from team_scores
        for rank, row in enumerate(team_scores.itertuples(index=False), start=1):
            rank_label = ctk.CTkLabel(table_frame, text=str(rank), font=("Arial", 12), width=20, anchor="w")
            rank_label.grid(row=rank, column=0, padx=5, pady=5)

            team_label = ctk.CTkLabel(table_frame, text=row[0], font=("Arial", 12), width=20, anchor="w")
            team_label.grid(row=rank, column=1, padx=5, pady=5)

            score_label = ctk.CTkLabel(table_frame, text=str(row[1]), font=("Arial", 12), width=20, anchor="w")
            score_label.grid(row=rank, column=2, padx=5, pady=5)

    # Refresh the table initially to show data
    refresh_scoreboard()

    # Add a refresh button
    refresh_button = ctk.CTkButton(scoreboard_frame, text="Refresh Scores", command=lambda: refresh_scoreboard)
    refresh_button.pack(pady=20)


def refresh_scoreboard(table_frame, scores):
    # Clear the existing rows except for the header
    for widget in table_frame.winfo_children()[3:]:
        widget.destroy()

    # Repopulate the table with updated scores
    for rank, data in enumerate(scores, start=1):
        rank_label = ctk.CTkLabel(table_frame, text=str(rank), font=("Arial", 12), width=20, anchor="w")
        rank_label.grid(row=rank, column=0, padx=5, pady=5)

        team_label = ctk.CTkLabel(table_frame, text=data["team"], font=("Arial", 12), width=20, anchor="w")
        team_label.grid(row=rank, column=1, padx=5, pady=5)

        score_label = ctk.CTkLabel(table_frame, text=str(data["score"]), font=("Arial", 12), width=20, anchor="w")
        score_label.grid(row=rank, column=2, padx=5, pady=5)


def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    regular_user_interface.show_regular_user_frame(root=parent_frame)



if __name__ == "__main__":
    # Create example team data for testing
    example_teams = [
        {"Team Name": "Team Alpha", "Score": 85},
        {"Team Name": "Team Beta", "Score": 78},
        {"Team Name": "Team Gamma", "Score": 90},
        {"Team Name": "Team Delta", "Score": 70},
        {"Team Name": "Team Epsilon", "Score": 65},
    ]

    df = pd.DataFrame(example_teams)
    df.to_csv("teams.csv", index=False)