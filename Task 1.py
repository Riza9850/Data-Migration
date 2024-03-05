import psycopg2  # Assuming PostgreSQL database.
import requests

# Data Extraction

def Consumer_Data_Extraction():
    # Connect to ABC Utility Company's database
    connection = psycopg2.connect(user="username",
                                  password="password",
                                  host="hostname",
                                  port="port",
                                  database="database_name")
    cursor = connection.cursor()

    # Example query to extract consumer data
    cursor.execute("SELECT consumer_id, name, address, contact_number, email_address, account_number, meter_number, tariff_plan, consumption_history, payment_status FROM consumer_data_table")
    Consumer_data = cursor.fetchall()

    # Close database connection
    cursor.close()
    connection.close()

    return Consumer_data

# Data Mapping

def Map_Data(Consumer_data):
    Mapped_Data = []
    
    # Itteration to map the data.

    for consumer in Consumer_data:
        Mapped_Data = {
            'Consumer ID': consumer[0],
            'First Name': consumer[1].split()[0],
            'Last Name': consumer[1].split()[1],
            'Address Line 1': consumer[2],
            'Address Line 2': '',
            'City': '',
            'State': '',
            'Zip Code': '',
            'Phone Number': consumer[3],
            'Email Address': consumer[4],
        }
        Mapped_Data.append(Mapped_Consumer)

    return Mapped_Data


# Transform the consumer_data 


def Transform_Data(Consumer_data):
    Transformed_Data = []
    for consumer in Consumer_data:
        consumer_id = consumer[0]
        name_parts = consumer[1].split()
        first_name = name_parts[0]
        last_name = name_parts[-1] if len(name_parts) > 1 else ''
        address_parts = consumer[2].split(',')
        address_line_1 = address_parts[0].strip() if address_parts else ''
        address_line_2 = address_parts[1].strip() if len(address_parts) > 1 else ''
        city_state_zip = address_parts[-1].strip() if len(address_parts) > 1 else ''
        city_state_zip_parts = city_state_zip.split()
        city = city_state_zip_parts[0]
        state = city_state_zip_parts[1]
        zip_code = city_state_zip_parts[2] if len(city_state_zip_parts) > 2 else ''
        contact_number = consumer[3]
        email_address = consumer[4]

        transformed_consumer = {
            'Consumer ID': consumer_id,
            'First Name': first_name,
            'Last Name': last_name,
            'Address Line 1': address_line_1,
            'Address Line 2': address_line_2,
            'City': city,
            'State': state,
            'Zip Code': zip_code,
            'Phone Number': contact_number,
            'Email Address': email_address,
        }
        Transformed_Data.append(transformed_consumer)

    return Transformed_Data


# Load the Transformed_Data in SMART360 platform.
# Using SMART360 API endpoint for data ingestion.

def load_data(Transformed_Data):
    api_endpoint = "https://smart360api.com/consumer/data"
    headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN', 'Content-Type': 'application/json'}
    
    for consumer in Transformed_Data:
        response = requests.post(api_endpoint, json=consumer, headers=headers)

        if response.status_code == 200:
            print(f"Data loaded successfully for Consumer ID: {consumer['Consumer ID']}")
        else:
            print(f"Failed to load data for Consumer ID: {consumer['Consumer ID']}")


def main():

    # Extaraction of data from MySQL Database
    consumer_data = Consumer_Data_Extraction()

    # Map Data to SMART360 format.
    map_data = Map_Data(Consumer_data)

    # Transform data into SMART360 Format
    transformed_data = Transform_Data(Consumer_data)

    # Loading the data into SMART360
    load_data(Transformed_Data)


if _name_ == "_main_":
    main()