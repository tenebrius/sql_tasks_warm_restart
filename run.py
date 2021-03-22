from main import sqs, ScheduledShutdown

# Get the queue object
sqs.queue('emails').process_queue(shutdown_policy=ScheduledShutdown())