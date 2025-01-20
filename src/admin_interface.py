import customtkinter as ctk
import pandas as pd
from tkinter import simpledialog, messagebox

def load_data(filename):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame()

def save_data(filename, data):
    data.to_csv(filename, index=False)

def view_all_teams(frame):
    teams = load_data("teams.csv")
    if teams.empty:
        label = ctk.CTkLabel(frame, text="No teams registered.")
        label.pack(pady=5)
    else:
        for index, team in teams.iterrows():
            team_label = ctk.CTkLabel(frame, text=f"{team['Team']} - {team['Score']} Points")
            team_label.pack(pady=5)

def add_new_team(frame):
    teams = load_data("teams.csv")
    new_team = simpledialog.askstring("Add Team", "Enter the name of the new team:")
    if new_team:
        if teams.empty:
            teams = pd.DataFrame(columns=["Team", "Score"])
        if new_team not in teams['Team'].values:
            teams = teams.append({"Team": new_team, "Score": 0}, ignore_index=True)
            save_data("teams.csv", teams)
            messagebox.showinfo("Success", f"Team '{new_team}' added.")
        else:
            messagebox.showerror("Error", f"Team '{new_team}' already exists.")

def remove_team(frame):
    teams = load_data("teams.csv")
    team_to_remove = simpledialog.askstring("Remove Team", "Enter the name of the team to remove:")
    if team_to_remove:
        if team_to_remove in teams['Team'].values:
            teams = teams[teams['Team'] != team_to_remove]
            save_data("teams.csv", teams)
            messagebox.showinfo("Success", f"Team '{team_to_remove}' removed.")
        else:
            messagebox.showerror("Error", f"Team '{team_to_remove}' does not exist.")

def view_all_games(frame):
    games = load_data("games.csv")
    if games.empty:
        label = ctk.CTkLabel(frame, text="No games registered.")
        label.pack(pady=5)
    else:
        for index, game in games.iterrows():
            game_label = ctk.CTkLabel(frame, text=f"{game['Game']}")
            game_label.pack(pady=5)

def add_new_game(frame):
    games = load_data("games.csv")
    new_game = simpledialog.askstring("Add Game", "Enter the name of the new game:")
    if new_game:
        if games.empty:
            games = pd.DataFrame(columns=["Game"])
        if new_game not in games['Game'].values:
            games = games.append({"Game": new_game}, ignore_index=True)
            save_data("games.csv", games)
            messagebox.showinfo("Success", f"Game '{new_game}' added.")
        else:
            messagebox.showerror("Error", f"Game '{new_game}' already exists.")

def remove_game(frame):
    games = load_data("games.csv")
    game_to_remove = simpledialog.askstring("Remove Game", "Enter the name of the game to remove:")
    if game_to_remove:
        if game_to_remove in games['Game'].values:
            games = games[games['Game'] != game_to_remove]
            save_data("games.csv", games)
            messagebox.showinfo("Success", f"Game '{game_to_remove}' removed.")
        else:
            messagebox.showerror("Error", f"Game '{game_to_remove}' does not exist.")

def record_match(frame):
    matches = load_data("matches.csv")
    teams = load_data("teams.csv")
    games = load_data("games.csv")

    if teams.empty or games.empty:
        messagebox.showerror("Error", "Teams or Games are not registered yet.")
        return

    date = simpledialog.askstring("Match Date", "Enter match date (DD-MM-YYYY):")
    team_1 = simpledialog.askstring("Team 1", "Enter the first team:")
    team_2 = simpledialog.askstring("Team 2", "Enter the second team:")
    game = simpledialog.askstring("Game", "Enter the game title:")

    if team_1 in teams['Team'].values and team_2 in teams['Team'].values and game in games['Game'].values:
        winner = simpledialog.askstring("Winner", "Enter the winning team:")
        if winner in [team_1, team_2]:
            if matches.empty:
                matches = pd.DataFrame(columns=["Date", "Team 1", "Team 2", "Game", "Winner"])
            matches = matches.append({
                "Date": date,
                "Team 1": team_1,
                "Team 2": team_2,
                "Game": game,
                "Winner": winner
            }, ignore_index=True)

            teams.loc[teams['Team'] == winner, 'Score'] += 1
            save_data("matches.csv", matches)
            save_data("teams.csv", teams)

            messagebox.showinfo("Success", "Match recorded successfully.")
        else:
            messagebox.showerror("Error", "Winner must be one of the competing teams.")
    else:
        messagebox.showerror("Error", "Invalid team or game selection.")

def show_admin_frame(root):
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new frame
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=50, padx=50, fill="both", expand=True)

    # Title
    title_label = ctk.CTkLabel(frame, text="Admin Dashboard", font=("Arial", 24))
    title_label.pack(pady=20)

    # Buttons
    view_teams_button = ctk.CTkButton(
        frame, text="View All Teams", font=("Arial", 16), command=lambda: view_all_teams(frame)
    )
    view_teams_button.pack(pady=10)

    add_team_button = ctk.CTkButton(
        frame, text="Add New Team", font=("Arial", 16), command=lambda: add_new_team(frame)
    )
    add_team_button.pack(pady=10)

    remove_team_button = ctk.CTkButton(
        frame, text="Remove Team", font=("Arial", 16), command=lambda: remove_team(frame)
    )
    remove_team_button.pack(pady=10)

    view_games_button = ctk.CTkButton(
        frame, text="View All Games", font=("Arial", 16), command=lambda: view_all_games(frame)
    )
    view_games_button.pack(pady=10)

    add_game_button = ctk.CTkButton(
        frame, text="Add New Game", font=("Arial", 16), command=lambda: add_new_game(frame)
    )
    add_game_button.pack(pady=10)

    remove_game_button = ctk.CTkButton(
        frame, text="Remove Game", font=("Arial", 16), command=lambda: remove_game(frame)
    )
    remove_game_button.pack(pady=10)

    record_match_button = ctk.CTkButton(
        frame, text="Record Match", font=("Arial", 16), command=lambda: record_match(frame)
    )
    record_match_button.pack(pady=10)

    back_button = ctk.CTkButton(
        frame, text="Back to Main Menu", font=("Arial", 16), command=lambda: root.destroy()
    )
    back_button.pack(pady=10)
