import os
import time
import pandas as pd
import random
import google.generativeai as genai
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from better_profanity import profanity


class ContentModerator:
    """Class for detecting offensive content in comments using Gemini API."""
    
    def __init__(self, api_key: str = None, use_profanity_filter: bool = True, mock_mode: bool = False):
        """
        Initialize the ContentModerator.
        
        Args:
            api_key: Gemini API key (defaults to environment variable)
            use_profanity_filter: Whether to use profanity pre-filtering
            mock_mode: Run in mock mode without calling the API (for demo/testing)
        """
        self.mock_mode = mock_mode
        
        # Load environment variables if API key not provided
        if api_key is None and not self.mock_mode:
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            
        if not api_key and not self.mock_mode:
            raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY in .env file or pass directly.")
        
        # Configure API if not in mock mode
        if not self.mock_mode:
            try:
                genai.configure(api_key=api_key)
                # Use the most capable model available for content moderation
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            except Exception as e:
                print(f"Warning: Error configuring Gemini API: {str(e)}")
                print("Falling back to mock mode for demonstration purposes.")
                self.mock_mode = True
        
        self.use_profanity_filter = use_profanity_filter
        
        # Initialize profanity filter if enabled
        if self.use_profanity_filter:
            profanity.load_censor_words()
            
        # Keywords for mock detection
        self.mock_keywords = {
            'hate_speech': ['foreigners', 'hate', 'discriminatory', 'racist', 'country'],
            'harassment': ['stupid', 'idiots', 'losers', 'fat', 'basement', 'kill yourself', 'sucks'],
            'profanity': ['f***', 'f**k', 'shit', 'damn'],
            'threat': ['shoot', 'kill', 'threat', 'die'],
            'misinformation': ['secretly', 'spying', 'government', 'sheeple', 'wake up'],
            'toxicity': ['annoying', 'waste', 'useless', 'bankrupt', 'violating']
        }
    
    def pre_filter_profanity(self, comment: str) -> bool:
        """
        Pre-filter comments for obvious profanity.
        
        Args:
            comment: Comment text to check
            
        Returns:
            Boolean indicating if profanity was detected
        """
        return profanity.contains_profanity(comment)
    
    def mock_analyze_comment(self, comment: str) -> Dict:
        """
        Analyze a comment using keyword matching instead of API.
        
        Args:
            comment: Comment text to analyze
            
        Returns:
            Dictionary with mock moderation results
        """
        comment_lower = comment.lower()
        
        # Check for offensive content using keywords
        is_offensive = False
        offense_type = None
        explanations = []
        
        for otype, keywords in self.mock_keywords.items():
            for keyword in keywords:
                if keyword.lower() in comment_lower:
                    is_offensive = True
                    # If multiple offense types match, choose the more severe one
                    if offense_type is None:
                        offense_type = otype
                        explanations.append(f"Contains potentially {otype} term '{keyword}'")
                    elif self.get_severity_score(otype) > self.get_severity_score(offense_type):
                        offense_type = otype
                        explanations.append(f"Contains potentially {otype} term '{keyword}'")
        
        # Additional heuristics for mockup
        if '!' in comment and any(term in comment_lower for term in ['hate', 'stupid', 'annoying', 'violating']):
            is_offensive = True
            if offense_type is None:
                offense_type = 'toxicity'
            explanations.append("Strong negative sentiment detected")
        
        return {
            'is_offensive': is_offensive,
            'offense_type': offense_type,
            'explanation': '; '.join(explanations) if explanations else "No offensive content detected",
            'pre_filtered': False,
            'mock_mode': True
        }
    
    def get_severity_score(self, offense_type: str) -> int:
        """
        Get severity score for offense type prioritization.
        
        Args:
            offense_type: Type of offense
            
        Returns:
            Severity score (higher is more severe)
        """
        severity_order = {
            'threat': 6,
            'hate_speech': 5,
            'harassment': 4, 
            'profanity': 3,
            'misinformation': 2,
            'toxicity': 1,
            None: 0
        }
        return severity_order.get(offense_type, 0)
    
    def analyze_comment(self, comment: str) -> Dict:
        """
        Analyze a comment for offensive content using Gemini API.
        
        Args:
            comment: Comment text to analyze
            
        Returns:
            Dictionary with moderation results
        """
        # Pre-filter with profanity detector if enabled
        pre_filtered = False
        if self.use_profanity_filter:
            pre_filtered = self.pre_filter_profanity(comment)
        
        # Skip API call if pre-filtered and confidently offensive
        if pre_filtered:
            return {
                'is_offensive': True,
                'offense_type': 'profanity',
                'explanation': 'Comment contains explicit profanity based on keyword matching',
                'pre_filtered': True,
                'mock_mode': False
            }
            
        # Use mock analysis if in mock mode
        if self.mock_mode:
            return self.mock_analyze_comment(comment)
        
        # Regular API flow - this should be the default path according to project requirements
        # Construct prompt for Gemini API
        prompt = f"""
        Analyze the following comment for offensive or inappropriate content:
        
        "{comment}"
        
        Determine if the comment is offensive or inappropriate (Yes/No).
        If yes, classify the offense type into ONE of these categories:
        - hate_speech (attacking specific groups)
        - harassment (targeting individuals)
        - profanity (explicit language)
        - threat (violent intentions)
        - misinformation (false claims)
        - toxicity (generally negative/harmful)
        
        Provide a brief explanation (max 20 words).
        
        Format your response as a JSON object with these keys:
        - is_offensive (boolean)
        - offense_type (string, one of the categories above, or null if not offensive)
        - explanation (string)
        """
        
        try:
            # Rate limiting to avoid hitting API limits
            time.sleep(0.5)
            
            # Call Gemini API
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # Parse response - handle both proper JSON and text formats
            try:
                # Try to parse as JSON if the model returned proper JSON
                import json
                if "{" in result_text and "}" in result_text:
                    result_json = json.loads(result_text.strip())
                    # Add pre_filtered flag
                    result_json['pre_filtered'] = False
                    result_json['mock_mode'] = False
                    return result_json
                else:
                    # Manual parsing if not in JSON format
                    is_offensive = "yes" in result_text.lower()
                    
                    # Extract offense type
                    offense_type = None
                    if is_offensive:
                        for otype in ["hate_speech", "harassment", "profanity", "threat", "misinformation", "toxicity"]:
                            if otype in result_text.lower():
                                offense_type = otype
                                break
                    
                    # Extract explanation
                    explanation = result_text.split("explanation")[-1].strip()
                    if ":" in explanation:
                        explanation = explanation.split(":", 1)[1].strip()
                    
                    return {
                        'is_offensive': is_offensive,
                        'offense_type': offense_type,
                        'explanation': explanation[:100],  # Limit length
                        'pre_filtered': False,
                        'mock_mode': False
                    }
            except Exception as e:
                # Only log the error and fall back to mock mode if necessary
                print(f"Error parsing API response: {str(e)}. Falling back to mock mode.")
                return self.mock_analyze_comment(comment)
                
        except Exception as e:
            # Only log the error and fall back to mock mode if necessary
            print(f"Error calling Gemini API: {str(e)}. Falling back to mock mode.")
            return self.mock_analyze_comment(comment)
    
    def analyze_comments_batch(self, comments_df: pd.DataFrame, 
                              text_column: str = 'comment_text',
                              batch_size: int = 10,
                              show_progress: bool = True) -> pd.DataFrame:
        """
        Analyze a batch of comments from a DataFrame.
        
        Args:
            comments_df: DataFrame containing comments
            text_column: Column name containing comment text
            batch_size: Number of comments to process before saving progress
            show_progress: Whether to print progress updates
            
        Returns:
            DataFrame with moderation results added
        """
        # Create result columns if they don't exist
        if 'is_offensive' not in comments_df.columns:
            comments_df['is_offensive'] = False
        if 'offense_type' not in comments_df.columns:
            comments_df['offense_type'] = None
        if 'explanation' not in comments_df.columns:
            comments_df['explanation'] = None
        if 'pre_filtered' not in comments_df.columns:
            comments_df['pre_filtered'] = False
        if 'mock_mode' not in comments_df.columns:
            comments_df['mock_mode'] = False
            
        total_comments = len(comments_df)
        
        if self.mock_mode and show_progress:
            print("\n⚠️ Running in MOCK MODE - using keyword matching instead of Gemini API")
            print("This is for demonstration purposes only.\n")
        
        # Process all comments
        for i, (index, row) in enumerate(comments_df.iterrows()):
            # Skip already processed comments
            if not pd.isna(row['explanation']):
                continue
                
            # Analyze the comment
            result = self.analyze_comment(row[text_column])
            
            # Update the DataFrame
            comments_df.at[index, 'is_offensive'] = result['is_offensive']
            comments_df.at[index, 'offense_type'] = result['offense_type']
            comments_df.at[index, 'explanation'] = result['explanation']
            comments_df.at[index, 'pre_filtered'] = result.get('pre_filtered', False)
            comments_df.at[index, 'mock_mode'] = result.get('mock_mode', False)
            
            # Show progress
            if show_progress and (i + 1) % batch_size == 0:
                print(f"Processed {i + 1}/{total_comments} comments ({((i + 1) / total_comments) * 100:.1f}%)")
                
        return comments_df 