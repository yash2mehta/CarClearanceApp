from flask_restx import fields

# Request Models
preset_with_users_model = {
    'preset_name': fields.String(required=True, description="Name of the preset"),
    'travellers': fields.List(fields.Nested({
        'passport_number': fields.String(required=True, description="Passport number of the traveller")
    }), required=True, description="List of travellers to add to the preset")
}

update_preset_travellers_model = {
    'preset_id': fields.Integer(required=True, description="ID of the preset to update"),
    'traveller_ids': fields.List(fields.Integer, required=True, description="List of traveller IDs to add to the preset")
}

update_preset_name_model = {
    'preset_id': fields.Integer(required=True, description="ID of the preset to update"),
    'preset_name': fields.String(required=True, description="New name for the preset")
}

# Response Models
preset_details_model = {
    'user_id': fields.Integer(readonly=True, description="ID of the user"),
    'presets': fields.List(fields.Nested({
        'preset_id': fields.Integer(readonly=True, description="ID of the preset"),
        'preset_name': fields.String(required=True, description="Name of the preset"),
        'passenger_count': fields.Integer(required=True, description="Number of passengers in the preset")
    }))
}

preset_with_users_response_model = {
    'preset_id': fields.Integer(readonly=True, description="ID of the preset"),
    'preset_name': fields.String(required=True, description="Name of the preset"),
    'created_by_user_id': fields.Integer(description="ID of the user who created the preset"),
    'travellers_added': fields.List(fields.Nested({
        'user_id': fields.Integer(readonly=True, description="ID of the traveller"),
        'first_name': fields.String(description="First name of the traveller"),
        'middle_name': fields.String(description="Middle name of the traveller"),
        'last_name': fields.String(description="Last name of the traveller"),
        'passport_number': fields.String(description="Passport number of the traveller")
    }), description="List of travellers added to the preset")
}

preset_summary_model = {
    'preset_id': fields.Integer(readonly=True, description="ID of the preset"),
    'preset_name': fields.String(required=True, description="Name of the preset"),
    'passenger_count': fields.Integer(required=True, description="Number of passengers in the preset"),
    'created_at': fields.DateTime(description="When the preset was created"),
    'updated_at': fields.DateTime(description="When the preset was last updated")
} 