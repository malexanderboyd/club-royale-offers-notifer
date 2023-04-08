# parse arguments
param(
  [Parameter(Mandatory=$true)]
  [string]$check
)

# extract individual checks
$checks = $check.Split(" ")

Write-Host $checks

# Start the Docker containers
docker-compose up -d

# loop through the array and run the Python script for each item
foreach ($check in $checks) {
    $lastName, $rewardNumber = $check.split(',')
    & python main.py $lastname $rewardnumber

    # Activate the Python virtual environment
    $env:Path = "$pwd/venv/Scripts;" + $env:Path
    . $pwd/venv/Scripts/activate.ps1

    # Set the environment variables for the current pair
    $env:LASTNAME = $lastName
    $env:REWARDNUMBER = $rewardNumber

    # Run the Python script and print the output
    Write-Host "Launching $check"
    $output = python scraper.py
    Write-Host $output

    # Deactivate the Python virtual environment
    deactivate
}

# Stop the Docker containers
docker-compose down
