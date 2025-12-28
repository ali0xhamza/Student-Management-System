import json
import os
from datetime import datetime
import re

class Student:
    def __init__(self, student_id, name, age, email, phone, course, grade=None):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.email = email
        self.phone = phone
        self.course = course
        self.grade = grade
        self.enrollment_date = datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'course': self.course,
            'grade': self.grade,
            'enrollment_date': self.enrollment_date
        }
    
    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Course: {self.course}, Grade: {self.grade if self.grade else 'Not Assigned'}"

class StudentManagementSystem:
    def __init__(self, data_file='students_data.json'):
        self.data_file = data_file
        self.students = self.load_data()
    
    def load_data(self):
        """Load student data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    # Convert dictionary back to Student objects
                    students = {}
                    for sid, student_data in data.items():
                        students[sid] = Student(
                            student_data['student_id'],
                            student_data['name'],
                            student_data['age'],
                            student_data['email'],
                            student_data['phone'],
                            student_data['course'],
                            student_data['grade']
                        )
                    return students
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def save_data(self):
        """Save student data to JSON file"""
        data = {sid: student.to_dict() for sid, student in self.students.items()}
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=4)
    
    def generate_student_id(self):
        """Generate a unique student ID"""
        if not self.students:
            return "STU001"
        
        # Find the highest student ID
        max_id = 0
        for sid in self.students.keys():
            num = int(sid[3:])  # Extract numeric part after 'STU'
            if num > max_id:
                max_id = num
        
        new_id = max_id + 1
        return f"STU{new_id:03d}"
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Validate phone number format"""
        pattern = r'^\+?[0-9]{10,15}$'
        return re.match(pattern, phone) is not None
    
    def add_student(self):
        """Add a new student to the system"""
        print("\n" + "="*50)
        print("ADD NEW STUDENT")
        print("="*50)
        
        # Generate student ID
        student_id = self.generate_student_id()
        
        # Get student details
        name = input("Enter student name: ").strip()
        while not name:
            print("Name cannot be empty!")
            name = input("Enter student name: ").strip()
        
        age = input("Enter student age: ").strip()
        while not age.isdigit() or int(age) < 5 or int(age) > 100:
            print("Age must be a number between 5 and 100!")
            age = input("Enter student age: ").strip()
        
        email = input("Enter student email: ").strip()
        while not self.validate_email(email):
            print("Invalid email format! Please enter a valid email.")
            email = input("Enter student email: ").strip()
        
        phone = input("Enter student phone number: ").strip()
        while not self.validate_phone(phone):
            print("Invalid phone number! Please enter 10-15 digits.")
            phone = input("Enter student phone number: ").strip()
        
        course = input("Enter course name: ").strip()
        while not course:
            print("Course cannot be empty!")
            course = input("Enter course name: ").strip()
        
        # Create new student object
        student = Student(student_id, name, int(age), email, phone, course)
        self.students[student_id] = student
        self.save_data()
        
        print(f"\n✅ Student added successfully!")
        print(f"Student ID: {student_id}")
        print(f"Name: {name}")
        print(f"Course: {course}")
    
    def view_all_students(self):
        """Display all students"""
        print("\n" + "="*50)
        print("ALL STUDENTS")
        print("="*50)
        
        if not self.students:
            print("No students found in the system.")
            return
        
        print(f"Total Students: {len(self.students)}\n")
        for student in self.students.values():
            print(f"{student}")
            print(f"  Age: {student.age}, Email: {student.email}")
            print(f"  Phone: {student.phone}, Enrolled: {student.enrollment_date}")
            print("-" * 30)
    
    def search_student(self):
        """Search for a student by ID or name"""
        print("\n" + "="*50)
        print("SEARCH STUDENT")
        print("="*50)
        
        search_term = input("Enter student ID or name to search: ").strip().lower()
        
        if not search_term:
            print("Search term cannot be empty!")
            return
        
        results = []
        for student in self.students.values():
            if (search_term in student.student_id.lower() or 
                search_term in student.name.lower()):
                results.append(student)
        
        if results:
            print(f"\nFound {len(results)} matching student(s):\n")
            for student in results:
                print(f"{student}")
                print(f"  Age: {student.age}, Email: {student.email}")
                print(f"  Phone: {student.phone}, Course: {student.course}")
                print(f"  Grade: {student.grade if student.grade else 'Not Assigned'}")
                print("-" * 30)
        else:
            print("No students found matching your search.")
    
    def update_student(self):
        """Update student information"""
        print("\n" + "="*50)
        print("UPDATE STUDENT INFORMATION")
        print("="*50)
        
        student_id = input("Enter student ID to update: ").strip().upper()
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found!")
            return
        
        student = self.students[student_id]
        
        print(f"\nCurrent information for {student.name}:")
        print(f"1. Name: {student.name}")
        print(f"2. Age: {student.age}")
        print(f"3. Email: {student.email}")
        print(f"4. Phone: {student.phone}")
        print(f"5. Course: {student.course}")
        print(f"6. Grade: {student.grade if student.grade else 'Not Assigned'}")
        
        try:
            choice = int(input("\nSelect field to update (1-6) or 0 to cancel: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            return
        
        if choice == 0:
            print("Update cancelled.")
            return
        
        if choice == 1:
            new_name = input("Enter new name: ").strip()
            while not new_name:
                print("Name cannot be empty!")
                new_name = input("Enter new name: ").strip()
            student.name = new_name
            print("Name updated successfully!")
        
        elif choice == 2:
            new_age = input("Enter new age: ").strip()
            while not new_age.isdigit() or int(new_age) < 5 or int(new_age) > 100:
                print("Age must be a number between 5 and 100!")
                new_age = input("Enter new age: ").strip()
            student.age = int(new_age)
            print("Age updated successfully!")
        
        elif choice == 3:
            new_email = input("Enter new email: ").strip()
            while not self.validate_email(new_email):
                print("Invalid email format! Please enter a valid email.")
                new_email = input("Enter new email: ").strip()
            student.email = new_email
            print("Email updated successfully!")
        
        elif choice == 4:
            new_phone = input("Enter new phone number: ").strip()
            while not self.validate_phone(new_phone):
                print("Invalid phone number! Please enter 10-15 digits.")
                new_phone = input("Enter new phone number: ").strip()
            student.phone = new_phone
            print("Phone number updated successfully!")
        
        elif choice == 5:
            new_course = input("Enter new course: ").strip()
            while not new_course:
                print("Course cannot be empty!")
                new_course = input("Enter new course: ").strip()
            student.course = new_course
            print("Course updated successfully!")
        
        elif choice == 6:
            new_grade = input("Enter new grade (A, B, C, D, F or leave empty): ").strip().upper()
            if new_grade and new_grade in ['A', 'B', 'C', 'D', 'F']:
                student.grade = new_grade
                print("Grade updated successfully!")
            elif new_grade == '':
                student.grade = None
                print("Grade cleared successfully!")
            else:
                print("Invalid grade! Please enter A, B, C, D, or F.")
                return
        
        else:
            print("Invalid choice!")
            return
        
        self.save_data()
    
    def delete_student(self):
        """Delete a student from the system"""
        print("\n" + "="*50)
        print("DELETE STUDENT")
        print("="*50)
        
        student_id = input("Enter student ID to delete: ").strip().upper()
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found!")
            return
        
        student = self.students[student_id]
        
        print(f"\nAre you sure you want to delete the following student?")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Course: {student.course}")
        
        confirmation = input("\nType 'YES' to confirm deletion: ").strip().upper()
        
        if confirmation == 'YES':
            del self.students[student_id]
            self.save_data()
            print(f"✅ Student {student_id} deleted successfully!")
        else:
            print("Deletion cancelled.")
    
    def assign_grade(self):
        """Assign or update grade for a student"""
        print("\n" + "="*50)
        print("ASSIGN GRADE TO STUDENT")
        print("="*50)
        
        student_id = input("Enter student ID: ").strip().upper()
        
        if student_id not in self.students:
            print(f"Student with ID {student_id} not found!")
            return
        
        student = self.students[student_id]
        
        print(f"\nStudent: {student.name}")
        print(f"Current Grade: {student.grade if student.grade else 'Not Assigned'}")
        
        grade = input("Enter grade (A, B, C, D, F or leave empty to clear): ").strip().upper()
        
        if grade and grade in ['A', 'B', 'C', 'D', 'F']:
            student.grade = grade
            self.save_data()
            print(f"✅ Grade {grade} assigned to {student.name} successfully!")
        elif grade == '':
            student.grade = None
            self.save_data()
            print(f"✅ Grade cleared for {student.name}!")
        else:
            print("Invalid grade! Please enter A, B, C, D, or F.")
    
    def generate_report(self):
        """Generate various reports"""
        print("\n" + "="*50)
        print("GENERATE REPORTS")
        print("="*50)
        
        print("1. Students by Course")
        print("2. Students by Grade")
        print("3. Students without Grades")
        print("4. Overall Statistics")
        
        try:
            choice = int(input("\nSelect report type (1-4): "))
        except ValueError:
            print("Invalid input!")
            return
        
        if choice == 1:
            self.report_by_course()
        elif choice == 2:
            self.report_by_grade()
        elif choice == 3:
            self.report_without_grades()
        elif choice == 4:
            self.report_statistics()
        else:
            print("Invalid choice!")
    
    def report_by_course(self):
        """Generate report grouped by course"""
        courses = {}
        for student in self.students.values():
            course = student.course
            if course not in courses:
                courses[course] = []
            courses[course].append(student)
        
        print("\n" + "="*50)
        print("STUDENTS BY COURSE")
        print("="*50)
        
        for course, students in courses.items():
            print(f"\n📚 {course} ({len(students)} students):")
            for student in students:
                print(f"  • {student.name} (ID: {student.student_id}, Grade: {student.grade if student.grade else 'N/A'})")
    
    def report_by_grade(self):
        """Generate report grouped by grade"""
        grades = {'A': [], 'B': [], 'C': [], 'D': [], 'F': [], 'No Grade': []}
        
        for student in self.students.values():
            if student.grade:
                grades[student.grade].append(student)
            else:
                grades['No Grade'].append(student)
        
        print("\n" + "="*50)
        print("STUDENTS BY GRADE")
        print("="*50)
        
        for grade, students in grades.items():
            if students:
                print(f"\n📊 Grade {grade} ({len(students)} students):")
                for student in students:
                    print(f"  • {student.name} (ID: {student.student_id}, Course: {student.course})")
    
    def report_without_grades(self):
        """List students without grades"""
        students_without_grades = [s for s in self.students.values() if not s.grade]
        
        print("\n" + "="*50)
        print("STUDENTS WITHOUT GRADES")
        print("="*50)
        
        if students_without_grades:
            print(f"Total: {len(students_without_grades)} students\n")
            for student in students_without_grades:
                print(f"  • {student.name} (ID: {student.student_id}, Course: {student.course})")
        else:
            print("All students have grades assigned!")
    
    def report_statistics(self):
        """Generate overall statistics"""
        print("\n" + "="*50)
        print("SYSTEM STATISTICS")
        print("="*50)
        
        total_students = len(self.students)
        
        if total_students == 0:
            print("No students in the system.")
            return
        
        # Age statistics
        ages = [s.age for s in self.students.values()]
        avg_age = sum(ages) / len(ages)
        
        # Grade statistics
        grades = [s.grade for s in self.students.values() if s.grade]
        grade_count = len(grades)
        
        # Course statistics
        courses = {}
        for student in self.students.values():
            if student.course in courses:
                courses[student.course] += 1
            else:
                courses[student.course] = 1
        
        print(f"Total Students: {total_students}")
        print(f"Average Age: {avg_age:.1f} years")
        print(f"Students with Grades: {grade_count}/{total_students}")
        print(f"Students without Grades: {total_students - grade_count}/{total_students}")
        
        print("\n📈 Course Distribution:")
        for course, count in courses.items():
            percentage = (count / total_students) * 100
            print(f"  {course}: {count} students ({percentage:.1f}%)")
    
    def export_to_file(self):
        """Export student data to a text file"""
        filename = input("Enter filename to export (without extension): ").strip()
        if not filename:
            filename = f"students_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filename += ".txt"
        
        try:
            with open(filename, 'w') as file:
                file.write("="*60 + "\n")
                file.write("STUDENT MANAGEMENT SYSTEM - EXPORT\n")
                file.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("="*60 + "\n\n")
                
                file.write(f"Total Students: {len(self.students)}\n\n")
                
                for student in self.students.values():
                    file.write(f"Student ID: {student.student_id}\n")
                    file.write(f"Name: {student.name}\n")
                    file.write(f"Age: {student.age}\n")
                    file.write(f"Email: {student.email}\n")
                    file.write(f"Phone: {student.phone}\n")
                    file.write(f"Course: {student.course}\n")
                    file.write(f"Grade: {student.grade if student.grade else 'Not Assigned'}\n")
                    file.write(f"Enrollment Date: {student.enrollment_date}\n")
                    file.write("-"*40 + "\n\n")
            
            print(f"✅ Data exported successfully to '{filename}'!")
        
        except Exception as e:
            print(f"Error exporting data: {e}")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("STUDENT MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student Information")
        print("5. Delete Student")
        print("6. Assign Grade to Student")
        print("7. Generate Reports")
        print("8. Export Data to File")
        print("9. System Statistics")
        print("0. Exit")
        print("="*50)
    
    def run(self):
        """Main program loop"""
        print("\n" + "="*50)
        print("WELCOME TO STUDENT MANAGEMENT SYSTEM")
        print("="*50)
        print(f"Loaded {len(self.students)} student(s) from database.")
        
        while True:
            self.display_menu()
            
            try:
                choice = int(input("\nEnter your choice (0-9): "))
            except ValueError:
                print("Invalid input! Please enter a number between 0 and 9.")
                continue
            
            if choice == 0:
                print("\nThank you for using Student Management System!")
                print("Goodbye!")
                break
            
            elif choice == 1:
                self.add_student()
            
            elif choice == 2:
                self.view_all_students()
            
            elif choice == 3:
                self.search_student()
            
            elif choice == 4:
                self.update_student()
            
            elif choice == 5:
                self.delete_student()
            
            elif choice == 6:
                self.assign_grade()
            
            elif choice == 7:
                self.generate_report()
            
            elif choice == 8:
                self.export_to_file()
            
            elif choice == 9:
                self.report_statistics()
            
            else:
                print("Invalid choice! Please enter a number between 0 and 9.")
            
            input("\nPress Enter to continue...")

# Main program
if __name__ == "__main__":
    system = StudentManagementSystem()
    system.run() 