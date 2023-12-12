from datetime import datetime, timedelta

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.rental_history = {}  # Dictionary to store user's rental history

    def rent_car(self, car_id, rental_date):
        self.rental_history[car_id] = rental_date

    def return_car(self, car_id, return_date):
        if car_id in self.rental_history:
            rental_date = self.rental_history.pop(car_id)
            rental_period = (return_date - rental_date).days
            return rental_period
        return None


class CarRentalSystem:
    def __init__(self):
        self.inventory = {}  # Dictionary to store car inventory
        self.rented_cars = {}  # Dictionary to store currently rented cars
        self.users = {}  # Dictionary to store user information

    def add_car_to_inventory(self, car_name, car_id):
        if car_id not in self.inventory:
            self.inventory[car_id] = car_name
            print(f"Added car {car_name} (ID: {car_id}) to inventory.")
        else:
            print(f"Car with ID {car_id} already exists in inventory.")

    def remove_car_from_inventory(self, car_id):
        if car_id in self.inventory:
            car_name = self.inventory.pop(car_id)
            print(f"Removed car {car_name} (ID: {car_id}) from inventory.")
            # If the car is returned, remove it from the rented cars list and users' rental history
            if car_id in self.rented_cars:
                user_id = self.rented_cars.pop(car_id)
                self.users[user_id].return_car(car_id, datetime.now())
        else:
            print(f"Car with ID {car_id} not found in inventory.")

    def get_currently_rented_cars(self):
        return self.rented_cars

    def get_currently_available_cars(self):
        available_cars = {car_id: car_name for car_id, car_name in self.inventory.items() if car_id not in self.rented_cars}
        return available_cars

    def get_current_car_inventory(self):
        return self.inventory

    def add_user(self, user_id, name):
        if user_id not in self.users:
            self.users[user_id] = User(user_id, name)
            print(f"User {name} (ID: {user_id}) added.")
        else:
            print(f"User with ID {user_id} already exists.")

    def add_rental_instance(self, car_id, user_id, rental_date):
        if car_id in self.inventory and car_id not in self.rented_cars and user_id in self.users:
            self.rented_cars[car_id] = user_id
            self.users[user_id].rent_car(car_id, rental_date)
            print(f"Car (ID: {car_id}) rented by user {user_id}.")
        elif car_id in self.rented_cars:
            print(f"Car (ID: {car_id}) is already rented.")
        elif user_id not in self.users:
            print(f"User with ID {user_id} not found.")
        else:
            print(f"Car with ID {car_id} not found in inventory.")

    def add_returned_instance(self, car_id, return_date):
        if car_id in self.rented_cars:
            user_id = self.rented_cars.pop(car_id)
            rental_period = self.users[user_id].return_car(car_id, return_date)
            if rental_period is not None:
                rental_cost = rental_period * 50  # Example cost calculation
                print(f"Car (ID: {car_id}) returned by user {user_id}. Rental cost: ${rental_cost}")
        else:
            print(f"Car (ID: {car_id}) was not rented or does not exist in the inventory.")

    def list_all_users(self):
        return self.users

    def list_rental_history(self, user_id):
        if user_id in self.users:
            user = self.users[user_id]
            return user.rental_history
        else:
            print(f"User with ID {user_id} not found.")
            return {}

    def calculate_rental_cost(self, car_id, return_date):
        if car_id in self.rented_cars:
            user_id = self.rented_cars[car_id]
            user = self.users[user_id]
            rental_date = user.rental_history.get(car_id)
            if rental_date:
                rental_period = (return_date - rental_date).days
                rental_cost = rental_period * 50  # Example cost calculation
                return rental_cost
            else:
                print(f"Rental history not found for car (ID: {car_id}).")
        else:
            print(f"Car (ID: {car_id}) was not rented or does not exist in the inventory.")

    def extend_rental(self, car_id, user_id, extension_days):
        if car_id in self.rented_cars and car_id in self.inventory and user_id in self.users:
            user = self.users[user_id]
            if car_id in user.rental_history:
                rental_date = user.rental_history[car_id]
                extended_return_date = rental_date + timedelta(days=extension_days)
                self.users[user_id].rental_history[car_id] = extended_return_date
                print(f"Rental for car (ID: {car_id}) extended by {extension_days} days for user {user_id}.")
            else:
                print(f"Car (ID: {car_id}) not found in user's rental history.")
        else:
            print(f"Car with ID {car_id} or user with ID {user_id} not found in inventory.")

    def find_user_by_name(self, name):
        for user_id, user in self.users.items():
            if user.name == name:
                return user_id
        return None

    def transfer_rental(self, car_id, from_user_id, to_user_id):
        if car_id in self.rented_cars and car_id in self.inventory and from_user_id in self.users and to_user_id in self.users:
            if self.rented_cars[car_id] == from_user_id:
                self.rented_cars[car_id] = to_user_id
                print(f"Rental for car (ID: {car_id}) transferred from user {from_user_id} to user {to_user_id}.")
            else:
                print(f"Car (ID: {car_id}) is not currently rented by user {from_user_id}.")
        else:
            print(f"Car with ID {car_id}, user with ID {from_user_id}, or user with ID {to_user_id} not found.")

    def list_rented_cars_by_user(self, user_id):
        rented_cars = {}
        for car_id, renter_id in self.rented_cars.items():
            if renter_id == user_id:
                rented_cars[car_id] = self.inventory[car_id]
        return rented_cars

    def list_rented_cars_by_date_range(self, start_date, end_date):
        rented_cars = {}
        for car_id, renter_id in self.rented_cars.items():
            rental_date = self.users[renter_id].rental_history.get(car_id)
            if rental_date and start_date <= rental_date <= end_date:
                rented_cars[car_id] = self.inventory[car_id]
        return rented_cars
