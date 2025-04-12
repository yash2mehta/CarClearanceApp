# API Documentation

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users/retrieve-name-by-passport` | Retrieve full name by passport number |
| GET | `/users/{user_id}/profile` | Get user profile info |
| PUT | `/users/{user_id}/update-profile` | Update user profile |
| PUT | `/users/{user_id}/update-traveller` | Update traveller info |

### Presets

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/presets/create` | Create a new preset |
| GET | `/presets/{user_id}/created-presets-with-users` | Get created presets with user info |
| GET | `/presets/{user_id}/created-presets-with-users-additional` | Get created presets with additional info |
| DELETE | `/presets/{user_id}/delete-preset` | Delete a preset |
| GET | `/presets/{user_id}/preset-summary` | Get summary of presets |
| PUT | `/presets/{user_id}/update-preset-travellers-passport` | Update preset travellers using passport numbers |

### Passes

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/passes/create` | Create a new pass |
| POST | `/passes/details` | Get details of a specific pass |
| PUT | `/passes/update` | Update a pass |
| DELETE | `/passes/{user_id}/delete-pass` | Delete a pass |
| GET | `/passes/{user_id}/details` | Get all passes with details |
| GET | `/passes/{user_id}/passes` | Retrieve current passes |
| GET | `/passes/{user_id}/passes-history-all` | Get all past passes |

### Travellers

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/travellers/batch-add-travellers` | Batch add travellers by passport |
| POST | `/travellers/{user_id}/add-traveller` | Add a traveller for the user |
| DELETE | `/travellers/{user_id}/delete-traveller-by-passport` | Delete a traveller by passport |
| GET | `/travellers/{user_id}/get-travellers` | Retrieve unassociated travellers |

### Vehicles

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/vehicles/{user_id}/add-vehicle` | Add a vehicle to the user |
| DELETE | `/vehicles/{user_id}/delete-vehicle-by-number` | Delete a vehicle by number |
| GET | `/vehicles/{user_id}/get-all-vehicles` | Retrieve all vehicles linked to a user | 