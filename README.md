# FomoSapiensCryptoDipHunter

FomoSapiensCryptoDipHunter is a crypto trading bot designed to assist in making trading decisions on the crypto exchange market. The bot integrates advanced technical indicators, real-time performance monitoring, and dynamic parameter adjustments to enhance trading efficiency. It provides an intuitive web interface for real-time analysis and sends telegram or email alerts for buy or sell signals.

## Features

- Multiple Independent Dip Hunters: Run different dip hunters with unique currencies and strategies.
- Automated Telegram or Email Notifications: Receive telegram or email alerts when entering buy or sell zones.
- Binance API Integration: Fetch real-time market data.
- Real-Time Monitoring: View live technical analysis.

## Installation

To install and set up the bot locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FomoSapiensCryptoDipHunter.git
cd FomoSapiensCryptoDipHunter
```

2. Set up a Python virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your environment variables by creating a .env file with your Binance API credentials, database URL, and telegram, email configuration.
```bash
APP_SECRET_KEY = 'your_turbo_secret_key'
CSRF_SECRET_KEY = 'your_total_secret_key'
GMAIL_USERNAME = 'gmail@username.com'
GMAIL_APP_PASSWORD="gmail_app_password"
TELEGRAM_API_SECRET="telegram_api_secret_key"
RECAPTCHA_PUBLIC_KEY = "recaptcha_public_key"
RECAPTCHA_PRIVATE_KEY = "recaptcha_private_key"
BINANCE_GENERAL_API_KEY='binance_general_api_key'
BINANCE_GENERAL_API_SECRET='binance_general_api_secret'
GOOGLE_CLIENT_ID='your_google_client_id'
GOOGLE_SECRET_KEY='your_google_secret_key'
# Add other required environment variables...
```

5. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Creade superuser
```bash
python manage.py createsuperuser
```

7. Run tests:
```bash
python manage.py test
```

8. Run the django application:
```bash
python manage.py runserver
```
or
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

9. Tweak, pimp, improve and have fun.

## Usage

### Once the bot is running, you can access the web interface to:
- Adjust parameters, settings, and trading strategies.
- Monitor real-time market data and performance.
- Receive email alerts for buy/sell signals.

## Technologies Used
- **Python**: The primary language used for development.
- **Django**: A web framework used for building the application interface.
- **Binance API**: For fetching market data and executing trades.
- **NumPy, Pandas and TALib**: Libraries used for implementing trading algorithms and data processing.

## Important! 
Familiarize yourself thoroughly with the source code. Understand its operation. Only then will you be able to customize and adjust scripts to your own needs, preferences, and requirements. Only then will you be able to use it correctly and avoid potential issues. Knowledge of the underlying code is essential for making informed decisions and ensuring the successful implementation of the bot for your specific use case. Make sure to review all components and dependencies before running the scripts.

Code created by me, with no small contribution from Dr. Google and Mr. ChatGPT.
Any comments welcome.

FomoSapiensCryptoDipHunter Project is under GNU General Public License Version 3, 29 June 2007