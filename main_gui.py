"""
GUI application for PriceSpy Lite scraper
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime
import os

from scraper import ProductScraper
from data_processor import DataProcessor


class PriceSpyGUI:
    """Main GUI application for PriceSpy Lite"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PriceSpy Lite - Web Scraper")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variables
        self.num_pages_var = tk.IntVar(value=1)
        self.output_format_var = tk.StringVar(value="CSV")
        self.is_scraping = False
        
        # Create UI
        self._create_widgets()
        
    def _create_widgets(self):
        """Create all GUI widgets"""
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame, 
            text="🔍 PriceSpy Lite", 
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#ecf0f1")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Settings Frame
        settings_frame = tk.LabelFrame(
            content_frame, 
            text="Scraping Settings",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            padx=15,
            pady=15
        )
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Number of pages
        pages_frame = tk.Frame(settings_frame, bg="#ecf0f1")
        pages_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            pages_frame, 
            text="Number of pages to scrape:",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT)
        
        pages_spinbox = tk.Spinbox(
            pages_frame,
            from_=1,
            to=50,
            textvariable=self.num_pages_var,
            width=10,
            font=("Arial", 10)
        )
        pages_spinbox.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            pages_frame,
            text="(1-50 pages)",
            font=("Arial", 9),
            fg="#7f8c8d",
            bg="#ecf0f1"
        ).pack(side=tk.LEFT)
        
        # Output format
        format_frame = tk.Frame(settings_frame, bg="#ecf0f1")
        format_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            format_frame,
            text="Output format:",
            font=("Arial", 10),
            bg="#ecf0f1"
        ).pack(side=tk.LEFT)
        
        csv_radio = tk.Radiobutton(
            format_frame,
            text="CSV",
            variable=self.output_format_var,
            value="CSV",
            font=("Arial", 10),
            bg="#ecf0f1"
        )
        csv_radio.pack(side=tk.LEFT, padx=10)
        
        excel_radio = tk.Radiobutton(
            format_frame,
            text="Excel",
            variable=self.output_format_var,
            value="Excel",
            font=("Arial", 10),
            bg="#ecf0f1"
        )
        excel_radio.pack(side=tk.LEFT)
        
        # Target website info
        info_frame = tk.Frame(settings_frame, bg="#ecf0f1")
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(
            info_frame,
            text="Target: books.toscrape.com",
            font=("Arial", 9, "italic"),
            fg="#27ae60",
            bg="#ecf0f1"
        ).pack(side=tk.LEFT)
        
        # Start Button
        self.start_button = tk.Button(
            content_frame,
            text="🚀 Start Scraping",
            command=self._start_scraping,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            height=2,
            cursor="hand2"
        )
        self.start_button.pack(fill=tk.X, pady=(0, 15))
        
        # Progress Frame
        progress_frame = tk.LabelFrame(
            content_frame,
            text="Progress",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1",
            padx=15,
            pady=15
        )
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            progress_frame,
            text="Ready to start scraping...",
            font=("Arial", 10),
            bg="#ecf0f1",
            fg="#34495e"
        )
        self.status_label.pack(pady=5)
        
        # Log text area
        log_frame = tk.Frame(progress_frame, bg="#ecf0f1")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_frame,
            height=10,
            font=("Courier", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            yscrollcommand=scrollbar.set
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)
        
    def _log(self, message: str):
        """Add message to log area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def _update_progress(self, current: int, total: int, message: str):
        """Update progress bar and status"""
        progress = (current / total) * 100
        self.progress_bar['value'] = progress
        self.status_label.config(text=message)
        self._log(message)
        
    def _start_scraping(self):
        """Start the scraping process in a separate thread"""
        if self.is_scraping:
            messagebox.showwarning("Already Running", "Scraping is already in progress!")
            return
        
        # Validate inputs
        num_pages = self.num_pages_var.get()
        if num_pages < 1 or num_pages > 50:
            messagebox.showerror("Invalid Input", "Number of pages must be between 1 and 50")
            return
        
        # Disable button and clear log
        self.start_button.config(state=tk.DISABLED, text="Scraping...")
        self.log_text.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        self.is_scraping = True
        
        # Start scraping in a separate thread
        thread = threading.Thread(target=self._scrape_data, daemon=True)
        thread.start()
        
    def _scrape_data(self):
        """Perform the scraping operation (runs in separate thread)"""
        try:
            num_pages = self.num_pages_var.get()
            output_format = self.output_format_var.get()
            
            self._log("Initializing scraper...")
            scraper = ProductScraper(rate_limit=0.5, max_retries=3)
            
            self._log(f"Starting to scrape {num_pages} page(s)...")
            
            # Scrape products
            products = scraper.scrape_multiple_pages(
                num_pages,
                progress_callback=self._update_progress
            )
            
            if not products:
                self._log("No products found!")
                messagebox.showwarning("No Data", "No products were scraped. Please try again.")
                return
            
            self._log(f"Successfully scraped {len(products)} products")
            
            # Process data
            self._log("Processing and deduplicating data...")
            processor = DataProcessor()
            df = processor.process_products(products)
            
            # Get statistics
            stats = processor.get_summary_stats(df)
            self._log(f"Total unique products: {stats['total_products']}")
            if stats['total_products'] > 0:
                self._log(f"Average price: £{stats.get('avg_price', 0):.2f}")
                self._log(f"Price range: £{stats.get('min_price', 0):.2f} - £{stats.get('max_price', 0):.2f}")
                self._log(f"Average rating: {stats.get('avg_rating', 0):.1f}/5")
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if output_format == "CSV":
                filename = f"pricespy_results_{timestamp}.csv"
                success = processor.save_to_csv(df, filename)
            else:
                filename = f"pricespy_results_{timestamp}.xlsx"
                success = processor.save_to_excel(df, filename)
            
            if success:
                self._log(f"✓ Results saved to: {filename}")
                self.progress_bar['value'] = 100
                self.status_label.config(text="Scraping completed successfully!")
                
                # Show success message with option to open file
                result = messagebox.askyesno(
                    "Success!",
                    f"Successfully scraped {stats['total_products']} products!\n\n"
                    f"File saved: {filename}\n\n"
                    f"Would you like to open the output folder?"
                )
                
                if result:
                    # Open file location
                    import subprocess
                    folder_path = os.path.dirname(os.path.abspath(filename))
                    subprocess.Popen(['xdg-open', folder_path])
            else:
                self._log("✗ Failed to save results")
                messagebox.showerror("Error", "Failed to save results to file")
                
        except Exception as e:
            self._log(f"✗ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        finally:
            # Re-enable button
            self.is_scraping = False
            self.start_button.config(state=tk.NORMAL, text="🚀 Start Scraping")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PriceSpyGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
