import socket
import sys
import time

import ayon_api

SENDER = f"example-processor-{socket.gethostname()}"

def main():
    while True:
        job = ayon_api.enroll_event_job(
            source_topic="entity.folder.status_changed",
            target_topic="my_cool_status_changed_event",
            sender=SENDER,
            description="someone changed something",
            max_retries=3,
        )

        if not job:
            time.sleep(5)
            continue

        src_job = ayon_api.get_event(job["dependsOn"])
        ayon_project_name = src_job["project"]

        ayon_api.update_event(
            job["id"],
            sender=SENDER,
            status="in_progress",
            project_name=ayon_project_name,
            description=f"doing some work on entity which was {src_job['payload']['newValue']}...",
        )

        time.sleep(10)

        ayon_api.update_event(
            job["id"],
            sender=SENDER,
            status="finished",
            project_name=ayon_project_name,
            description="My job is done!",
        )




if __name__ == "__main__":
    try:
        ayon_api.init_service()
        connected = True
    except Exception:
        sys.exit(1)

    main()
