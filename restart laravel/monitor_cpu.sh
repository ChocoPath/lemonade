#!/bin/bash

# Configuration
CPU_THRESHOLD=80
SERVICE_NAME="php-fpm" 
LARAVEL_PROJECT_PATH="/mini-laravel-project/" # Replace with your project path
RESTART_COMMAND="sudo systemctl restart $SERVICE_NAME" # Command to restart the service

# Get CPU usage
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')

# Check if CPU usage exceeds the threshold
if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
  echo "$(date): CPU usage is $CPU_USAGE%, exceeding the threshold of $CPU_THRESHOLD%."

  #Optional: Log the high CPU usage to a file for later analysis.
  echo "$(date): High CPU usage detected: $CPU_USAGE%" >> /var/log/high_cpu_monitor.log

  # Optional: check if artisan queue:work is running and restart it if it is running
  if pgrep -f "artisan queue:work" > /dev/null
  then
    echo "$(date): Restarting artisan queue:work"
    php $LARAVEL_PROJECT_PATH/artisan queue:restart
  fi

  # Restart the service
  echo "$(date): Restarting $SERVICE_NAME..."
  $RESTART_COMMAND

  if [[ $? -eq 0 ]]; then
    echo "$(date): $SERVICE_NAME restarted successfully."
  else
    echo "$(date): ERROR: Failed to restart $SERVICE_NAME."
    #Add more error handling, such as sending an email alert.
    #Example:
    #mail -s "Error restarting service" "admin@example.com" <<< "Failed to restart $SERVICE_NAME on $(hostname)"
  fi
else
  echo "$(date): CPU usage is $CPU_USAGE%, within acceptable limits."
fi