from database import get_connection
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
def get_dashboard_counts():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Total donors
        cursor.execute("SELECT COUNT(*) FROM Donor")
        total_donors = cursor.fetchone()[0]

        # Available donors
        cursor.execute("SELECT COUNT(*) FROM Donor WHERE availability = 1")
        available_donors = cursor.fetchone()[0]

        # Total blood requests
        cursor.execute("SELECT COUNT(*) FROM Blood_Request")
        total_requests = cursor.fetchone()[0]

        # Pending requests
        cursor.execute(
            "SELECT COUNT(*) FROM Blood_Request WHERE status = 'Pending'"
        )
        pending_requests = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return (
            total_donors,
            available_donors,
            total_requests,
            pending_requests
        )
    except Exception as e:
        print("Dashboard error:", e)

        return (0, 0, 0, 0)
def register_donor():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    blood_group = blood_group_combo.get().strip()
    phone = phone_entry.get().strip()
    location = location_entry.get().strip()
    availability = availability_combo.get().strip()

    if not name or not age or not blood_group or not phone or not location:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all required fields."
        )
        return

    try:
        age = int(age)

        if age <= 0:
            messagebox.showwarning(
                "Invalid Age",
                "Please enter a valid age."
            )
            return

        available_value = 1 if availability == "Available" else 0

        connection = get_connection()
        cursor = connection.cursor()

        # Generate the next donor ID
        cursor.execute(
            "SELECT COALESCE(MAX(donor_id), 0) + 1 FROM Donor"
        )
        new_donor_id = cursor.fetchone()[0]

        query = """
            INSERT INTO Donor
            (donor_id, name, age, blood_group, phone, location, availability)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            new_donor_id,
            name,
            age,
            blood_group,
            phone,
            location,
            available_value
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Donor registered successfully!"
        )

        clear_donor_form()

    except ValueError:
        messagebox.showerror(
            "Invalid Age",
            "Age must be a number."
        )

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )


def clear_donor_form():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    blood_group_combo.set("")
    phone_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    availability_combo.set("Available")
def show_donor_registration():
    global name_entry
    global age_entry
    global blood_group_combo
    global phone_entry
    global location_entry
    global availability_combo

    # Clear the main area
    for widget in main_area.winfo_children():
        widget.destroy()

    # Heading
    tk.Label(
        main_area,
        text="Donor Registration",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    # Form frame
    form_frame = tk.Frame(
        main_area,
        bg=WHITE,
        padx=30,
        pady=25
    )
    form_frame.pack(fill="x", padx=35)

    # Name
    tk.Label(
        form_frame,
        text="Name",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=0, column=0, sticky="w", pady=10)

    name_entry = tk.Entry(
        form_frame,
        font=("Arial", 12),
        width=35
    )
    name_entry.grid(row=0, column=1, padx=20, pady=10)

    # Age
    tk.Label(
        form_frame,
        text="Age",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=1, column=0, sticky="w", pady=10)

    age_entry = tk.Entry(
        form_frame,
        font=("Arial", 12),
        width=35
    )
    age_entry.grid(row=1, column=1, padx=20, pady=10)

    # Blood Group
    tk.Label(
        form_frame,
        text="Blood Group",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=2, column=0, sticky="w", pady=10)

    blood_group_combo = ttk.Combobox(
        form_frame,
        values=[
            "A+", "A-",
            "B+", "B-",
            "AB+", "AB-",
            "O+", "O-"
        ],
        state="readonly",
        font=("Arial", 12),
        width=33
    )
    blood_group_combo.grid(row=2, column=1, padx=20, pady=10)

    # Phone
    tk.Label(
        form_frame,
        text="Phone",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=3, column=0, sticky="w", pady=10)

    phone_entry = tk.Entry(
        form_frame,
        font=("Arial", 12),
        width=35
    )
    phone_entry.grid(row=3, column=1, padx=20, pady=10)

    # Location
    tk.Label(
        form_frame,
        text="Location",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=4, column=0, sticky="w", pady=10)

    location_entry = tk.Entry(
        form_frame,
        font=("Arial", 12),
        width=35
    )
    location_entry.grid(row=4, column=1, padx=20, pady=10)

    # Availability
    tk.Label(
        form_frame,
        text="Availability",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=5, column=0, sticky="w", pady=10)

    availability_combo = ttk.Combobox(
        form_frame,
        values=["Available", "Not Available"],
        state="readonly",
        font=("Arial", 12),
        width=33
    )
    availability_combo.set("Available")
    availability_combo.grid(row=5, column=1, padx=20, pady=10)

    # Buttons
    button_frame = tk.Frame(
        form_frame,
        bg=WHITE
    )
    button_frame.grid(
        row=6,
        column=0,
        columnspan=2,
        pady=25
    )

    tk.Button(
        button_frame,
        text="Register Donor",
        font=("Arial", 12, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE,
        padx=20,
        pady=10,
        bd=0,
        command=register_donor
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Clear",
        font=("Arial", 12),
        padx=25,
        pady=10,
        command=clear_donor_form
    ).pack(side="left", padx=10)
def show_donor_list():
    # Clear the main area
    for widget in main_area.winfo_children():
        widget.destroy()

    tk.Label(
        main_area,
        text="Donor List",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    # Table frame
    table_frame = tk.Frame(
        main_area,
        bg=WHITE
    )
    table_frame.pack(fill="both", expand=True, padx=35, pady=10)

    columns = (
        "donor_id",
        "name",
        "age",
        "blood_group",
        "phone",
        "location",
        "availability"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    tree.heading("donor_id", text="ID")
    tree.heading("name", text="Name")
    tree.heading("age", text="Age")
    tree.heading("blood_group", text="Blood Group")
    tree.heading("phone", text="Phone")
    tree.heading("location", text="Location")
    tree.heading("availability", text="Availability")

    tree.column("donor_id", width=60)
    tree.column("name", width=150)
    tree.column("age", width=70)
    tree.column("blood_group", width=100)
    tree.column("phone", width=130)
    tree.column("location", width=120)
    tree.column("availability", width=120)

    tree.pack(fill="both", expand=True, padx=20, pady=20)

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT donor_id, name, age, blood_group,
                   phone, location, availability
            FROM Donor
            ORDER BY donor_id
        """)

        donors = cursor.fetchall()

        for donor in donors:
            availability = "Available" if donor[6] == 1 else "Not Available"

            tree.insert(
                "",
                "end",
                values=(
                    donor[0],
                    donor[1],
                    donor[2],
                    donor[3],
                    donor[4],
                    donor[5],
                    availability
                )
            )

        cursor.close()
        connection.close()

    except Exception as e:
        messagebox.showerror(
            "Database Error",
            str(e)
        )
def show_find_donor():
    for widget in main_area.winfo_children():
        widget.destroy()

    tk.Label(
        main_area,
        text="Find Donor",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    search_frame = tk.Frame(
        main_area,
        bg=WHITE,
        padx=20,
        pady=20
    )
    search_frame.pack(fill="x", padx=35)

    tk.Label(
        search_frame,
        text="Blood Group",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=0, column=0, padx=10)

    blood_search = ttk.Combobox(
        search_frame,
        values=[
            "All",
            "A+", "A-",
            "B+", "B-",
            "AB+", "AB-",
            "O+", "O-"
        ],
        state="readonly",
        width=15
    )
    blood_search.set("All")
    blood_search.grid(row=0, column=1, padx=10)

    tk.Label(
        search_frame,
        text="Location",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=0, column=2, padx=10)

    location_search = tk.Entry(
        search_frame,
        font=("Arial", 12),
        width=20
    )
    location_search.grid(row=0, column=3, padx=10)

    columns = (
        "donor_id",
        "name",
        "age",
        "blood_group",
        "phone",
        "location"
    )

    tree = ttk.Treeview(
        main_area,
        columns=columns,
        show="headings"
    )

    headings = {
        "donor_id": "ID",
        "name": "Name",
        "age": "Age",
        "blood_group": "Blood Group",
        "phone": "Phone",
        "location": "Location"
    }

    for column in columns:
        tree.heading(column, text=headings[column])
        tree.column(column, width=120)

    tree.pack(
        fill="both",
        expand=True,
        padx=35,
        pady=20
    )

    def search_donors():
        for item in tree.get_children():
            tree.delete(item)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            blood_group = blood_search.get()
            location = location_search.get().strip()

            query = """
                SELECT donor_id, name, age, blood_group, phone, location
                FROM Donor
                WHERE availability = 1
            """

            values = []

            if blood_group != "All":
                query += " AND blood_group = %s"
                values.append(blood_group)

            if location:
                query += " AND location LIKE %s"
                values.append("%" + location + "%")

            query += " ORDER BY donor_id"

            cursor.execute(query, values)

            donors = cursor.fetchall()

            for donor in donors:
                tree.insert("", "end", values=donor)

            cursor.close()
            connection.close()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        search_frame,
        text="Search",
        font=("Arial", 12, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE,
        padx=20,
        pady=8,
        bd=0,
        command=search_donors
    ).grid(row=0, column=4, padx=15)
def show_blood_request():
    for widget in main_area.winfo_children():
        widget.destroy()

    tk.Label(
        main_area,
        text="Blood Request",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    form_frame = tk.Frame(
        main_area,
        bg=WHITE,
        padx=30,
        pady=25
    )
    form_frame.pack(fill="x", padx=35)

    # Recipient ID
    tk.Label(
        form_frame,
        text="Recipient ID",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=0, column=0, sticky="w", pady=10)

    recipient_entry = tk.Entry(
        form_frame,
        font=("Arial", 12),
        width=35
    )
    recipient_entry.grid(row=0, column=1, padx=20, pady=10)

    # Blood Group
    tk.Label(
        form_frame,
        text="Blood Group",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=1, column=0, sticky="w", pady=10)

    blood_group_combo = ttk.Combobox(
        form_frame,
        values=[
            "A+", "A-",
            "B+", "B-",
            "AB+", "AB-",
            "O+", "O-"
        ],
        state="readonly",
        font=("Arial", 12),
        width=33
    )
    blood_group_combo.grid(row=1, column=1, padx=20, pady=10)

    # Units Required
    tk.Label(
        form_frame,
        text="Units Required",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=2, column=0, sticky="w", pady=10)

    units_entry = tk.Entry(
        form_frame,
        font=("Arial", 12),
        width=35
    )
    units_entry.grid(row=2, column=1, padx=20, pady=10)

    # Urgency
    tk.Label(
        form_frame,
        text="Urgency",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=3, column=0, sticky="w", pady=10)

    urgency_combo = ttk.Combobox(
        form_frame,
        values=[
            "Low",
            "Medium",
            "High",
            "Emergency"
        ],
        state="readonly",
        font=("Arial", 12),
        width=33
    )
    urgency_combo.set("Medium")
    urgency_combo.grid(row=3, column=1, padx=20, pady=10)

    # Bank ID
    tk.Label(
        form_frame,
        text="Blood Bank ID",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=4, column=0, sticky="w", pady=10)

    bank_entry = tk.Entry(
        form_frame,
        font=("Arial", 12),
        width=35
    )
    bank_entry.grid(row=4, column=1, padx=20, pady=10)

    def submit_request():
        recipient_id = recipient_entry.get().strip()
        blood_group = blood_group_combo.get().strip()
        units = units_entry.get().strip()
        urgency = urgency_combo.get().strip()
        bank_id = bank_entry.get().strip()

        if not recipient_id or not blood_group or not units:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in Recipient ID, Blood Group and Units Required."
            )
            return

        try:
            recipient_id = int(recipient_id)
            units = int(units)

            if units <= 0:
                messagebox.showwarning(
                    "Invalid Units",
                    "Units required must be greater than 0."
                )
                return

            bank_id = int(bank_id) if bank_id else None

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COALESCE(MAX(request_id), 0) + 1
                FROM Blood_Request
                """
            )

            new_request_id = cursor.fetchone()[0]

            query = """
                INSERT INTO Blood_Request
                (
                    request_id,
                    recipient_id,
                    blood_group,
                    units_required,
                    request_date,
                    urgency,
                    status,
                    bank_id
                )
                VALUES (%s, %s, %s, %s, CURDATE(), %s, %s, %s)
            """

            values = (
                new_request_id,
                recipient_id,
                blood_group,
                units,
                urgency,
                "Pending",
                bank_id
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Blood request submitted successfully!"
            )

            recipient_entry.delete(0, tk.END)
            units_entry.delete(0, tk.END)
            bank_entry.delete(0, tk.END)
            blood_group_combo.set("")
            urgency_combo.set("Medium")

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Recipient ID, Units and Blood Bank ID must be numbers."
            )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
        form_frame,
        text="Submit Request",
        font=("Arial", 12, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE,
        padx=20,
        pady=10,
        bd=0,
        command=submit_request
    ).grid(
        row=5,
        column=0,
        columnspan=2,
        pady=25
    )


def show_request_management():
    for widget in main_area.winfo_children():
        widget.destroy()

    tk.Label(
        main_area,
        text="Request Management",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    # Status update controls
    control_frame = tk.Frame(main_area, bg=BG_COLOR)
    control_frame.pack(fill="x", padx=35, pady=10)

    tk.Label(
        control_frame,
        text="New Status:",
        font=("Arial", 12, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(side="left", padx=(0, 10))

    status_var = tk.StringVar(value="Pending")

    status_dropdown = ttk.Combobox(
        control_frame,
        textvariable=status_var,
        values=("Pending", "Donor Found", "Completed", "Cancelled"),
        state="readonly",
        width=18
    )
    status_dropdown.pack(side="left", padx=5)

    table_frame = tk.Frame(main_area, bg=WHITE)
    table_frame.pack(fill="both", expand=True, padx=35, pady=10)

    columns = (
        "request_id",
        "recipient_id",
        "blood_group",
        "units_required",
        "request_date",
        "urgency",
        "status",
        "bank_id"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    headings = {
        "request_id": "Request ID",
        "recipient_id": "Recipient ID",
        "blood_group": "Blood Group",
        "units_required": "Units",
        "request_date": "Request Date",
        "urgency": "Urgency",
        "status": "Status",
        "bank_id": "Blood Bank ID"
    }

    for column in columns:
        tree.heading(column, text=headings[column])
        tree.column(column, width=110, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
    scrollbar.pack(side="right", fill="y", pady=10)

    def load_requests():
        for item in tree.get_children():
            tree.delete(item)

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT request_id, recipient_id, blood_group,
                       units_required, request_date, urgency,
                       status, bank_id
                FROM Blood_Request
                ORDER BY request_id DESC
            """)

            for request in cursor.fetchall():
                tree.insert("", "end", values=request)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def update_status():
        selected = tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Request",
                "Please select a blood request from the table."
            )
            return

        request = tree.item(selected[0], "values")
        request_id = request[0]
        new_status = status_var.get()

        if request[6] == new_status:
            messagebox.showinfo(
                "No Change",
                "This request already has that status."
            )
            return

        connection = None
        cursor = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE Blood_Request
                SET status = %s
                WHERE request_id = %s
            """, (new_status, request_id))

            connection.commit()

            messagebox.showinfo(
                "Success",
                f"Request {request_id} status updated to {new_status}."
            )

            load_requests()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    tk.Button(
        control_frame,
        text="Update Status",
        command=update_status,
        font=("Arial", 11, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE,
        padx=12,
        pady=6
    ).pack(side="left", padx=15)

    load_requests()

def show_match_donor():
    for widget in main_area.winfo_children():
        widget.destroy()

    tk.Label(
        main_area,
        text="Match Donor",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    top_frame = tk.Frame(main_area, bg=WHITE, padx=20, pady=20)
    top_frame.pack(fill="x", padx=35, pady=10)

    tk.Label(
        top_frame,
        text="Select Blood Request ID",
        font=("Arial", 12),
        bg=WHITE
    ).pack(side="left", padx=10)

    request_combo = ttk.Combobox(
        top_frame,
        state="readonly",
        width=20,
        font=("Arial", 12)
    )
    request_combo.pack(side="left", padx=10)

    columns = ("donor_id", "name", "blood_group", "phone", "location")

    table_frame = tk.Frame(main_area, bg=WHITE)
    table_frame.pack(fill="both", expand=True, padx=35, pady=10)

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    headings = {
        "donor_id": "Donor ID",
        "name": "Name",
        "blood_group": "Blood Group",
        "phone": "Phone",
        "location": "Location"
    }

    for column in columns:
        tree.heading(column, text=headings[column])
        tree.column(column, width=130, anchor="center")

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_requests():
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT request_id, blood_group, status
                FROM Blood_Request
                ORDER BY request_id DESC
            """)

            requests = cursor.fetchall()

            request_combo["values"] = [
                f"{r[0]} - {r[1]} ({r[2]})" for r in requests
            ]

            if requests:
                request_combo.current(0)

            cursor.close()
            connection.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def find_matches():
        for item in tree.get_children():
            tree.delete(item)

        selected = request_combo.get()

        if not selected:
            messagebox.showwarning(
                "Select Request",
                "Please select a blood request first."
            )
            return

        try:
            request_id = int(selected.split(" - ")[0])

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT blood_group
                FROM Blood_Request
                WHERE request_id = %s
            """, (request_id,))

            request = cursor.fetchone()

            if not request:
                messagebox.showwarning(
                    "Not Found",
                    "The selected blood request was not found."
                )
                cursor.close()
                connection.close()
                return

            required_group = request[0]

            cursor.execute("""
                SELECT donor_id, name, blood_group, phone, location
                FROM Donor
                WHERE availability = 1
                  AND blood_group = %s
                ORDER BY donor_id
            """, (required_group,))

            donors = cursor.fetchall()

            for donor in donors:
                tree.insert("", "end", values=donor)

            cursor.close()
            connection.close()

            if donors:
                messagebox.showinfo(
                    "Matches Found",
                    f"Found {len(donors)} available donor(s) "
                    f"with blood group {required_group}."
                )
            else:
                messagebox.showinfo(
                    "No Matches",
                    f"No available donors with blood group "
                    f"{required_group} were found."
                )

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    tk.Button(
        top_frame,
        text="Find Matches",
        font=("Arial", 11, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE,
        padx=15,
        pady=8,
        bd=0,
        command=find_matches
    ).pack(side="left", padx=10)

    load_requests()

def show_record_donation():
    for widget in main_area.winfo_children():
        widget.destroy()

    tk.Label(
        main_area,
        text="Record Donation",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    form_frame = tk.Frame(
        main_area,
        bg=WHITE,
        padx=30,
        pady=25
    )
    form_frame.pack(fill="x", padx=35)

    tk.Label(
        form_frame,
        text="Donor ID",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=0, column=0, sticky="w", pady=10)

    donor_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    donor_entry.grid(row=0, column=1, padx=20, pady=10)

    tk.Label(
        form_frame,
        text="Request ID",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=1, column=0, sticky="w", pady=10)

    request_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    request_entry.grid(row=1, column=1, padx=20, pady=10)

    tk.Label(
        form_frame,
        text="Units Donated",
        font=("Arial", 12),
        bg=WHITE
    ).grid(row=2, column=0, sticky="w", pady=10)

    units_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    units_entry.grid(row=2, column=1, padx=20, pady=10)

    def save_donation():
        donor_id = donor_entry.get().strip()
        request_id = request_entry.get().strip()
        units = units_entry.get().strip()

        if not donor_id or not request_id or not units:
            messagebox.showwarning(
                "Missing Information",
                "Please enter Donor ID, Request ID and Units Donated."
            )
            return

        connection = None
        cursor = None

        try:
            donor_id = int(donor_id)
            request_id = int(request_id)
            units = int(units)

            if donor_id <= 0 or request_id <= 0 or units <= 0:
                messagebox.showwarning(
                    "Invalid Input",
                    "IDs and units must be greater than zero."
                )
                return

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT donor_id FROM Donor WHERE donor_id = %s",
                (donor_id,)
            )
            if cursor.fetchone() is None:
                messagebox.showerror(
                    "Invalid Donor",
                    "That Donor ID does not exist."
                )
                return

            cursor.execute(
                "SELECT request_id FROM Blood_Request WHERE request_id = %s",
                (request_id,)
            )
            if cursor.fetchone() is None:
                messagebox.showerror(
                    "Invalid Request",
                    "That Request ID does not exist."
                )
                return

            cursor.execute(
                "SELECT COALESCE(MAX(donation_id), 0) + 1 FROM Donation"
            )
            donation_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO Donation
                    (donation_id, donor_id, request_id,
                     donation_date, units_donated)
                VALUES (%s, %s, %s, CURDATE(), %s)
                """,
                (donation_id, donor_id, request_id, units)
            )

            connection.commit()

            messagebox.showinfo(
                "Success",
                "Donation recorded successfully!"
            )

            donor_entry.delete(0, tk.END)
            request_entry.delete(0, tk.END)
            units_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Donor ID, Request ID and units must be numbers."
            )

        except Exception as e:
            if connection:
                connection.rollback()

            messagebox.showerror("Database Error", str(e))

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    tk.Button(
        form_frame,
        text="Record Donation",
        font=("Arial", 12, "bold"),
        bg=SIDEBAR_COLOR,
        fg=WHITE,
        padx=20,
        pady=10,
        bd=0,
        command=save_donation
    ).grid(row=3, column=0, columnspan=2, pady=25)

def show_reports():
    for widget in main_area.winfo_children():
        widget.destroy()

    tk.Label(
        main_area,
        text="Reports & Statistics",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    stats_frame = tk.Frame(main_area, bg=BG_COLOR)
    stats_frame.pack(fill="x", padx=35, pady=10)

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM Donor")
        total_donors = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Donor WHERE availability = 1"
        )
        available_donors = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Donation")
        total_donations = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Blood_Request")
        total_requests = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM Blood_Request
            WHERE status = 'Pending'
        """)
        pending_requests = cursor.fetchone()[0]

        cursor.execute("""
            SELECT blood_group, COUNT(*)
            FROM Donor
            GROUP BY blood_group
            ORDER BY blood_group
        """)
        blood_group_data = cursor.fetchall()

        cursor.execute("""
            SELECT status, COUNT(*)
            FROM Blood_Request
            GROUP BY status
            ORDER BY status
        """)
        request_status_data = cursor.fetchall()

        cursor.close()
        connection.close()

        stats = [
            ("Total Donors", total_donors),
            ("Available Donors", available_donors),
            ("Total Donations", total_donations),
            ("Total Requests", total_requests),
            ("Pending Requests", pending_requests)
        ]

        for index, (label, value) in enumerate(stats):
            card = tk.Frame(
                stats_frame,
                bg=WHITE,
                padx=20,
                pady=20,
                highlightbackground="#dddddd",
                highlightthickness=1
            )
            card.grid(
                row=index // 3,
                column=index % 3,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=label,
                font=("Arial", 11),
                bg=WHITE,
                fg=TEXT_COLOR
            ).pack(anchor="w")

            tk.Label(
                card,
                text=str(value),
                font=("Arial", 24, "bold"),
                bg=WHITE,
                fg=SIDEBAR_COLOR
            ).pack(anchor="w", pady=(8, 0))

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)

        # Blood group report
        blood_frame = tk.Frame(main_area, bg=WHITE, padx=20, pady=15)
        blood_frame.pack(fill="x", padx=45, pady=10)

        tk.Label(
            blood_frame,
            text="Donors by Blood Group",
            font=("Arial", 15, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(0, 10))

        blood_text = tk.Text(
            blood_frame,
            height=max(2, len(blood_group_data)),
            font=("Arial", 11),
            bg=WHITE,
            relief="flat"
        )
        blood_text.pack(fill="x")

        for group, count in blood_group_data:
            blood_text.insert("end", f"{group}: {count} donor(s)\n")

        blood_text.config(state="disabled")

        # Request status report
        request_frame = tk.Frame(main_area, bg=WHITE, padx=20, pady=15)
        request_frame.pack(fill="x", padx=45, pady=10)

        tk.Label(
            request_frame,
            text="Requests by Status",
            font=("Arial", 15, "bold"),
            bg=WHITE,
            fg=TEXT_COLOR
        ).pack(anchor="w", pady=(0, 10))

        request_text = tk.Text(
            request_frame,
            height=max(2, len(request_status_data)),
            font=("Arial", 11),
            bg=WHITE,
            relief="flat"
        )
        request_text.pack(fill="x")

        if request_status_data:
            for status, count in request_status_data:
                request_text.insert("end", f"{status}: {count} request(s)\n")
        else:
            request_text.insert("end", "No requests recorded yet.\n")

        request_text.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Reports Error", str(e))

def show_about():
    for widget in main_area.winfo_children():
        widget.destroy()

    tk.Label(
        main_area,
        text="About Blood Emergency Link",
        font=("Arial", 26, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(anchor="w", padx=35, pady=(30, 20))

    about_frame = tk.Frame(
        main_area,
        bg=WHITE,
        padx=35,
        pady=30
    )
    about_frame.pack(fill="both", expand=True, padx=35, pady=10)

    tk.Label(
        about_frame,
        text="Blood Emergency Link",
        font=("Arial", 24, "bold"),
        bg=WHITE,
        fg=SIDEBAR_COLOR
    ).pack(anchor="center", pady=(10, 20))

    tk.Label(
        about_frame,
        text=(
            "Project Overview\n\n"
            "Blood Emergency Link is a database-driven application "
            "designed to help users manage blood donors and blood requests.\n\n"
            "Objective\n\n"
            "To organize donor information, record blood requests, "
            "identify potential donors by blood group, and maintain "
            "donation records in one system.\n\n"
            "Key Features\n\n"
            "• Donor Registration and Management\n"
            "• Search Available Donors by Blood Group and Location\n"
            "• Submit and Manage Blood Requests\n"
            "• Match Requests with Potential Donors\n"
            "• Record Donations\n"
            "• View Reports and Statistics\n\n"
            "Technologies Used\n\n"
            "Python | Tkinter | MySQL | Aiven Cloud Database\n\n"
            "Academic Project: Database Management Systems (DBMS)"
        ),
        font=("Arial", 12),
        bg=WHITE,
        fg=TEXT_COLOR,
        justify="left",
        wraplength=700
    ).pack(anchor="w", fill="x", pady=10)

    tk.Label(
        about_frame,
        text="Note: Actual blood transfusions require verification by qualified medical professionals.",
        font=("Arial", 10, "italic"),
        bg=WHITE,
        fg=TEXT_COLOR,
        wraplength=700
    ).pack(anchor="w", pady=(15, 5))

root = tk.Tk()
root.title("Blood Emergency Link")
root.geometry("1000x650")
root.minsize(900, 600)

# ---------- COLORS ----------
BG_COLOR = "#f5f7fb"
SIDEBAR_COLOR = "#b71c1c"
WHITE = "#ffffff"
TEXT_COLOR = "#333333"

root.configure(bg=BG_COLOR)

# ---------- SIDEBAR ----------
sidebar = tk.Frame(root, bg=SIDEBAR_COLOR, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

title = tk.Label(
    sidebar,
    text="Blood\nEmergency Link",
    font=("Arial", 20, "bold"),
    fg=WHITE,
    bg=SIDEBAR_COLOR
)
title.pack(pady=40)

# ---------- MAIN AREA ----------
main_area = tk.Frame(root, bg=BG_COLOR)
main_area.pack(side="right", fill="both", expand=True)

heading = tk.Label(
    main_area,
    text="Dashboard",
    font=("Arial", 26, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
)
heading.pack(anchor="w", padx=35, pady=(30, 20))


# ---------- DASHBOARD CARDS ----------
cards_frame = tk.Frame(main_area, bg=BG_COLOR)
cards_frame.pack(fill="x", padx=30)


def create_card(parent, title, value):
    card = tk.Frame(
        parent,
        bg=WHITE,
        width=200,
        height=120,
        highlightbackground="#dddddd",
        highlightthickness=1
    )
    card.pack(side="left", padx=10, pady=10)
    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 12),
        fg="#666666",
        bg=WHITE
    ).pack(pady=(20, 5))

    tk.Label(
        card,
        text=value,
        font=("Arial", 25, "bold"),
        fg=SIDEBAR_COLOR,
        bg=WHITE
    ).pack()


total_donors, available_donors, total_requests, pending_requests = get_dashboard_counts()

create_card(cards_frame, "Total Donors", str(total_donors))
create_card(cards_frame, "Available Donors", str(available_donors))
create_card(cards_frame, "Blood Requests", str(total_requests))
create_card(cards_frame, "Pending Requests", str(pending_requests))


def show_dashboard():
    for widget in main_area.winfo_children():
        widget.destroy()

    title = tk.Label(
        main_area,
        text="Dashboard",
        font=("Arial", 22, "bold"),
        fg=TEXT_COLOR,
        bg=BG_COLOR
    )
    title.pack(anchor="w", padx=45, pady=(30, 20))

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM Donor")
        total_donors = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM Donor WHERE availability = 1"
        )
        available_donors = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Blood_Request")
        total_requests = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Donation")
        total_donations = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        stats = [
            ("Total Donors", total_donors),
            ("Available Donors", available_donors),
            ("Blood Requests", total_requests),
            ("Donations Recorded", total_donations)
        ]

        for label_text, value in stats:
            tk.Label(
                main_area,
                text=f"{label_text}: {value}",
                font=("Arial", 15, "bold"),
                fg=TEXT_COLOR,
                bg=WHITE,
                padx=20,
                pady=15
            ).pack(fill="x", padx=45, pady=7)

        tk.Button(
            main_area,
            text="Refresh Dashboard",
            command=show_dashboard,
            font=("Arial", 12, "bold"),
            bg=SIDEBAR_COLOR,
            fg=WHITE,
            padx=15,
            pady=8
        ).pack(anchor="w", padx=45, pady=20)

    except Exception as error:
        messagebox.showerror("Database Error", str(error))

# ---------- SIDEBAR BUTTONS ----------
def sidebar_button(text):
    button = tk.Button(
        sidebar,
        text=text,
        font=("Arial", 12),
        fg=WHITE,
        bg=SIDEBAR_COLOR,
        activebackground="#8e0000",
        activeforeground=WHITE,
        bd=0,
        anchor="w",
        padx=30,
        pady=12
    )
    button.pack(fill="x")
    return button


sidebar_button("Dashboard").config(command=show_dashboard)
sidebar_button("Donor Registration").config(command=show_donor_registration)
sidebar_button("Donor Management").config(command=show_donor_list)
sidebar_button("Find Donor").config(command=show_find_donor)
sidebar_button("Blood Request").config(command=show_blood_request)
sidebar_button("Request Management").config(
    command=show_request_management
)
sidebar_button("Match Donor").config(command=show_match_donor)
sidebar_button("Record Donation").config(
    command=show_record_donation
)
sidebar_button("Reports").config(command=show_reports)
sidebar_button("About").config(command=show_about)



# ---------- WELCOME MESSAGE ----------
welcome = tk.Label(
    main_area,
    text="Welcome to Blood Emergency Link",
    font=("Arial", 18, "bold"),
    fg=TEXT_COLOR,
    bg=BG_COLOR
)
welcome.pack(anchor="w", padx=45, pady=(50, 10))

description = tk.Label(
    main_area,
    text="Connect blood donors with patients during emergency situations.",
    font=("Arial", 12),
    fg="#666666",
    bg=BG_COLOR
)
description.pack(anchor="w", padx=45)


root.mainloop()