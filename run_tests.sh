#!/bin/bash

# prompting the user to input the full path to the project directory
echo "Enter the full path to the project directory (up to aether-blog-application): "
read project_path

# checking if the directory exists
if [ ! -d "$project_path" ]; then
    echo "Error: The directory '$project_path' does not exist. Please provide the correct path."
    exit 1
fi

# changing to the project directory
cd "$project_path" || exit

# asking for the virtual environment path
echo "Enter the full path to your virtual environment directory: "
read venv_path

# checking if the virtual environment exists
if [ ! -d "$venv_path" ]; then
    echo "Error: The virtual environment directory '$venv_path' does not exist."
    exit 1
fi

# activating the virtual environment
. "$venv_path/bin/activate"

# creating the test-logs directory if it doesn't exist
test_logs_dir="$project_path/test-logs"
if [ ! -d "$test_logs_dir" ]; then
    echo "Creating test-logs directory..."
    mkdir -p "$test_logs_dir"
fi

# running Django tests and save output to logs
python3 manage.py test > "$test_logs_dir/test_results.log" 2>&1

