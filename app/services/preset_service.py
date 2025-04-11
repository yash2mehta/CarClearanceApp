from app import db
from app.api.models import Preset, PresetTraveller, UserSensitiveInformation
from app.utils.helpers import format_traveller_info

class PresetService:
    @staticmethod
    def create_preset(user_id, preset_name, travellers):
        """Create a new preset with travellers."""
        user = UserSensitiveInformation.query.get(user_id)
        if not user:
            return None, "User not found"

        if not preset_name:
            return None, "Preset name is required"

        new_preset = Preset(preset_name=preset_name, user_id=user_id)
        db.session.add(new_preset)
        db.session.commit()

        preset_id = new_preset.preset_id
        travellers_added = []

        for traveller in travellers:
            passport_number = traveller.get("passport_number")
            user_sensitive = UserSensitiveInformation.query.filter_by(passport_number=passport_number).first()
            if not user_sensitive:
                return None, f"Traveller with passport number {passport_number} not found"

            traveller_user_id = user_sensitive.user_id
            preset_traveller = PresetTraveller(preset_id=preset_id, user_id=traveller_user_id)
            db.session.add(preset_traveller)

            travellers_added.append(format_traveller_info(user_sensitive))

        db.session.commit()

        return {
            "preset_id": preset_id,
            "preset_name": preset_name,
            "created_by_user_id": user_id,
            "travellers_added": travellers_added
        }, None

    @staticmethod
    def get_preset_summary(user_id):
        """Get summary of all presets for a user."""
        user = UserSensitiveInformation.query.get(user_id)
        if not user:
            return None, "User not found"

        presets = Preset.query.filter_by(user_id=user_id).all()
        presets_list = []

        for p in presets:
            passenger_count = db.session.query(PresetTraveller).filter_by(preset_id=p.preset_id).count()
            presets_list.append({
                "preset_id": p.preset_id,
                "preset_name": p.preset_name,
                "passenger_count": passenger_count
            })

        return {
            "user_id": user_id,
            "presets": presets_list
        }, None

    @staticmethod
    def delete_preset(user_id, preset_id):
        """Delete a preset and its associated travellers."""
        user = UserSensitiveInformation.query.get(user_id)
        if not user:
            return None, "User not found"

        preset = Preset.query.get(preset_id)
        if not preset:
            return None, "Preset not found"

        if preset.user_id != user_id:
            return None, "This preset does not belong to the specified user"

        try:
            PresetTraveller.query.filter_by(preset_id=preset_id).delete()
            db.session.delete(preset)
            db.session.commit()
            return {"message": f"Preset with ID {preset_id} has been deleted successfully"}, None

        except Exception as e:
            db.session.rollback()
            return None, f"Error deleting preset: {str(e)}" 