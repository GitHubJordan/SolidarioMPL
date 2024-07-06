#!/bin/bash

# Detect the operating system
OS=$(uname)
echo "Detected OS: $OS"

if [ "$OS" = "Linux" ]; then
    PYTHON=python3
    VENV_ACTIVATE=".venv/bin/activate"
elif [ "$OS" = "Darwin" ]; then
    # MacOS specific settings
    PYTHON=python3
    VENV_ACTIVATE="venv/bin/activate"
elif [ "$OS" = "MINGW32_NT" ] || [ "$OS" = "MINGW64_NT" ]; then
    # Windows specific settings
    PYTHON=python
    VENV_ACTIVATE="venv\\Scripts\\activate"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source $VENV_ACTIVATE

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found, skipping dependency installation."
fi

# Run Django commands
echo "Running: $PYTHON manage.py makemigrations"
$PYTHON manage.py makemigrations

echo "Running: $PYTHON manage.py migrate"
$PYTHON manage.py migrate

echo "Running: $PYTHON manage.py collectstatic --noinput"
$PYTHON manage.py collectstatic --noinput

echo "Running: $PYTHON manage.py runserver"
$PYTHON manage.py runserver
