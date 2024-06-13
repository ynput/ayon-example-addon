import socket
import sys
import time

import ayon_api


SENDER = f"example-service-{socket.gethostname()}"


def process_event():
    job = ayon_api.enroll_event_job(
        source_topic="entity.folder.status_changed",
        target_topic="example.approval_handler",
        sender=SENDER,
        description="Approved folder detected. Thinking...",
        max_retries=3,
        events_filter={
            "conditions": [
                {
                    "key": "payload/newValue",
                    "value": "Approved",
                }
            ]
        }
    )

    if not job:
        time.sleep(5)
        return

    src_job = ayon_api.get_event(job["dependsOn"])
    ayon_project_name = src_job["project"]

    ayon_api.update_event(
        job["id"],
        sender=SENDER,
        status="in_progress",
        project_name=ayon_project_name,
        description="Stand by. I am pretending to do something...",
    )

    time.sleep(2)

    ayon_api.update_event(
        job["id"],
        sender=SENDER,
        status="finished",
        project_name=ayon_project_name,
        description=f"Good job {src_job['user']}! Your folder has been approved.",
    )


def main():
    while True:
        process_event()


if __name__ == "__main__":
    try:
        ayon_api.init_service()
        connected = True
    except Exception:
        sys.exit(1)

    main()
