'''
    Python Inventory Management System

    A console-based Inventory Management System where users can add, delete, update, search, and save items — similar to what you are  use in a small shop or warehouse.

    📌 Key Features (and what skills they cover)
    Feature	Python Topics You will Use
    Add / Update / Delete items	Variables, Lists, Dictionaries
    Search items	Loops, Conditional Logic
    Save data to file	File I/O
    Load data from file	File I/O
    Use classes for items	OOP (Classes & Objects)
    Menu navigation	Functions, Control Flow
    Option to sort or filter	Lists & loops'''


print("PATEL ELECTRONIC INVENTORY MANAGMENT SYSTEM")

import ast
import datetime
class inv_mangement:
   
    def add_item(self):
        print("THIS IS CONSOLE TO ADD DATA")

        l1 = []   

        name_item = input("GIVE THE NAME OF THE DEVICE YOU WANT TO ADD : ").upper()
        num_item = int(input("GIVE THE NUMBER OF ITEM YOU WANT TO ADD : "))

        i = 0  
        with open("inventory_patel_electronic.txt", "a") as file:

            while i < num_item:
               self.item_name = input(f"GIVE THE NAME OF {name_item} : ")
               self.item_price = int(input(f"GIVE THE PRICE OF THE {name_item} : "))
               self.brand = input("GIVE THE BRAND NAME : ")
    
               item_dict = {
                    "device_type": name_item,
                    "name": self.item_name,
                    "price": self.item_price,
                    "brand": self.brand
                }

               l1.append(item_dict)
               i += 1

            for item in l1:
                file.write(str(item) + "\n")
            print(F"THE ITEMS IS SUCESSFULLY FETCHED WITH FILES TOTAL ITEM IS {num_item}")    


    def device_list(self, device_type):
      count = 0
    
      with open("inventory_patel_electronic.txt", "r") as file:
          for line in file:
            item = ast.literal_eval(line.strip())  

            if item["device_type"].lower() == device_type.lower():
                print(f"{item["name"]} -- > ₹ {item["price"]} --> brand {item["brand"]}")
                count += 1
 
          print(f"\nTotal {device_type} available: {count}")
    


    def selling_item(self):  
     print("===== THIS IS THE SELLING SITE (PATEL ELECTRONICS) =====\n")
    
     device_type = input("GIVE THE TYPE OF THE DEVICE YOU WANT TO : ")
     brand = input(f"GIVE THE BRAND OF THE {device_type} YOU WANT : ")
    
     count = 0
     matched_items = []
     

     with open("inventory_patel_electronic.txt", "r") as file:
        for line in file:
            item = ast.literal_eval(line.strip())

            if (
                item["device_type"].lower() == device_type.lower()
                and
                item["brand"].lower() == brand.lower()
            ):
                matched_items.append(item)
                count += 1

    # Show matching items
     if count > 0:
        print(f"\nAVAILABLE {device_type.upper()} IN BRAND {brand.upper()}:\n")
        
        for i, product in enumerate(matched_items, start=1):
            print(f"{i}. Model : {product['name']}")
            print(f"   Price : ₹{product['price']}")
            print("-" * 40)

        print(f"\nTotal {device_type} available in brand {brand}: {count}")

        coustomer_choice = input("\nDO YOU WANT TO BUY? (yes/no): ").lower()

        if coustomer_choice == "yes":
            name = input("NAME OF THE BUYER --> ")
            ph_no  = int(input("GIVE THE PHONE NUMBER --> "))
            enter_choice = int(input("GIVE THE NUMBER OF PRODUCT WANT TO BUY : " ))
            selected = matched_items[enter_choice - 1]   

            print("\n----- HERE IS YOUR BILL -----\n")

            now = datetime.datetime.now()
            formatted = now.strftime("%d-%m-%Y %H:%M:%S")
            print(f"NAME          : {name}")
            print(f"PH_NO         : {ph_no}")
            print(f"SELLING TYPE  : {selected['device_type']}")
            print(f"BRAND         : {selected['brand']}")
            print(f"MODEL         : {selected['name']}")
            print(f"PRICE  + (10 % Discount) : Original Price ₹{[selected['price']]} \n After Discount To Pay -->₹ {selected['price'] * 0.1 - selected['price']}")
            print(f"DATE & TIME   : {formatted}")
            print("\nTHANK YOU FOR SHOPPING WITH PATEL ELECTRONICS 🙏")

        else:
         print(f"\nSORRY ❌ No {device_type} available in brand {brand}.")


patel = inv_mangement()                         
menu =  "1: Add Item , 2: List Device , 3: Sell Item , 4: Exit"
print(menu)

choice = input("Enter a number  the choice: ")

match choice:
    case "1":
        print("You entered choice Add item")
        patel.add_item()
    case "2":
        print("You entered choice list device")
        patel.device_list(device_type= input("GIVE THE TYPE OF THE DVICE YOU WANT THE LIST OF -->"))
    case "3":
        print("You entered choice sell item")
        patel.selling_item()
    case "4":  
        print("You entered choice exit")
        print("THANKS FOR VISITING HOPE TO SEE AGIAN")




   


                 

