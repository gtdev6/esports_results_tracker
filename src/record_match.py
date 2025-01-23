import customtkinter as ctk
import pandas as pd
import os
import admin_interface
from datetime import datetime


def create_root_record_match_frame(frame, parent_frame):
    global record_output_lbl

    for widget in frame.winfo_children():
        widget.destroy()

    # Create a new frame
    record_match_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    record_match_main_frame.configure(fg_color="#202020")
    record_match_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    header_frame = ctk.CTkFrame(record_match_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    label = ctk.CTkLabel(header_frame, text="Record Match", font=("Arial", 20))
    label.pack(side="left", padx=10)
    label.place(relx=0.5, rely=0.5, anchor="center")

    back_button = ctk.CTkButton(
        header_frame,
        text="Back",
        command=lambda: go_back_callback(record_match_main_frame, parent_frame)
    )
    back_button.pack(side="right", padx=10)

    # Date Entry
    date_frame = ctk.CTkFrame(record_match_main_frame, fg_color="#202020")
    date_frame.pack(fill="none", pady=10, padx=10, side="top")

    date_label = ctk.CTkLabel(date_frame, text="Match Date",
                              width=150,
                              height=50,
                              font=("Arial", 20))
    date_label.pack(side="left", padx=10)

    date_entry = ctk.CTkEntry(
        date_frame,
        placeholder_text="Enter Date (DD-MM-YYYY)",
        width=350,
        height=50,
        font=("Arial", 20)
    )
    date_entry.pack(pady=10, padx=10)

    # Team A Selection
    team_one_frame = ctk.CTkFrame(record_match_main_frame, fg_color="#202020")
    team_one_frame.pack(fill="none", pady=10, padx=10, side="top")

    team_one_label = ctk.CTkLabel(team_one_frame, text="Team A",
                                  width=150,
                                  height=50,
                                  font=("Arial", 20))
    team_one_label.pack(side="left", padx=10)

    team_names = load_team_names()
    team_combobox_values = team_names if team_names else ["No teams exist"]
    team_one_var = ctk.StringVar(value=team_combobox_values[0])
    team_one_combobox = ctk.CTkComboBox(
        team_one_frame,
        values=team_combobox_values,
        variable=team_one_var,
        width=350,
        height=50,
        font=("Arial", 20),
    )
    team_one_combobox.pack(side="top", padx=10, pady=10)

    # Game Selection
    games_frame = ctk.CTkFrame(record_match_main_frame, fg_color="#202020")
    games_frame.pack(fill="none", pady=10, padx=10, side="top")

    games_label = ctk.CTkLabel(games_frame, text="Select Game",
                               width=150,
                               height=50,
                               font=("Arial", 20))
    games_label.pack(side="left", padx=10)

    game_names = load_game_names()
    game_combobox_values = game_names if game_names else ["No games exist"]
    game_var = ctk.StringVar(value=game_combobox_values[0])
    games_combobox = ctk.CTkComboBox(
        games_frame,
        values=game_combobox_values,
        variable=game_var,
        width=350,
        height=50,
        font=("Arial", 20),
    )
    games_combobox.pack(side="top", padx=10, pady=10)

    # Team B Selection
    team_two_frame = ctk.CTkFrame(record_match_main_frame, fg_color="#202020")
    team_two_frame.pack(fill="none", pady=10, padx=10, side="top")

    team_two_label = ctk.CTkLabel(team_two_frame, text="Team B",
                                  width=150,
                                  height=50,
                                  font=("Arial", 20))
    team_two_label.pack(side="left", padx=10)

    team_two_var = ctk.StringVar(value=team_combobox_values[0])
    team_two_combobox = ctk.CTkComboBox(
        team_two_frame,
        values=team_combobox_values,
        variable=team_two_var,
        width=350,
        height=50,
        font=("Arial", 20),
    )
    team_two_combobox.pack(side="top", padx=10, pady=10)


    winning_team_frame = ctk.CTkFrame(record_match_main_frame, fg_color="#202020")
    winning_team_frame.pack(fill="none", pady=10, padx=10, side="top")

    winning_team_label = ctk.CTkLabel(winning_team_frame, text="Winning Team",
                                  width=150,
                                  height=50,
                                  font=("Arial", 20))
    winning_team_label.pack(side="left", padx=10)

    winning_team_var = ctk.StringVar(value=team_combobox_values[0])
    winning_team_combobox = ctk.CTkComboBox(
        winning_team_frame,
        values=team_combobox_values,
        variable=winning_team_var,
        width=350,
        height=50,
        font=("Arial", 20),
    )
    winning_team_combobox.pack(side="top", padx=10, pady=10)

    record_output_lbl = ctk.CTkLabel(record_match_main_frame, text="", font=("Arial", 14), height=0)
    record_output_lbl.configure(text_color="red")
    record_output_lbl.pack(side="top")

    save_button = ctk.CTkButton(
        record_match_main_frame,
        text="Save Match Record",
        width=350,
        height=50,
        font=("Arial", 16),
        command=lambda: save_record_match(
            date_entry.get(),
            team_one_var.get(),
            team_two_var.get(),
            game_var.get(),
            winning_team_var.get()
        ),
    )
    save_button.pack(pady=20)


def load_team_names():
    file_path = "src/teams.csv"
    if not os.path.isfile(file_path):
        return []
    try:
        df = pd.read_csv(file_path)
        if "Team Name" in df.columns:
            return df["Team Name"].tolist()
    except Exception as e:
        print(f"Error loading teams.csv: {e}")
    return []


def load_game_names():
    file_path = "src/games.csv"
    if not os.path.isfile(file_path):
        return []
    try:
        df = pd.read_csv(file_path)
        if "Game Name" in df.columns:
            return df["Game Name"].tolist()
    except Exception as e:
        print(f"Error loading games.csv: {e}")
    return []


def update_team_score(winning_team):
    file_path = "src/teams.csv"
    if not os.path.isfile(file_path):
        print("teams.csv file does not exist.")
        return

    try:
        df = pd.read_csv(file_path)

        if "Team Name" not in df.columns or "Score" not in df.columns:
            print("teams.csv is missing required columns.")
            return

        if winning_team not in df["Team Name"].values:
            print(f"Winning team '{winning_team}' not found in teams.csv.")
            return

        df.loc[df["Team Name"] == winning_team, "Score"] += 1

        df.to_csv(file_path, index=False)
        print(f"1 point awarded to '{winning_team}'. Updated scores saved.")
    except Exception as e:
        print(f"Error updating team score: {e}")


# def save_record_match(date, team_a, team_b, game, winning_team):

#     try:
#         datetime.strptime(date, "%d-%m-%Y")
#     except ValueError:
#         print("Invalid date format. Use DD-MM-YYYY.")
#         record_output_lbl.configure(text="Invalid date format. Use DD-MM-YYYY.", text_color="red")

#         return


#     if team_a == "No teams exist" or team_b == "No teams exist" or game == "No games exist":
#         print("Invalid input: Please ensure teams and game exist.")
#         record_output_lbl.configure(text="Invalid input: Please ensure teams and game exist.", text_color="red")
#         return

#     if team_a == team_b:
#         print("Team A and Team B cannot be the same.")
#         record_output_lbl.configure(text="Team A and Team B cannot be the same.", text_color="red")
#         return

#     if winning_team not in [team_a, team_b]:
#         print("Winning team must be either Team A or Team B.")
#         record_output_lbl.configure(text="Winning team must be either Team A or Team B.", text_color="red")
#         return

#     file_path = "src/matches.csv"
#     if not os.path.isfile(file_path):
#         with open(file_path, mode="w", newline="", encoding="utf-8") as file:
#             file.write("Match ID,Team A,Team B,Game,Winning Team,Date\n")


#     try:
#         if os.path.isfile(file_path):
#             df = pd.read_csv(file_path)
#         else:
#             df = pd.DataFrame(columns=["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"])

#         match_id = len(df) + 1

#         new_row = pd.DataFrame([{
#             "Match ID": match_id,
#             "Team A": team_a,
#             "Team B": team_b,
#             "Game": game,
#             "Winning Team": winning_team,
#             "Date": date,
#         }])

#         updated_df = pd.concat([df, new_row], ignore_index=True)

#         updated_df.to_csv(file_path, index=False)
#         print(f"Match record saved successfully: {new_row.to_dict(orient='records')[0]}")
#         record_output_lbl.configure(text="Match record saved successfully.", text_color="green")
#         update_team_score(winning_team)

#     except Exception as e:
#         print(f"Error saving match record: {e}")

def save_record_match(date, team_a, team_b, game, winning_team):
    try:
        # Validate date format
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Use DD-MM-YYYY.")
        record_output_lbl.configure(text="Invalid date format. Use DD-MM-YYYY.", text_color="red")
        return

    # Validate inputs
    if team_a == "No teams exist" or team_b == "No teams exist" or game == "No games exist":
        print("Invalid input: Please ensure teams and game exist.")
        record_output_lbl.configure(text="Invalid input: Please ensure teams and game exist.", text_color="red")
        return

    if team_a == team_b:
        print("Team A and Team B cannot be the same.")
        record_output_lbl.configure(text="Team A and Team B cannot be the same.", text_color="red")
        return

    if winning_team not in [team_a, team_b]:
        print("Winning team must be either Team A or Team B.")
        record_output_lbl.configure(text="Winning team must be either Team A or Team B.", text_color="red")
        return

    # Ensure the matches file exists
    file_path = "src/matches.csv"
    if not os.path.isfile(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            file.write("Match ID,Team A,Team B,Game,Winning Team,Date\n")

    try:
        # Load existing data or create a new DataFrame
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
        else:
            df = pd.DataFrame(columns=["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"])

        # Generate Match ID and add a new row
        match_id = len(df) + 1
        new_row = {
            "Match ID": match_id,
            "Team A": team_a,
            "Team B": team_b,
            "Game": game,
            "Winning Team": winning_team,
            "Date": date,  # Date is already validated
        }

        # Append the new row and save back to CSV
        updated_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        updated_df.to_csv(file_path, index=False, encoding="utf-8")
        print(f"Match record saved successfully: {new_row}")
        record_output_lbl.configure(text="Match record saved successfully.", text_color="green")
        update_team_score(winning_team)
    except Exception as e:
        print(f"Error saving match record: {e}")




def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()
    for widget in parent_frame.winfo_children():
        widget.destroy()
    admin_interface.show_admin_frame(root=parent_frame)
