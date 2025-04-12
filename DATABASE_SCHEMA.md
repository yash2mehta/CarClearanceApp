# Database Schema Documentation

## Database Tables

### Users Table

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| user_id | Integer | Primary Key, Auto-increment | Unique identifier for each user |
| first_name | String(50) | Not Null | User's first name |
| middle_name | String(50) | Nullable | User's middle name (optional) |
| last_name | String(50) | Not Null | User's last name |
| date_of_birth | Date | Not Null | User's date of birth |
| passport_issuing_country | String(255) | Not Null | Country that issued the passport |
| passport_number | String(20) | Not Null, Unique | Unique passport number of the user |
| passport_expiry | Date | Not Null | Passport expiration date |

### UserVehicle Table

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| user_vehicle_id | Integer | Primary Key, Auto-increment | Unique ID for each user-vehicle mapping |
| user_id | Integer | Foreign Key → UserSensitiveInformation.user_id, Not Null | References the user who owns the vehicle |
| vehicle_id | Integer | Foreign Key → Vehicle.vehicle_id, Not Null | References the associated vehicle |
| user_vehicle_model | String(100) | Not Null | Model of the vehicle assigned by the user |

### Vehicle Table

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| vehicle_id | Integer | Primary Key, Auto-increment | Unique identifier for each vehicle |
| vehicle_number | String(20) | Not Null, Unique | Vehicle's registration number |

### Pass Table

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| pass_id | Integer | Primary Key, Auto-increment | Unique identifier for each pass |
| creator_user_id | Integer | Foreign Key → UserSensitiveInformation.user_id, Not Null | User who created the pass |
| pass_date | DateTime | Not Null | Date when the pass is intended to be used |
| expiry_datetime | DateTime | Not Null | Expiry date and time of the pass |
| pass_utilized | Boolean | Not Null, Default: False | Status indicating if the pass has been used |

### PassTraveller Table

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| pass_traveller_id | Integer | Primary Key, Auto-increment | Unique ID for the pass-traveller relationship |
| pass_id | Integer | Foreign Key → Pass.pass_id, Not Null | References the associated pass |
| user_id | Integer | Foreign Key → UserSensitiveInformation.user_id, Not Null | References the traveller user |

### Preset Table

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| preset_id | Integer | Primary Key, Auto-increment | Unique identifier for the preset |
| preset_name | String(100) | Not Null | Name assigned to the preset |
| user_id | Integer | Foreign Key → UserSensitiveInformation.user_id, Not Null | Creator of the preset |

### PresetTraveller Table

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| preset_traveller_id | Integer | Primary Key, Auto-increment | Unique ID for the preset-traveller relationship |
| preset_id | Integer | Foreign Key → Preset.preset_id, Not Null | References the preset |
| user_id | Integer | Foreign Key → UserSensitiveInformation.user_id, Not Null | References the traveller user |

### UserTraveller Table

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| user_traveller_id | Integer | Primary Key, Auto-increment | Unique ID for user-traveller relationship |
| creator_user_id | Integer | Foreign Key → UserSensitiveInformation.user_id, Not Null | User who created this traveller list |
| traveller_id | Integer | Foreign Key → UserSensitiveInformation.user_id, Not Null | Referenced traveller (also a user record) | 