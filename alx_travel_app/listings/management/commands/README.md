# alx_travel_app_0x00

## 0. Database Modeling and Data Seeding in Django

### Objective
Define the database models, create serializers for API data representation, and implement a management command to seed the database.

### Instructions

#### Duplicate Project:
Duplicate the project `alx_travel_app` to `alx_travel_app_0x00`.

#### Create Models:
In `listings/models.py`, define `Listing`, `Booking`, and `Review` models with appropriate fields and relationships.

#### Set Up Serializers:
Create serializers in `listings/serializers.py` for `Listing` and `Booking`.

#### Implement Seeders:
Create a management command in `listings/management/commands/seed.py` to populate the database with sample listings data.

#### Run Seed Command:
Test the seeder by running the command:

```bash
python manage.py seed

