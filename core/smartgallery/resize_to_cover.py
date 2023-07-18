from io import BytesIO
from PIL import Image as PILImage
from django.core.files.uploadedfile import InMemoryUploadedFile


def resize_and_crop(self, size):
    # Open the original image using PIL
    pil_image = PILImage.open(self.image.path)

    # if pil_image.mode == 'RGBA':
    #     pil_image = pil_image.convert('RGB')

    # Get the size of the original image
    width, height = pil_image.size

    # Calculate the scale factor for zooming
    scale_factor = max(size[0] / width, size[1] / height)

    # Calculate the new size after zooming
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Resize the image using the calculated scale factor
    pil_image = pil_image.resize((new_width, new_height), PILImage.LANCZOS)

    # Calculate the crop box to cover the target size
    left = (new_width - size[0]) / 2
    top = (new_height - size[1]) / 2
    right = left + size[0]
    bottom = top + size[1]

    # Crop the image to cover the target size
    cropped_image = pil_image.crop((left, top, right, bottom))

    # Set the image quality (adjust this as needed, 0-100)
    image_quality = 80

    # Create a BytesIO object to store the resized and cropped image data
    resized_io = BytesIO()

    # Save the resized and cropped image to the BytesIO object
    cropped_image.save(resized_io, format='JPEG', quality=image_quality)

    # Create a new InMemoryUploadedFile with the resized and cropped image data
    resized_file = InMemoryUploadedFile(
        resized_io,
        None,
        f"{self.image.name.split('.')[0]}_thumbnail.jpg",  # Name the thumbnail image as per your requirement
        'image/jpeg',
        resized_io.getbuffer().nbytes,
        None
    )

    return resized_file
