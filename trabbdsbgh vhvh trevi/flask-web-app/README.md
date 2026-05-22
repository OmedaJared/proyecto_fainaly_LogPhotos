# Flask Web Application

This is a Flask web application that allows users to register, log in, upload files, and manage their files through a user-friendly interface. The application is designed to be accessible from any device.

## Features

- User registration and authentication
- Password recovery functionality
- File upload and management
- Responsive design for mobile and desktop devices

## Project Structure

```
flask-web-app
├── src
│   ├── app.py                # Main entry point of the application
│   ├── config.py             # Configuration settings
│   ├── requirements.txt       # Required Python packages
│   ├── routes
│   │   ├── __init__.py       # Initializes the routes package
│   │   ├── auth.py           # Authentication-related routes
│   │   └── files.py          # File management routes
│   ├── utils
│   │   ├── __init__.py       # Initializes the utils package
│   │   ├── email.py          # Email utility functions
│   │   └── tokens.py         # Token generation and validation
│   └── templates
│       ├── base.html         # Base HTML template
│       ├── login.html        # Login page template
│       ├── register.html     # Registration page template
│       ├── recover.html      # Password recovery page template
│       ├── reset.html        # Password reset page template
│       └── dashboard.html     # User dashboard template
├── uploads                    # Directory for uploaded files
├── .env                       # Environment variables
├── .gitignore                 # Git ignore file
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-web-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r src/requirements.txt
   ```

4. Set up environment variables in the `.env` file.

## Usage

1. Run the application:
   ```
   python src/app.py
   ```

2. Access the application in your web browser at `http://127.0.0.1:5000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.