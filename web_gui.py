"""
Web-based GUI for PriceSpy Lite scraper (Flask alternative to Tkinter)
Works on all platforms including macOS with Tkinter issues
"""
from flask import Flask, render_template, request, jsonify, send_file
import os
from datetime import datetime
import threading
import time

from scraper import ProductScraper
from data_processor import DataProcessor


app = Flask(__name__)

# Global state for scraping progress
scraping_state = {
    'is_running': False,
    'progress': 0,
    'total_pages': 0,
    'current_page': 0,
    'status': 'Ready',
    'logs': [],
    'result_file': None,
    'stats': {}
}


def log_message(message):
    """Add a log message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    scraping_state['logs'].append(log_entry)
    print(log_entry)


def update_progress(current, total, message):
    """Update progress callback"""
    scraping_state['current_page'] = current
    scraping_state['total_pages'] = total
    scraping_state['progress'] = int((current / total) * 100)
    scraping_state['status'] = message
    log_message(message)


def scrape_task(num_pages, output_format):
    """Background scraping task"""
    try:
        scraping_state['is_running'] = True
        scraping_state['logs'] = []
        scraping_state['progress'] = 0
        scraping_state['result_file'] = None
        
        log_message("Initializing scraper...")
        scraper = ProductScraper(rate_limit=0.5, max_retries=3)
        
        log_message(f"Starting to scrape {num_pages} page(s)...")
        
        # Scrape products
        products = scraper.scrape_multiple_pages(
            num_pages,
            progress_callback=update_progress
        )
        
        if not products:
            log_message("No products found!")
            scraping_state['status'] = 'No products found'
            return
        
        log_message(f"Successfully scraped {len(products)} products")
        
        # Process data
        log_message("Processing and deduplicating data...")
        processor = DataProcessor()
        df = processor.process_products(products)
        
        # Get statistics
        stats = processor.get_summary_stats(df)
        scraping_state['stats'] = stats
        
        log_message(f"Total unique products: {stats['total_products']}")
        if stats['total_products'] > 0:
            log_message(f"Average price: £{stats.get('avg_price', 0):.2f}")
            log_message(f"Price range: £{stats.get('min_price', 0):.2f} - £{stats.get('max_price', 0):.2f}")
            log_message(f"Average rating: {stats.get('avg_rating', 0):.1f}/5")
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format == "csv":
            filename = f"pricespy_results_{timestamp}.csv"
            success = processor.save_to_csv(df, filename)
        else:
            filename = f"pricespy_results_{timestamp}.xlsx"
            success = processor.save_to_excel(df, filename)
        
        if success:
            scraping_state['result_file'] = filename
            log_message(f"✓ Results saved to: {filename}")
            scraping_state['progress'] = 100
            scraping_state['status'] = 'Completed successfully!'
        else:
            log_message("✗ Failed to save results")
            scraping_state['status'] = 'Failed to save results'
            
    except Exception as e:
        log_message(f"✗ Error: {str(e)}")
        scraping_state['status'] = f'Error: {str(e)}'
    
    finally:
        scraping_state['is_running'] = False


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/start', methods=['POST'])
def start_scraping():
    """Start scraping endpoint"""
    if scraping_state['is_running']:
        return jsonify({'error': 'Scraping already in progress'}), 400
    
    data = request.json
    num_pages = int(data.get('num_pages', 1))
    output_format = data.get('output_format', 'csv')
    
    if num_pages < 1 or num_pages > 50:
        return jsonify({'error': 'Number of pages must be between 1 and 50'}), 400
    
    # Start scraping in background thread
    thread = threading.Thread(target=scrape_task, args=(num_pages, output_format), daemon=True)
    thread.start()
    
    return jsonify({'status': 'started'})


@app.route('/api/status')
def get_status():
    """Get current scraping status"""
    return jsonify(scraping_state)


@app.route('/api/download/<filename>')
def download_file(filename):
    """Download result file"""
    if os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    # Create templates directory and HTML file
    os.makedirs('templates', exist_ok=True)
    
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PriceSpy Lite - Web Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: #2c3e50;
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.8;
            font-size: 0.9em;
        }
        
        .content {
            padding: 30px;
        }
        
        .settings-box {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .form-group input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: border-color 0.3s;
        }
        
        .form-group input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .radio-group {
            display: flex;
            gap: 20px;
        }
        
        .radio-group label {
            display: flex;
            align-items: center;
            cursor: pointer;
            font-weight: normal;
        }
        
        .radio-group input[type="radio"] {
            margin-right: 8px;
            cursor: pointer;
        }
        
        .btn-primary {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .progress-box {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 25px;
            margin-top: 20px;
        }
        
        .progress-bar-container {
            background: #e0e0e0;
            border-radius: 10px;
            height: 30px;
            overflow: hidden;
            margin-bottom: 15px;
        }
        
        .progress-bar {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        
        .status-text {
            text-align: center;
            color: #2c3e50;
            font-weight: 600;
            margin-bottom: 15px;
        }
        
        .log-box {
            background: #2c3e50;
            color: #ecf0f1;
            border-radius: 8px;
            padding: 15px;
            height: 200px;
            overflow-y: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.5;
        }
        
        .log-box::-webkit-scrollbar {
            width: 8px;
        }
        
        .log-box::-webkit-scrollbar-track {
            background: #34495e;
            border-radius: 4px;
        }
        
        .log-box::-webkit-scrollbar-thumb {
            background: #667eea;
            border-radius: 4px;
        }
        
        .stats-box {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-item {
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.5em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-size: 0.85em;
            color: #7f8c8d;
        }
        
        .download-btn {
            display: inline-block;
            margin-top: 15px;
            padding: 12px 30px;
            background: #27ae60;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: background 0.3s;
        }
        
        .download-btn:hover {
            background: #229954;
        }
        
        .info-badge {
            display: inline-block;
            background: #27ae60;
            color: white;
            padding: 5px 12px;
            border-radius: 5px;
            font-size: 0.85em;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 PriceSpy Lite</h1>
            <p>Web Scraper - No Installation Required</p>
            <span class="info-badge">Target: books.toscrape.com</span>
        </div>
        
        <div class="content">
            <div class="settings-box">
                <h2 style="margin-bottom: 20px; color: #2c3e50;">Scraping Settings</h2>
                
                <div class="form-group">
                    <label for="num_pages">Number of pages to scrape (1-50):</label>
                    <input type="number" id="num_pages" min="1" max="50" value="1">
                </div>
                
                <div class="form-group">
                    <label>Output format:</label>
                    <div class="radio-group">
                        <label>
                            <input type="radio" name="format" value="csv" checked>
                            CSV
                        </label>
                        <label>
                            <input type="radio" name="format" value="excel">
                            Excel
                        </label>
                    </div>
                </div>
                
                <button class="btn-primary" id="startBtn" onclick="startScraping()">
                    🚀 Start Scraping
                </button>
            </div>
            
            <div class="progress-box">
                <h3 style="margin-bottom: 15px; color: #2c3e50;">Progress</h3>
                
                <div class="progress-bar-container">
                    <div class="progress-bar" id="progressBar" style="width: 0%">0%</div>
                </div>
                
                <div class="status-text" id="statusText">Ready to start scraping...</div>
                
                <div id="statsBox" style="display: none;"></div>
                
                <div id="downloadBox" style="text-align: center; display: none;">
                    <a href="#" id="downloadLink" class="download-btn">📥 Download Results</a>
                </div>
                
                <div class="log-box" id="logBox">
                    Waiting to start...
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let statusInterval = null;
        
        function startScraping() {
            const numPages = parseInt(document.getElementById('num_pages').value);
            const format = document.querySelector('input[name="format"]:checked').value;
            const startBtn = document.getElementById('startBtn');
            
            if (numPages < 1 || numPages > 50) {
                alert('Number of pages must be between 1 and 50');
                return;
            }
            
            startBtn.disabled = true;
            startBtn.textContent = 'Scraping...';
            document.getElementById('downloadBox').style.display = 'none';
            document.getElementById('statsBox').style.display = 'none';
            
            fetch('/api/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({num_pages: numPages, output_format: format})
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    startBtn.disabled = false;
                    startBtn.textContent = '🚀 Start Scraping';
                } else {
                    // Start polling for status
                    statusInterval = setInterval(updateStatus, 500);
                }
            });
        }
        
        function updateStatus() {
            fetch('/api/status')
            .then(response => response.json())
            .then(data => {
                // Update progress bar
                const progressBar = document.getElementById('progressBar');
                progressBar.style.width = data.progress + '%';
                progressBar.textContent = data.progress + '%';
                
                // Update status text
                document.getElementById('statusText').textContent = data.status;
                
                // Update logs
                const logBox = document.getElementById('logBox');
                logBox.innerHTML = data.logs.join('<br>');
                logBox.scrollTop = logBox.scrollHeight;
                
                // Show stats if available
                if (data.stats && data.stats.total_products > 0) {
                    const statsHtml = `
                        <div class="stats-box">
                            <div class="stat-item">
                                <div class="stat-value">${data.stats.total_products}</div>
                                <div class="stat-label">Products</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">£${data.stats.avg_price ? data.stats.avg_price.toFixed(2) : '0.00'}</div>
                                <div class="stat-label">Avg Price</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">${data.stats.avg_rating ? data.stats.avg_rating.toFixed(1) : '0.0'}/5</div>
                                <div class="stat-label">Avg Rating</div>
                            </div>
                        </div>
                    `;
                    document.getElementById('statsBox').innerHTML = statsHtml;
                    document.getElementById('statsBox').style.display = 'block';
                }
                
                // Show download link if file is ready
                if (data.result_file) {
                    const downloadLink = document.getElementById('downloadLink');
                    downloadLink.href = '/api/download/' + data.result_file;
                    document.getElementById('downloadBox').style.display = 'block';
                }
                
                // Re-enable button if not running
                if (!data.is_running) {
                    clearInterval(statusInterval);
                    document.getElementById('startBtn').disabled = false;
                    document.getElementById('startBtn').textContent = '🚀 Start Scraping';
                }
            });
        }
    </script>
</body>
</html>'''
    
    with open('templates/index.html', 'w') as f:
        f.write(html_content)
    
    print("\n" + "="*60)
    print("🚀 PriceSpy Lite Web Interface Starting...")
    print("="*60)
    print("\n📱 Open your browser and go to:")
    print("\n   http://localhost:5000")
    print("\n   or")
    print("\n   http://127.0.0.1:5000")
    print("\n" + "="*60)
    print("Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)
