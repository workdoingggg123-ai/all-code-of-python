import random , string

class plane_ticket:

  def __init__(self ,fro, to):
    self.fro = fro
    self.to = to


  @staticmethod
  def greet():
    print(f"Welcome for Booking Ticket App")  


  def Show_status(self):
    self.plane_no  = ''.join(random.choices(string.ascii_uppercase, k=2)) + str(random.randint(100,999))
    self.bording_pass =''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    self.seat_type = random.choice(["Economy", "Business"])
    seat_no = str(random.randint(1, 9)) + random.choice(string.ascii_uppercase)
    self.choose = self.seat_type + " " + seat_no
    self.company = random.choice(["AIRBUS" , 'INDIGO', 'AIRINDIA', 'EMIRATES', 'LUFSTANCES','AIRFRANCE'])


    print("=========================\nTHE TICKET BOOKED\n==========================")
    print(f"From -----> {self.fro}\nTo -----> {self.to}")
    print(f"In plane -----> {self.company}")
    print(f"Plane No -----> {self.plane_no}\nBoarding Pass -----> {self.bording_pass}")
    print(f"Seat -----> {self.choose}")

    
  def Ticker_fare(self):
    if self.seat_type =="Business":
     self.Ticket_fare  = random.randint(6000,15000)  
    else:
      self.Ticket_fare = random.randint(1000,5000) 
   
    print(f"The Ticker Fare from {self.fro} to {self.to} is {self.Ticket_fare} ₹")


BY = input("GIVE THE AIRPORT NAME TO BOARD : ")
TO = input("GIVE THE DRSTINATION NAME : ")
pa = plane_ticket(BY , TO)
pa.greet()
pa.Show_status()
pa.Ticker_fare()