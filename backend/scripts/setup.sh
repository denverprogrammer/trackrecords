# Ensure Python 3.12 is installed
# If using pyenv
pyenv install 3.12.0
pyenv global 3.12.0

# Install pipenv if not already installed
pip install pipenv

# Create a virtual environment with Python 3.12
export PIPENV_VENV_IN_PROJECT=1; pipenv --python 3.12

# Activate the virtual environment
pipenv install
