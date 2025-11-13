from PIL import Image
import exifread


def convert_to_degrees(value):
    d = float(value.values[0])
    m = float(value.values[1])
    s = float(value.values[2])
    return d + (m / 60.0) + (s / 3600.0)


def get_basic_metadata(image_path):
    with Image.open(image_path) as img:
        print(f"\n[Basic Image Information]")
        print(f"Image Format: {img.format}")
        print(f"Image Size: {img.size} pixels")
        print(f"Image Mode: {img.mode}\n")



def get_exif_metadata(image_path):
    with open(image_path, 'rb') as img_file:
        tags = exifread.process_file(img_file)

        print("[EXIF Metadata]")
        exif_keys = [
            "Image Make", "Image Model", "Image DateTime", 
            "EXIF FNumber", "EXIF ExposureTime", "EXIF ISOSpeedRatings", 
            "EXIF FocalLength", "EXIF LensModel"
        ]
        for tag in exif_keys:
            if tag in tags:
                print(f"{tag}: {tags[tag]}")

        # Extract GPS info if available
        print("\n[GPS Information]")
        gps_latitude = tags.get("GPS GPSLatitude")
        gps_latitude_ref = tags.get("GPS GPSLatitudeRef")
        gps_longitude = tags.get("GPS GPSLongitude")
        gps_longitude_ref = tags.get("GPS GPSLongitudeRef")

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = convert_to_degrees(gps_latitude)
            lon = convert_to_degrees(gps_longitude)

            if gps_latitude_ref.values[0] != 'N':
                lat = -lat
            if gps_longitude_ref.values[0] != 'E':
                lon = -lon

            print(f"Latitude: {lat:.6f}°")
            print(f"Longitude: {lon:.6f}°")
        else:
            print("No GPS data available.")



if __name__ == "__main__":
    image_path = input("Enter the path to the image: ")

    try:
        print("[+] Extracting basic metadata...")
        get_basic_metadata(image_path)

        print("\n[+] Extracting EXIF metadata...")
        get_exif_metadata(image_path)
    except FileNotFoundError:
        print("[-] Error: The specified file was not found.")



