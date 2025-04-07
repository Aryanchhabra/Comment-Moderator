import os
import json
import pandas as pd
from typing import Dict, List, Union, Tuple


class CommentLoader:
    """Class for loading and processing comment data from files."""
    
    def __init__(self, file_path: str):
        """
        Initialize the CommentLoader with a file path.
        
        Args:
            file_path: Path to the comment file (CSV or JSON)
        """
        self.file_path = file_path
        self.data = None
        self.file_extension = os.path.splitext(file_path)[1].lower()
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from the file path.
        
        Returns:
            DataFrame containing comment data
        
        Raises:
            ValueError: If file format is not supported
        """
        if self.file_extension == '.csv':
            self.data = pd.read_csv(self.file_path)
        elif self.file_extension == '.json':
            self.data = pd.read_json(self.file_path)
        else:
            raise ValueError(f"Unsupported file format: {self.file_extension}. Use CSV or JSON.")
        
        # Ensure required columns are present
        required_columns = ['comment_id', 'username', 'comment_text']
        for col in required_columns:
            if col not in self.data.columns:
                raise ValueError(f"Required column '{col}' not found in the data file.")
        
        return self.data
    
    def get_data_summary(self) -> Dict:
        """
        Generate a summary of the loaded comment data.
        
        Returns:
            Dictionary containing data summary
        """
        if self.data is None:
            self.load_data()
            
        return {
            'total_comments': len(self.data),
            'unique_users': self.data['username'].nunique(),
            'avg_comment_length': int(self.data['comment_text'].str.len().mean()),
            'sample_preview': self.data.head(3).to_dict('records')
        }
    
    def save_data(self, data: pd.DataFrame, output_path: str) -> str:
        """
        Save processed data to a file.
        
        Args:
            data: DataFrame to save
            output_path: Path to save the output file
            
        Returns:
            Path to the saved file
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save to the same format as the input file
        if self.file_extension == '.csv':
            data.to_csv(output_path, index=False)
        elif self.file_extension == '.json':
            data.to_json(output_path, orient='records', indent=2)
        
        return output_path


def load_comments(file_path: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Helper function to load comments and get summary.
    
    Args:
        file_path: Path to the comment file
        
    Returns:
        Tuple of (DataFrame, summary_dict)
    """
    loader = CommentLoader(file_path)
    data = loader.load_data()
    summary = loader.get_data_summary()
    return data, summary 