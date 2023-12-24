import mysql.connector

# Function to establish a MySQL connection
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="chitransh",
            password="abcd",
            database="hospital"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to create the patient table if it doesn't exist
def create_patient_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT,
            gender VARCHAR(10),
            diagnosis VARCHAR(255)
        )
    """)
    connection.commit()

# Function to add a patient record to the database
def add_patient(connection):
    cursor = connection.cursor()
    name = input("Enter patient name: ")
    age = int(input("Enter patient age: "))
    gender = input("Enter patient gender: ")
    diagnosis = input("Enter patient diagnosis: ")

    cursor.execute("""
        INSERT INTO patients (name, age, gender, diagnosis)
        VALUES (%s, %s, %s, %s)
    """, (name, age, gender, diagnosis))

    connection.commit()
    print("Patient record added successfully!")

# Function to display all patient records
def fetch_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM patients")
    results = cursor.fetchall()

    if results:
        print("\nPatient Records:")
        for patient in results:
            print(f"ID: {patient[0]}, Name: {patient[1]}, Age: {patient[2]}, Gender: {patient[3]}, Diagnosis: {patient[4]}")
    else:
        print("No patient records found.")

# Function to delete a patient record
def delete_patient(connection):
    cursor = connection.cursor()
    patient_id = int(input("Enter the ID of the patient to delete: "))

    cursor.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
    connection.commit()

    if cursor.rowcount > 0:
        print("Patient record deleted successfully!")
    else:
        print("Patient not found.")

# Function to search patient by name
def search_patient(connection):
    name_to_search = input("Enter patient name to search: ")
    found = False

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE name LIKE %s", (f"%{name_to_search}%",))
    results = cursor.fetchall()

    if results:
        print("\nPatient Records:")
        for patient in results:
            print(f"ID: {patient['id']}, Name: {patient['name']}, Age: {patient['age']}, "
                  f"Gender: {patient['gender']}, Diagnosis: {patient['diagnosis']}")
    else:
        print("No patient records found.")

# Function to update a patient record
def update_patient(connection):
    cursor = connection.cursor()

    try:
        patient_id = int(input("Enter the ID of the patient to update: "))
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()

        if not patient:
            print("Patient not found.")
            return

        patient_list = list(patient)  # Convert the tuple to a list

        print("\nCurrent Patient Information:")
        print(f"ID: {patient_list[0]}, Name: {patient_list[1]}, Age: {patient_list[2]}, Gender: {patient_list[3]}, Diagnosis: {patient_list[4]}")

        name = input("Enter updated patient name (leave blank to keep the current name): ")
        age = int(input("Enter updated patient age (0 to keep the current age): "))
        gender = input("Enter updated patient gender (leave blank to keep the current gender): ")
        diagnosis = input("Enter updated patient diagnosis (leave blank to keep the current diagnosis): ")

        # Update the list
        if name:
            patient_list[1] = name
        if age:
            patient_list[2] = age
        if gender:
            patient_list[3] = gender
        if diagnosis:
            patient_list[4] = diagnosis

        cursor.execute("""
            UPDATE patients
            SET name = %s, age = %s, gender = %s, diagnosis = %s
            WHERE id = %s
        """, (patient_list[1], patient_list[2], patient_list[3], patient_list[4], patient_id))

        connection.commit()
        print("Patient record updated successfully!")

    except ValueError:
        print("Invalid input. Please enter a valid patient ID.")

# Main hospital management system function
def hospital_management_system():
    connection = connect_to_mysql()

    if connection:
        create_patient_table(connection)

        while True:
            print("\nHospital Management System Menu:")
            print("1. Add Patient Record")
            print("2. Delete Patient Record")
            print("3. Update Patient Record")
            print("4. Display All Records")
            print("5. Search Patient Record")
            print("6. Exit")

            choice = int(input("Enter your choice (1-6): "))

            if choice == 1:
                add_patient(connection)
            elif choice == 2:
                delete_patient(connection)
            elif choice == 3:
                update_patient(connection)
            elif choice == 4:
                fetch_data(connection)
            elif choice == 5:
                search_patient(connection)
            elif choice == 6:
                print("Exiting the Hospital Management System. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

        connection.close()

if __name__ == "__main__":
    hospital_management_system()
