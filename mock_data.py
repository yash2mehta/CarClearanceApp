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

    user_sensitive5 = UserSensitiveInformation(
        user_id=5,
        first_name="Test",
        middle_name="",
        last_name="Master",
        date_of_birth=datetime(1989, 12, 2).date(),
        passport_issuing_country="Germany",
        passport_number="ABCDE12345",
        passport_expiry=datetime(2030, 9, 15).date()
    )

    # Adding 50 new users with diverse information
    user_sensitive6 = UserSensitiveInformation(
        user_id=6,
        first_name="Élise",
        middle_name="Marie",
        last_name="Dubois",
        date_of_birth=datetime(1995, 4, 18).date(),
        passport_issuing_country="France",
        passport_number="FR12AB34CD",
        passport_expiry=datetime(2028, 11, 30).date()
    )

    user_sensitive7 = UserSensitiveInformation(
        user_id=7,
        first_name="Hans",
        middle_name="Jürgen",
        last_name="Schmidt",
        date_of_birth=datetime(1978, 9, 5).date(),
        passport_issuing_country="Germany",
        passport_number="DE987654321",
        passport_expiry=datetime(2027, 3, 15).date()
    )

    user_sensitive8 = UserSensitiveInformation(
        user_id=8,
        first_name="Sofia",
        middle_name="Isabella",
        last_name="García",
        date_of_birth=datetime(1992, 7, 22).date(),
        passport_issuing_country="Spain",
        passport_number="ES123456789",
        passport_expiry=datetime(2029, 5, 10).date()
    )

    user_sensitive9 = UserSensitiveInformation(
        user_id=9,
        first_name="Liam",
        middle_name="James",
        last_name="O'Connor",
        date_of_birth=datetime(1987, 2, 14).date(),
        passport_issuing_country="Ireland",
        passport_number="IE987654321",
        passport_expiry=datetime(2026, 8, 20).date()
    )

    user_sensitive10 = UserSensitiveInformation(
        user_id=10,
        first_name="Alessandro",
        middle_name="Marco",
        last_name="Rossi",
        date_of_birth=datetime(1993, 11, 30).date(),
        passport_issuing_country="Italy",
        passport_number="IT123456789",
        passport_expiry=datetime(2028, 4, 12).date()
    )

    user_sensitive11 = UserSensitiveInformation(
        user_id=11,
        first_name="Yuki",
        middle_name="Hiroshi",
        last_name="Tanaka",
        date_of_birth=datetime(1991, 6, 8).date(),
        passport_issuing_country="Japan",
        passport_number="JP987654321",
        passport_expiry=datetime(2027, 9, 25).date()
    )

    user_sensitive12 = UserSensitiveInformation(
        user_id=12,
        first_name="Wei",
        middle_name="Chen",
        last_name="Li",
        date_of_birth=datetime(1986, 3, 17).date(),
        passport_issuing_country="China",
        passport_number="CN123456789",
        passport_expiry=datetime(2029, 7, 3).date()
    )

    user_sensitive13 = UserSensitiveInformation(
        user_id=13,
        first_name="Priya",
        middle_name="Anjali",
        last_name="Patel",
        date_of_birth=datetime(1994, 8, 11).date(),
        passport_issuing_country="India",
        passport_number="IN987654321",
        passport_expiry=datetime(2026, 12, 15).date()
    )

    user_sensitive14 = UserSensitiveInformation(
        user_id=14,
        first_name="Mohammed",
        middle_name="Ahmed",
        last_name="Al-Sayed",
        date_of_birth=datetime(1988, 5, 23).date(),
        passport_issuing_country="United Arab Emirates",
        passport_number="AE123456789",
        passport_expiry=datetime(2028, 2, 28).date()
    )

    user_sensitive15 = UserSensitiveInformation(
        user_id=15,
        first_name="Olga",
        middle_name="Ivanovna",
        last_name="Petrova",
        date_of_birth=datetime(1990, 10, 7).date(),
        passport_issuing_country="Russia",
        passport_number="RU987654321",
        passport_expiry=datetime(2027, 6, 18).date()
    )

    user_sensitive16 = UserSensitiveInformation(
        user_id=16,
        first_name="Lars",
        middle_name="Erik",
        last_name="Andersen",
        date_of_birth=datetime(1985, 1, 29).date(),
        passport_issuing_country="Denmark",
        passport_number="DK123456789",
        passport_expiry=datetime(2029, 10, 5).date()
    )

    user_sensitive17 = UserSensitiveInformation(
        user_id=17,
        first_name="Astrid",
        middle_name="Linnea",
        last_name="Nilsson",
        date_of_birth=datetime(1993, 12, 14).date(),
        passport_issuing_country="Sweden",
        passport_number="SE987654321",
        passport_expiry=datetime(2026, 4, 22).date()
    )

    user_sensitive18 = UserSensitiveInformation(
        user_id=18,
        first_name="Johan",
        middle_name="Willem",
        last_name="de Vries",
        date_of_birth=datetime(1987, 7, 3).date(),
        passport_issuing_country="Netherlands",
        passport_number="NL123456789",
        passport_expiry=datetime(2028, 8, 30).date()
    )

    user_sensitive19 = UserSensitiveInformation(
        user_id=19,
        first_name="Elena",
        middle_name="Maria",
        last_name="Popovici",
        date_of_birth=datetime(1992, 4, 19).date(),
        passport_issuing_country="Romania",
        passport_number="RO987654321",
        passport_expiry=datetime(2027, 11, 7).date()
    )

    user_sensitive20 = UserSensitiveInformation(
        user_id=20,
        first_name="Kazimierz",
        middle_name="Jan",
        last_name="Kowalski",
        date_of_birth=datetime(1989, 9, 25).date(),
        passport_issuing_country="Poland",
        passport_number="PL123456789",
        passport_expiry=datetime(2029, 1, 14).date()
    )

    user_sensitive21 = UserSensitiveInformation(
        user_id=21,
        first_name="Sven",
        middle_name="Magnus",
        last_name="Bergström",
        date_of_birth=datetime(1991, 2, 8).date(),
        passport_issuing_country="Norway",
        passport_number="NO987654321",
        passport_expiry=datetime(2026, 5, 30).date()
    )

    user_sensitive22 = UserSensitiveInformation(
        user_id=22,
        first_name="Isabella",
        middle_name="Sofia",
        last_name="Silva",
        date_of_birth=datetime(1994, 6, 12).date(),
        passport_issuing_country="Brazil",
        passport_number="BR123456789",
        passport_expiry=datetime(2028, 3, 25).date()
    )

    user_sensitive23 = UserSensitiveInformation(
        user_id=23,
        first_name="Carlos",
        middle_name="Miguel",
        last_name="Rodríguez",
        date_of_birth=datetime(1986, 11, 17).date(),
        passport_issuing_country="Mexico",
        passport_number="MX987654321",
        passport_expiry=datetime(2027, 7, 9).date()
    )

    user_sensitive24 = UserSensitiveInformation(
        user_id=24,
        first_name="Aisha",
        middle_name="Fatima",
        last_name="Khan",
        date_of_birth=datetime(1993, 3, 28).date(),
        passport_issuing_country="Pakistan",
        passport_number="PK123456789",
        passport_expiry=datetime(2029, 9, 16).date()
    )

    user_sensitive25 = UserSensitiveInformation(
        user_id=25,
        first_name="Hassan",
        middle_name="Ali",
        last_name="Abdullah",
        date_of_birth=datetime(1988, 8, 5).date(),
        passport_issuing_country="Saudi Arabia",
        passport_number="SA987654321",
        passport_expiry=datetime(2026, 12, 3).date()
    )

    user_sensitive26 = UserSensitiveInformation(
        user_id=26,
        first_name="Nina",
        middle_name="Ivanova",
        last_name="Kovač",
        date_of_birth=datetime(1990, 5, 21).date(),
        passport_issuing_country="Croatia",
        passport_number="HR123456789",
        passport_expiry=datetime(2028, 4, 7).date()
    )

    user_sensitive27 = UserSensitiveInformation(
        user_id=27,
        first_name="Viktor",
        middle_name="Ivanov",
        last_name="Ivanov",
        date_of_birth=datetime(1987, 10, 13).date(),
        passport_issuing_country="Bulgaria",
        passport_number="BG987654321",
        passport_expiry=datetime(2027, 2, 19).date()
    )

    user_sensitive28 = UserSensitiveInformation(
        user_id=28,
        first_name="Eva",
        middle_name="Maria",
        last_name="Nováková",
        date_of_birth=datetime(1992, 1, 24).date(),
        passport_issuing_country="Czech Republic",
        passport_number="CZ123456789",
        passport_expiry=datetime(2029, 6, 11).date()
    )

    user_sensitive29 = UserSensitiveInformation(
        user_id=29,
        first_name="János",
        middle_name="István",
        last_name="Nagy",
        date_of_birth=datetime(1989, 7, 9).date(),
        passport_issuing_country="Hungary",
        passport_number="HU987654321",
        passport_expiry=datetime(2026, 10, 28).date()
    )

    user_sensitive30 = UserSensitiveInformation(
        user_id=30,
        first_name="Marta",
        middle_name="Anna",
        last_name="Wójcik",
        date_of_birth=datetime(1991, 12, 31).date(),
        passport_issuing_country="Poland",
        passport_number="PL987654321",
        passport_expiry=datetime(2028, 5, 17).date()
    )

    user_sensitive31 = UserSensitiveInformation(
        user_id=31,
        first_name="Lukas",
        middle_name="Michael",
        last_name="Weber",
        date_of_birth=datetime(1986, 4, 2).date(),
        passport_issuing_country="Austria",
        passport_number="AT123456789",
        passport_expiry=datetime(2027, 8, 23).date()
    )

    user_sensitive32 = UserSensitiveInformation(
        user_id=32,
        first_name="Sophie",
        middle_name="Claire",
        last_name="Martin",
        date_of_birth=datetime(1993, 9, 16).date(),
        passport_issuing_country="Belgium",
        passport_number="BE987654321",
        passport_expiry=datetime(2029, 1, 5).date()
    )

    user_sensitive33 = UserSensitiveInformation(
        user_id=33,
        first_name="Andreas",
        middle_name="Johann",
        last_name="Müller",
        date_of_birth=datetime(1988, 2, 27).date(),
        passport_issuing_country="Switzerland",
        passport_number="CH123456789",
        passport_expiry=datetime(2026, 11, 14).date()
    )

    user_sensitive34 = UserSensitiveInformation(
        user_id=34,
        first_name="Maria",
        middle_name="Isabel",
        last_name="González",
        date_of_birth=datetime(1990, 6, 8).date(),
        passport_issuing_country="Argentina",
        passport_number="AR987654321",
        passport_expiry=datetime(2028, 3, 30).date()
    )

    user_sensitive35 = UserSensitiveInformation(
        user_id=35,
        first_name="Marek",
        middle_name="Jan",
        last_name="Nowak",
        date_of_birth=datetime(1987, 6, 30).date(),
        passport_issuing_country="Poland",
        passport_number="PL987654322",
        passport_expiry=datetime(2027, 9, 20).date()
    )

    user_sensitive36 = UserSensitiveInformation(
        user_id=36,
        first_name="Fatima",
        middle_name="Zahra",
        last_name="Benali",
        date_of_birth=datetime(1992, 3, 15).date(),
        passport_issuing_country="Morocco",
        passport_number="MA987654321",
        passport_expiry=datetime(2029, 9, 28).date()
    )

    user_sensitive37 = UserSensitiveInformation(
        user_id=37,
        first_name="Jin",
        middle_name="Wei",
        last_name="Zhang",
        date_of_birth=datetime(1989, 8, 4).date(),
        passport_issuing_country="South Korea",
        passport_number="KR123456789",
        passport_expiry=datetime(2026, 12, 10).date()
    )

    user_sensitive38 = UserSensitiveInformation(
        user_id=38,
        first_name="Ming",
        middle_name="Hui",
        last_name="Wong",
        date_of_birth=datetime(1991, 1, 19).date(),
        passport_issuing_country="Hong Kong",
        passport_number="HK987654321",
        passport_expiry=datetime(2028, 5, 3).date()
    )

    user_sensitive39 = UserSensitiveInformation(
        user_id=39,
        first_name="Ravi",
        middle_name="Kumar",
        last_name="Singh",
        date_of_birth=datetime(1986, 5, 11).date(),
        passport_issuing_country="India",
        passport_number="IN123456788",
        passport_expiry=datetime(2027, 10, 25).date()
    )

    user_sensitive40 = UserSensitiveInformation(
        user_id=40,
        first_name="Siti",
        middle_name="Aminah",
        last_name="Abdullah",
        date_of_birth=datetime(1993, 10, 7).date(),
        passport_issuing_country="Malaysia",
        passport_number="MY987654321",
        passport_expiry=datetime(2029, 2, 18).date()
    )

    user_sensitive41 = UserSensitiveInformation(
        user_id=41,
        first_name="Taro",
        middle_name="Yamamoto",
        last_name="Suzuki",
        date_of_birth=datetime(1988, 2, 14).date(),
        passport_issuing_country="Japan",
        passport_number="JP123456788",
        passport_expiry=datetime(2026, 6, 30).date()
    )

    user_sensitive42 = UserSensitiveInformation(
        user_id=42,
        first_name="Mei",
        middle_name="Ling",
        last_name="Chen",
        date_of_birth=datetime(1990, 7, 23).date(),
        passport_issuing_country="Taiwan",
        passport_number="TW987654321",
        passport_expiry=datetime(2028, 1, 12).date()
    )

    user_sensitive43 = UserSensitiveInformation(
        user_id=43,
        first_name="Raj",
        middle_name="Kumar",
        last_name="Sharma",
        date_of_birth=datetime(1987, 12, 5).date(),
        passport_issuing_country="Nepal",
        passport_number="NP123456789",
        passport_expiry=datetime(2027, 4, 20).date()
    )

    user_sensitive44 = UserSensitiveInformation(
        user_id=44,
        first_name="Ahmad",
        middle_name="Rizki",
        last_name="Hidayat",
        date_of_birth=datetime(1992, 4, 29).date(),
        passport_issuing_country="Indonesia",
        passport_number="ID987654321",
        passport_expiry=datetime(2029, 8, 7).date()
    )

    user_sensitive45 = UserSensitiveInformation(
        user_id=45,
        first_name="Nguyen",
        middle_name="Thi",
        last_name="Pham",
        date_of_birth=datetime(1989, 9, 13).date(),
        passport_issuing_country="Vietnam",
        passport_number="VN123456789",
        passport_expiry=datetime(2026, 3, 25).date()
    )

    user_sensitive46 = UserSensitiveInformation(
        user_id=46,
        first_name="Kim",
        middle_name="Soo",
        last_name="Park",
        date_of_birth=datetime(1991, 1, 27).date(),
        passport_issuing_country="South Korea",
        passport_number="KR987654322",
        passport_expiry=datetime(2028, 8, 15).date()
    )

    user_sensitive47 = UserSensitiveInformation(
        user_id=47,
        first_name="Muhammad",
        middle_name="Ali",
        last_name="Hassan",
        date_of_birth=datetime(1986, 6, 9).date(),
        passport_issuing_country="Bangladesh",
        passport_number="BD123456789",
        passport_expiry=datetime(2027, 11, 30).date()
    )

    user_sensitive48 = UserSensitiveInformation(
        user_id=48,
        first_name="Anastasia",
        middle_name="Ivanovna",
        last_name="Sokolova",
        date_of_birth=datetime(1993, 10, 21).date(),
        passport_issuing_country="Ukraine",
        passport_number="UA987654321",
        passport_expiry=datetime(2029, 2, 8).date()
    )

    user_sensitive49 = UserSensitiveInformation(
        user_id=49,
        first_name="Dimitris",
        middle_name="Ioannis",
        last_name="Papadopoulos",
        date_of_birth=datetime(1988, 3, 17).date(),
        passport_issuing_country="Greece",
        passport_number="GR123456789",
        passport_expiry=datetime(2026, 9, 22).date()
    )

    user_sensitive50 = UserSensitiveInformation(
        user_id=50,
        first_name="Luis",
        middle_name="Miguel",
        last_name="García",
        date_of_birth=datetime(1990, 8, 4).date(),
        passport_issuing_country="Colombia",
        passport_number="CO987654321",
        passport_expiry=datetime(2028, 4, 15).date()
    )

    user_sensitive51 = UserSensitiveInformation(
        user_id=51,
        first_name="Ji-hoon",
        middle_name="Min",
        last_name="Park",
        date_of_birth=datetime(1993, 4, 12).date(),
        passport_issuing_country="South Korea",
        passport_number="KR987654322",
        passport_expiry=datetime(2028, 8, 15).date()
    )

    user_sensitive52 = UserSensitiveInformation(
        user_id=52,
        first_name="Fernando",
        middle_name="José",
        last_name="Silva",
        date_of_birth=datetime(1992, 5, 11).date(),
        passport_issuing_country="Portugal",
        passport_number="PT987654321",
        passport_expiry=datetime(2029, 10, 3).date()
    )

    user_sensitive53 = UserSensitiveInformation(
        user_id=53,
        first_name="Anna",
        middle_name="Maria",
        last_name="Kowalczyk",
        date_of_birth=datetime(1989, 2, 25).date(),
        passport_issuing_country="Poland",
        passport_number="PL123456788",
        passport_expiry=datetime(2026, 7, 19).date()
    )

    user_sensitive54 = UserSensitiveInformation(
        user_id=54,
        first_name="Erik",
        middle_name="Lars",
        last_name="Jensen",
        date_of_birth=datetime(1991, 7, 8).date(),
        passport_issuing_country="Norway",
        passport_number="NO987654322",
        passport_expiry=datetime(2028, 1, 24).date()
    )

    user_sensitive55 = UserSensitiveInformation(
        user_id=55,
        first_name="Maria",
        middle_name="Isabel",
        last_name="Santos",
        date_of_birth=datetime(1986, 11, 15).date(),
        passport_issuing_country="Brazil",
        passport_number="BR123456788",
        passport_expiry=datetime(2027, 3, 7).date()
    )

    vehicle1 = Vehicle(vehicle_number='SKR9859E')  # Toyota Corolla
    vehicle2 = Vehicle(vehicle_number='SGB267D')   # Honda Civic
    vehicle3 = Vehicle(vehicle_number='GBH1206B')  # Tesla Model 3
    vehicle4 = Vehicle(vehicle_number='GBL1368X')  # BMW X5
    vehicle5 = Vehicle(vehicle_number='MKL8721Z')  # Mercedes-Benz C-Class (New vehicle)
    vehicle6 = Vehicle(vehicle_number='RXA4123M')  # Audi A4 (New vehicle)
    
    # New vehicles for user 2
    vehicle7 = Vehicle(vehicle_number='SJX1234A')  # Lexus RX
    vehicle8 = Vehicle(vehicle_number='SJY5678B')  # Volvo XC90
    vehicle9 = Vehicle(vehicle_number='SJZ9012C')  # Porsche Cayenne
    vehicle10 = Vehicle(vehicle_number='SKA3456D')  # Range Rover Sport
    vehicle11 = Vehicle(vehicle_number='SKB7890E')  # Jaguar F-PACE
    vehicle12 = Vehicle(vehicle_number='SKC1234F')  # Land Rover Discovery
    vehicle13 = Vehicle(vehicle_number='SKD5678G')  # Maserati Levante
    vehicle14 = Vehicle(vehicle_number='SKE9012H')  # Bentley Bentayga
    vehicle15 = Vehicle(vehicle_number='SKF3456I')  # Rolls-Royce Cullinan
    vehicle16 = Vehicle(vehicle_number='SKG7890J')  # Lamborghini Urus

    user_vehicle1 = UserVehicle(user_id=1, vehicle_id=1, user_vehicle_model="Toyota Corolla")
    user_vehicle2 = UserVehicle(user_id=2, vehicle_id=1, user_vehicle_model="Honda Civic")
    user_vehicle3 = UserVehicle(user_id=2, vehicle_id=2, user_vehicle_model="Honda Accord")
    user_vehicle4 = UserVehicle(user_id=3, vehicle_id=2, user_vehicle_model="Mazda CX-5")
    user_vehicle5 = UserVehicle(user_id=4, vehicle_id=3, user_vehicle_model="Tesla Model 3")
    user_vehicle6 = UserVehicle(user_id=4, vehicle_id=4, user_vehicle_model="BMW X5")
    # New vehicles for user 1
    user_vehicle7 = UserVehicle(user_id=1, vehicle_id=5, user_vehicle_model="Mercedes-Benz C-Class")
    user_vehicle8 = UserVehicle(user_id=1, vehicle_id=6, user_vehicle_model="Audi A4")
    
    # New user vehicles for user 2
    user_vehicle9 = UserVehicle(user_id=2, vehicle_id=7, user_vehicle_model="Lexus RX")
    user_vehicle10 = UserVehicle(user_id=2, vehicle_id=8, user_vehicle_model="Volvo XC90")
    user_vehicle11 = UserVehicle(user_id=2, vehicle_id=9, user_vehicle_model="Porsche Cayenne")
    user_vehicle12 = UserVehicle(user_id=2, vehicle_id=10, user_vehicle_model="Range Rover Sport")
    user_vehicle13 = UserVehicle(user_id=2, vehicle_id=11, user_vehicle_model="Jaguar F-PACE")
    user_vehicle14 = UserVehicle(user_id=2, vehicle_id=12, user_vehicle_model="Land Rover Discovery")
    user_vehicle15 = UserVehicle(user_id=2, vehicle_id=13, user_vehicle_model="Maserati Levante")
    user_vehicle16 = UserVehicle(user_id=2, vehicle_id=14, user_vehicle_model="Bentley Bentayga")
    user_vehicle17 = UserVehicle(user_id=2, vehicle_id=15, user_vehicle_model="Rolls-Royce Cullinan")
    user_vehicle18 = UserVehicle(user_id=2, vehicle_id=16, user_vehicle_model="Lamborghini Urus")

    pass1 = Pass(creator_user_id=1, pass_date=datetime(2025, 3, 7, 8, 15), expiry_datetime=datetime(2025, 3, 8, 8, 15), pass_utilized=True)
    pass2 = Pass(creator_user_id=2, pass_date=datetime(2025, 3, 12, 0, 0), expiry_datetime=datetime(2025, 3, 13, 0, 0), pass_utilized=False)
    pass3 = Pass(creator_user_id=4, pass_date=datetime(2025, 3, 7, 0, 0), expiry_datetime=datetime(2025, 3, 8, 0, 0), pass_utilized=False)
    pass4 = Pass(creator_user_id=4, pass_date=datetime(2025, 2, 19, 0, 0), expiry_datetime=datetime(2025, 2, 20, 0, 0), pass_utilized=False)
    pass5 = Pass(creator_user_id=1, pass_date=datetime(2025, 2, 25, 0, 0), expiry_datetime=datetime(2025, 2, 26, 0, 0), pass_utilized=False)

    # New passes for user 1
    pass6 = Pass(creator_user_id=1, pass_date=datetime(2025, 3, 7, 14, 30), expiry_datetime=datetime(2025, 3, 8, 14, 30), pass_utilized=True)  # Same date as pass1 but pass_utilized=False
    pass7 = Pass(creator_user_id=1, pass_date=datetime(2025, 4, 15, 0, 0), expiry_datetime=datetime(2025, 4, 16, 0, 0), pass_utilized=True)  # Different date pass
    
    # New passes for user 2
    pass8 = Pass(creator_user_id=2, pass_date=datetime(2025, 4, 1, 9, 0), expiry_datetime=datetime(2025, 4, 2, 9, 0), pass_utilized=True)
    pass9 = Pass(creator_user_id=2, pass_date=datetime(2025, 4, 15, 14, 30), expiry_datetime=datetime(2025, 4, 16, 14, 30), pass_utilized=False)
    pass10 = Pass(creator_user_id=2, pass_date=datetime(2025, 5, 1, 10, 0), expiry_datetime=datetime(2025, 5, 2, 10, 0), pass_utilized=False)
    pass11 = Pass(creator_user_id=2, pass_date=datetime(2025, 5, 15, 16, 0), expiry_datetime=datetime(2025, 5, 16, 16, 0), pass_utilized=False)
    pass12 = Pass(creator_user_id=2, pass_date=datetime(2025, 6, 1, 11, 0), expiry_datetime=datetime(2025, 6, 2, 11, 0), pass_utilized=False)

    pass_traveller1 = PassTraveller(pass_id=1, user_id=1)  # Alice as traveller for SKR9859E
    pass_traveller2 = PassTraveller(pass_id=1, user_id=2)  # Bob as traveller for SKR9859E
    pass_traveller3 = PassTraveller(pass_id=2, user_id=2)  # Bob as traveller for SGB267D
    pass_traveller4 = PassTraveller(pass_id=2, user_id=3)  # Charlie as traveller for SGB267D
    pass_traveller5 = PassTraveller(pass_id=6, user_id=1)  # Alice as traveller for pass6
    pass_traveller6 = PassTraveller(pass_id=6, user_id=2)  # Bob as co-traveller for pass6
    pass_traveller7 = PassTraveller(pass_id=6, user_id=3)  # Charlie as co-traveller for pass6
    pass_traveller8 = PassTraveller(pass_id=6, user_id=4)  # Dave as co-traveller for pass6
    pass_traveller9 = PassTraveller(pass_id=7, user_id=1)  # Alice as traveller for pass7
    pass_traveller10 = PassTraveller(pass_id=7, user_id=2)  # Bob as co-traveller for pass7
    pass_traveller11 = PassTraveller(pass_id=3, user_id=4)
    pass_traveller12 = PassTraveller(pass_id=3, user_id=5)
    pass_traveller13 = PassTraveller(pass_id=4, user_id=4)
    pass_traveller14 = PassTraveller(pass_id=4, user_id=5)
    pass_traveller15 = PassTraveller(pass_id=5, user_id=1)
    pass_traveller16 = PassTraveller(pass_id=5, user_id=2)
    pass_traveller17 = PassTraveller(pass_id=5, user_id=3)
    
    # New pass travellers for user 2's passes
    pass_traveller18 = PassTraveller(pass_id=8, user_id=2)  # Bob as traveller for pass8
    pass_traveller19 = PassTraveller(pass_id=8, user_id=3)  # Charlie as co-traveller for pass8
    pass_traveller20 = PassTraveller(pass_id=9, user_id=2)  # Bob as traveller for pass9
    pass_traveller21 = PassTraveller(pass_id=9, user_id=4)  # Dave as co-traveller for pass9
    pass_traveller22 = PassTraveller(pass_id=10, user_id=2)  # Bob as traveller for pass10
    pass_traveller23 = PassTraveller(pass_id=10, user_id=5)  # Test as co-traveller for pass10
    pass_traveller24 = PassTraveller(pass_id=11, user_id=2)  # Bob as traveller for pass11
    pass_traveller25 = PassTraveller(pass_id=11, user_id=6)  # Élise as co-traveller for pass11
    pass_traveller26 = PassTraveller(pass_id=12, user_id=2)  # Bob as traveller for pass12
    pass_traveller27 = PassTraveller(pass_id=12, user_id=7)  # Hans as co-traveller for pass12

    # Updated pass travellers for user 2's passes with 3-10 users per pass
    # Pass 8: 5 users
    pass_traveller18 = PassTraveller(pass_id=8, user_id=2)  # Bob as traveller for pass8
    pass_traveller19 = PassTraveller(pass_id=8, user_id=3)  # Charlie as co-traveller for pass8
    pass_traveller20 = PassTraveller(pass_id=8, user_id=4)  # Dave as co-traveller for pass8
    pass_traveller21 = PassTraveller(pass_id=8, user_id=5)  # Test as co-traveller for pass8
    pass_traveller22 = PassTraveller(pass_id=8, user_id=6)  # Élise as co-traveller for pass8
    
    # Pass 9: 8 users
    pass_traveller23 = PassTraveller(pass_id=9, user_id=2)  # Bob as traveller for pass9
    pass_traveller24 = PassTraveller(pass_id=9, user_id=4)  # Dave as co-traveller for pass9
    pass_traveller25 = PassTraveller(pass_id=9, user_id=7)  # Hans as co-traveller for pass9
    pass_traveller26 = PassTraveller(pass_id=9, user_id=8)  # Sofia as co-traveller for pass9
    pass_traveller27 = PassTraveller(pass_id=9, user_id=9)  # Liam as co-traveller for pass9
    pass_traveller28 = PassTraveller(pass_id=9, user_id=10)  # Alessandro as co-traveller for pass9
    pass_traveller29 = PassTraveller(pass_id=9, user_id=11)  # Yuki as co-traveller for pass9
    pass_traveller30 = PassTraveller(pass_id=9, user_id=12)  # Wei as co-traveller for pass9
    
    # Pass 10: 3 users
    pass_traveller31 = PassTraveller(pass_id=10, user_id=2)  # Bob as traveller for pass10
    pass_traveller32 = PassTraveller(pass_id=10, user_id=5)  # Test as co-traveller for pass10
    pass_traveller33 = PassTraveller(pass_id=10, user_id=13)  # Priya as co-traveller for pass10
    
    # Pass 11: 10 users
    pass_traveller34 = PassTraveller(pass_id=11, user_id=2)  # Bob as traveller for pass11
    pass_traveller35 = PassTraveller(pass_id=11, user_id=6)  # Élise as co-traveller for pass11
    pass_traveller36 = PassTraveller(pass_id=11, user_id=14)  # Mohammed as co-traveller for pass11
    pass_traveller37 = PassTraveller(pass_id=11, user_id=15)  # Olga as co-traveller for pass11
    pass_traveller38 = PassTraveller(pass_id=11, user_id=16)  # Lars as co-traveller for pass11
    pass_traveller39 = PassTraveller(pass_id=11, user_id=17)  # Astrid as co-traveller for pass11
    pass_traveller40 = PassTraveller(pass_id=11, user_id=18)  # Johan as co-traveller for pass11
    pass_traveller41 = PassTraveller(pass_id=11, user_id=19)  # Elena as co-traveller for pass11
    pass_traveller42 = PassTraveller(pass_id=11, user_id=20)  # Kazimierz as co-traveller for pass11
    pass_traveller43 = PassTraveller(pass_id=11, user_id=21)  # Sven as co-traveller for pass11
    
    # Pass 12: 7 users
    pass_traveller44 = PassTraveller(pass_id=12, user_id=2)  # Bob as traveller for pass12
    pass_traveller45 = PassTraveller(pass_id=12, user_id=7)  # Hans as co-traveller for pass12
    pass_traveller46 = PassTraveller(pass_id=12, user_id=22)  # Isabella as co-traveller for pass12
    pass_traveller47 = PassTraveller(pass_id=12, user_id=23)  # Carlos as co-traveller for pass12
    pass_traveller48 = PassTraveller(pass_id=12, user_id=24)  # Aisha as co-traveller for pass12
    pass_traveller49 = PassTraveller(pass_id=12, user_id=25)  # Hassan as co-traveller for pass12
    pass_traveller50 = PassTraveller(pass_id=12, user_id=26)  # Nina as co-traveller for pass12

    preset1 = Preset(preset_name="Work Trip", user_id=1)
    preset2 = Preset(preset_name="Vacation Mode", user_id=1)
    preset3 = Preset(preset_name="Conference Travel", user_id=2)
    preset4 = Preset(preset_name="Weekend Getaway", user_id=3)
    preset5 = Preset(preset_name="Family Visit", user_id=4)
    
    # New presets for user ID 2
    preset6 = Preset(preset_name="Business Meeting", user_id=2)
    preset7 = Preset(preset_name="Team Building", user_id=2)
    preset8 = Preset(preset_name="Client Visit", user_id=2)
    preset9 = Preset(preset_name="Project Kickoff", user_id=2)
    preset10 = Preset(preset_name="Annual Retreat", user_id=2)

    preset_traveller1 = PresetTraveller(preset_id=1, user_id=1)
    preset_traveller2 = PresetTraveller(preset_id=1, user_id=2)
    preset_traveller3 = PresetTraveller(preset_id=2, user_id=1)
    preset_traveller4 = PresetTraveller(preset_id=3, user_id=2)
    preset_traveller5 = PresetTraveller(preset_id=4, user_id=3)
    preset_traveller6 = PresetTraveller(preset_id=5, user_id=4)
    preset_traveller7 = PresetTraveller(preset_id=5, user_id=1)

    # New preset travellers for user ID 2's presets
    # Preset 6: 4 users
    preset_traveller8 = PresetTraveller(preset_id=6, user_id=2)  # Bob as creator
    preset_traveller9 = PresetTraveller(preset_id=6, user_id=3)  # Charlie as traveller
    preset_traveller10 = PresetTraveller(preset_id=6, user_id=4)  # Dave as traveller
    preset_traveller11 = PresetTraveller(preset_id=6, user_id=5)  # Test as traveller
    
    # Preset 7: 6 users
    preset_traveller12 = PresetTraveller(preset_id=7, user_id=2)  # Bob as creator
    preset_traveller13 = PresetTraveller(preset_id=7, user_id=6)  # Élise as traveller
    preset_traveller14 = PresetTraveller(preset_id=7, user_id=7)  # Hans as traveller
    preset_traveller15 = PresetTraveller(preset_id=7, user_id=8)  # Sofia as traveller
    preset_traveller16 = PresetTraveller(preset_id=7, user_id=9)  # Liam as traveller
    preset_traveller17 = PresetTraveller(preset_id=7, user_id=10)  # Alessandro as traveller
    
    # Preset 8: 3 users
    preset_traveller18 = PresetTraveller(preset_id=8, user_id=2)  # Bob as creator
    preset_traveller19 = PresetTraveller(preset_id=8, user_id=11)  # Yuki as traveller
    preset_traveller20 = PresetTraveller(preset_id=8, user_id=12)  # Wei as traveller
    
    # Preset 9: 5 users
    preset_traveller21 = PresetTraveller(preset_id=9, user_id=2)  # Bob as creator
    preset_traveller22 = PresetTraveller(preset_id=9, user_id=13)  # Priya as traveller
    preset_traveller23 = PresetTraveller(preset_id=9, user_id=14)  # Mohammed as traveller
    preset_traveller24 = PresetTraveller(preset_id=9, user_id=15)  # Olga as traveller
    preset_traveller25 = PresetTraveller(preset_id=9, user_id=16)  # Lars as traveller
    
    # Preset 10: 4 users
    preset_traveller26 = PresetTraveller(preset_id=10, user_id=2)  # Bob as creator
    preset_traveller27 = PresetTraveller(preset_id=10, user_id=17)  # Astrid as traveller
    preset_traveller28 = PresetTraveller(preset_id=10, user_id=18)  # Johan as traveller
    preset_traveller29 = PresetTraveller(preset_id=10, user_id=19)  # Elena as traveller

    # New Table: UserTraveller (Tracks manually added travellers)
    user_traveller1 = UserTraveller(creator_user_id=1, traveller_id=2)
    user_traveller2 = UserTraveller(creator_user_id=1, traveller_id=3)
    user_traveller3 = UserTraveller(creator_user_id=3, traveller_id=1)
    user_traveller4 = UserTraveller(creator_user_id=4, traveller_id=2)

    user_traveller5 = UserTraveller(creator_user_id=2, traveller_id=4)
    
    # Additional user travellers for user ID 2
    user_traveller6 = UserTraveller(creator_user_id=2, traveller_id=5)  # Test as traveller
    user_traveller7 = UserTraveller(creator_user_id=2, traveller_id=6)  # Élise as traveller
    user_traveller8 = UserTraveller(creator_user_id=2, traveller_id=7)  # Hans as traveller
    user_traveller9 = UserTraveller(creator_user_id=2, traveller_id=8)  # Sofia as traveller
    user_traveller10 = UserTraveller(creator_user_id=2, traveller_id=9)  # Liam as traveller
    user_traveller11 = UserTraveller(creator_user_id=2, traveller_id=10)  # Alessandro as traveller
    user_traveller12 = UserTraveller(creator_user_id=2, traveller_id=11)  # Yuki as traveller
    user_traveller13 = UserTraveller(creator_user_id=2, traveller_id=12)  # Wei as traveller
    user_traveller14 = UserTraveller(creator_user_id=2, traveller_id=13)  # Priya as traveller
    user_traveller15 = UserTraveller(creator_user_id=2, traveller_id=14)  # Mohammed as traveller


    # Adding all records to the session
    db.session.add_all([
        user_sensitive1, user_sensitive2, user_sensitive3, user_sensitive4, user_sensitive5,
        user_sensitive6, user_sensitive7, user_sensitive8, user_sensitive9, user_sensitive10,
        user_sensitive11, user_sensitive12, user_sensitive13, user_sensitive14, user_sensitive15,
        user_sensitive16, user_sensitive17, user_sensitive18, user_sensitive19, user_sensitive20,
        user_sensitive21, user_sensitive22, user_sensitive23, user_sensitive24, user_sensitive25,
        user_sensitive26, user_sensitive27, user_sensitive28, user_sensitive29, user_sensitive30,
        user_sensitive31, user_sensitive32, user_sensitive33, user_sensitive34, user_sensitive35,
        user_sensitive36, user_sensitive37, user_sensitive38, user_sensitive39, user_sensitive40,
        user_sensitive41, user_sensitive42, user_sensitive43, user_sensitive44, user_sensitive45,
        user_sensitive46, user_sensitive47, user_sensitive48, user_sensitive49, user_sensitive50,
        user_sensitive51, user_sensitive52, user_sensitive53, user_sensitive54, user_sensitive55,
        vehicle1, vehicle2, vehicle3, vehicle4, vehicle5, vehicle6, vehicle7, vehicle8, vehicle9, vehicle10,
        vehicle11, vehicle12, vehicle13, vehicle14, vehicle15, vehicle16,
        user_vehicle1, user_vehicle2, user_vehicle3, user_vehicle4, user_vehicle5, user_vehicle6, user_vehicle7, user_vehicle8,
        user_vehicle9, user_vehicle10, user_vehicle11, user_vehicle12, user_vehicle13, user_vehicle14, user_vehicle15, user_vehicle16, user_vehicle17, user_vehicle18,
        pass1, pass2, pass3, pass4, pass5, pass6, pass7, pass8, pass9, pass10, pass11, pass12,
        pass_traveller1, pass_traveller2, pass_traveller3, pass_traveller4, pass_traveller5, 
        pass_traveller6, pass_traveller7, pass_traveller8, pass_traveller9, pass_traveller10, pass_traveller11, pass_traveller12, pass_traveller13, pass_traveller14, pass_traveller15, pass_traveller16, pass_traveller17,
        pass_traveller18, pass_traveller19, pass_traveller20, pass_traveller21, pass_traveller22, pass_traveller23, pass_traveller24, pass_traveller25, pass_traveller26, pass_traveller27,
        pass_traveller28, pass_traveller29, pass_traveller30, pass_traveller31, pass_traveller32, pass_traveller33, pass_traveller34, pass_traveller35, pass_traveller36, pass_traveller37,
        pass_traveller38, pass_traveller39, pass_traveller40, pass_traveller41, pass_traveller42, pass_traveller43, pass_traveller44, pass_traveller45, pass_traveller46, pass_traveller47,
        pass_traveller48, pass_traveller49, pass_traveller50,
        preset1, preset2, preset3, preset4, preset5, preset6, preset7, preset8, preset9, preset10,
        preset_traveller1, preset_traveller2, preset_traveller3, preset_traveller4, preset_traveller5, 
        preset_traveller6, preset_traveller7,
        preset_traveller8, preset_traveller9, preset_traveller10, preset_traveller11, preset_traveller12, preset_traveller13, preset_traveller14, preset_traveller15, preset_traveller16, preset_traveller17,
        preset_traveller18, preset_traveller19, preset_traveller20, preset_traveller21, preset_traveller22, preset_traveller23, preset_traveller24, preset_traveller25, preset_traveller26, preset_traveller27,
        preset_traveller28, preset_traveller29,
        user_traveller1, user_traveller2, user_traveller3, user_traveller4, user_traveller5, user_traveller6, user_traveller7, user_traveller8, user_traveller9, user_traveller10, user_traveller11, user_traveller12, user_traveller13, user_traveller14, user_traveller15
    ])


    # Commit the session to save the records to the database
    db.session.commit()
    print("✅ Mock data inserted successfully.")
