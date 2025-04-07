import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional


class ReportGenerator:
    """Class for generating reports from analyzed comment data."""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the ReportGenerator.
        
        Args:
            data: DataFrame containing analyzed comments
        """
        self.data = data
        
        # Ensure required columns are present
        required_columns = ['comment_id', 'username', 'comment_text', 
                           'is_offensive', 'offense_type', 'explanation']
        
        for col in required_columns:
            if col not in self.data.columns:
                raise ValueError(f"Required column '{col}' not found in the data.")
                
    def generate_summary_report(self) -> Dict:
        """
        Generate a summary report of offensive comments.
        
        Returns:
            Dictionary containing report data
        """
        # Filter offensive comments
        offensive_comments = self.data[self.data['is_offensive'] == True]
        
        # Count by offense type
        offense_type_counts = offensive_comments['offense_type'].value_counts().to_dict()
        
        # Calculate percentages
        total_comments = len(self.data)
        offensive_count = len(offensive_comments)
        
        # Get most severe offensive comments
        # Severity order: threat > hate_speech > harassment > profanity > misinformation > toxicity
        severity_order = {
            'threat': 6,
            'hate_speech': 5,
            'harassment': 4, 
            'profanity': 3,
            'misinformation': 2,
            'toxicity': 1,
            None: 0  # For non-offensive comments
        }
        
        # Add severity score
        self.data['severity_score'] = self.data['offense_type'].map(severity_order)
        
        # Get top offensive comments
        top_offensive = self.data[self.data['is_offensive'] == True].sort_values(
            by='severity_score', ascending=False).head(5)
        
        top_offensive_list = []
        for _, row in top_offensive.iterrows():
            top_offensive_list.append({
                'comment_id': row['comment_id'],
                'username': row['username'],
                'comment_text': row['comment_text'],
                'offense_type': row['offense_type'],
                'explanation': row['explanation']
            })
        
        # Generate summary
        summary = {
            'total_comments': total_comments,
            'offensive_comments': offensive_count,
            'offensive_percentage': round((offensive_count / total_comments) * 100, 2),
            'offense_type_breakdown': offense_type_counts,
            'top_offensive_comments': top_offensive_list,
            'pre_filtered_count': self.data['pre_filtered'].sum()
        }
        
        return summary
    
    def print_summary_report(self, summary: Optional[Dict] = None):
        """
        Print a formatted summary report to the console.
        
        Args:
            summary: Report summary (generated if not provided)
        """
        if summary is None:
            summary = self.generate_summary_report()
            
        print("\n" + "="*60)
        print("📊 COMMENT MODERATION SUMMARY REPORT 📊".center(60))
        print("="*60)
        
        print(f"\n📝 TOTAL COMMENTS: {summary['total_comments']}")
        print(f"🚨 OFFENSIVE COMMENTS: {summary['offensive_comments']} ({summary['offensive_percentage']}%)")
        
        if summary.get('pre_filtered_count', 0) > 0:
            print(f"⚡ PRE-FILTERED BY PROFANITY DETECTOR: {summary['pre_filtered_count']}")
            
        print("\n📋 OFFENSE TYPE BREAKDOWN:")
        
        for offense_type, count in summary['offense_type_breakdown'].items():
            print(f"  • {offense_type}: {count} comments")
            
        print("\n⚠️ TOP OFFENSIVE COMMENTS:")
        
        for i, comment in enumerate(summary['top_offensive_comments']):
            print(f"\n  {i+1}. [ID: {comment['comment_id']}] by {comment['username']}")
            print(f"     \"{comment['comment_text']}\"")
            print(f"     Type: {comment['offense_type']} | {comment['explanation']}")
            
        print("\n" + "="*60)
    
    def plot_offense_type_distribution(self, output_path: str = None):
        """
        Generate a bar chart showing offense type distribution.
        
        Args:
            output_path: Path to save the plot image (optional)
        """
        # Filter offensive comments
        offensive_comments = self.data[self.data['is_offensive'] == True]
        
        # Count by offense type
        offense_counts = offensive_comments['offense_type'].value_counts()
        
        # Set up the plot
        plt.figure(figsize=(10, 6))
        bars = sns.barplot(x=offense_counts.index, y=offense_counts.values, palette='viridis')
        
        # Add labels and title
        plt.title('Offensive Comment Distribution by Type', fontsize=15)
        plt.xlabel('Offense Type', fontsize=12)
        plt.ylabel('Number of Comments', fontsize=12)
        plt.xticks(rotation=45)
        
        # Add count labels on bars
        for i, count in enumerate(offense_counts.values):
            bars.text(i, count + 0.1, str(count), ha='center')
            
        plt.tight_layout()
        
        # Save if output path provided
        if output_path:
            plt.savefig(output_path)
            print(f"Plot saved to {output_path}")
            
        plt.close()
        
    def generate_html_report(self, output_path: str) -> str:
        """
        Generate an HTML report from the moderation results.
        
        Args:
            output_path: Path to save the HTML report
            
        Returns:
            Path to the saved HTML file
        """
        # Get summary data
        summary = self.generate_summary_report()
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vyorius Comment Moderation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; color: #333; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
                h2 {{ color: #3498db; margin-top: 30px; }}
                .summary-box {{ background-color: #f8f9fa; border-radius: 5px; padding: 20px; margin-bottom: 30px; }}
                .stats {{ display: flex; justify-content: space-around; flex-wrap: wrap; }}
                .stat-card {{ background-color: white; border-radius: 5px; padding: 15px; margin: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); min-width: 200px; text-align: center; }}
                .stat-card h3 {{ margin-top: 0; color: #2c3e50; }}
                .stat-card .number {{ font-size: 24px; font-weight: bold; color: #3498db; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px 15px; border-bottom: 1px solid #ddd; text-align: left; }}
                th {{ background-color: #3498db; color: white; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .offense-type {{ display: inline-block; padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; color: white; }}
                .hate_speech {{ background-color: #e74c3c; }}
                .harassment {{ background-color: #9b59b6; }}
                .profanity {{ background-color: #e67e22; }}
                .threat {{ background-color: #c0392b; }}
                .misinformation {{ background-color: #f39c12; }}
                .toxicity {{ background-color: #d35400; }}
                .footer {{ margin-top: 50px; text-align: center; font-size: 14px; color: #7f8c8d; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Vyorius Comment Moderation Report</h1>
                
                <div class="summary-box">
                    <h2>Summary Statistics</h2>
                    <div class="stats">
                        <div class="stat-card">
                            <h3>Total Comments</h3>
                            <div class="number">{summary['total_comments']}</div>
                        </div>
                        <div class="stat-card">
                            <h3>Offensive Comments</h3>
                            <div class="number">{summary['offensive_comments']} ({summary['offensive_percentage']}%)</div>
                        </div>
                        <div class="stat-card">
                            <h3>Pre-Filtered</h3>
                            <div class="number">{summary.get('pre_filtered_count', 0)}</div>
                        </div>
                    </div>
                </div>
                
                <h2>Offense Type Breakdown</h2>
                <table>
                    <tr>
                        <th>Offense Type</th>
                        <th>Count</th>
                        <th>Percentage</th>
                    </tr>
        """
        
        # Add offense type rows
        for offense_type, count in summary['offense_type_breakdown'].items():
            percentage = round((count / summary['offensive_comments']) * 100, 1) if summary['offensive_comments'] > 0 else 0
            html_content += f"""
                    <tr>
                        <td><span class="offense-type {offense_type}">{offense_type}</span></td>
                        <td>{count}</td>
                        <td>{percentage}%</td>
                    </tr>
            """
            
        # Add top offensive comments section
        html_content += """
                </table>
                
                <h2>Top Offensive Comments</h2>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Comment</th>
                        <th>Offense Type</th>
                        <th>Explanation</th>
                    </tr>
        """
        
        # Add comment rows
        for comment in summary['top_offensive_comments']:
            html_content += f"""
                    <tr>
                        <td>{comment['comment_id']}</td>
                        <td>{comment['username']}</td>
                        <td>{comment['comment_text']}</td>
                        <td><span class="offense-type {comment['offense_type']}">{comment['offense_type']}</span></td>
                        <td>{comment['explanation']}</td>
                    </tr>
            """
            
        # Close HTML
        html_content += """
                </table>
                
                <div class="footer">
                    <p>Generated by Vyorius Comment Moderation Tool</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return output_path 