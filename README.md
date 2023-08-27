# SmartGallery: A Django-based Image Gallery

**SmartGallery** is a versatile image gallery project developed using the Django framework (Python). This project empowers you to:

- Create and manage albums
- Upload images and associate them with YouTube video links
- Modify albums and images (reorder, sort, adjust columns)
- Configure album visibility settings
- Choose between grid or masonry gallery views
- Process uploaded images (generate thumbnails and full-size images for lightbox galleries) by adjusting resolution and quality
- Customize the menu (reorder and rename items)
- Incorporate social media links with Font Awesome icons, allowing you to edit their order, labels, and icons
- Extract EXIF data from images and display it in the lightbox view
- Access GEO information and coordinates, viewable on Google Maps
- Edit site settings, including logo upload, meta data configuration, and font styling for captions and footer text
- Edit EXIF data directly
- Explore a timeline view (masonry layout) presenting all site images, organized and titled by the year they were taken
- Translate the admin section of the site; currently supports English and Russian languages, with the option to change this in the General Settings of the Site Settings section
- Benefit from a template editor equipped with syntax highlighting (HTML, CSS, JS) for the Main (index) and About Me pages, powered by CodeMirror
- Leverage Django's built-in and custom tags with filters within the Template Editor

## Setup and Configuration

To utilize Django, the project requires a **SECRET_KEY** for security. The following methods are employed to obtain this key:

1. Retrieve it from the operating system's environment variables using the key: **SECRET_KEY**
2. Obtain it from a `.env` file located near the `settings.py` file, using the format `secret_prod = 'Your key'`
3. Fall back to the default value specified in `settings.py`

To generate a secret key, you can use tools like [djecrety.ir](https://djecrety.ir) or [miniwebtool.com](https://miniwebtool.com/django-secret-key-generator/).

## Deployment Options

You can initiate the use of this project through either `docker-compose` or manual setup involving `systemd`, Gunicorn, NGINX, and Certbot. For manual setup, follow these steps:

1. Clone the repository: `git clone https://github.com/endlessnights/photogallery.git`
2. Navigate to the `photogallery` directory and create a virtual environment: `python3 -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Update pip and install requirements: `pip install --upgrade pip`, `pip install -r core/requirements.txt`
5. Generate an SQLite database with tables: `python manage.py makemigrations smartgallery`, followed by `python manage.py migrate`
6. If you're starting with Docker or manual setup, Django will automatically create a demo user. Remember to change the default username, password, and email:
   - **Login:** root
   - **Password:** RootPassword
  
7. NGINX Configuration:

<details>
<summary>Example of NGINX configuration</summary>

```nginx
server {
    server_name endlessnights.ru;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/smartgallery/core;           # Path to the static directory
    }
    
    location /media/ {
        root /var/www/smartgallery/core;           # Path to the media directory
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/run/smartgallery.sock;
    }
    
    client_max_body_size 300M;
    proxy_read_timeout 300;
    proxy_connect_timeout 300;
    proxy_send_timeout 300;
}
```

Support the developer on [Patreon](https://www.patreon.com/developerusername).


Some screenshots:

<img width="1680" alt="image" src="https://github.com/endlessnights/photogallery/assets/17062701/657dcf45-c441-405a-981e-8a43e8a5622f">
<img width="1680" alt="image" src="https://github.com/endlessnights/photogallery/assets/17062701/63845045-4eaf-40d9-8086-84a0199e8277">
<img width="1679" alt="image" src="https://github.com/endlessnights/photogallery/assets/17062701/31fd9156-9126-4230-9412-a2e9462cab09">
<img width="1679" alt="image" src="https://github.com/endlessnights/photogallery/assets/17062701/293e8ab0-2f25-4229-b86b-6ba8ef8941c6">

