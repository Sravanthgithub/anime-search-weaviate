import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import weaviate

# Weaviate Client Setup
client = weaviate.Client(url="http://localhost:8080")

# Function to search for similar images in Weaviate
def search_similar_images(img_str):
    sourceImage = {"image": img_str}

    weaviate_results = client.query.get(
        "MyImages", ["text", "image"]
    ).with_near_image(sourceImage, encode=False).with_limit(2).do()

    return weaviate_results.get("data", {}).get("Get", {}).get("MyImages", [])

# Function to display similar images
def display_similar_images(similar_images):
    if not similar_images:
        st.warning("No similar images found in the database. Please upload something else.")
    else:
        images = [base64.b64decode(result.get("image")) for result in similar_images]

        with st.container():
            for idx, col in enumerate(st.columns(len(images))):
                col.image(images[idx], use_column_width=True)

def main():
    # Streamlit Config
    st.set_page_config(page_title="Image Search Engine")

    st.title("Image Search Engine")
    st.markdown("Upload an image and Weaviate vector database will find out a similar one")

    uploaded_img = st.file_uploader("Upload Your Image", type=["JPG", "PNG"], accept_multiple_files=False)

    if uploaded_img is not None:
        # Display the uploaded image
        img_pil = Image.open(uploaded_img)
        st.image(img_pil, use_column_width=True)
        st.markdown("---")

        # Convert the uploaded image to a base64 string
        bytes_data = uploaded_img.read()
        img_str = base64.b64encode(bytes_data).decode()

        # Search for similar images
        similar_images = search_similar_images(img_str)
        display_similar_images(similar_images)

if __name__ == "__main__":
    main()



