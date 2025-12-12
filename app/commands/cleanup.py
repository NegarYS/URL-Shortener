"""
Command for manually cleaning up expired links.
Run with: poetry run python -m app.commands.cleanup
"""

import sys
from datetime import datetime

from app.db.session import SessionLocal
from app.repositories.link_repository import LinkRepository


def cleanup_expired_links(verbose: bool = False) -> int:
    """Delete expired links and return count of deleted items."""
    db = SessionLocal()
    try:
        repo = LinkRepository(db)
        deleted_count = repo.delete_expired_links()

        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Deleted {deleted_count} expired links")

        return deleted_count

    except Exception as e:
        print(f"❌ Error: {e}")
        return 0

    finally:
        db.close()


if __name__ == "__main__":
    print("🧹 Cleaning up expired links...")

    deleted = cleanup_expired_links()

    if deleted > 0:
        print(f"✅ Cleanup complete. {deleted} link(s) deleted.")
    else:
        print("✅ No expired links found.")