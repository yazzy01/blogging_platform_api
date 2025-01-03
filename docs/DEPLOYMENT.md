# Deployment Guide

## Prerequisites

- Python 3.8+
- PostgreSQL (for production)
- Redis (for caching and background tasks)
- Environment variables configured

## Environment Variables

Create a `.env` file with the following variables:

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Social Authentication
GOOGLE_OAUTH2_KEY=your-google-oauth-client-id
GOOGLE_OAUTH2_SECRET=your-google-oauth-client-secret
GITHUB_KEY=your-github-oauth-client-id
GITHUB_SECRET=your-github-oauth-client-secret

# AWS S3 (for media storage)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=your-region
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blogging_platform_api.git
   cd blogging_platform_api
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Production Deployment

### Using Gunicorn and Nginx

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Create Gunicorn systemd service:
   ```bash
   sudo nano /etc/systemd/system/blogging_platform.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Blogging Platform API
   After=network.target

   [Service]
   User=yourusername
   Group=yourgroup
   WorkingDirectory=/path/to/blogging_platform_api
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/gunicorn core.wsgi:application --workers 3 --bind unix:/path/to/blogging_platform.sock

   [Install]
   WantedBy=multi-user.target
   ```

3. Configure Nginx:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           root /path/to/blogging_platform_api;
       }

       location /media/ {
           root /path/to/blogging_platform_api;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/blogging_platform.sock;
       }
   }
   ```

4. Enable and start services:
   ```bash
   sudo systemctl start blogging_platform
   sudo systemctl enable blogging_platform
   sudo systemctl restart nginx
   ```

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t blogging_platform_api .
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

## SSL Configuration

1. Install Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. Obtain SSL certificate:
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

## Monitoring

1. Install monitoring tools:
   ```bash
   pip install sentry-sdk
   ```

2. Configure Sentry in settings.py:
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration

   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[DjangoIntegration()],
       traces_sample_rate=1.0,
   )
   ```

## Backup

1. Create backup script:
   ```bash
   #!/bin/bash
   DATE=$(date +%Y-%m-%d_%H-%M-%S)
   BACKUP_DIR="/path/to/backups"
   
   # Database backup
   pg_dump dbname > $BACKUP_DIR/db_$DATE.sql
   
   # Media files backup
   tar -czf $BACKUP_DIR/media_$DATE.tar.gz /path/to/media
   
   # Remove backups older than 30 days
   find $BACKUP_DIR -type f -mtime +30 -exec rm {} \;
   ```

2. Schedule with cron:
   ```bash
   0 0 * * * /path/to/backup.sh
   ```

## Security Checklist

- [ ] Debug mode disabled
- [ ] Secret key changed
- [ ] ALLOWED_HOSTS configured
- [ ] SSL certificate installed
- [ ] Database password secure
- [ ] Media files protected
- [ ] Regular backups configured
- [ ] Monitoring set up
- [ ] Rate limiting enabled
- [ ] Security headers configured
