"""Command-line interface for crules."""
from pathlib import Path
import logging
import click
from . import config, file_ops

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

@click.command()
@click.argument('languages', nargs=-1, required=False)
@click.option('-f', '--force', is_flag=True, help='Force overwrite existing files')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@click.option('-l', '--list', 'show_list', is_flag=True, help='List available language rules')
@click.option('-s', '--setup', 'setup_dirs', is_flag=True, help='Create necessary directories and files')
def main(languages: tuple[str, ...], force: bool, verbose: bool, show_list: bool, setup_dirs: bool) -> None:
    """Generate .cursorrules file combining global and language-specific rules."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Handle --setup option
        if setup_dirs:
            logger.info("Setting up crules directory structure...")
            if file_ops.setup_directory_structure(verbose):
                logger.info("Setup complete!")
            else:
                raise click.ClickException("Setup failed")
            return

        # Load configuration
        cfg = config.load_config()
        global_rules = Path(cfg['global_rules_path']).expanduser()
        lang_rules_dir = Path(cfg['language_rules_dir']).expanduser()
        
        # Handle --list option
        if show_list:
            file_ops.list_available_languages(lang_rules_dir)
            return
            
        # Require languages argument if not listing or setting up
        if not languages:
            raise click.UsageError("Please specify at least one language or use --list to see available options")
        
        # Suggest setup if directories don't exist
        if not global_rules.exists() or not lang_rules_dir.exists():
            raise click.ClickException(
                "Required directories not found. Run 'crules --setup' to create them."
            )
            
        # Validate files exist
        if not file_ops.check_files_exist(global_rules, lang_rules_dir, languages):
            raise click.ClickException("Required files not found")
            
        # Handle existing files
        if not file_ops.backup_existing_rules(force):
            return
            
        # Combine rules
        content = file_ops.combine_rules(
            global_rules, 
            lang_rules_dir,
            languages,
            cfg['delimiter']
        )
        
        # Write output file
        output_file = Path(".cursorrules")
        output_file.write_text(content)
        logger.info(f"Successfully created {output_file}")
        
    except Exception as e:
        raise click.ClickException(str(e)) 