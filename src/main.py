import customtkinter as ctk
import regular_user_interface
import admin_interface




def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("E-Sports Results Tracker")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    root.state("zoomed")

    create_main_menu(root)

    root.mainloop()



def create_main_menu(root):
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(pady=50, padx=50, fill="both", expand=True)

    title_label = ctk.CTkLabel(frame, text="Dashboard", font=("Arial", 24))
    title_label.pack(pady=20)

    main_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="#202020")
    main_frame.pack(pady=50, padx=50, fill="none", side="top")


    regular_user_button = ctk.CTkButton(
        main_frame,
        text="Regular User",
        font=("Arial", 16),
        width=200,
        height=80,
        command=lambda: regular_user_interface.show_regular_user_frame(root)
    )
    regular_user_button.pack(pady=40, padx=40, side="left")

    admin_button = ctk.CTkButton(
        main_frame,
        text="Admin",
        font=("Arial", 16),
        width=200,
        height=80,
        command=lambda: admin_interface.show_admin_frame(root)
    )
    admin_button.pack(pady=40, padx=40, side="left")


if __name__ == "__main__":
    main()
