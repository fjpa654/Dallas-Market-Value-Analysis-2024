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
            if not multipolygon:
                continue  # Skip rows where the multipolygon data is missing or blank

            # Extracting all the coordinate pairs from the multipolygon string
            points = re.findall(r'(\-?\d+\.\d+) (\-?\d+\.\d+)', multipolygon)
            for idx, point in enumerate(points):
                longitude, latitude = point
                writer.writerow({
                    'Geoid': geoid,
                    'PointOrder': idx + 1,
                    'Latitude': latitude,
                    'Longitude': longitude
                })

if __name__ == '__main__':
    input_csv = 'Dallas_Market_Value_Analysis_20241120.csv'
    output_csv = 'Processed_Multipolygon_Data.csv'
    process_multipolygon(input_csv, output_csv)
