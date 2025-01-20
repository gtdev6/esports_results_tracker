import customtkinter as ctk
import pandas as pd
import os
from src import regular_user_interface


def ensure_matches_file():
    # Define the path to the matches.csv file
    file_path = "matches.csv"

    # Check if the file exists
    if not os.path.exists(file_path):
        # Create a new DataFrame with the required columns
        columns = ["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"]
        df = pd.DataFrame(columns=columns)

        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=False)
        print(f"Created {file_path} with columns {columns}")


def load_recent_matches():
    try:
        ensure_matches_file()  # Ensure the file exists

        # Load matches from CSV
        matches = pd.read_csv("matches.csv")

        # Ensure the "Date" column is datetime
        matches["Date"] = pd.to_datetime(matches["Date"], errors='coerce')

        # Sort matches by date in descending order
        recent_matches = matches.sort_values(by="Date", ascending=False).head(5)  # Get the 5 most recent matches

        return recent_matches
    except Exception as e:
        print(f"Error loading matches: {e}")
        return pd.DataFrame(columns=["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"])


def show_recent_matches(frame, parent_frame):

    # Hide the parent frame
    for widget in frame.winfo_children():
        widget.destroy()


    # Create a new frame
    recent_matches_frame = ctk.CTkFrame(frame, corner_radius=10)
    recent_matches_frame.configure(fg_color="#202020")
    recent_matches_frame.pack(pady=0, padx=0, fill="both", expand=True)

    # Create a frame for the label and back button
    header_frame = ctk.CTkFrame(recent_matches_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    # Add a label in the header frame
    label = ctk.CTkLabel(header_frame, text="Recent Matches", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")

    # Create a back button in the header frame
    back_button = ctk.CTkButton(header_frame, text="Back", command=lambda: go_back_callback(recent_matches_frame, parent_frame))
    back_button.pack(side="right", padx=10)


    # Create a frame to hold the table
    table_frame = ctk.CTkFrame(recent_matches_frame)
    table_frame.pack(pady=10, padx=20, fill="x")

    # Create the table header
    headers = ["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), width=20, anchor="w")
        header_label.grid(row=0, column=col, padx=5, pady=5)

    # Load data from CSV
    recent_matches = load_recent_matches()

    # Function to refresh table
    def refresh_table():
        # Clear existing data rows except for the headers
        for widget in table_frame.winfo_children()[len(headers):]:
            widget.destroy()

        # Add refreshed data from recent_matches
        for row_idx, match in recent_matches.iterrows():
            for col_idx, value in enumerate(match):
                # Ensure each cell is displayed properly
                data_label = ctk.CTkLabel(
                    table_frame, text=str(value), font=("Arial", 12), width=20, anchor="w"
                )
                data_label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

    # Refresh the table initially to show data
    refresh_table()

    # Add a refresh button
    refresh_button = ctk.CTkButton(recent_matches_frame, text="Refresh Data", command=refresh_table)
    refresh_button.pack(pady=20)



def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    regular_user_interface.show_regular_user_frame(root=parent_frame)


if __name__ == "__main__":
    # Create example data for testing
    example_data = [
        {"Match ID": "001", "Team A": "Team Alpha", "Team B": "Team Beta", "Game": "Fortnite", "Winning Team": "Team Alpha", "Date": "2025-01-19"},
        {"Match ID": "002", "Team A": "Team Gamma", "Team B": "Team Delta", "Game": "Valorant", "Winning Team": "Team Delta", "Date": "2025-01-18"},
        {"Match ID": "003", "Team A": "Team Epsilon", "Team B": "Team Zeta", "Game": "CS:GO", "Winning Team": "Team Zeta", "Date": "2025-01-17"},
        {"Match ID": "004", "Team A": "Team Omega", "Team B": "Team Sigma", "Game": "Apex Legends", "Winning Team": "Team Omega", "Date": "2025-01-16"},
        {"Match ID": "005", "Team A": "Team Theta", "Team B": "Team Lambda", "Game": "PUBG", "Winning Team": "Team Lambda", "Date": "2025-01-15"},
    ]

    df = pd.DataFrame(example_data)
    df.to_csv("matches.csv", index=False)
