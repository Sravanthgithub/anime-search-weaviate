import os
import re
import weaviate

# Weaviate Client Setup
client = weaviate.Client(url="http://localhost:8080")

def set_up_batch():
    """
    Prepare batching configuration to speed up deleting and importing data.
    """
    client.batch.configure(
        batch_size=100,
        dynamic=True,
        timeout_retries=3,
        callback=None,
    )

def clear_up_MyImages():
    """
    Remove all objects from the MyImages collection.
    This is useful if we want to rerun the import with different pictures.
    """
    try:
        with client.batch as batch:
            batch.delete_objects(
                class_name="MyImages",
                # same where operator as in the GraphQL API
                where={"operator": "NotEqual", "path": ["text"], "valueString": "x"},
                output="verbose",
            )
        print("All objects from MyImages collection have been deleted.")
    except Exception as e:
        print(f"Error while clearing MyImages collection: {e}")

def import_data():
    """
    Process all images in the [base64_images] folder and import them into the MyImages collection.
    """
    base64_images_folder = "./b64_img"

    try:
        with client.batch as batch:
            num_files = len(os.listdir(base64_images_folder))
            for idx, encoded_file_path in enumerate(os.listdir(base64_images_folder), 1):
                with open(os.path.join(base64_images_folder, encoded_file_path)) as file:
                    file_lines = file.readlines()

                base64_encoding = " ".join(file_lines).replace("\n", "").replace(" ", "")

                # remove .b64 to get the original file name
                image_file = encoded_file_path.replace(".b64", "")

                # remove image file extension and swap - for " " to get the breed name
                breed = re.sub(r".(jpg|jpeg|png)", "", image_file).replace("-", " ")

                # The properties from our schema
                data_properties = {"image": base64_encoding, "text": image_file}

                batch.add_data_object(data_properties, "MyImages")

                # Progress tracking
                print(f"Processed file {idx}/{num_files} - {image_file}")

        print("All objects have been uploaded to Weaviate.")
    except Exception as e:
        print(f"Error while importing data: {e}")

def main():
    # Streamlit Config
    print("Setting up batch processing...")
    set_up_batch()

    # Clearing existing data in the collection
    print("Clearing existing data in MyImages collection...")
    clear_up_MyImages()

    # Import data into Weaviate
    print("Importing data into MyImages collection...")
    import_data()

if __name__ == "__main__":
    main()
