import mysql.connector

# CONNECTING TO DATABASE
try:
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="Diamond162423", database="inn_reservation")
    print("CONNECTED DATABASE TO PYTHON")
except mysql.connector.Error as e:
    print("Error")

mycursor = mydb.cursor()

# MAIN MENU SCREEN WHEN EXECUTING

while True:
    print("\n*************Welcome to The LIRS system*************")
    print("Please enter a number related to the following option to continue: ")
    print("_______________________________\n")
    print("\tCheck-out: 1\n\tCheck-in: 2\n\tExit: 3")
    print("_______________________________")

    option = input("Your option: ")

    if option == "1":
        print("************Checkout Process*************")

        phone = input("Please give your phone number: ")
        print("Checkout in Progress. . . . .")

        mycursor.execute("""
            SELECT r.id, c.first_name, c.last_name, r.accommodation_days, ir.room_type, r.cost
            FROM inn_reservation r
            JOIN inn_customer c ON r.customer_id = c.id
            JOIN inn_room ir ON r.room_type = ir.id
            WHERE c.phone_number = %s
            """, (phone,))

        reservation = mycursor.fetchone()

        if reservation:
            id, first_name, last_name, accommodation_days, room_type, cost = reservation
            print("Your invoice information is:")

            print("-------------------- Pacific Inn --------------------")
            print(f"Checkout process for phone number {phone} completed successfully.")
            print("Your invoice information is:")
            print(f"Name: {first_name} {last_name}")
            print(f"Accommodation: {accommodation_days} days")
            print(f"Room type: {room_type}")
            print(f"Total Cost: ${cost}")
            print("-------------------Thank you, See You Next Time---------------------")

            # Update reservation as checked-out
            update_reservation_query = "UPDATE inn_reservation SET checkout = 1 WHERE id = %s"
            mycursor.execute(update_reservation_query, (reservation[0],))

            # Increase availability in inn_room table
            update_room_availability_query = """
             UPDATE inn_room r
            JOIN inn_reservation res ON r.id = res.room_type
            SET r.availability = r.availability + 1
            WHERE res.id = %s
            """
            mycursor.execute(update_room_availability_query, (reservation[0],))
            mydb.commit()

            # Write the invoice details to a text file
            with open(f"reservation_file{id}.txt", "w") as file:
                file.write("Your invoice information:\n")
                file.write("-------------------- Pacific Inn ------------------\n")
                file.write(f"Checkout process for phone number {phone} completed successfully.\n")
                file.write(f"Name: {first_name} {last_name}\n")
                file.write(f"Accommodation: {accommodation_days} days\n")
                file.write(f"Room type: {room_type}\n")
                file.write(f"Total Cost: ${cost}\n")
        else:
            print(f"No active reservation found for phone number {phone}.")

    elif option == "2":
        print("************Check-in process*************")
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        email = input("Enter email address: ")
        phone_number = int(input("Enter phone number: "))
        room_type = input("Enter room type (S, P, O, E): ").upper()  # Convert to uppercase for case-insensitivity
        accommodation_days = int(input("Enter the number of days for accommodation: "))

        # Check if the selected room type is available
        mycursor.execute("SELECT id, room_type FROM inn_room WHERE availability > 0 ORDER BY room_type")
        availability = mycursor.fetchall()

        if not availability:
            print("No available rooms. Check-in process cannot be completed.")
        else:
            for room in availability:
                print(f"Room ID: {room[0]}, Room Type: {room[1]}")

            try:
                # Mapping of user input to room type IDs
                room_type_mapping = {'S': 1, 'P': 2, 'O': 3, 'E': 4}
                room_type_id = room_type_mapping.get(room_type)

                # Insert customer into inn_customer table
                insert_customer_query = """
                INSERT INTO inn_customer (first_name, last_name, email, phone_number)
                VALUES (%s, %s, %s, %s)
                """
                mycursor.execute(insert_customer_query, (first_name, last_name, email, phone_number))

                customer_id = mycursor.lastrowid

                # Insert customer room details into inn_reservation table
                insert_reservation_query = """
                INSERT INTO inn_reservation (room_type, customer_id, accommodation_days, checkout)
                VALUES (%s, %s, %s, 0)
                """
                mycursor.execute(insert_reservation_query, (room_type_id, customer_id, accommodation_days))
                mydb.commit()

                # Update availability in inn_room table
                update_availability_query = "UPDATE inn_room SET availability = availability - 1 WHERE id = %s"
                mycursor.execute(update_availability_query, (room_type_id,))
                mydb.commit()

                print("Check-in process completed successfully.")
            except mysql.connector.Error as e:
                print(f"Error during check-in process: {e}")

    elif option == "3":
        print("Exiting the program. Goodbye!")
        break

mydb.close()
