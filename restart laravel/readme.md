## Usage
1.  **Save the script:** Save the script to a file, for example, `monitor_cpu.sh`.
2.  **Make it executable:** `chmod +x monitor_cpu.sh`
3.  **Configure:** Edit the script and set the correct values for the configuration variables at the top of the script.
4.  **Schedule it with cron:** Add a cron job to run the script periodically (e.g., every 5 minutes):

    ```bash
    crontab -e
    ```

    Add the following line to your crontab (adjust the path if necessary):

    ```
    */5 * * * * /monitor_cpu.sh
    ```