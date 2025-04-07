import os
import sys
import click
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from vyorius_comment_moderator.comment_loader import CommentLoader
from vyorius_comment_moderator.content_moderator import ContentModerator
from vyorius_comment_moderator.report_generator import ReportGenerator


@click.group()
def cli():
    """Vyorius Comment Moderation Tool - Analyzes comments for offensive content."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output-file', '-o', type=click.Path(), help='Path to output file')
@click.option('--api-key', '-k', help='Gemini API key (overrides .env)')
@click.option('--use-profanity-filter/--no-profanity-filter', default=True, 
             help='Use profanity pre-filtering')
@click.option('--generate-html/--no-html', default=False, 
             help='Generate HTML report')
@click.option('--generate-plot/--no-plot', default=False, 
             help='Generate offense type distribution plot')
@click.option('--mock-mode/--api-mode', default=False,
             help='Run in mock mode without API calls (for demo/testing)')
def moderate(input_file, output_file, api_key, use_profanity_filter, generate_html, generate_plot, mock_mode):
    """Analyze comments in INPUT_FILE for offensive content."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Determine output file path if not provided
        if not output_file:
            input_path = Path(input_file)
            output_file = str(input_path.parent / f"{input_path.stem}_moderated{input_path.suffix}")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
        
        # Load comments
        click.echo(f"Loading comments from {input_file}...")
        loader = CommentLoader(input_file)
        comments_df = loader.load_data()
        summary = loader.get_data_summary()
        
        # Display summary
        click.echo(f"Loaded {summary['total_comments']} comments from {summary['unique_users']} unique users.")
        click.echo(f"Average comment length: {summary['avg_comment_length']} characters.")
        
        # Initialize moderator
        click.echo("Initializing content moderator...")
        if mock_mode:
            click.echo("⚠️ Running in MOCK MODE - No API calls will be made.")
            click.echo("This is for demonstration purposes only.")
        
        moderator = ContentModerator(api_key=api_key, 
                                     use_profanity_filter=use_profanity_filter,
                                     mock_mode=mock_mode)
        
        # Analyze comments
        click.echo("Analyzing comments for offensive content...")
        click.echo("This may take some time depending on the number of comments.")
        click.echo("Press Ctrl+C to stop at any time.")
        
        try:
            moderated_df = moderator.analyze_comments_batch(comments_df)
            
            # Save results
            click.echo(f"Saving moderation results to {output_file}...")
            loader.save_data(moderated_df, output_file)
            
            # Generate report
            report_generator = ReportGenerator(moderated_df)
            report_summary = report_generator.generate_summary_report()
            
            # Print report
            report_generator.print_summary_report(report_summary)
            
            # Generate HTML report if requested
            if generate_html:
                html_output = os.path.splitext(output_file)[0] + "_report.html"
                click.echo(f"Generating HTML report to {html_output}...")
                report_generator.generate_html_report(html_output)
            
            # Generate plot if requested
            if generate_plot:
                plot_output = os.path.splitext(output_file)[0] + "_plot.png"
                click.echo(f"Generating offense type distribution plot to {plot_output}...")
                report_generator.plot_offense_type_distribution(plot_output)
                
            click.echo("Moderation complete!")
                
        except KeyboardInterrupt:
            click.echo("\nOperation cancelled by user.")
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def preview(input_file):
    """Preview comments in INPUT_FILE without moderation."""
    try:
        # Load comments
        loader = CommentLoader(input_file)
        comments_df = loader.load_data()
        summary = loader.get_data_summary()
        
        # Display summary
        click.echo("\n=== Comment File Summary ===")
        click.echo(f"File: {input_file}")
        click.echo(f"Total comments: {summary['total_comments']}")
        click.echo(f"Unique users: {summary['unique_users']}")
        click.echo(f"Average comment length: {summary['avg_comment_length']} characters")
        
        # Preview comments
        click.echo("\n=== Comment Preview ===")
        for i, (_, row) in enumerate(comments_df.head(5).iterrows()):
            click.echo(f"{i+1}. [ID: {row['comment_id']}] {row['username']}: {row['comment_text']}")
            
        click.echo(f"\nShowing 5 of {summary['total_comments']} comments.")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli() 