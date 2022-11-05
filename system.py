class School:
   def __init__(self):
    self.username="aziz"
    self.password = "1234"


   def __str__(self):
      print("Class of a school system") 


   def change_password(self):
    password = input("Enter old password: ")
    if password == self.password:
        password1 = input("Enter new password: ")
        password2 = input("Re-Enter new password: ")
        if password1 !=password2:
            print("Passwords do not match")
            return self.change_password()
        else:
            password = password2    
            self.password = password
            print("Password succesfully changed")

    else:
        print("Your Password in incorrect")   
        return self.change_password()
   
        


   def read_credentials(self):
    print("Your username is :", self.username)
    print("Your password is :", self.password)


   def enter_courses(self):
    print("Input below the courses you are to offer this semester separating them by comma")
    courses = input("")
    courses = courses.replace(",","\n")
    with open("student_courses.txt" , "w") as file:
        file.write(courses)


   def add_courses(self):
    print("Input below the courses you want to add separating them by comma")
    courses1 = input("")
    courses1 = courses1.replace(",","\n")
    with open("student_courses.txt" , "a") as file:
        file.write("\n")
        file.write(courses1)
    


   def view_courses(self):
    with open("student_courses.txt", "r") as file:
        data = file.read().splitlines()
        for line in data:
            print(line)




