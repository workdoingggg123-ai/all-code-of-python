import random, string, datetime, json, os
import tkinter as tk
from tkinter import messagebox
from flask import Flask, request
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import mysql.connector

# =========================
# CORE BOOKING CLASS
# =========================

class AirlineSystem:

    total_seats = [f"{r}{c}" for r in range(1,21) for c in "ABCDEF"]
    booked_seats = []

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.booking_id = ''.join(random.choices(string.ascii_uppercase+string.digits,k=8))
        self.date = str(datetime.date.today() + datetime.timedelta(days=random.randint(1,30)))
        self.passengers = []
        self.status = "CONFIRMED"
        self.total_fare = 0

    # -------------------------
    # PASSENGERS
    # -------------------------
    def add_passenger(self, name, age, gender):
        self.passengers.append({"name":name,"age":age,"gender":gender})

    # -------------------------
    # SEAT SELECTION
    # -------------------------
    def select_seat(self, seat, passenger_index):
        if seat in AirlineSystem.total_seats and seat not in AirlineSystem.booked_seats:
            AirlineSystem.booked_seats.append(seat)
            self.passengers[passenger_index]["seat"] = seat
        else:
            raise Exception("Seat Not Available")

    # -------------------------
    # FARE CALCULATION
    # -------------------------
    def calculate_fare(self):
        self.total_fare = len(self.passengers) * random.randint(3000,8000)

    # -------------------------
    # PAYMENT
    # -------------------------
    def payment(self, method):
        self.payment_method = method
        self.payment_status = "PAID"

    # -------------------------
    # SAVE TO FILE
    # -------------------------
    def save_to_file(self):
        data = self.__dict__
        with open("bookings.json","a") as f:
            f.write(json.dumps(data)+"\n")

    # -------------------------
    # SAVE TO DATABASE
    # -------------------------
    def save_to_db(self):
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="yourpassword",
                database="airline"
            )
            cursor = db.cursor()
            query = "INSERT INTO bookings (booking_id, source, destination, fare, status) VALUES (%s,%s,%s,%s,%s)"
            values = (self.booking_id,self.source,self.destination,self.total_fare,self.status)
            cursor.execute(query,values)
            db.commit()
        except:
            print("Database Not Connected")

    # -------------------------
    # PDF GENERATOR
    # -------------------------
    def generate_pdf(self):
        file_name = f"{self.booking_id}.pdf"
        doc = SimpleDocTemplate(file_name)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("AIRLINE TICKET", styles["Title"]))
        elements.append(Spacer(1,12))
        elements.append(Paragraph(f"Booking ID: {self.booking_id}", styles["Normal"]))
        elements.append(Paragraph(f"Route: {self.source} -> {self.destination}", styles["Normal"]))
        elements.append(Paragraph(f"Date: {self.date}", styles["Normal"]))
        elements.append(Paragraph(f"Fare: {self.total_fare} ₹", styles["Normal"]))
        elements.append(Paragraph(f"Status: {self.status}", styles["Normal"]))

        for p in self.passengers:
            elements.append(Paragraph(str(p), styles["Normal"]))

        doc.build(elements)

# =========================
# ADMIN PANEL
# =========================

def admin_panel():
    password = input("Enter Admin Password: ")
    if password == "admin123":
        print("\n--- BOOKINGS DATA ---")
        if os.path.exists("bookings.json"):
            with open("bookings.json","r") as f:
                print(f.read())
        else:
            print("No Data Found")
    else:
        print("Wrong Password")

# =========================
# GUI VERSION
# =========================

def launch_gui():
    def book():
        source = entry_from.get()
        dest = entry_to.get()
        name = entry_name.get()

        system = AirlineSystem(source,dest)
        system.add_passenger(name,25,"Male")
        system.select_seat("1A",0)
        system.calculate_fare()
        system.payment("UPI")
        system.save_to_file()
        system.generate_pdf()

        messagebox.showinfo("Success",f"Ticket Booked\nID: {system.booking_id}")

    root = tk.Tk()
    root.title("Airline Booking GUI")
    root.geometry("400x400")

    tk.Label(root,text="From").pack()
    entry_from = tk.Entry(root)
    entry_from.pack()

    tk.Label(root,text="To").pack()
    entry_to = tk.Entry(root)
    entry_to.pack()

    tk.Label(root,text="Name").pack()
    entry_name = tk.Entry(root)
    entry_name.pack()

    tk.Button(root,text="Book Ticket",command=book).pack(pady=20)

    root.mainloop()

# =========================
# FLASK WEB APP
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <h2>Airline Booking</h2>
    <form method="post" action="/book">
    Name:<input name="name"><br>
    From:<input name="from"><br>
    To:<input name="to"><br>
    <button type="submit">Book</button>
    </form>
    '''

@app.route("/book",methods=["POST"])
def book_ticket():
    name = request.form["name"]
    source = request.form["from"]
    dest = request.form["to"]

    system = AirlineSystem(source,dest)
    system.add_passenger(name,30,"Male")
    system.select_seat("2B",0)
    system.calculate_fare()
    system.payment("CARD")
    system.save_to_file()
    system.generate_pdf()

    return f"Ticket Booked Successfully! Booking ID: {system.booking_id}"

# =========================
# ANALYTICS DASHBOARD
# =========================

def analytics():
    total = 0
    if os.path.exists("bookings.json"):
        with open("bookings.json","r") as f:
            for line in f:
                data = json.loads(line)
                total += data["total_fare"]
    print("Total Revenue:", total)

# =========================
# MAIN MENU
# =========================

if __name__ == "__main__":

    while True:
        print("\n1. Console Booking")
        print("2. Admin Panel")
        print("3. Launch GUI")
        print("4. Run Web App")
        print("5. Analytics")
        print("6. Exit")

        choice = input("Choose Option: ")

        if choice == "1":
            s = input("From: ")
            d = input("To: ")
            system = AirlineSystem(s,d)

            count = int(input("Passengers: "))
            for i in range(count):
                n = input("Name: ")
                a = input("Age: ")
                g = input("Gender: ")
                system.add_passenger(n,a,g)
                seat = input("Seat: ")
                system.select_seat(seat,i)

            system.calculate_fare()
            system.payment("UPI")
            system.save_to_file()
            system.save_to_db()
            system.generate_pdf()

            print("Booking Completed! ID:",system.booking_id)

        elif choice == "2":
            admin_panel()

        elif choice == "3":
            launch_gui()

        elif choice == "4":
            app.run(debug=True)

        elif choice == "5":
            analytics()

        elif choice == "6":
            break