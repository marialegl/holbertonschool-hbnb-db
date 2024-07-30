"""v1_add_initial_schema

Revision ID: a4b4cdecc30e
Revises: 
Create Date: 2024-07-30 07:20:11.883705

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a4b4cdecc30e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        -- Create table for User
        CREATE TABLE "user" (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT FALSE,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    op.execute("""
        -- Create table for Host
        CREATE TABLE host (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES "user"(id)
        );
    """)

    op.execute("""
        -- Create table for Guest
        CREATE TABLE guest (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES "user"(id)
        );
    """)

    op.execute("""
        -- Create table for Place
        CREATE TABLE place (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            address VARCHAR(255),
            city_id INT NOT NULL,
            latitude FLOAT,
            longitude FLOAT,
            number_of_rooms INT,
            number_of_bathrooms INT,
            price_per_night FLOAT,
            max_guests INT,
            host_id INT NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (city_id) REFERENCES city(id),
            FOREIGN KEY (host_id) REFERENCES host(id)
        );
    """)

    op.execute("""
        -- Create table for Amenities
        CREATE TABLE amenities (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            place_id INT NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (place_id) REFERENCES place(id)
        );
    """)

    op.execute("""
        -- Create table for Country
        CREATE TABLE country (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    op.execute("""
        -- Create table for State
        CREATE TABLE state (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            country_id INT NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (country_id) REFERENCES country(id)
        );
    """)

    op.execute("""
        -- Create table for City
        CREATE TABLE city (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            state_id INT NOT NULL,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (state_id) REFERENCES state(id)
        );
    """)

    op.execute("""
        -- Create table for Review
        CREATE TABLE review (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            place_id INT NOT NULL,
            feedback TEXT,
            rating INT,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deleted BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES "user"(id),
            FOREIGN KEY (place_id) REFERENCES place(id)
        );
    """)


def downgrade() -> None:
    op.execute("""DROP TABLE IF EXISTS review;""")
    op.execute("""DROP TABLE IF EXISTS city;""")
    op.execute("""DROP TABLE IF EXISTS state;""")
    op.execute("""DROP TABLE IF EXISTS country;""")
    op.execute("""DROP TABLE IF EXISTS amenities;""")
    op.execute("""DROP TABLE IF EXISTS place;""")
    op.execute("""DROP TABLE IF EXISTS guest;""")
    op.execute("""DROP TABLE IF EXISTS host;""")
    op.execute("""DROP TABLE IF EXISTS "user";""")
