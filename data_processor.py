"""
Data processing module for cleaning and exporting scraped product data
"""
import pandas as pd
import re
from typing import List, Dict


class DataProcessor:
    """Process and export scraped product data"""
    
    @staticmethod
    def normalize_price(price_str: str) -> float:
        """
        Convert price string to numeric value
        
        Args:
            price_str: Price string (e.g., '£51.77')
            
        Returns:
            Float value of price
        """
        if not price_str:
            return 0.0
        
        # Remove currency symbols and other non-numeric characters except decimal point
        cleaned = re.sub(r'[^\d.]', '', price_str)
        
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    @staticmethod
    def clean_availability(availability_str: str) -> str:
        """
        Clean availability string
        
        Args:
            availability_str: Raw availability string
            
        Returns:
            Cleaned availability status
        """
        if not availability_str:
            return "Unknown"
        
        # Extract just the status part (e.g., "In stock" from "\n    In stock\n")
        cleaned = availability_str.strip()
        
        # Simplify to just "In stock" or "Out of stock"
        if "in stock" in cleaned.lower():
            return "In stock"
        elif "out of stock" in cleaned.lower():
            return "Out of stock"
        else:
            return cleaned
    
    @staticmethod
    def deduplicate_products(products: List[Dict]) -> List[Dict]:
        """
        Remove duplicate products based on URL
        
        Args:
            products: List of product dictionaries
            
        Returns:
            Deduplicated list of products
        """
        if not products:
            return []
        
        # Use URL as the unique identifier
        seen_urls = set()
        unique_products = []
        
        for product in products:
            url = product.get('url')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_products.append(product)
            elif not url:
                # If no URL, keep it anyway (shouldn't happen with our scraper)
                unique_products.append(product)
        
        duplicates_removed = len(products) - len(unique_products)
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate products")
        
        return unique_products
    
    @staticmethod
    def process_products(products: List[Dict]) -> pd.DataFrame:
        """
        Process raw product data into a clean DataFrame
        
        Args:
            products: List of product dictionaries
            
        Returns:
            Processed pandas DataFrame
        """
        if not products:
            return pd.DataFrame()
        
        # Deduplicate first
        unique_products = DataProcessor.deduplicate_products(products)
        
        # Convert to DataFrame
        df = pd.DataFrame(unique_products)
        
        # Normalize price column
        if 'price' in df.columns:
            df['price_numeric'] = df['price'].apply(DataProcessor.normalize_price)
        
        # Clean availability column
        if 'availability' in df.columns:
            df['availability'] = df['availability'].apply(DataProcessor.clean_availability)
        
        # Reorder columns for better readability
        column_order = ['title', 'price', 'price_numeric', 'rating', 'availability', 'url']
        existing_columns = [col for col in column_order if col in df.columns]
        df = df[existing_columns]
        
        return df
    
    @staticmethod
    def save_to_csv(df: pd.DataFrame, filename: str) -> bool:
        """
        Save DataFrame to CSV file
        
        Args:
            df: DataFrame to save
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False
    
    @staticmethod
    def save_to_excel(df: pd.DataFrame, filename: str) -> bool:
        """
        Save DataFrame to Excel file
        
        Args:
            df: DataFrame to save
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Products')
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Products']
                for idx, col in enumerate(df.columns, 1):
                    max_length = max(
                        df[col].astype(str).apply(len).max(),
                        len(col)
                    )
                    # Add a little extra space
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[chr(64 + idx)].width = adjusted_width
            
            print(f"Data saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving to Excel: {e}")
            return False
    
    @staticmethod
    def get_summary_stats(df: pd.DataFrame) -> Dict[str, any]:
        """
        Get summary statistics from the DataFrame
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary with summary statistics
        """
        if df.empty:
            return {
                'total_products': 0,
                'avg_price': 0.0,
                'min_price': 0.0,
                'max_price': 0.0,
                'avg_rating': 0.0
            }
        
        stats = {
            'total_products': len(df)
        }
        
        if 'price_numeric' in df.columns:
            stats['avg_price'] = df['price_numeric'].mean()
            stats['min_price'] = df['price_numeric'].min()
            stats['max_price'] = df['price_numeric'].max()
        
        if 'rating' in df.columns:
            stats['avg_rating'] = df['rating'].mean()
        
        return stats
