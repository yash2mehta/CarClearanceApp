from datetime import datetime
from db_instance import db # Import the database instance
from models import UserSensitiveInformation, Vehicle, UserVehicle, Pass, PassTraveller, Preset, PresetTraveller, UserTraveller
import hashlib

def insert_mock_data():
    # Insert mock data into the database
    user_sensitive1 = UserSensitiveInformation(
        user_id=1,
        first_name="Alice",
        middle_name=None,
        last_name="Smith",
        date_of_birth=datetime(1990, 5, 15).date(),
        passport_issuing_country="United States",
        passport_number="A12345678",
        passport_expiry=datetime(2030, 12, 1).date()
    )

    user_sensitive2 = UserSensitiveInformation(
        user_id=2,
        first_name="Bob",
        middle_name="J",
        last_name="Johnson",
        date_of_birth=datetime(1985, 8, 23).date(),
        passport_issuing_country="Canada",
        passport_number="C98765432",
        passport_expiry=datetime(2028, 7, 10).date()
    )

    user_sensitive3 = UserSensitiveInformation(
        user_id=3,
        first_name="Charlie",
        middle_name=None,
        last_name="Brown",
        date_of_birth=datetime(1992, 3, 10).date(),
        passport_issuing_country="United Kingdom",
        passport_number="UK7654321",
        passport_expiry=datetime(2027, 6, 30).date()
    )

    user_sensitive4 = UserSensitiveInformation(
        user_id=4,
        first_name="Dave",
        middle_name="M",
        last_name="Wilson",
        date_of_birth=datetime(1989, 11, 2).date(),
        passport_issuing_country="Australia",
        passport_number="AU11223344",
        passport_expiry=datetime(2029, 9, 15).date()
    )

    vehicle1 = Vehicle(vehicle_number='SKR9859E')
    vehicle2 = Vehicle(vehicle_number='SGB267D')
    vehicle3 = Vehicle(vehicle_number='GBH1206B')
    vehicle4 = Vehicle(vehicle_number='GBL1368X')
    vehicle5 = Vehicle(vehicle_number='AAAAAAAA')

    user_vehicle1 = UserVehicle(user_id=1, vehicle_id=1, user_vehicle_model = "User Model 1")
    user_vehicle2 = UserVehicle(user_id=2, vehicle_id=1, user_vehicle_model = "User Model 2")
    user_vehicle3 = UserVehicle(user_id=2, vehicle_id=2, user_vehicle_model = "User Model 2.1")
    user_vehicle4 = UserVehicle(user_id=3, vehicle_id=2, user_vehicle_model = "User Model 3")
    user_vehicle5 = UserVehicle(user_id=4, vehicle_id=3, user_vehicle_model = "User Model 4")
    user_vehicle6 = UserVehicle(user_id=4, vehicle_id=4, user_vehicle_model = "User Model 4.1")

    pass1 = Pass(creator_user_id=1, pass_date=datetime(2025, 3, 7, 0, 0), expiry_datetime=datetime(2025, 3, 8, 0, 0), pass_utilized=True)
    pass2 = Pass(creator_user_id=2, pass_date=datetime(2025, 3, 12, 0, 0), expiry_datetime=datetime(2025, 3, 13, 0, 0), pass_utilized=False)
    pass3 = Pass(creator_user_id=4, pass_date=datetime(2025, 3, 7, 0, 0), expiry_datetime=datetime(2025, 3, 8, 0, 0), pass_utilized=False)
    pass4 = Pass(creator_user_id=4, pass_date=datetime(2025, 2, 19, 0, 0), expiry_datetime=datetime(2025, 2, 20, 0, 0), pass_utilized=False)
    pass5 = Pass(creator_user_id=1, pass_date=datetime(2025, 2, 25, 0, 0), expiry_datetime=datetime(2025, 2, 26, 0, 0), pass_utilized=False)

    pass_traveller1 = PassTraveller(pass_id=1, user_id=1)  # Alice as traveller for SKR9859E
    pass_traveller2 = PassTraveller(pass_id=1, user_id=2)  # Bob as traveller for SKR9859E
    pass_traveller3 = PassTraveller(pass_id=2, user_id=2)  # Bob as traveller for SGB267D
    pass_traveller4 = PassTraveller(pass_id=2, user_id=3)  # Charlie as traveller for SGB267D

    preset1 = Preset(preset_name="Work Trip", user_id=1)
    preset2 = Preset(preset_name="Vacation Mode", user_id=1)
    preset3 = Preset(preset_name="Conference Travel", user_id=2)
    preset4 = Preset(preset_name="Weekend Getaway", user_id=3)
    preset5 = Preset(preset_name="Family Visit", user_id=4)

    preset_traveller1 = PresetTraveller(preset_id=1, user_id=1)
    preset_traveller2 = PresetTraveller(preset_id=1, user_id=2)
    preset_traveller3 = PresetTraveller(preset_id=2, user_id=1)
    preset_traveller4 = PresetTraveller(preset_id=3, user_id=2)
    preset_traveller5 = PresetTraveller(preset_id=4, user_id=3)
    preset_traveller6 = PresetTraveller(preset_id=5, user_id=4)
    preset_traveller7 = PresetTraveller(preset_id=5, user_id=1)

    # New Table: UserTraveller (Tracks manually added travellers)
    user_traveller1 = UserTraveller(creator_user_id=1, traveller_id=2)
    user_traveller2 = UserTraveller(creator_user_id=1, traveller_id=3)
    user_traveller3 = UserTraveller(creator_user_id=2, traveller_id=4)
    user_traveller4 = UserTraveller(creator_user_id=3, traveller_id=1)
    user_traveller5 = UserTraveller(creator_user_id=4, traveller_id=2)

    # Adding all records to the session
    db.session.add_all([
        user_sensitive1, user_sensitive2, user_sensitive3, user_sensitive4,
        vehicle1, vehicle2, vehicle3, vehicle4,
        user_vehicle1, user_vehicle2, user_vehicle3, user_vehicle4, user_vehicle5, user_vehicle6,
        pass1, pass2, pass3, pass4, pass5,
        pass_traveller1, pass_traveller2, pass_traveller3, pass_traveller4,
        preset1, preset2, preset3, preset4, preset5,
        preset_traveller1, preset_traveller2, preset_traveller3, preset_traveller4, preset_traveller5, preset_traveller6, preset_traveller7,
        user_traveller1, user_traveller2, user_traveller3, user_traveller4, user_traveller5
    ])

    # Commit the session to save the records to the database
    db.session.commit()
    print("✅ Mock data inserted successfully.")

