import customtkinter as ctk
import admin_interface
import pandas as pd
import os

def create_root_remove_game_frame(frame, parent_frame):
    global combobox, remove_btn, remove_game_entry_lbl

    for widget in frame.winfo_children():
        widget.destroy()

    remove_main_frame = ctk.CTkFrame(frame, corner_radius=10)
    remove_main_frame.configure(fg_color="#202020")
    remove_main_frame.pack(pady=0, padx=0, fill="both", expand=True)

    header_frame = ctk.CTkFrame(remove_main_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    label = ctk.CTkLabel(header_frame, text="Remove Game", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")

    back_button = ctk.CTkButton(header_frame, text="Back",
                                command=lambda: go_back_callback(remove_main_frame, parent_frame))
    back_button.pack(side="right", padx=10)

    main_frame = ctk.CTkFrame(remove_main_frame, corner_radius=10, fg_color="#212121")
    main_frame.pack(pady=(100, 40), padx=40, fill="none", side="top")

    game_names = load_game_names()

    if game_names:
        combobox_values = game_names
        remove_btn_state = "normal"
    else:
        combobox_values = ["No games exist"]
        remove_btn_state = "disabled"

    combobox_var = ctk.StringVar(value=combobox_values[0])
    combobox = ctk.CTkComboBox(
        main_frame,
        values=combobox_values,
        variable=combobox_var,
        width=350,
        height=50,
        font=("Arial", 20)
    )
    combobox.pack(side="top", padx=20, pady=20)

    remove_game_entry_lbl = ctk.CTkLabel(remove_main_frame, text="", font=("Arial", 14), height=0)
    remove_game_entry_lbl.configure(text_color="green")
    remove_game_entry_lbl.pack(side="top")

    # Remove Game Button
    remove_btn = ctk.CTkButton(
        main_frame,
        width=350,
        height=50,
        text="Remove Game",
        font=("Arial", 16),
        state=remove_btn_state,
        command=lambda: remove_game(combobox_var.get())
    )
    remove_btn.pack(side="top", padx=20, pady=20)


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


def remove_game(game_name):
    file_path = "src/games.csv"
    if not os.path.isfile(file_path):
        print("No games file found.")
        return

    try:
        df = pd.read_csv(file_path)
        if "Game Name" not in df.columns:
            print("Invalid file format.")
            return

        if game_name not in df["Game Name"].values:
            print(f"Game '{game_name}' does not exist.")
            return

        df = df[df["Game Name"] != game_name]

        df.to_csv(file_path, index=False)
        print(f"Game '{game_name}' removed successfully!")
        remove_game_entry_lbl.configure(text=f"Game '{game_name}' removed successfully!", text_color="green")

        refresh_combobox()

    except Exception as e:
        print(f"Error removing game: {e}")


def refresh_combobox():
    game_names = load_game_names()

    if game_names:
        combobox.configure(values=game_names)
        combobox.set(game_names[0])  # Set the first value as selected
        remove_btn.configure(state="normal")  # Enable the remove button
    else:
        combobox.configure(values=["No games exist"])
        combobox.set("No games exist")
        remove_btn.configure(state="disabled")  # Disable the remove button



def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    admin_interface.show_admin_frame(root=parent_frame)

