import customtkinter as ctk

from src import regular_user_interface

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

    # Placeholder data for the scoreboard
    scores = [
        {"team": "Team Alpha", "score": 85},
        {"team": "Team Beta", "score": 78},
        {"team": "Team Gamma", "score": 90},
        {"team": "Team Delta", "score": 70},
        {"team": "Team Epsilon", "score": 65}
    ]

    # Sort scores in descending order
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    # Populate the table with data
    for rank, data in enumerate(scores, start=1):
        rank_label = ctk.CTkLabel(table_frame, text=str(rank), font=("Arial", 12), width=20, anchor="w")
        rank_label.grid(row=rank, column=0, padx=5, pady=5)

        team_label = ctk.CTkLabel(table_frame, text=data["team"], font=("Arial", 12), width=20, anchor="w")
        team_label.grid(row=rank, column=1, padx=5, pady=5)

        score_label = ctk.CTkLabel(table_frame, text=str(data["score"]), font=("Arial", 12), width=20, anchor="w")
        score_label.grid(row=rank, column=2, padx=5, pady=5)

    # Add a refresh button
    refresh_button = ctk.CTkButton(scoreboard_frame, text="Refresh Scores", command=lambda: refresh_scoreboard(table_frame, scores))
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

