import click
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.utils.cleanup import cleanup_expired_urls
from app.utils.cache import url_cache

@click.group()
def cli():
    """Maintenance commands for URL shortener."""
    pass

@cli.command()
@click.option('--days', default=30, help='Delete URLs older than specified days')
def cleanup(days):
    """Clean up expired and old URLs."""
    session = SessionLocal()
    try:
        deleted = cleanup_expired_urls(session)
        click.echo(f"Cleaned up {deleted} expired URLs")
        
        # Clear cache
        url_cache.cache.clear()
        url_cache.access_times.clear()
        click.echo("Cache cleared")
    finally:
        session.close()

@cli.command()
def stats():
    """Show database statistics."""
    session = SessionLocal()
    try:
        total = session.execute("SELECT COUNT(*) FROM urls").scalar()
        active = session.execute(
            "SELECT COUNT(*) FROM urls WHERE expires_at > CURRENT_TIMESTAMP"
        ).scalar()
        expired = session.execute(
            "SELECT COUNT(*) FROM urls WHERE expires_at <= CURRENT_TIMESTAMP"
        ).scalar()
        
        click.echo(f"Total URLs: {total}")
        click.echo(f"Active URLs: {active}")
        click.echo(f"Expired URLs: {expired}")
    finally:
        session.close()

if __name__ == "__main__":
    cli()