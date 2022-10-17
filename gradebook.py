'''
A user may enter the following commands with any form of capitalization.
Quit: Quits the function
Edit Grade: Will edit the grade of a student's assignment within the class file. If there is a no student, a condition statement is displayed. 
Input Grades: Will ask for an assignment and the grade of each student.
Print Student: Will ask for a student's first and last name and print out their assignment scores, percent grade, and letter grade.
Print Class: Will print out every student's name along with their percentage and letter grade.
'''

file_name = open('gradebook.txt', 'r')
#numerating lines
line0=file_name.readlines(1) #title
line1=file_name.readlines(1) #name
line2=file_name.readlines(1) #weight
line3=file_name.readlines(1) #max score
line4=file_name.readlines() #data
List = open('gradebook.txt').readlines()

#this is to split each line at the comma
for i in line0:
  line0 = i.strip('\n').split(",")
for i in line1:
  line1 = i.strip('\n').split(",")
for i in line2:
  line2 = i.strip('\n').split(",")
for i in line3:
  line3 = i.strip('\n').split(",")
# making list of weights
weights = []
for i in line2:
  if i.isdigit():
    weights.append(int(i))

#making list of max scores
max_scores = []
for i in line3:
  if i.isdigit():
    max_scores.append(int(i))
line0_s=str(line0)   #title
line1_s=str(line1)  #name
line2_s=str(line2) #weight
line3_s=str(line3) #max score
line4_s=str(line4) #data

#generaliziation of student names: for all numbers of students
student_names = []
all_student_names = []
count = 0
for i in line4:                #Collection of student names and coressponding scores
  student_names.append((i.strip(' ').split(","))[:2])
  student = student_names[count]
  student[0], student[1] = student[1], student[0]
  student = ' '.join(student).strip()
  all_student_names.append(student)
  count += 1

# Find total assignment numbers
counter = 0
for i in range(len(line3)):
  if line3[i].isdigit():
    counter += 1
total_assignments=counter
#find total students
counter = 0
for i in range(len(line4_s)):
  if line4_s[i] == "'":
    counter += 1

total_students=counter/2
total_students=int(total_students) #turns string to int
def update_grade_book(grade_book, file_name, assignments, weights, max_scores): # Updating Gradebook file with new values and averages from edit

  grades = open(file_name).readlines()

  grades[0] = 'MCS 260 Gradebook Fall 2022\n'
  grades[1] = f"Last Name, First Name, {', '.join([str(w) for w in list(assignments)])}, Percent Grade, Letter Grade\n"
  grades[2] = f"Weights, {', '.join([str(w) for w in list(weights)])}\n"
  grades[3] = f"Max, Scores, {', '.join([str(w) for w in list(max_scores)])}\n"
  
  counter = 4
  for key in grade_book:
    student_scores = []
    for k in grade_book[key].values():
      student_scores.append(k)
    grades[counter] = f"{(key.split())[1]}, {(key.split())[0]}, {', '.join([str(w) for w in list(student_scores)])}, {percent_grade(weights, max_scores, student_scores)}, {letter_grade(percent_grade(weights, max_scores, student_scores))}\n"    #writing lines to grades data
    counter += 1

  with open(file_name, 'w') as file:
    file.writelines(grades) #Writing lines to file
    file.close() #Closing file
    
def letter_grade(curve):     # Defining letter grades
  if curve <= 59.0:                #proper grading scale 
    return 'F'     
  elif curve >= 60.0 and curve <= 69.0:          
    return 'D'      
  elif curve >= 70.0 and curve <= 79.0:          
    return 'C'      
  elif curve >= 80.0 and curve <= 89.0:          
    return 'B'      
  elif curve >= 90.0 and curve <= 100.0:          
    return 'A'      
  else:          
    return 'Undefined' 

#collects assignment names into a list
assignments = line1[2:total_assignments+2]
#collects students scores 
all_student_scores = []
for i in line4:
  all_student_scores.append(dict(zip(assignments, i.strip('\n').split(",")[2:7])))

for i in all_student_scores:
  for j in i:
    i[j] = int(i[j])

#percent grade function should now work
#Defining a Percent grade function
def percent_grade(weights, max_scores, scores):
  # Function turns values of weights and scores  and averages for % grade
  numerator = 0
  denominator = 0
  for i in range(len(scores)):  #Formulate Percent grade Equation
    #add each term in the numerator and denominator
    numerator += float(weights[i])*(float(scores[i])/int(max_scores[i]))
    denominator += weights[i]
  percent_grade = (numerator/denominator)*100.0
  return round(percent_grade, 2) #This rounds percent grade to two decimal places
  
grade_book = dict(zip(all_student_names, all_student_scores)) #This combines the lists of student names and student scores into a dictionary


command = input('Enter command: ')    #.lower for case sensitivity
def command_line(command): #This is a recursive function which processes the command
  if command.lower() == 'quit': # saying that if the function  equal quit it will quit and update gradebook
    update_grade_book(grade_book, 'gradebook.txt',assignments, weights, max_scores)     #calling function to update file
    quit() # exit
  # Conditional Statements for commands 
  elif command.lower() == 'edit grade': # For editing grades - .lower allows for case sensitivity accommodation 
    first_name = input('First Name: ')  # For naming + conditions for name
    last_name = input('Last Name: ')
    student_name = first_name + ' ' + last_name
    if student_name in grade_book.keys():    
      assignment_name = input('Assignment Name: ')    # Input for assignment names and conditions for assignment
      if assignment_name in grade_book[student_name].keys():    
        grade = input('Grade: ')
        grade_book[student_name][assignment_name] = grade
        command = input('Enter command:')
        return command_line(command)
      else:  # Statements for No Assignment w name
        print('There is no assignment with this name.')
        command = input('Enter command:')
        return command_line(command)
    else:
      print('There is no student with this name.') #statements for No student w name
      command = input('Enter command:')
      return command_line(command)
  #For input of grades with proper inputs
  elif command.lower() == 'input grades': #inputting of grades for an assignment and storing it in gradebook
    assignment_name = input('Assignment Name:')
    for i in grade_book.keys():
      if assignment_name in grade_book[i].keys():
        grade_book[i][assignment_name] = input(i + ': ')
    command = input('Enter command:')
    command_line(command)

  #printing students gradebook
  elif command.lower() == 'print student':
    first_name = input('First Name:') 
    last_name = input('Last Name:')
    student_name = first_name + ' ' + last_name
    if student_name in grade_book.keys(): 
      student_scores = []
      for i, j in grade_book[student_name].items(): #j is value, i is keys
        student_scores.append(j)
        print(f"{i}: {j}")
      #Calling percent_grade function and letter_grade function
      percent = percent_grade(weights, max_scores, student_scores) #print letter grade and percentage
      grade = letter_grade(percent)
      print(f"Percent Grade: {percent}%")
      print(f"Letter Grade: {grade}")
      command = input('Enter command:')
      command_line(command)
    else:
      print('There is no student with this name.')
      command = input('Enter command:')
  elif command.lower() == 'print class':
    for i in grade_book:
      student_scores = []
      for j, k in grade_book[i].items():
        student_scores.append(k)
      print (f"{(i.split())[1]}, {(i.split())[0]}: {percent_grade(weights, max_scores, student_scores)}% {letter_grade(percent_grade(weights, max_scores, student_scores))}") #This prints the last name, first names, percent grade, and letter grade
    command = input('Enter command:')
    command_line(command)

  else:
    print('Please enter one of the following: Quit, Edit Grade, Input Grades, Print Student, Print Class') #condition statements for commands
    command = input('Enter command:')
    command_line(command)

command_line(command)
    
