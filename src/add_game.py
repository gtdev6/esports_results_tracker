import customtkinter as ctk
import admin_interface
import pandas as pd
import os

def create_root_add_game_frame(frame, parent_frame):
    global game_entry_lbl
    for widget in frame.winfo_children():
        widget.destroy()

    add_game_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    add_game_main_frame.configure(fg_color="#202020")
    add_game_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    header_frame = ctk.CTkFrame(add_game_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    label = ctk.CTkLabel(header_frame, text="Add Game", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")

    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(add_game_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)

    game_entry = ctk.CTkEntry(
        add_game_main_frame, placeholder_text="Enter Game Name", width=350, height=50, font=("Arial", 20)
    )
    game_entry.pack(pady=20)

    game_entry_lbl = ctk.CTkLabel(add_game_main_frame, text="", font=("Arial", 14), height=0)
    game_entry_lbl.configure(text_color="red")
    game_entry_lbl.pack(side="top")

    save_button = ctk.CTkButton(
        add_game_main_frame,
        text="Save Game",
        width=350,
        height=50,
        font=("Arial", 16),
        command=lambda: save_game(game_entry)
    )
    save_button.pack(pady=20)



def create_games_file():
    file_path = "src/games.csv"
    if not os.path.isfile(file_path):
        try:
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                file.write("Game Name\n")
            print("games.csv file created successfully.")
        except Exception as e:
            print(f"Error creating games.csv: {e}")

def save_game(entry):
    game_name = entry.get().strip()

    if not game_name:
        game_entry_lbl.configure(text="Game name cannot be empty.", text_color="red")
        return
    else:
        game_entry_lbl.configure(text="")

    create_games_file()

    file_path = "src/games.csv"

    try:
        df = pd.read_csv(file_path)
        if "Game Name" in df.columns and game_name in df["Game Name"].values:
            game_entry_lbl.configure(text=f"Game '{game_name}' already exists.", text_color="red")
            return
    except Exception as e:
        print(f"Error reading games.csv: {e}")
        return

    try:
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            file.write(f"{game_name}\n")
        print(f"Game '{game_name}' saved successfully!")
        game_entry_lbl.configure(text="Game saved successfully!", text_color="green")
        entry.delete(0, "end")
    except Exception as e:
        print(f"Error saving game: {e}")



def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    admin_interface.show_admin_frame(root=parent_frame)

