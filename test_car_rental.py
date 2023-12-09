import unittest
from datetime import datetime, timedelta
from car_rental_system import CarRentalSystem

class TestCarRentalSystem(unittest.TestCase):
    def setUp(self):
        self.system = CarRentalSystem()
        self.system.add_car_to_inventory(1, "Toyota Corolla")
        self.system.add_car_to_inventory(2, "Honda Civic")
        self.system.add_user(101, "Alice")
        self.system.add_user(102, "Bob")

    def test_add_car_to_inventory(self):
        self.system.add_car_to_inventory(3, "Ford Mustang")
        self.assertIn(3, self.system.get_current_car_inventory())

    def test_remove_car_from_inventory(self):
        self.system.remove_car_from_inventory(1)
        self.assertNotIn(1, self.system.get_current_car_inventory())

    def test_add_user(self):
        self.system.add_user(103, "Charlie")
        self.assertIn(103, self.system.list_all_users())

    def test_add_rental_instance(self):
        rental_date = datetime(2023, 1, 1)
        self.system.add_rental_instance(1, 101, rental_date)
        self.assertEqual(self.system.get_currently_rented_cars()[1], 101)
        self.assertEqual(self.system.list_rental_history(101), {1: rental_date})

    def test_add_returned_instance(self):
        rental_date = datetime(2023, 1, 1)
        return_date = datetime(2023, 1, 5)
        self.system.add_rental_instance(1, 101, rental_date)
        self.system.add_returned_instance(1, return_date)
        self.assertNotIn(1, self.system.get_currently_rented_cars())

    def test_list_rented_cars_by_user(self):
        rental_date_1 = datetime(2023, 1, 1)
        rental_date_2 = datetime(2023, 1, 3)
        self.system.add_rental_instance(1, 101, rental_date_1)
        self.system.add_rental_instance(2, 101, rental_date_2)
        rented_cars = self.system.list_rented_cars_by_user(101)
        self.assertEqual(len(rented_cars), 2)
        self.assertIn(1, rented_cars)
        self.assertIn(2, rented_cars)

    def test_list_rented_cars_by_date_range(self):
        rental_date_1 = datetime(2023, 1, 1)
        rental_date_2 = datetime(2023, 1, 3)
        return_date_1 = datetime(2023, 1, 5)
        return_date_2 = datetime(2023, 1, 6)
        self.system.add_rental_instance(1, 101, rental_date_1)
        self.system.add_rental_instance(2, 101, rental_date_2)
        self.system.add_returned_instance(1, return_date_1)
        self.system.add_returned_instance(2, return_date_2)
        rented_cars = self.system.list_rented_cars_by_date_range(rental_date_1, return_date_2)
        self.assertEqual(len(rented_cars), 0)

    def test_calculate_rental_cost(self):
        rental_date = datetime(2023, 1, 1)
        return_date = datetime(2023, 1, 6)
        self.system.add_rental_instance(1, 101, rental_date)
        rental_cost = self.system.calculate_rental_cost(1, return_date)
        self.assertEqual(rental_cost, 250)  # 5 days * $50 per day

    def test_extend_rental(self):
        rental_date = datetime(2023, 1, 1)
        self.system.add_rental_instance(1, 101, rental_date)
        extended_return_date = rental_date + timedelta(days=3)
        self.system.extend_rental(1, 101, 3)
        self.assertEqual(self.system.list_rental_history(101)[1], extended_return_date)

    def test_find_user_by_name(self):
        user_id = self.system.find_user_by_name("Alice")
        self.assertEqual(user_id, 101)

    def test_transfer_rental(self):
        rental_date = datetime(2023, 1, 1)
        self.system.add_rental_instance(1, 101, rental_date)
        self.system.transfer_rental(1, 101, 102)
        self.assertTrue(self.system.rented_cars[1]==102)
        #self.assertNotIn(1, self.system.users[101].rental_history)
        #self.assertIn(1, self.system.users[102].rental_history)

if __name__ == "__main__":
    unittest.main()
