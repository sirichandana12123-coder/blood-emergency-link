import streamlit as st
import mysql.connector
from dotenv import load_dotenv
import os

# Load database settings from your existing .env
load_dotenv()

st.set_page_config(
    page_title="Blood Emergency Link",
    page_icon="🩸",
    layout="wide"
)

# ---------------- DATABASE ----------------

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False
    )


def execute_query(query, values=(), fetch=False):
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, values)

        if fetch:
            return cursor.fetchall()

        connection.commit()
        return True

    except Exception as e:
        st.error(f"Database Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# ---------------- STYLE ----------------

st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}

[data-testid="stSidebar"] {
    background-color: #b71c1c;
}

[data-testid="stSidebar"] * {
    color: white !important;
}

h1, h2, h3 {
    color: #333333;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #dddddd;
    text-align: center;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #b71c1c;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

st.sidebar.title("🩸 Blood")
st.sidebar.title("Emergency Link")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Donor Registration",
        "Donor Management",
        "Find Donor",
        "Blood Request",
        "Request Management",
        "Match Donor",
        "Record Donation",
        "Reports",
        "About"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("Dashboard")

    total_donors = execute_query(
        "SELECT COUNT(*) FROM Donor",
        fetch=True
    )

    available_donors = execute_query(
        "SELECT COUNT(*) FROM Donor WHERE availability = 1",
        fetch=True
    )

    total_requests = execute_query(
        "SELECT COUNT(*) FROM Blood_Request",
        fetch=True
    )

    pending_requests = execute_query(
        "SELECT COUNT(*) FROM Blood_Request WHERE status = 'Pending'",
        fetch=True
    )

    total_donors = total_donors[0][0] if total_donors else 0
    available_donors = available_donors[0][0] if available_donors else 0
    total_requests = total_requests[0][0] if total_requests else 0
    pending_requests = pending_requests[0][0] if pending_requests else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Donors", total_donors)
    c2.metric("Available Donors", available_donors)
    c3.metric("Blood Requests", total_requests)
    c4.metric("Pending Requests", pending_requests)

    st.divider()

    st.header("Welcome to Blood Emergency Link")
    st.write(
        "Connect blood donors with patients during emergency situations."
    )

    if st.button("🔄 Refresh Dashboard"):
        st.rerun()


# =========================================================
# DONOR REGISTRATION
# =========================================================

elif page == "Donor Registration":

    st.title("Donor Registration")

    with st.form("donor_form"):

        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)

        blood_group = st.selectbox(
            "Blood Group",
            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )

        phone = st.text_input("Phone")
        location = st.text_input("Location")

        availability = st.selectbox(
            "Availability",
            ["Available", "Not Available"]
        )

        submitted = st.form_submit_button("Register Donor")

        if submitted:

            if not name or not phone or not location:
                st.warning("Please fill in all required fields.")

            else:

                available_value = 1 if availability == "Available" else 0

                result = execute_query(
                    """
                    SELECT COALESCE(MAX(donor_id), 0) + 1
                    FROM Donor
                    """,
                    fetch=True
                )

                new_donor_id = result[0][0]

                success = execute_query(
                    """
                    INSERT INTO Donor
                    (
                        donor_id,
                        name,
                        age,
                        blood_group,
                        phone,
                        location,
                        availability
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        new_donor_id,
                        name,
                        age,
                        blood_group,
                        phone,
                        location,
                        available_value
                    )
                )

                if success:
                    st.success(
                        f"Donor registered successfully! Donor ID: {new_donor_id}"
                    )


# =========================================================
# DONOR MANAGEMENT
# =========================================================

elif page == "Donor Management":

    st.title("Donor Management")

    donors = execute_query(
        """
        SELECT donor_id, name, age, blood_group,
               phone, location, availability
        FROM Donor
        ORDER BY donor_id
        """,
        fetch=True
    )

    if donors:

        table_data = []

        for donor in donors:
            table_data.append({
                "ID": donor[0],
                "Name": donor[1],
                "Age": donor[2],
                "Blood Group": donor[3],
                "Phone": donor[4],
                "Location": donor[5],
                "Availability":
                    "Available" if donor[6] == 1 else "Not Available"
            })

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No donors found.")


# =========================================================
# FIND DONOR
# =========================================================

elif page == "Find Donor":

    st.title("Find Donor")

    col1, col2 = st.columns(2)

    with col1:
        blood_group = st.selectbox(
            "Blood Group",
            [
                "All",
                "A+", "A-",
                "B+", "B-",
                "AB+", "AB-",
                "O+", "O-"
            ]
        )

    with col2:
        location = st.text_input("Location")

    if st.button("🔍 Search Donors"):

        query = """
        SELECT donor_id, name, age,
               blood_group, phone, location
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

        donors = execute_query(
            query,
            values,
            fetch=True
        )

        if donors:

            table_data = []

            for donor in donors:
                table_data.append({
                    "ID": donor[0],
                    "Name": donor[1],
                    "Age": donor[2],
                    "Blood Group": donor[3],
                    "Phone": donor[4],
                    "Location": donor[5]
                })

            st.dataframe(
                table_data,
                use_container_width=True,
                hide_index=True
            )

            st.success(f"Found {len(donors)} available donor(s).")

        else:
            st.warning("No matching donors found.")


# =========================================================
# BLOOD REQUEST
# =========================================================

elif page == "Blood Request":

    st.title("Blood Request")

    with st.form("request_form"):

        recipient_id = st.number_input(
            "Recipient ID",
            min_value=1,
            step=1
        )

        blood_group = st.selectbox(
            "Blood Group",
            ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
        )

        units = st.number_input(
            "Units Required",
            min_value=1,
            step=1
        )

        urgency = st.selectbox(
            "Urgency",
            ["Low", "Medium", "High", "Emergency"]
        )

        bank_id = st.number_input(
            "Blood Bank ID",
            min_value=0,
            step=1
        )

        submitted = st.form_submit_button("Submit Request")

        if submitted:

            result = execute_query(
                """
                SELECT COALESCE(MAX(request_id), 0) + 1
                FROM Blood_Request
                """,
                fetch=True
            )

            request_id = result[0][0]

            actual_bank_id = bank_id if bank_id > 0 else None

            success = execute_query(
                """
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
                VALUES
                (%s, %s, %s, %s, CURDATE(), %s, %s, %s)
                """,
                (
                    request_id,
                    recipient_id,
                    blood_group,
                    units,
                    urgency,
                    "Pending",
                    actual_bank_id
                )
            )

            if success:
                st.success(
                    f"Blood request submitted successfully! "
                    f"Request ID: {request_id}"
                )


# =========================================================
# REQUEST MANAGEMENT
# =========================================================

elif page == "Request Management":

    st.title("Request Management")

    requests = execute_query(
        """
        SELECT request_id, recipient_id, blood_group,
               units_required, request_date,
               urgency, status, bank_id
        FROM Blood_Request
        ORDER BY request_id DESC
        """,
        fetch=True
    )

    if requests:

        table_data = []

        for r in requests:
            table_data.append({
                "Request ID": r[0],
                "Recipient ID": r[1],
                "Blood Group": r[2],
                "Units": r[3],
                "Date": r[4],
                "Urgency": r[5],
                "Status": r[6],
                "Blood Bank ID": r[7]
            })

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )

        request_ids = [r[0] for r in requests]

        selected_id = st.selectbox(
            "Select Request",
            request_ids
        )

        new_status = st.selectbox(
            "New Status",
            [
                "Pending",
                "Donor Found",
                "Completed",
                "Cancelled"
            ]
        )

        if st.button("Update Status"):

            success = execute_query(
                """
                UPDATE Blood_Request
                SET status = %s
                WHERE request_id = %s
                """,
                (new_status, selected_id)
            )

            if success:
                st.success(
                    f"Request {selected_id} updated to {new_status}."
                )
                st.rerun()

    else:
        st.info("No blood requests found.")


# =========================================================
# MATCH DONOR
# =========================================================

elif page == "Match Donor":

    st.title("Match Donor")

    requests = execute_query(
        """
        SELECT request_id, blood_group, status
        FROM Blood_Request
        ORDER BY request_id DESC
        """,
        fetch=True
    )

    if requests:

        request_options = {
            f"{r[0]} - {r[1]} ({r[2]})": r[0]
            for r in requests
        }

        selected = st.selectbox(
            "Select Blood Request",
            list(request_options.keys())
        )

        if st.button("🔎 Find Matches"):

            request_id = request_options[selected]

            request = execute_query(
                """
                SELECT blood_group
                FROM Blood_Request
                WHERE request_id = %s
                """,
                (request_id,),
                fetch=True
            )

            if request:

                required_group = request[0][0]

                donors = execute_query(
                    """
                    SELECT donor_id, name,
                           blood_group, phone, location
                    FROM Donor
                    WHERE availability = 1
                    AND blood_group = %s
                    ORDER BY donor_id
                    """,
                    (required_group,),
                    fetch=True
                )

                if donors:

                    table_data = []

                    for donor in donors:
                        table_data.append({
                            "Donor ID": donor[0],
                            "Name": donor[1],
                            "Blood Group": donor[2],
                            "Phone": donor[3],
                            "Location": donor[4]
                        })

                    st.dataframe(
                        table_data,
                        use_container_width=True,
                        hide_index=True
                    )

                    st.success(
                        f"Found {len(donors)} available donor(s) "
                        f"with blood group {required_group}."
                    )

                else:
                    st.warning(
                        f"No available donors with blood group "
                        f"{required_group} were found."
                    )

    else:
        st.info("No blood requests available.")


# =========================================================
# RECORD DONATION
# =========================================================

elif page == "Record Donation":

    st.title("Record Donation")

    with st.form("donation_form"):

        donor_id = st.number_input(
            "Donor ID",
            min_value=1,
            step=1
        )

        request_id = st.number_input(
            "Request ID",
            min_value=1,
            step=1
        )

        units = st.number_input(
            "Units Donated",
            min_value=1,
            step=1
        )

        submitted = st.form_submit_button(
            "Record Donation"
        )

        if submitted:

            donor_exists = execute_query(
                """
                SELECT donor_id
                FROM Donor
                WHERE donor_id = %s
                """,
                (donor_id,),
                fetch=True
            )

            request_exists = execute_query(
                """
                SELECT request_id
                FROM Blood_Request
                WHERE request_id = %s
                """,
                (request_id,),
                fetch=True
            )

            if not donor_exists:
                st.error("That Donor ID does not exist.")

            elif not request_exists:
                st.error("That Request ID does not exist.")

            else:

                result = execute_query(
                    """
                    SELECT COALESCE(MAX(donation_id), 0) + 1
                    FROM Donation
                    """,
                    fetch=True
                )

                donation_id = result[0][0]

                success = execute_query(
                    """
                    INSERT INTO Donation
                    (
                        donation_id,
                        donor_id,
                        request_id,
                        donation_date,
                        units_donated
                    )
                    VALUES
                    (%s, %s, %s, CURDATE(), %s)
                    """,
                    (
                        donation_id,
                        donor_id,
                        request_id,
                        units
                    )
                )

                if success:
                    st.success(
                        f"Donation recorded successfully! "
                        f"Donation ID: {donation_id}"
                    )


# =========================================================
# REPORTS
# =========================================================

elif page == "Reports":

    st.title("Reports & Statistics")

    total_donors = execute_query(
        "SELECT COUNT(*) FROM Donor",
        fetch=True
    )[0][0]

    available_donors = execute_query(
        "SELECT COUNT(*) FROM Donor WHERE availability = 1",
        fetch=True
    )[0][0]

    total_donations = execute_query(
        "SELECT COUNT(*) FROM Donation",
        fetch=True
    )[0][0]

    total_requests = execute_query(
        "SELECT COUNT(*) FROM Blood_Request",
        fetch=True
    )[0][0]

    pending_requests = execute_query(
        """
        SELECT COUNT(*)
        FROM Blood_Request
        WHERE status = 'Pending'
        """,
        fetch=True
    )[0][0]

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Donors", total_donors)
    c2.metric("Available Donors", available_donors)
    c3.metric("Total Donations", total_donations)

    c4, c5 = st.columns(2)

    c4.metric("Total Requests", total_requests)
    c5.metric("Pending Requests", pending_requests)

    st.divider()

    st.subheader("Donors by Blood Group")

    blood_data = execute_query(
        """
        SELECT blood_group, COUNT(*)
        FROM Donor
        GROUP BY blood_group
        ORDER BY blood_group
        """,
        fetch=True
    )

    if blood_data:
        st.bar_chart(
            {
                row[0]: row[1]
                for row in blood_data
            }
        )

    st.subheader("Requests by Status")

    status_data = execute_query(
        """
        SELECT status, COUNT(*)
        FROM Blood_Request
        GROUP BY status
        ORDER BY status
        """,
        fetch=True
    )

    if status_data:

        for status, count in status_data:
            st.write(f"**{status}:** {count} request(s)")


# =========================================================
# ABOUT
# =========================================================

elif page == "About":

    st.title("About Blood Emergency Link")

    st.subheader("Project Overview")

    st.write(
        """
        Blood Emergency Link is a database-driven application
        designed to help manage blood donors and blood requests.
        """
    )

    st.subheader("Objective")

    st.write(
        """
        To organize donor information, record blood requests,
        identify potential donors by blood group, and maintain
        donation records in one system.
        """
    )

    st.subheader("Key Features")

    st.write("""
    - Donor Registration and Management
    - Search Available Donors
    - Submit and Manage Blood Requests
    - Match Requests with Potential Donors
    - Record Donations
    - Reports and Statistics
    """)

    st.subheader("Technologies")

    st.write(
        "Python | Streamlit | MySQL | Aiven Cloud Database"
    )

    st.info(
        "Actual blood transfusions require verification by qualified "
        "medical professionals."
    )
