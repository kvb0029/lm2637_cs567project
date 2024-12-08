#RoHotel Room Booking Project

import datetime

# Constants
ROOM_TYPES = {
    'Single': {'rate': 100, 'capacity': 1},
    'Double': {'rate': 150, 'capacity': 2},
    'Suite': {'rate': 300, 'capacity': 4}
}
MIN_DAYS_BEFORE_CANCELLATION = 2

# Room class
class Room:
    def __init__(self, room_number, room_type):
        self.room_number = room_number
        self.room_type = room_type
        self.rate = ROOM_TYPES[room_type]['rate']
        self.is_booked = False

    def book(self):
        if self.is_booked:
            return f"Room {self.room_number} is already booked."
        self.is_booked = True
        return f"Room {self.room_number} booked successfully."

    def cancel_booking(self):
        if not self.is_booked:
            return f"Room {self.room_number} is not currently booked."
        self.is_booked = False
        return f"Booking for room {self.room_number} has been canceled."

# Booking class
class Booking:
    def __init__(self, customer_name, room, check_in_date, check_out_date):
        self.customer_name = customer_name
        self.room = room
        self.check_in_date = check_in_date
        self.check_out_date = check_out_date
        self.booked_on = datetime.datetime.now()
        self.is_active = True

    def cancel(self):
        if not self.is_active:
            return "Booking is already canceled."
        self.room.cancel_booking()
        self.is_active = False
        return "Booking canceled successfully."

    def calculate_cost(self):
        nights = (self.check_out_date - self.check_in_date).days
        return nights * self.room.rate

# Hotel class
class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.bookings = []

    def add_room(self, room_number, room_type):
        if room_type not in ROOM_TYPES:
            return "Invalid room type."
        self.rooms.append(Room(room_number, room_type))
        return f"Room {room_number} added as a {room_type}."

    def view_room_availability(self):
        available_rooms = [f"Room {room.room_number}: {room.room_type}" for room in self.rooms if not room.is_booked]
        return available_rooms if available_rooms else ["No rooms available."]

    def find_available_room(self, room_type):
        for room in self.rooms:
            if room.room_type == room_type and not room.is_booked:
                return room
        return None

    def book_room(self, customer_name, room_type, check_in_date, check_out_date):
        room = self.find_available_room(room_type)
        if not room:
            return "No available rooms of this type."
        room.book()
        booking = Booking(customer_name, room, check_in_date, check_out_date)
        self.bookings.append(booking)
        return f"Room {room.room_number} booked for {customer_name} from {check_in_date} to {check_out_date}."

    def cancel_booking(self, customer_name):
        for booking in self.bookings:
            if booking.customer_name == customer_name and booking.is_active:
                cancellation_notice_period = (booking.check_in_date - datetime.datetime.now().date()).days
                if cancellation_notice_period < MIN_DAYS_BEFORE_CANCELLATION:
                    return "Cancellation denied. Insufficient notice."
                return booking.cancel()
        return "Active booking not found for cancellation."

    def get_booking_summary(self):
        summary = []
        for booking in self.bookings:
            if booking.is_active:
                summary.append(
                    f"Booking for {booking.customer_name}: Room {booking.room.room_number} "
                    f"from {booking.check_in_date} to {booking.check_out_date}, Cost: {booking.calculate_cost()}"
                )
        return summary

def exit_program():
    print("Exiting the system.")
    quit()

def main():
    hotel = Hotel("Grand Stay")
    
    hotel.add_room(101, 'Single')
    hotel.add_room(102, 'Double')
    hotel.add_room(201, 'Suite')
    hotel.add_room(301, 'Single')
    hotel.add_room(302, 'Double')

    while True:
        print("\n=== Hotel Booking System ===")
        print("1. Book a Room")
        print("2. Cancel a Booking")
        print("3. View Booking Summary")
        print("4. View Room Availability")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_name = input("Enter customer name: ")
            room_type = input(f"Enter room type ({', '.join(ROOM_TYPES.keys())}): ")
            check_in = datetime.datetime.strptime(
                input("Enter check-in date (YYYY-MM-DD): "), "%Y-%m-%d"
            ).date()
            check_out = datetime.datetime.strptime(
                input("Enter check-out date (YYYY-MM-DD): "), "%Y-%m-%d"
            ).date()
            print(hotel.book_room(customer_name, room_type, check_in, check_out))
        
        elif choice == "2":
            customer_name = input("Enter customer name to cancel booking: ")
            print(hotel.cancel_booking(customer_name))

        elif choice == "3":
            summary = hotel.get_booking_summary()
            if not summary:
                print("No active bookings found.")
            else:
                for line in summary:
                    print(line)

        elif choice == "4":
            availability = hotel.view_room_availability()
            for room in availability:
                print(room)

        elif choice == "5":
            exit_program()
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()