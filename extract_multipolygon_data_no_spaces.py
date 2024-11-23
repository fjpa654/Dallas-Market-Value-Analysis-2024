import csv
import re
import sys

def process_multipolygon(input_file, output_file):
    # Set a high but safe limit for field size
    max_int = 2147483647
    csv.field_size_limit(max_int)

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['Geoid', 'PointOrder', 'Latitude', 'Longitude']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Use the actual column name with BOM prefix
        geom_column = '\ufeffthe_geom'  # Corrected column name with BOM

        for row in reader:
            geoid = row['geoid']
            multipolygon = row[geom_column]  # Use the BOM-prefixed column name

            # Skip rows where geoid is missing or multipolygon data is just blank spaces
            if not geoid.strip() or not multipolygon.strip():
                continue

            # Extracting all the coordinate pairs from the multipolygon string
            points = re.findall(r'(-?\d+\.\d+)\s+(-?\d+\.\d+)', multipolygon)
            if not points:
                continue  # Skip rows with no coordinate data

            point_order = 1
            for point in points:
                longitude, latitude = point
                try:
                    # Convert longitude and latitude to float and floor to 4 decimal places
                    longitude_float = float(longitude)
                    latitude_float = float(latitude)
                    floored_longitude = f'{longitude_float:.4f}'
                    floored_latitude = f'{latitude_float:.4f}'

                    writer.writerow({
                        'Geoid': geoid,
                        'PointOrder': point_order,
                        'Latitude': floored_latitude,
                        'Longitude': floored_longitude
                    })
                    point_order += 1
                except ValueError:
                    # Skip if longitude or latitude are not valid numbers
                    continue

if __name__ == '__main__':
    input_csv = 'Dallas_Market_Value_Analysis_20241120.csv'
    output_csv = 'Processed_Multipolygon_Data_no_spaces.csv'
    process_multipolygon(input_csv, output_csv)
