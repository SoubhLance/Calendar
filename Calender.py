import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, timedelta
import json
import os

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Calendar Application")
        self.root.geometry("600x700")
        
        self.events_file = "calendar_events.json"
        self.current_date = datetime.now()
        self.events = {}  # Initialize events dictionary
        self.load_events()  # Load events before setting up GUI
        self.setup_gui()

    def setup_gui(self):
        self.create_header()
        self.create_date_selector()
        self.create_calendar_display()
        self.create_event_manager()
        self.create_quick_navigation()
        self.create_search_section()
        self.update_calendar()

    def create_header(self):
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        self.header = ttk.Label(self.root, text="Calendar & Event Manager", style="Title.TLabel")
        self.header.pack(pady=10)

    def create_date_selector(self):
        date_frame = ttk.Frame(self.root)
        date_frame.pack(fill="x", padx=20)

        self.year_var = tk.StringVar(value=str(self.current_date.year))
        self.month_var = tk.StringVar(value=str(self.current_date.month))

        ttk.Label(date_frame, text="Year:").pack(side="left", padx=5)
        self.year_entry = ttk.Entry(date_frame, width=6, textvariable=self.year_var)
        self.year_entry.pack(side="left", padx=5)

        ttk.Label(date_frame, text="Month:").pack(side="left", padx=5)
        months = [(str(i), calendar.month_name[i]) for i in range(1, 13)]
        self.month_combo = ttk.Combobox(date_frame, values=[m[1] for m in months], width=10)
        self.month_combo.set(calendar.month_name[self.current_date.month])
        self.month_combo.pack(side="left", padx=5)

        ttk.Button(date_frame, text="Show", command=self.update_calendar).pack(side="left", padx=5)

    def create_calendar_display(self):
        self.calendar_frame = ttk.Frame(self.root)
        self.calendar_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.cal_display = tk.Text(self.calendar_frame, width=50, height=12, font=("Courier", 12))
        self.cal_display.pack(pady=5)

    def create_event_manager(self):
        event_frame = ttk.LabelFrame(self.root, text="Event Manager")
        event_frame.pack(pady=10, padx=20, fill="x")

        ttk.Label(event_frame, text="Date (YYYY-MM-DD):").pack(pady=5)
        self.event_date = ttk.Entry(event_frame)
        self.event_date.pack(pady=5)
        self.event_date.insert(0, self.current_date.strftime("%Y-%m-%d"))

        ttk.Label(event_frame, text="Time (HH:MM):").pack(pady=5)
        self.event_time = ttk.Entry(event_frame)
        self.event_time.pack(pady=5)

        ttk.Label(event_frame, text="Description:").pack(pady=5)
        self.event_desc = ttk.Entry(event_frame, width=50)
        self.event_desc.pack(pady=5)

        button_frame = ttk.Frame(event_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Event", command=self.add_event).pack(side="left", padx=5)
        ttk.Button(button_frame, text="View Events", command=self.view_events).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Event", command=self.delete_event).pack(side="left", padx=5)

    def create_quick_navigation(self):
        nav_frame = ttk.Frame(self.root)
        nav_frame.pack(pady=5, padx=20)
        
        ttk.Button(nav_frame, text="Previous Month", command=self.prev_month).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Today", command=self.goto_today).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="Next Month", command=self.next_month).pack(side="left", padx=5)

    def create_search_section(self):
        search_frame = ttk.LabelFrame(self.root, text="Search Events")
        search_frame.pack(pady=10, padx=20, fill="x")

        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side="left", padx=5, pady=5)
        ttk.Button(search_frame, text="Search", command=self.search_events).pack(side="left", padx=5, pady=5)

    def update_calendar(self):
        try:
            year = int(self.year_var.get())
            month = list(calendar.month_name).index(self.month_combo.get())
            
            cal = calendar.TextCalendar(calendar.SUNDAY)
            cal_text = cal.formatmonth(year, month)
            
            self.cal_display.delete(1.0, tk.END)
            self.cal_display.insert(tk.END, cal_text)
            
            self.highlight_events(year, month)
        except ValueError:
            messagebox.showerror("Error", "Invalid year or month")

    def highlight_events(self, year, month):
        for date, events in self.events.items():
            try:
                event_date = datetime.strptime(date, "%Y-%m-%d")
                if event_date.year == year and event_date.month == month:
                    # Find the position of the day number in the calendar text
                    cal_text = self.cal_display.get("1.0", tk.END)
                    day_str = f"{event_date.day:2d}"
                    start_idx = "1.0"
                    while True:
                        start_idx = self.cal_display.search(day_str, start_idx, tk.END)
                        if not start_idx:
                            break
                        # Check if this is the actual day number (not part of another number)
                        if self.cal_display.get(f"{start_idx}-1c") in [" ", "\n"]:
                            end_idx = f"{start_idx}+{len(day_str)}c"
                            self.cal_display.tag_add("event", start_idx, end_idx)
                            break
                        start_idx = f"{start_idx}+1c"
                    
                    self.cal_display.tag_configure("event", background="yellow")
            except ValueError:
                continue

    def load_events(self):
        if os.path.exists(self.events_file):
            try:
                with open(self.events_file, 'r') as f:
                    self.events = json.load(f)
            except json.JSONDecodeError:
                self.events = {}
        else:
            self.events = {}

    def save_events(self):
        with open(self.events_file, 'w') as f:
            json.dump(self.events, f, indent=4)

    def add_event(self):
        try:
            date = self.event_date.get()
            time = self.event_time.get()
            desc = self.event_desc.get()
            
            if not desc:
                messagebox.showerror("Error", "Please enter an event description")
                return
                
            datetime.strptime(date, "%Y-%m-%d")
            if time:
                datetime.strptime(time, "%H:%M")
            
            event_key = date
            if event_key not in self.events:
                self.events[event_key] = []
            
            self.events[event_key].append({
                "time": time,
                "description": desc,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            self.save_events()
            self.update_calendar()
            messagebox.showinfo("Success", "Event added successfully!")
            self.event_desc.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format")

    def view_events(self):
        if not self.events:
            messagebox.showinfo("Events", "No events found")
            return
            
        events_window = tk.Toplevel(self.root)
        events_window.title("All Events")
        events_window.geometry("400x500")
        
        events_text = tk.Text(events_window, wrap=tk.WORD, width=45, height=25)
        events_text.pack(padx=10, pady=10)
        
        for date in sorted(self.events.keys()):
            events_text.insert(tk.END, f"\nDate: {date}\n")
            for event in self.events[date]:
                time_str = f" at {event['time']}" if event['time'] else ""
                events_text.insert(tk.END, f"- {event['description']}{time_str}\n")
        
        events_text.config(state=tk.DISABLED)

    def delete_event(self):
        if not self.events:
            messagebox.showinfo("Delete Event", "No events to delete")
            return
            
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Event")
        delete_window.geometry("400x300")
        
        ttk.Label(delete_window, text="Select date:").pack(pady=5)
        date_combo = ttk.Combobox(delete_window, values=sorted(self.events.keys()))
        date_combo.pack(pady=5)
        
        def show_events_for_date(*args):
            date = date_combo.get()
            if date in self.events:
                event_listbox.delete(0, tk.END)
                for idx, event in enumerate(self.events[date]):
                    time_str = f" at {event['time']}" if event['time'] else ""
                    event_listbox.insert(tk.END, f"{event['description']}{time_str}")
        
        date_combo.bind('<<ComboboxSelected>>', show_events_for_date)
        
        event_listbox = tk.Listbox(delete_window, width=45, height=10)
        event_listbox.pack(pady=10)
        
        def delete_selected():
            date = date_combo.get()
            selection = event_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select an event to delete")
                return
                
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this event?"):
                del self.events[date][selection[0]]
                if not self.events[date]:
                    del self.events[date]
                self.save_events()
                self.update_calendar()
                delete_window.destroy()
                messagebox.showinfo("Success", "Event deleted successfully!")
        
        ttk.Button(delete_window, text="Delete Selected", command=delete_selected).pack(pady=10)

    def search_events(self):
        query = self.search_entry.get().lower()
        if not query:
            messagebox.showinfo("Search", "Please enter a search term")
            return
            
        results = []
        for date, events in self.events.items():
            for event in events:
                if query in event['description'].lower():
                    time_str = f" at {event['time']}" if event['time'] else ""
                    results.append(f"{date}: {event['description']}{time_str}")
        
        if results:
            results_window = tk.Toplevel(self.root)
            results_window.title("Search Results")
            results_window.geometry("400x300")
            
            results_text = tk.Text(results_window, wrap=tk.WORD, width=45, height=15)
            results_text.pack(padx=10, pady=10)
            
            for result in results:
                results_text.insert(tk.END, f"{result}\n")
            results_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Search Results", "No matching events found")

    def prev_month(self):
        current = datetime.strptime(f"{self.year_var.get()}-{self.month_combo.get()}", "%Y-%B")
        new_date = current.replace(day=1) - timedelta(days=1)
        self.update_date_selector(new_date)

    def next_month(self):
        current = datetime.strptime(f"{self.year_var.get()}-{self.month_combo.get()}", "%Y-%B")
        last_day = calendar.monthrange(current.year, current.month)[1]
        new_date = current.replace(day=last_day) + timedelta(days=1)
        self.update_date_selector(new_date)

    def goto_today(self):
        self.update_date_selector(datetime.now())

    def update_date_selector(self, date):
        self.year_var.set(str(date.year))
        self.month_combo.set(calendar.month_name[date.month])
        self.update_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
