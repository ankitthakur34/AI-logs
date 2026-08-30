from app.models.blocker_event import BlockerEvent


class PriorityService:

    DDL_COMMANDS = {
        "CREATE TABLE",
        "ALTER TABLE",
        "DROP TABLE",
        "TRUNCATE TABLE"
    }

    WRITE_COMMANDS = {
        "INSERT",
        "UPDATE",
        "DELETE"
    }

    @staticmethod
    def calculate_priority(
        event: BlockerEvent
    ) -> str:

        blocker_command = (
            event.blocker_command or ""
        ).strip().upper()

        waiter_command = (
            event.waiter_command or ""
        ).strip().upper()

        job = (
            event.job or ""
        ).strip().lower()

        # -------------------------------
        # CRITICAL
        # -------------------------------
        if (
            blocker_command in PriorityService.DDL_COMMANDS
            or waiter_command in PriorityService.DDL_COMMANDS
        ):
            return "CRITICAL"

        # -------------------------------
        # HIGH
        # -------------------------------
        if (
            blocker_command in PriorityService.WRITE_COMMANDS
            and "integrations/mssql" in job
        ):
            return "HIGH"

        # -------------------------------
        # MEDIUM
        # -------------------------------
        if (
            blocker_command == "SELECT"
            and waiter_command in PriorityService.WRITE_COMMANDS
        ):
            return "MEDIUM"

        # -------------------------------
        # LOW
        # -------------------------------
        return "LOW"