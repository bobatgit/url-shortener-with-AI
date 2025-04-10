import click
import os
import shutil
from pathlib import Path

@click.group()
def cli():
    """Environment management commands."""
    pass

@cli.command()
@click.argument('environment', type=click.Choice(['development', 'production', 'testing']))
def switch(environment):
    """Switch between different environments."""
    root_dir = Path(__file__).parent.parent
    env_file = root_dir / f'.env.{environment}'
    target_file = root_dir / '.env'
    
    if not env_file.exists():
        click.echo(f"Error: {env_file} does not exist")
        return
    
    shutil.copy(str(env_file), str(target_file))
    click.echo(f"Switched to {environment} environment")

@cli.command()
def current():
    """Show current environment."""
    root_dir = Path(__file__).parent.parent
    env_file = root_dir / '.env'
    
    if not env_file.exists():
        click.echo("No environment set")
        return
    
    with open(env_file) as f:
        for line in f:
            if line.startswith('ENVIRONMENT='):
                env = line.strip().split('=')[1]
                click.echo(f"Current environment: {env}")
                return
    
    click.echo("Environment not set in .env file")

if __name__ == '__main__':
    cli()