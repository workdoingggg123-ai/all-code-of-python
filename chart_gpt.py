# -------------------------------------------------------------
# FULL INVENTORY MANAGEMENT SYSTEM
# -------------------------------------------------------------

import sqlite3, datetime, os, sys
import pandas as pd, qrcode
from colorama import init, Fore, Style
import matplotlib.pyplot as plt
from fpdf import FPDF

init(autoreset=True)

# ---------------- DATABASE SETUP ----------------
DB_NAME = "inventory_system.db"
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# Tables
c.execute('''CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                device_type TEXT,
                brand TEXT,
                price REAL,
                quantity INTEGER
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS sales(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                customer_name TEXT,
                customer_phone TEXT,
                quantity INTEGER,
                total_price REAL,
                discount REAL,
                date_time TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT UNIQUE,
                loyalty_points INTEGER DEFAULT 0
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )''')
conn.commit()

# ---------------- UTILITY FUNCTIONS ----------------
def print_colored(text, color=Fore.GREEN):
    print(color + text + Style.RESET_ALL)

def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print_colored("Invalid number. Try again.", Fore.RED)

def calculate_discount(price, discount_percent=10, buy_x_get_y=None, quantity=1):
    total = price * quantity
    if buy_x_get_y:
        x, y = buy_x_get_y
        free_units = (quantity // (x + y)) * y
        total -= free_units * price
    return total * (1 - discount_percent / 100)

def backup_db():
    backup_file = f"backup_inventory_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    conn.backup(sqlite3.connect(backup_file))
    print_colored(f"Backup saved to {backup_file}", Fore.CYAN)

def generate_qrcode(item_id, name):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f"ItemID:{item_id}, Name:{name}")
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"qrcode_item_{item_id}.png")

def save_receipt_pdf(sale_id):
    c.execute("SELECT * FROM sales WHERE id=?", (sale_id,))
    sale = c.fetchone()
    c.execute("SELECT * FROM items WHERE id=?", (sale[1],))
    item = c.fetchone()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "PATEL ELECTRONICS RECEIPT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Customer: {sale[2]} | Phone: {sale[3]}", ln=True)
    pdf.cell(0, 10, f"Item: {item[1]} | Brand: {item[3]} | Type: {item[2]}", ln=True)
    pdf.cell(0, 10, f"Quantity: {sale[4]} | Total: ₹{sale[5]:.2f} | Discount: {sale[6]}%", ln=True)
    pdf.cell(0, 10, f"Date: {sale[7]}", ln=True)
    filename = f"receipt_{sale_id}.pdf"
    pdf.output(filename)
    print_colored(f"Receipt saved as {filename}", Fore.CYAN)

# ---------------- AUTHENTICATION ----------------
def login():
    print_colored("LOGIN TO INVENTORY SYSTEM", Fore.YELLOW)
    username = input("Username: ")
    password = input("Password: ")
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    if result:
        print_colored(f"Login successful! Role: {result[0]}", Fore.CYAN)
        return result[0]
    else:
        print_colored("Invalid credentials.", Fore.RED)
        return None

def register_admin():
    c.execute("SELECT * FROM users WHERE role='admin'")
    if not c.fetchone():
        print_colored("No admin found. Creating default admin.", Fore.YELLOW)
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")
        c.execute("INSERT INTO users(username, password, role) VALUES(?,?,?)", (username, password, 'admin'))
        conn.commit()

# ---------------- INVENTORY FUNCTIONS ----------------
def add_item():
    print_colored("ADD NEW ITEM", Fore.YELLOW)
    name = input("Item Name: ").strip()
    device_type = input("Device Type: ").strip()
    brand = input("Brand: ").strip()
    price = float(input("Price: "))
    quantity = input_int("Quantity: ")
    c.execute("INSERT INTO items(name, device_type, brand, price, quantity) VALUES(?,?,?,?,?)",
              (name, device_type, brand, price, quantity))
    conn.commit()
    item_id = c.lastrowid
    generate_qrcode(item_id, name)
    print_colored(f"Item '{name}' added with ID {item_id} and QR code generated.", Fore.GREEN)
    if quantity < 5:
        print_colored(f"⚠️ Low stock warning for {name}!", Fore.RED)
    return ("add", item_id)

def list_items():
    print_colored("LIST INVENTORY", Fore.YELLOW)
    filter_type = input("Filter by device type (Enter for all): ").strip()
    query = "SELECT * FROM items"
    params = ()
    if filter_type:
        query += " WHERE device_type LIKE ?"
        params = (f"%{filter_type}%",)
    c.execute(query, params)
    items = c.fetchall()
    if items:
        for item in items:
            print(f"ID:{item[0]} | Name:{item[1]} | Type:{item[2]} | Brand:{item[3]} | Price:{item[4]} | Qty:{item[5]}")
        print_colored(f"Total items: {len(items)}", Fore.CYAN)
    else:
        print_colored("No items found.", Fore.RED)
    return items

def update_item():
    print_colored("UPDATE ITEM", Fore.YELLOW)
    item_id = input_int("Enter Item ID to update: ")
    c.execute("SELECT * FROM items WHERE id=?", (item_id,))
    old_item = c.fetchone()
    if old_item:
        name = input(f"New Name [{old_item[1]}]: ") or old_item[1]
        device_type = input(f"New Type [{old_item[2]}]: ") or old_item[2]
        brand = input(f"New Brand [{old_item[3]}]: ") or old_item[3]
        price = input(f"New Price [{old_item[4]}]: ") or old_item[4]
        quantity = input(f"New Quantity [{old_item[5]}]: ") or old_item[5]
        c.execute("""UPDATE items SET name=?, device_type=?, brand=?, price=?, quantity=? WHERE id=?""",
                  (name, device_type, brand, float(price), int(quantity), item_id))
        conn.commit()
        print_colored(f"Item {item_id} updated successfully.", Fore.GREEN)
        return ("update", old_item)
    else:
        print_colored("Item not found.", Fore.RED)
        return None

def delete_item():
    print_colored("DELETE ITEM", Fore.YELLOW)
    item_id = input_int("Enter Item ID to delete: ")
    c.execute("SELECT * FROM items WHERE id=?", (item_id,))
    item = c.fetchone()
    if item:
        c.execute("DELETE FROM items WHERE id=?", (item_id,))
        conn.commit()
        print_colored(f"Item {item_id} deleted.", Fore.GREEN)
        return ("delete", item)
    else:
        print_colored("Item not found.", Fore.RED)
        return None

def search_items():
    print_colored("SEARCH ITEM", Fore.YELLOW)
    keyword = input("Enter keyword (name/brand/type): ").strip()
    c.execute("SELECT * FROM items WHERE name LIKE ? OR brand LIKE ? OR device_type LIKE ?",
              (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    items = c.fetchall()
    if items:
        for item in items:
            print(f"ID:{item[0]} | Name:{item[1]} | Type:{item[2]} | Brand:{item[3]} | Price:{item[4]} | Qty:{item[5]}")
    else:
        print_colored("No items found.", Fore.RED)

def sort_items():
    print_colored("SORT ITEMS", Fore.YELLOW)
    option = input("Sort by: 1-Price Low->High 2-Price High->Low 3-Name A->Z 4-Brand A->Z: ").strip()
    if option=="1":
        c.execute("SELECT * FROM items ORDER BY price ASC")
    elif option=="2":
        c.execute("SELECT * FROM items ORDER BY price DESC")
    elif option=="3":
        c.execute("SELECT * FROM items ORDER BY name ASC")
    elif option=="4":
        c.execute("SELECT * FROM items ORDER BY brand ASC")
    else:
        print_colored("Invalid option", Fore.RED)
        return
    items = c.fetchall()
    for item in items:
        print(f"ID:{item[0]} | Name:{item[1]} | Type:{item[2]} | Brand:{item[3]} | Price:{item[4]} | Qty:{item[5]}")

# ---------------- SALES / BILLING ----------------
def sell_item():
    print_colored("SELL ITEM", Fore.YELLOW)
    items = list_items()
    if not items:
        return None
    item_id = input_int("Enter Item ID to sell: ")
    c.execute("SELECT * FROM items WHERE id=?", (item_id,))
    item = c.fetchone()
    if not item:
        print_colored("Item not found.", Fore.RED)
        return None
    quantity = input_int("Quantity to sell: ")
    if quantity > item[5]:
        print_colored("Not enough stock.", Fore.RED)
        return None
    customer_name = input("Customer Name: ").strip()
    customer_phone = input("Customer Phone: ").strip()
    discount = input_int("Discount % (0 if none): ")
    total_price = calculate_discount(item[4], discount, buy_x_get_y=(2,1), quantity=quantity)
    now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    new_qty = item[5] - quantity
    c.execute("UPDATE items SET quantity=? WHERE id=?", (new_qty, item_id))
    c.execute("""INSERT INTO sales(item_id, customer_name, customer_phone, quantity, total_price, discount, date_time)
                 VALUES(?,?,?,?,?,?,?)""", (item_id, customer_name, customer_phone, quantity, total_price, discount, now))
    # Customer loyalty
    c.execute("SELECT * FROM customers WHERE phone=?", (customer_phone,))
    customer = c.fetchone()
    points = int(total_price // 100)
    if customer:
        c.execute("UPDATE customers SET loyalty_points=? WHERE phone=?", (customer[3]+points, customer_phone))
    else:
        c.execute("INSERT INTO customers(name, phone, loyalty_points) VALUES(?,?,?)", (customer_name, customer_phone, points))
    conn.commit()
    sale_id = c.lastrowid
    save_receipt_pdf(sale_id)
    print_colored(f"Sold {quantity} x {item[1]} | Total ₹{total_price:.2f} | Discount {discount}%", Fore.GREEN)
    print_colored(f"Remaining stock: {new_qty}", Fore.CYAN)
    if new_qty < 5:
        print_colored(f"⚠️ Low stock warning for {item[1]}!", Fore.RED)
    return ("sell", sale_id)

# ---------------- REPORTS / DASHBOARD ----------------
def daily_sales_report():
    print_colored("DAILY SALES REPORT", Fore.YELLOW)
    today = datetime.datetime.now().strftime("%d-%m-%Y")
    c.execute("SELECT * FROM sales WHERE date_time LIKE ?", (f"{today}%",))
    sales = c.fetchall()
    if sales:
        for sale in sales:
            print(f"SaleID:{sale[0]} | ItemID:{sale[1]} | Customer:{sale[2]} | Qty:{sale[4]} | Total:₹{sale[5]:.2f} | Discount:{sale[6]}% | Time:{sale[7]}")
        print_colored(f"Total sales today: {len(sales)}", Fore.CYAN)
    else:
        print_colored("No sales today.", Fore.RED)

def analytics_dashboard():
    print_colored("ANALYTICS DASHBOARD", Fore.YELLOW)
    # Stock levels
    c.execute("SELECT name, quantity FROM items")
    data = c.fetchall()
    if data:
        names = [d[0] for d in data]
        qtys = [d[1] for d in data]
        plt.figure(figsize=(10,5))
        plt.bar(names, qtys, color='skyblue')
        plt.xticks(rotation=45)
        plt.ylabel("Quantity")
        plt.title("Stock Levels")
        plt.show()
    # Sales trends
    c.execute("SELECT date_time, total_price FROM sales")
    data = c.fetchall()
    if data:
        dates = [d[0][:10] for d in data]  # extract date
        totals = [d[1] for d in data]
        df = pd.DataFrame({"Date": dates, "Total": totals})
        df_grouped = df.groupby("Date").sum()
        df_grouped.plot(kind='bar', figsize=(10,5), color='orange', legend=False)
        plt.ylabel("Total Sales")
        plt.title("Daily Sales")
        plt.show()

# ---------------- MAIN MENU ----------------
def main_menu(role):
    undo_stack = []
    while True:
        print_colored("\n===== INVENTORY MANAGEMENT MENU =====", Fore.YELLOW)
        print("1. Add Item\n2. Update Item\n3. Delete Item\n4. List Items\n5. Search Items\n6. Sort Items")
        print("7. Sell Item\n8. Daily Sales Report\n9. Analytics Dashboard\n10. Backup\n11. Undo Last Action\n12. Exit")
        choice = input("Enter choice: ").strip()
        match choice:
            case "1":
                result = add_item(); undo_stack.append(result)
            case "2":
                result = update_item(); undo_stack.append(result)
            case "3":
                result = delete_item(); undo_stack.append(result)
            case "4":
                list_items()
            case "5":
                search_items()
            case "6":
                sort_items()
            case "7":
                result = sell_item(); undo_stack.append(result)
            case "8":
                daily_sales_report()
            case "9":
                analytics_dashboard()
            case "10":
                backup_db()
            case "11":
                if undo_stack:
                    action = undo_stack.pop()
                    if action:
                        undo_action(action)
                else:
                    print_colored("Nothing to undo.", Fore.RED)
            case "12":
                print_colored("Exiting system. Goodbye!", Fore.CYAN)
                break
            case _:
                print_colored("Invalid choice, try again.", Fore.RED)

# ---------------- UNDO FUNCTION ----------------
def undo_action(action):
    type_action, data = action
    if type_action=="add":
        c.execute("DELETE FROM items WHERE id=?", (data,))
        conn.commit()
        print_colored(f"Undo: Added item {data} removed.", Fore.MAGENTA)
    elif type_action=="update":
        id = data[0]
        c.execute("""UPDATE items SET name=?, device_type=?, brand=?, price=?, quantity=? WHERE id=?""",
                  (data[1], data[2], data[3], data[4], data[5], id))
        conn.commit()
        print_colored(f"Undo: Update reverted for item {id}.", Fore.MAGENTA)
    elif type_action=="delete":
        c.execute("INSERT INTO items(id,name,device_type,brand,price,quantity) VALUES(?,?,?,?,?,?)", data)
        conn.commit()
        print_colored(f"Undo: Deleted item {data[0]} restored.", Fore.MAGENTA)
    elif type_action=="sell":
        sale_id = data
        c.execute("SELECT * FROM sales WHERE id=?", (sale_id,))
        sale = c.fetchone()
        if sale:
            c.execute("UPDATE items SET quantity=quantity+? WHERE id=?", (sale[4], sale[1]))
            c.execute("DELETE FROM sales WHERE id=?", (sale_id,))
            conn.commit()
            print_colored(f"Undo: Sale {sale_id} reverted.", Fore.MAGENTA)

# ---------------- RUN SYSTEM ----------------
if __name__ == "__main__":
    register_admin()
    role = None
    while not role:
        role = login()
    main_menu(role)