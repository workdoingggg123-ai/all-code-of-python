class Father:
    print("This is the father class attribute")

    def __init__(self, name, relation , father_age ):
        self.name = name
        self.relation = relation
        self.father_age = father_age
        


    def show_relation(self):
        print(f"The name is {self.name} and the relation is {self.relation}")


class Child(Father):
    print("This is the child class")

    def __init__(self, name, relation , father_age , child_age):
        super().__init__(name , relation , father_age )
        self.child_age = child_age
        
        

    def show_child(self):
        
        print(f" The name is {self.name} na d the name is {self.relation} and the age of the father is  {self.father_age }and the age of the child is {self.child_age}")


son = Child("Meet", "Son" , 40 , 18)
papa = Father("Bhavesh", "Father" ,40 )

papa.show_relation()
son.show_relation()
son.show_child()