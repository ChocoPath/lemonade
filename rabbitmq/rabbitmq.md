## RabbitMQ Prometheus Exporter

### Overview

The RabbitMQ Prometheus Exporter script fetches queue metrics from a RabbitMQ instance and exposes them in a format that Prometheus can scrape. The exporter collects key metrics like the total number of messages, ready messages, and unacknowledged messages from each queue in the RabbitMQ instance.

### Features

*   **RabbitMQ Metrics:** Exports the following metrics for each queue:
    *   `rabbitmq_individual_queue_messages`: Total count of messages in a RabbitMQ queue.
    *   `rabbitmq_individual_queue_messages_ready`: Count of ready messages in a RabbitMQ queue.
    *   `rabbitmq_individual_queue_messages_unacknowledged`: Count of unacknowledged messages in a RabbitMQ queue.
*   **Prometheus Exporter:** Exposes a `/metrics` endpoint for Prometheus to scrape.
*   **Customizable:** Allows configuration via environment variables to adjust RabbitMQ connection details, scrape intervals, and port.

### Requirements

*   Python 3.x
*   `requests` library
*   `prometheus_client` library

### Environment Variables

The following environment variables can be used to configure the script:

| Environment Variable | Default Value | Description                                                                   |
| :------------------- | :------------ | :----------------------------------------------------------------------------- |
| `RABBITMQ_HOST`      | `localhost`   | The hostname or IP address of the RabbitMQ instance to scrape.                 |
| `RABBITMQ_USER`      | `guest`       | The RabbitMQ username for authentication.                                       |
| `RABBITMQ_PASSWORD`  | `guest`       | The RabbitMQ password for authentication.                                       |
| `PORT`               | `8000`        | The port on which the Prometheus exporter server will run.                      |
| `INTERVAL`           | `10`          | The scrape interval (in seconds) for fetching RabbitMQ queue metrics. |

### Prometheus Metrics

The exporter exposes three primary metrics related to RabbitMQ queues:

*   **`rabbitmq_individual_queue_messages`**
    *   Description: Total count of messages in each RabbitMQ queue.
    *   Labels:
        *   `host`: The hostname of the RabbitMQ server.
        *   `vhost`: The virtual host of the RabbitMQ queue.
        *   `name`: The name of the queue.
*   **`rabbitmq_individual_queue_messages_ready`**
    *   Description: Count of messages that are ready to be consumed in each RabbitMQ queue.
    *   Labels:
        *   `host`: The hostname of the RabbitMQ server.
        *   `vhost`: The virtual host of the RabbitMQ queue.
        *   `name`: The name of the queue.
*   **`rabbitmq_individual_queue_messages_unacknowledged`**
    *   Description: Count of messages in each RabbitMQ queue that are unacknowledged (i.e., not yet acknowledged by consumers).
    *   Labels:
        *   `host`: The hostname of the RabbitMQ server.
        *   `vhost`: The virtual host of the RabbitMQ queue.
        *   `name`: The name of the queue.

### How to Run the Exporter

1.  **Install Dependencies**

    Install the required Python libraries using pip:

    ```bash
    pip3 install requests prometheus_client
    ```

2.  **Set Environment Variables**

    Configure the environment variables for your RabbitMQ instance and desired settings:

    ```bash
    export RABBITMQ_HOST="your_rabbitmq_host"
    export RABBITMQ_USER="your_rabbitmq_user"
    export RABBITMQ_PASSWORD="your_rabbitmq_password"
    export PORT=8000
    export INTERVAL=10
    ```

3.  **Run the Exporter**

    Start the exporter script:

    ```bash
    python rabbitmq_prometheus_exporter.py
    ```

    This will start a web server on the port specified by `PORT` (default is 8000) where Prometheus can scrape the metrics from.

4.  **Access Metrics**

    To view the metrics, navigate to:

    ```bash
    http://localhost:8000/metrics
    ```

    You should see the metrics in the Prometheus text-based format.

### Example Metrics Output

The metrics exposed by the exporter may look like this (example):

![Alt text](/Screenshot%202025-01-06%20at%209.30.21 AM.png)


## Integration with Prometheus

If you have a running Prometheus instance, you can configure it to scrape the metrics from this exporter by adding the following to your `prometheus.yml` file:

```yaml
scrape_configs:
  - job_name: 'rabbitmq_exporter'
    static_configs:
      - targets: ['localhost:8000']
```