import os
import base64
from pathlib import Path
import shutil

def image_to_base64():
    """
    Convert images to base64
    """
    img_path = Path("./img/")
    b64_path = Path("b64_img")

    for file_path in img_path.glob("*"):
        if file_path.is_file():
            filename = file_path.name
            try:
                with open(file_path, "rb") as f:
                    image_data = f.read()
                b64_data = base64.b64encode(image_data).decode("utf-8")
                with open(b64_path / f"{filename}.b64", "w") as f:
                    f.write(b64_data)
            except Exception as e:
                print(f"Error converting {filename}: {e}")


base_folder = "b64_img"
if os.path.exists(base_folder):
    shutil.rmtree(base_folder)
os.mkdir(base_folder)

image_to_base64()

print("Done")