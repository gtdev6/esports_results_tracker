import customtkinter as ctk
import pandas as pd
import os
import regular_user_interface


def ensure_matches_file():
    file_path = "src/matches.csv"

    if not os.path.exists(file_path):
        columns = ["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"]
        df = pd.DataFrame(columns=columns)

        df.to_csv(file_path, index=False)
        print(f"Created {file_path} with columns {columns}")


def load_recent_matches():
    try:
        ensure_matches_file()

        matches = pd.read_csv("src/matches.csv")

        matches["Date"] = pd.to_datetime(matches["Date"], errors='coerce')

        recent_matches = matches.sort_values(by="Date", ascending=False).head(5)

        recent_matches["Date"] = recent_matches["Date"].dt.strftime("%d-%m-%Y")

        return recent_matches
    except Exception as e:
        print(f"Error loading matches: {e}")
        return pd.DataFrame(columns=["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"])


def show_recent_matches(frame, parent_frame):

    for widget in frame.winfo_children():
        widget.destroy()

    recent_matches_frame = ctk.CTkFrame(frame, corner_radius=10)
    recent_matches_frame.configure(fg_color="#202020")
    recent_matches_frame.pack(pady=0, padx=0, fill="both", expand=True)

    header_frame = ctk.CTkFrame(recent_matches_frame, fg_color="#202020")
    header_frame.pack(fill="x", pady=20)

    label = ctk.CTkLabel(header_frame, text="Recent Matches", font=("Arial", 20))
    label.pack(side="left", padx=10)

    label.place(relx=0.5, rely=0.5, anchor="center")

    back_button = ctk.CTkButton(header_frame, text="Back", command=lambda: go_back_callback(recent_matches_frame, parent_frame))
    back_button.pack(side="right", padx=10)

    table_frame = ctk.CTkFrame(recent_matches_frame)
    table_frame.pack(pady=10, padx=20, fill="x")

    headers = ["Match ID", "Team A", "Team B", "Game", "Winning Team", "Date"]
    for col, header in enumerate(headers):
        header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), width=200, anchor="w")
        header_label.grid(row=0, column=col, padx=5, pady=5)

    recent_matches = load_recent_matches()

    def refresh_table():
        for widget in table_frame.winfo_children()[len(headers):]:
            widget.destroy()

        for row_idx, match in recent_matches.iterrows():
            for col_idx, value in enumerate(match):
                data_label = ctk.CTkLabel(
                    table_frame, text=str(value), font=("Arial", 12), width=200, anchor="w"
                )
                data_label.grid(row=row_idx + 1, column=col_idx, padx=5, pady=5)

    refresh_table()

    refresh_button = ctk.CTkButton(recent_matches_frame, text="Refresh Data", command=refresh_table)
    refresh_button.pack(pady=20)



def go_back_callback(current_frame, parent_frame):
    current_frame.destroy()

    for widget in parent_frame.winfo_children():
        widget.destroy()


    regular_user_interface.show_regular_user_frame(root=parent_frame)
