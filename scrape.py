import requests
from PIL import Image
import io
import os

import asyncio
import aiohttp
from fpdf import FPDF



# you provide these
data = [
    # dict(name="we-summer1997", url="https://ia902504.us.archive.org/BookReader/BookReaderImages.php?id=wholeearthsummer00unse&itemPath=%2F34%2Fitems%2Fwholeearthsummer00unse&server=ia902504.us.archive.org&page=n{}_w1000.jpg"),
    dict(name="we-winter1997", url="https://ia801405.us.archive.org/BookReader/BookReaderImages.php?id=wholeearthwinter00unse&itemPath=%2F25%2Fitems%2Fwholeearthwinter00unse&server=ia801405.us.archive.org&page=n{}_medium.jpg"),
    dict(name="we-winter2000", url="https://ia601404.us.archive.org/BookReader/BookReaderImages.php?id=wholeearthwinter00unse_1&itemPath=%2F29%2Fitems%2Fwholeearthwinter00unse_1&server=ia601404.us.archive.org&page=n{}_medium.jpg"),
    dict(name="cybernetic-frontiers", url="https://ia801501.us.archive.org/BookReader/BookReaderImages.php?id=iicyberneticfron00unse&itemPath=%2F31%2Fitems%2Fiicyberneticfron00unse&server=ia801501.us.archive.org&page=n{}_medium.jpg"),
    dict(name="wer-summer1986", url="https://ia601405.us.archive.org/BookReader/BookReaderImages.php?id=wholeearthreview00unse_6&itemPath=%2F34%2Fitems%2Fwholeearthreview00unse_6&server=ia601405.us.archive.org&page=n{}_medium.jpg")
]


async def scrape_images(session, data):
    prev_image = None
    folder_name = data['name']
    os.makedirs(folder_name, exist_ok=True)

    url = data['url']
    page_num = 1
    while True:
        formatted_url = url.format(page_num)
        async with session.get(formatted_url) as response:
            image_bytes = io.BytesIO(await response.read())
            image = Image.open(image_bytes)

            if prev_image and image.tobytes() == prev_image.tobytes():
                break
            

            image.save(f"{folder_name}/image_{page_num:03d}.jpg")
            prev_image = image
        page_num += 1
        # break
    
    

    os.makedirs('pdfs', exist_ok=True)
    pdf = FPDF(unit="mm", format=[215.9, 279.4])  # Format changed to 8.5in x 11in (in mm)

    for i in range(1, page_num):
        pdf.add_page()

        image_path = f"{folder_name}/image_{i:03d}.jpg"

        image = Image.open(image_path)
        width, height = image.size

        # Convert pixel in millimeter. FPDF uses millimeter instead of pixel
        width, height = float(width * 0.264583), float(height * 0.264583)

        # Calculate aspect ratio
        aspect = width / height

        # Magazine size is 215.9 x 279.4 mm (8.5x11 inches)
        pdf_width = 215.9
        pdf_height = 279.4

        # Fit image to page size and maintain aspect ratio
        if aspect >= 1.0:
            # If the image is wide
            new_width = pdf_width
            new_height = new_width / aspect
        else:
            # If the image is tall
            new_height = pdf_height
            new_width = new_height * aspect

        x_offset = (pdf_width - new_width) / 2
        y_offset = (pdf_height - new_height) / 2

        # Add image to pdf page
        pdf.image(image_path, x=x_offset, y=y_offset, w=new_width, h=new_height)


    
    pdf.output(f"pdfs/{folder_name}.pdf", "F")


async def main(data_array):
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_images(session, data) for data in data_array]
        await asyncio.gather(*tasks)



asyncio.run(main(data))