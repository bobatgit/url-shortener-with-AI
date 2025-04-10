import click
from alembic.config import Config
from alembic import command
import os
import sys

# Add parent directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db

@click.group()
def cli():
    """Database management commands."""
    pass

@cli.command()
def init():
    """Initialize the database."""
    click.echo("Initializing database...")
    init_db()
    click.echo("Database initialized successfully.")

@cli.command()
def migrate():
    """Run database migrations."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    click.echo("Database migrations completed successfully.")

@cli.command()
def rollback():
    """Rollback the last database migration."""
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, "-1")
    click.echo("Database rollback completed successfully.")

if __name__ == "__main__":
    cli()