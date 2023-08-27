SmartGallery made with Django (Python framework) 
Using this project you can:
1. Create albums 
2. Upload images and add Youtube Video link
3. Edit albums and images (reorder, sort, set columns) 
4. Album visibility settings
5. Set gallery view - as grid or masonry
6. Process uploaded images (thumbnails and full size for lightbox gallery): change resolution and quality
7. Edit menu (reorder, rename) 
8. Add social networks links with Fontawesome icons and edit them (reorder, rename, change icons) 
9. Get EXIF data from images and show in lightbox view 
10. Get GEO infortmation, coords, view them in google maps.
11. Edit site settings - upload logo, set meta data, font styling for captions, text to footer.
12. Edit EXIF data
13. Timeline view (masonry) for all images on site ordered and titled by captured year
14. Admin part of the site translation - now English and Russian; can be change in General Settings of Site Settings section
15. Template editor with syntax highlight (HTML, CSS, JS) for Main (index) and About me pages, powered by CodeMirror
16. Use django, project built-in and custom tags with filters in Template Editor

Django itself need SECRET_KEY. It will try to get it in several steps:
1. Get it from Envrironment variable of OS with key: SECRET_KEY
2. Get it from .env file located near settings.py with secret_prod = 'Your key'
3. Or take default value from settings.py 
To generate secret key use https://djecrety.ir or https://miniwebtool.com/django-secret-key-generator/ .

You can start using this prorject with docker-compose or from scratches via systemd+gunicon, nginx and certbot.
Steps to setup project from scratches:
1. git clone https://github.com/endlessnights/photogallery.git
2. cd photogallery directory and create venv using: 'python3 -m venv venv'
3. Activate venv 'source /venv/bin/activate' then update your pip and install all requirements: 'pip install --upgrade pip', 'pip install -r core/requirements.txt'
4. Then create sqlite db file with tables: 'python manage.py makemigrations smartgallery' then 'manage.py migrate'

If you start with docker or manual setup django will automatically create demo-user (don't forget to change username, password and e-mail):
- login: root
- password: RootPassword


[Support developer on Patreon](https://patreon.com/legeminus)

Some screenshots:

<img width="1680" alt="image" src="https://github.com/endlessnights/photogallery/assets/17062701/657dcf45-c441-405a-981e-8a43e8a5622f">
<img width="1680" alt="image" src="https://github.com/endlessnights/photogallery/assets/17062701/63845045-4eaf-40d9-8086-84a0199e8277">
<img width="1679" alt="image" src="https://github.com/endlessnights/photogallery/assets/17062701/3a5abf7b-a76a-4f5f-bd1d-ee82bde2c9d1">

