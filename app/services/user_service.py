from app import db
from app.api.models import UserSensitiveInformation
from datetime import datetime

class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        return UserSensitiveInformation.query.get(user_id)

    @staticmethod
    def get_user_by_passport(passport_number):
        return UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()

    @staticmethod
    def update_user_profile(user_id, data):
        user = UserSensitiveInformation.query.get(user_id)
        if not user:
            return None

        try:
            if 'first_name' in data and data['first_name']:
                user.first_name = data['first_name']

            if 'middle_name' in data and data['middle_name']:
                user.middle_name = data['middle_name']

            if 'last_name' in data and data['last_name']:
                user.last_name = data['last_name']

            if 'date_of_birth' in data and data['date_of_birth']:
                user.date_of_birth = datetime.strptime(data['date_of_birth'], "%Y-%m-%d").date()

            if 'nationality' in data and data['nationality']:
                user.passport_issuing_country = data['nationality']

            if 'passport_expiry' in data and data['passport_expiry']:
                user.passport_expiry = datetime.strptime(data['passport_expiry'], "%Y-%m-%d").date()

            if 'passport_number' in data and data['passport_number']:
                user.passport_number = data['passport_number']

            db.session.commit()
            return user

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_user_profile(user_id):
        user = UserSensitiveInformation.query.get(user_id)
        if not user:
            return None

        return {
            "user_id": user_id,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": user.last_name,
            "date_of_birth": user.date_of_birth.strftime("%Y-%m-%d") if user.date_of_birth else None,
            "nationality": user.passport_issuing_country,
            "passport_expiry": user.passport_expiry.strftime("%Y-%m-%d") if user.passport_expiry else None,
            "passport_number": user.passport_number
        } 