# 🔬 Control Systems Laboratory Incident Reporting System

## 📋 Description

This project is a comprehensive incident reporting system designed specifically for control systems laboratories. It provides a streamlined platform for students, teachers, and laboratory staff to report, track, and manage incidents that occur during laboratory sessions.

## ✨ Features

- 🔐 **Secure Authentication**: Role-based access control system (student, teacher, administrator)
- 📝 **Incident Reporting**: Detailed forms for reporting issues with equipment or safety concerns
- 🔄 **Status Tracking**: Real-time tracking of incident resolution process
- 📊 **Dashboard**: Visual representation of incident statistics and trends
- 🔔 **Notifications**: Automated alerts for relevant stakeholders
- 📱 **Responsive Design**: Access the platform from any device
- 📑 **Documentation**: Built-in equipment manuals and safety procedures

## 🏗️ Architecture

The system follows a Model-View-Controller (MVC) architecture pattern:

```
control-systems-laboratories/
├── app/
│   ├── controllers/    # Route handlers and business logic
│   ├── models/         # Database models and data access layer
│   ├── services/       # Business services and utilities
│   ├── static/         # CSS, JavaScript, and images
│   ├── templates/      # HTML templates
│   └── __init__.py     # Application factory
├── static/             # CSS, JS, images
├── templates/          # HTML templates (si no están en app/)
├── .env                # Environment variables (no subir a git)
├── .gitignore          # Git ignore file
├── requirements.txt    # Project dependencies
├── Procfile            # Render start command
└── app.py              # Application entry point
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/jairdevl/control-systems-laboratories.git systems-laboratory-control
cd systems-laboratory-control
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root with the following variables:

```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

## 🚀 Running the Application

### Development Server

```bash
python app.py
```

### Despliegue en Render

1. Sube tu código a un repositorio en GitHub.
2. Ve a [https://dashboard.render.com/](https://dashboard.render.com/) y crea un nuevo Web Service.
3. Conecta tu repositorio y selecciona Python como entorno.
4. Agrega las siguientes variables de entorno en Render:
    - DB_HOST
    - DB_PORT
    - DB_NAME
    - DB_USER
    - DB_PASSWORD
5. Asegúrate de tener un archivo `Procfile` con:
    ```
    web: gunicorn app:app
    ```
6. Render detectará cambios automáticamente con cada push a GitHub.
7. Consulta los logs en Render si ocurre algún error.

```bash
pip install gunicorn
gunicorn -w 4 "run:create_app()"
```

## 📊 Usage

1. Register an account with your institutional email
2. Log in to the system
3. Navigate to the dashboard
4. To report an incident, click on "New Incident Report" and fill out the form
5. Track the status of your reports from the "My Reports" section
6. Administrators can manage users and view all reports from the admin panel

## 🧪 Testing

Run the test suite with:

```bash
python -m pytest
```

## 📚 Documentation

Extensive documentation is available in the `docs/` directory. For API documentation, visit `/api/docs` when the application is running.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

Project Maintainer - [jairenriquez30@gmail.com]

---s