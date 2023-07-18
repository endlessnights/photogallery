from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile


def resize_and_crop(self, long_side):
    # Open the original image using PIL
    pil_image = PILImage.open(self.image.path)

    # Get the size of the original image
    width, height = pil_image.size

    # Calculate the aspect ratio of the original image
    aspect_ratio = width / height

    # Calculate the new size based on the provided long side while preserving the aspect ratio
    if width > height:
        new_width = long_side
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = long_side
        new_width = int(new_height * aspect_ratio)

    # Resize the image using the new size while preserving the aspect ratio
    pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)

    # Set the image quality (adjust this as needed, 0-100)
    image_quality = 80

    # Create a BytesIO object to store the resized image data
    resized_io = BytesIO()

    # Save the resized image to the BytesIO object
    pil_image.save(resized_io, format='JPEG', quality=image_quality)

    # Create a new InMemoryUploadedFile with the resized image data
    resized_file = InMemoryUploadedFile(
        resized_io,
        None,
        f"{self.image.name.split('.')[0]}_resized.jpg",  # Name the resized image as per your requirement
        'image/jpeg',
        resized_io.getbuffer().nbytes,
        None
    )

    return resized_file
