"""
TTL Scheduler - Automatically cleans up expired links every hour.
"""

import sys
import time
import threading
from datetime import datetime
from typing import Optional

import schedule

from app.commands.cleanup import cleanup_expired_links
from app.config import config


class TTLScheduler:
    """Scheduler that runs cleanup every hour when TTL is enabled."""

    def __init__(self):
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

    def _run_cleanup(self):
        """Execute the cleanup job."""
        try:
            deleted = cleanup_expired_links()
            return deleted
        except Exception as e:
            print(f"❌ Cleanup job error: {e}")
            return 0

    def _scheduler_loop(self):
        """Main scheduler loop running in background thread."""
        self.is_running = True

        if config.APP_TTL_HOURS > 0:
            schedule.every(1).hour.do(self._run_cleanup)
            print("🔄 TTL cleanup scheduled: every 1 hour")
        else:
            print("ℹ️ TTL disabled, no cleanup scheduled")
            return

        print(f"🚀 TTL Scheduler started at {datetime.now().strftime('%H:%M:%S')}")

        try:
            while self.is_running and not self.stop_event.is_set():
                schedule.run_pending()
                time.sleep(60)
        finally:
            self.is_running = False
            print("🛑 TTL Scheduler stopped")

    def start(self):
        """Start the scheduler in background thread."""
        if self.is_running:
            return

        self.stop_event.clear()
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the scheduler."""
        if not self.is_running:
            return

        self.is_running = False
        self.stop_event.set()

        if self.thread:
            self.thread.join(timeout=5)

        schedule.clear()


# Singleton instance
_scheduler_instance: Optional[TTLScheduler] = None


def start_ttl_scheduler():
    """Start the TTL scheduler (called from main.py)."""
    global _scheduler_instance

    if config.APP_TTL_HOURS <= 0:
        return

    if _scheduler_instance is not None and _scheduler_instance.is_running:
        return

    _scheduler_instance = TTLScheduler()
    _scheduler_instance.start()


def stop_ttl_scheduler():
    """Stop the TTL scheduler."""
    global _scheduler_instance

    if _scheduler_instance is not None:
        _scheduler_instance.stop()
        _scheduler_instance = None


if __name__ == "__main__":

    print("🔧 Testing TTL Scheduler...")

    if config.APP_TTL_HOURS <= 0:
        print("❌ TTL is disabled in config (APP_TTL_HOURS <= 0)")
        sys.exit(1)

    scheduler = TTLScheduler()
    scheduler.start()

    try:
        time.sleep(300)
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    finally:
        scheduler.stop()