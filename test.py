user_sensitive_info_model = api.model('UserSensitiveInformation', {
    'user_id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True, description="First name of the user"),
    'middle_name': fields.String(description="Middle name of the user"),
    'last_name': fields.String(required=True, description="Last name of the user"),
    'date_of_birth': fields.Date(required=True, description="Date of birth of the user"),
    'passport_issuing_country': fields.String(required=True, description="Nationality or country that issued the passport"),
    'passport_number': fields.String(required=True, description="Unique passport number"),
    'passport_expiry': fields.Date(required=True, description="Expiry date of the passport")
})





user_vehicle_model = api.model('UserVehicle', {
    'user_vehicle_id': fields.Integer(readonly=True),
    'user_id': fields.Integer(required=True, description="ID of the user who owns the vehicle"),
    'vehicle_id': fields.Integer(required=True, description="ID of the vehicle"),
    'user_vehicle_model': fields.String(required=True, description="Name the user has assigned to the vehicle aka model of the vehicle")
})

pass_model = api.model('Pass', {
    'pass_id': fields.Integer(readonly=True),
    'creator_user_id': fields.Integer(required=True, description="ID of the user who created the pass"),
    'pass_date': fields.DateTime(required=True, description="Date of the pass creation"),
    'expiry_datetime': fields.DateTime(required=True, description="Expiry date of the pass"),
    'pass_utilized': fields.Boolean(required=True, description="Whether the pass has been utilized or not")
})

pass_traveller_model = api.model('PassTraveller', {
    'pass_traveller_id': fields.Integer(readonly=True),
    'pass_id': fields.Integer(required=True, description="ID of the pass"),
    'user_id': fields.Integer(required=True, description="ID of the traveller using the pass")
})

preset_model = api.model('Preset', {
    'preset_id': fields.Integer(readonly=True),
    'preset_name': fields.String(required=True, description="Name of the preset"),
    'user_id': fields.Integer(required=True, description="ID of the user who created the preset")
})

preset_traveller_model = api.model('PresetTraveller', {
    'preset_traveller_id': fields.Integer(readonly=True),
    'preset_id': fields.Integer(required=True, description="ID of the preset"),
    'user_id': fields.Integer(required=True, description="ID of the traveller added to the preset")
})

user_traveller_model = api.model('UserTraveller', {
    'user_traveller_id': fields.Integer(readonly=True),
    'creator_user_id': fields.Integer(required=True, description="ID of the user who adds the traveller"),
    'traveller_id': fields.Integer(required=True, description="ID of the traveller added by the user")
})
