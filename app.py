import ctypes
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
import webbrowser

if sys.platform == "win32":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.example.CalendarApp")

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
COLORS = {
    'header': '#4B8BBE',
    'weekdays': '#306998',
    'weekend': 'red',
    'current_day': '#77DD77',
    'month_title': '#333333',
    'bg': '#FFFFFF',
    'hover': '#F0F0F0'
}

class DynamicCalendarApp:

    def __init__(self, parent, year=None, month=None):
        self.parent = parent
        self.parent.geometry("810x670")

        try:
            root.iconbitmap(resource_path("images/icon.ico"))

        except:
            pass
        now = datetime.now()
        self.year = year if year else now.year
        self.month = month if month else None
        self.setup_ui()
        self.year_entry.insert(0, str(self.year))

        if self.month:
            self.month_entry.insert(0, str(self.month))
        self.generate_calendar()

    def setup_ui(self):
        self.input_frame = ttk.Frame(self.parent, padding="10 10 10 10")
        self.input_frame.pack(fill='x')
        ttk.Label(self.input_frame, text="Year:").grid(row=0, column=0, sticky='w')
        self.year_entry = ttk.Entry(self.input_frame, width=10)
        self.year_entry.grid(row=0, column=1, sticky='w')
        self.year_entry.bind('<Return>', lambda event: self.generate_calendar())
        ttk.Label(self.input_frame, text="Month (optional):").grid(row=1, column=0, sticky='w')
        self.month_entry = ttk.Entry(self.input_frame, width=10)
        self.month_entry.grid(row=1, column=1, sticky='w')
        self.month_entry.bind('<Return>', lambda event: self.generate_calendar())
        generate_btn = ttk.Button(
            self.input_frame,
            text="Generate Calendar",
            command=self.generate_calendar
        )
        generate_btn.grid(row=2, column=0, columnspan=2, pady=10)
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill='both', expand=True)

    def generate_calendar(self):
        year_input = self.year_entry.get()
        month_input = self.month_entry.get()

        try:
            year = int(year_input)
            month = int(month_input) if month_input else None

            if month and (month < 1 or month > 12):
                raise ValueError("Month must be between 1-12")

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {e}")
            return
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if month:
            self.show_month_calendar(year, month)
        else:
            self.show_year_calendar(year)

    def show_month_calendar(self, year, month):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        today = datetime.now()
        container_frame = tk.Frame(self.main_frame, bg=COLORS['bg'])
        container_frame.pack(expand=True)
        title_label = tk.Label(
            container_frame,
            text=f"{month_name} {year}",
            font=('Arial', 14, 'bold'),
            bg=COLORS['header'],
            fg='white',
            pady=5
        )
        title_label.grid(row=0, column=0, columnspan=7, sticky='ew')
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for col, day in enumerate(weekdays):
            bg_color = COLORS['weekdays'] if col < 5 else COLORS['weekend']
            tk.Label(
                container_frame,
                text=day,
                width=5,
                relief='flat',
                anchor='center',
                bg=bg_color,
                fg='white',
                font=('Arial', 9, 'bold')
            ).grid(row=1, column=col)
        for row_idx, week in enumerate(cal, start=2):
            for col_idx, day in enumerate(week):

                if day == 0:
                    text = ''
                    bg_color = COLORS['bg']
                    fg_color = 'black'
                else:
                    text = str(day)
                    is_today = (year == today.year and month == today.month and day == today.day)
                    bg_color = COLORS['current_day'] if is_today else (COLORS['weekend'] if col_idx >= 5 else COLORS['bg'])
                    fg_color = 'white' if col_idx >= 5 else 'black'
                label = tk.Label(
                    container_frame,
                    text=text,
                    width=5,
                    relief='groove',
                    anchor='center',
                    bg=bg_color,
                    fg=fg_color,
                    font=('Arial', 9)
                )
                label.grid(row=row_idx, column=col_idx, padx=1, pady=1)

                if day != 0:
                    label.bind("<Button-1>", lambda e, y=year, m=month, d=day: self.search_online_special_day(y, m, d))
        for col in range(7):
            container_frame.columnconfigure(col, weight=0)
        for row in range(len(cal) + 2):
            container_frame.rowconfigure(row, weight=0)

    def show_year_calendar(self, year):
        canvas = tk.Canvas(self.main_frame, bg=COLORS['bg'])
        canvas.pack(side='left', fill='both', expand=True)
        frame = tk.Frame(canvas, bg=COLORS['bg'])
        canvas.create_window((0, 0), window=frame, anchor='nw')
        frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        month_colors = ['#4B8BBE', '#306998', '#029359', '#77DD77',
                       '#AEC6CF', '#836953', 'blue', '#B19CD9',
                       "#D78E28", '#C23B22', '#6A5ACD', '#008080']
        today = datetime.now()
        for month_num in range(1, 13):
            month_frame = tk.Frame(frame, relief='groove', borderwidth=1, bg=COLORS['bg'])
            row = (month_num - 1) // 4
            col = (month_num - 1) % 4
            month_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            self.add_month_content(year, month_num, month_frame, month_colors[month_num-1], today)
        for i in range(4):
            frame.columnconfigure(i, weight=1)
        for i in range(3):
            frame.rowconfigure(i, weight=1)

    def add_month_content(self, year, month, frame, title_color, today):
        cal = calendar.monthcalendar(year, month)
        month_name = calendar.month_name[month]
        tk.Label(
            frame,
            text=f"{month_name} {year}",
            font=('Arial', 10, 'bold'),
            bg=title_color,
            fg='white',
            pady=2
        ).grid(row=0, column=0, columnspan=7, sticky='ew')
        weekdays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
        for col, day in enumerate(weekdays):
            bg_color = COLORS['weekdays'] if col < 5 else COLORS['weekend']
            tk.Label(
                frame,
                text=day,
                width=3,
                relief='flat',
                anchor='center',
                bg=bg_color,
                fg='white',
                font=('Arial', 8, 'bold')
            ).grid(row=1, column=col)
        for row_idx, week in enumerate(cal, start=2):
            for col_idx, day in enumerate(week):

                if day == 0:
                    text = ''
                    bg_color = COLORS['bg']
                    fg_color = 'black'
                else:
                    text = str(day)
                    is_today = (year == today.year and month == today.month and day == today.day)
                    bg_color = COLORS['current_day'] if is_today else (COLORS['weekend'] if col_idx >= 5 else COLORS['bg'])
                    fg_color = 'white' if col_idx >= 5 else 'black'
                label = tk.Label(
                    frame,
                    text=text,
                    width=3,
                    relief='groove',
                    anchor='center',
                    bg=bg_color,
                    fg=fg_color,
                    font=('Arial', 8)
                )
                label.grid(row=row_idx, column=col_idx, sticky='nsew', padx=1, pady=1)

                if day != 0:
                    label.bind("<Button-1>", lambda e, y=year, m=month, d=day: self.search_online_special_day(y, m, d))

    def search_online_special_day(self, year, month, day):
        date_str = f"{year}-{month:02}-{day:02}"
        query = f"{date_str} special day"
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calendar - By SouRav Bhattacharya")
    app = DynamicCalendarApp(root)
    root.mainloop()
