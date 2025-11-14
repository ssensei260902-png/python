# 🤖 Python Automation Mastery - Complete Guide

## Comprehensive Automation Modules

This supplementary guide provides in-depth automation content to complement the main curriculum.

---

## Module 13: Python Automation Fundamentals

### 13.1 Introduction to Automation

Automation is about making computers do repetitive tasks for you. Python is perfect for this!

**Real-World Automation Use Cases:**
- Automatically backing up files
- Renaming thousands of files at once
- Sending scheduled emails
- Downloading data from websites
- Processing spreadsheets
- Monitoring system resources
- Generating reports
- Managing databases
- Controlling IoT devices

### 13.2 File System Automation

```python
import os
import shutil
from pathlib import Path
from datetime import datetime

# Automated file organizer
def organize_downloads(download_folder):
    """Organize files by type into folders"""

    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.flv'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp']
    }

    download_path = Path(download_folder)

    # Create category folders
    for category in file_types.keys():
        category_path = download_path / category
        category_path.mkdir(exist_ok=True)

    # Move files to appropriate folders
    for file in download_path.iterdir():
        if file.is_file():
            file_ext = file.suffix.lower()
            moved = False

            for category, extensions in file_types.items():
                if file_ext in extensions:
                    dest = download_path / category / file.name
                    shutil.move(str(file), str(dest))
                    print(f"Moved {file.name} to {category}/")
                    moved = True
                    break

            if not moved:
                other_path = download_path / 'Other'
                other_path.mkdir(exist_ok=True)
                dest = other_path / file.name
                shutil.move(str(file), str(dest))

# Automated backup system
def automated_backup(source_folder, backup_folder):
    """Create timestamped backups"""

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_{timestamp}"

    source = Path(source_folder)
    backup_dest = Path(backup_folder) / backup_name

    shutil.copytree(source, backup_dest)
    print(f"Backup created: {backup_dest}")

    # Clean old backups (keep last 5)
    backups = sorted(Path(backup_folder).glob('backup_*'))
    if len(backups) > 5:
        for old_backup in backups[:-5]:
            shutil.rmtree(old_backup)
            print(f"Removed old backup: {old_backup}")

# Batch file renaming
def batch_rename(folder, pattern, replacement):
    """Rename multiple files at once"""

    path = Path(folder)
    renamed_count = 0

    for file in path.iterdir():
        if file.is_file() and pattern in file.name:
            new_name = file.name.replace(pattern, replacement)
            new_path = path / new_name
            file.rename(new_path)
            print(f"Renamed: {file.name} → {new_name}")
            renamed_count += 1

    print(f"\nTotal files renamed: {renamed_count}")

# Duplicate file finder
def find_duplicates(folder):
    """Find duplicate files based on content"""

    import hashlib

    def file_hash(filepath):
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    hashes = {}
    duplicates = []

    for file in Path(folder).rglob('*'):
        if file.is_file():
            file_hash_value = file_hash(file)

            if file_hash_value in hashes:
                duplicates.append((file, hashes[file_hash_value]))
            else:
                hashes[file_hash_value] = file

    print(f"Found {len(duplicates)} duplicate files:")
    for dup, original in duplicates:
        print(f"  {dup} is duplicate of {original}")

    return duplicates
```

### 13.3 Email Automation

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class EmailAutomation:
    def __init__(self, smtp_server, smtp_port, email, password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_email(self, to_email, subject, body, attachments=None):
        """Send automated email"""

        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Add attachments
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {Path(file_path).name}'
                    )
                    msg.attach(part)

        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)

        print(f"Email sent to {to_email}")

    def send_bulk_emails(self, recipients, subject, body_template):
        """Send personalized emails to multiple recipients"""

        for recipient in recipients:
            personalized_body = body_template.format(**recipient)
            self.send_email(
                recipient['email'],
                subject,
                personalized_body
            )
            print(f"Sent email to {recipient['name']}")

# Automated report emailer
def send_daily_report():
    """Generate and send daily report"""

    # Generate report
    report = f"""
    Daily Report - {datetime.now().strftime('%Y-%m-%d')}
    ==========================================

    Tasks Completed: 15
    New Issues: 3
    System Uptime: 99.9%

    Details attached.
    """

    # Send email
    emailer = EmailAutomation(
        'smtp.gmail.com',
        587,
        'your-email@gmail.com',
        'your-password'
    )

    emailer.send_email(
        'recipient@example.com',
        'Daily Automated Report',
        report,
        attachments=['report.pdf']
    )
```

### 13.4 Web Scraping Automation

```python
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

class WebScraperAutomation:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_prices(self, product_urls):
        """Scrape product prices from multiple URLs"""

        results = []

        for url in product_urls:
            try:
                response = self.session.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract data (customize selectors for your target site)
                title = soup.find('h1', class_='product-title').text.strip()
                price = soup.find('span', class_='price').text.strip()

                results.append({
                    'timestamp': datetime.now(),
                    'title': title,
                    'price': price,
                    'url': url
                })

                print(f"Scraped: {title} - {price}")
                time.sleep(2)  # Be respectful, don't hammer servers

            except Exception as e:
                print(f"Error scraping {url}: {e}")

        return results

    def save_to_csv(self, data, filename):
        """Save scraped data to CSV"""

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if data:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

        print(f"Data saved to {filename}")

    def price_monitor(self, product_url, target_price, check_interval=3600):
        """Monitor price and alert when it drops below target"""

        print(f"Monitoring price... Target: ${target_price}")

        while True:
            data = self.scrape_prices([product_url])

            if data:
                current_price = float(data[0]['price'].replace('$', ''))

                if current_price <= target_price:
                    print(f"🎉 Price Alert! Price dropped to ${current_price}")
                    # Send notification (email, SMS, etc.)
                    break
                else:
                    print(f"Current price: ${current_price}, waiting...")

            time.sleep(check_interval)

# News aggregator automation
def aggregate_news(sources, keywords):
    """Scrape news from multiple sources"""

    all_articles = []

    for source in sources:
        try:
            response = requests.get(source['url'])
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = soup.find_all('article')

            for article in articles:
                title = article.find('h2').text if article.find('h2') else ''

                # Check if article matches keywords
                if any(keyword.lower() in title.lower() for keyword in keywords):
                    all_articles.append({
                        'source': source['name'],
                        'title': title,
                        'url': article.find('a')['href'] if article.find('a') else ''
                    })

        except Exception as e:
            print(f"Error with {source['name']}: {e}")

    return all_articles
```

### 13.5 Excel/CSV Automation

```python
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.chart import BarChart, Reference

class ExcelAutomation:
    def __init__(self, filename):
        self.filename = filename

    def merge_excel_files(self, file_list, output_file):
        """Merge multiple Excel files into one"""

        all_data = []

        for file in file_list:
            df = pd.read_excel(file)
            all_data.append(df)

        merged_df = pd.concat(all_data, ignore_index=True)
        merged_df.to_excel(output_file, index=False)

        print(f"Merged {len(file_list)} files into {output_file}")

    def clean_data(self, input_file, output_file):
        """Clean and process Excel data"""

        df = pd.read_excel(input_file)

        # Remove duplicates
        df = df.drop_duplicates()

        # Fill missing values
        df = df.fillna('')

        # Remove extra whitespace
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].str.strip()

        # Save cleaned data
        df.to_excel(output_file, index=False)
        print(f"Data cleaned and saved to {output_file}")

    def generate_report(self, data_file, output_file):
        """Generate formatted Excel report with charts"""

        # Read data
        df = pd.read_excel(data_file)

        # Create workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sales Report"

        # Write data
        for r_idx, row in enumerate(df.itertuples(index=False), 1):
            for c_idx, value in enumerate(row, 1):
                cell = ws.cell(row=r_idx, column=c_idx, value=value)

                # Format header
                if r_idx == 1:
                    cell.font = Font(bold=True, color="FFFFFF")
                    cell.fill = PatternFill(start_color="4472C4",
                                           end_color="4472C4",
                                           fill_type="solid")

        # Add chart
        chart = BarChart()
        chart.title = "Sales by Region"

        data = Reference(ws, min_col=2, min_row=1,
                        max_row=len(df)+1)
        categories = Reference(ws, min_col=1, min_row=2,
                              max_row=len(df)+1)

        chart.add_data(data, titles_from_data=True)
        chart.set_categories(categories)

        ws.add_chart(chart, "E5")

        # Save
        wb.save(output_file)
        print(f"Report generated: {output_file}")

    def automate_invoice_processing(self, invoices_folder):
        """Process multiple invoices automatically"""

        all_invoices = []

        for file in Path(invoices_folder).glob('*.xlsx'):
            df = pd.read_excel(file)

            # Calculate totals
            df['Total'] = df['Quantity'] * df['Unit Price']

            # Add to collection
            all_invoices.append({
                'invoice_file': file.name,
                'total_amount': df['Total'].sum(),
                'items': len(df)
            })

        # Create summary
        summary_df = pd.DataFrame(all_invoices)
        summary_df.to_excel('invoice_summary.xlsx', index=False)

        print(f"Processed {len(all_invoices)} invoices")
        return summary_df
```

### 13.6 PDF Automation

```python
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class PDFAutomation:
    def merge_pdfs(self, pdf_list, output_file):
        """Merge multiple PDFs into one"""

        merger = PdfMerger()

        for pdf in pdf_list:
            merger.append(pdf)

        merger.write(output_file)
        merger.close()

        print(f"Merged {len(pdf_list)} PDFs into {output_file}")

    def split_pdf(self, input_pdf, pages_per_file):
        """Split PDF into multiple files"""

        reader = PdfReader(input_pdf)
        total_pages = len(reader.pages)

        for i in range(0, total_pages, pages_per_file):
            writer = PdfWriter()

            for page_num in range(i, min(i + pages_per_file, total_pages)):
                writer.add_page(reader.pages[page_num])

            output_filename = f"split_{i//pages_per_file + 1}.pdf"
            with open(output_filename, 'wb') as output_file:
                writer.write(output_file)

            print(f"Created {output_filename}")

    def extract_text_from_pdfs(self, pdf_folder):
        """Extract text from all PDFs in folder"""

        results = {}

        for pdf_file in Path(pdf_folder).glob('*.pdf'):
            reader = PdfReader(pdf_file)
            text = ""

            for page in reader.pages:
                text += page.extract_text()

            results[pdf_file.name] = text
            print(f"Extracted text from {pdf_file.name}")

        return results

    def add_watermark(self, input_pdf, watermark_text, output_pdf):
        """Add watermark to all pages"""

        # Create watermark
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFont("Helvetica", 60)
        can.setFillAlpha(0.3)
        can.drawString(100, 400, watermark_text)
        can.save()

        packet.seek(0)
        watermark = PdfReader(packet)

        # Add to PDF
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page in reader.pages:
            page.merge_page(watermark.pages[0])
            writer.add_page(page)

        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

        print(f"Watermark added: {output_pdf}")
```

### 13.7 System Monitoring and Automation

```python
import psutil
import time
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.alert_threshold = {
            'cpu': 80,
            'memory': 85,
            'disk': 90
        }

    def get_system_stats(self):
        """Get current system statistics"""

        stats = {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_sent': psutil.net_io_counters().bytes_sent / 1024**2,
            'network_recv': psutil.net_io_counters().bytes_recv / 1024**2,
            'timestamp': datetime.now()
        }

        return stats

    def monitor_and_alert(self, interval=60):
        """Monitor system and alert on high usage"""

        print("Starting system monitor...")

        while True:
            stats = self.get_system_stats()

            # Check thresholds
            alerts = []

            if stats['cpu_percent'] > self.alert_threshold['cpu']:
                alerts.append(f"⚠️ HIGH CPU: {stats['cpu_percent']}%")

            if stats['memory_percent'] > self.alert_threshold['memory']:
                alerts.append(f"⚠️ HIGH MEMORY: {stats['memory_percent']}%")

            if stats['disk_percent'] > self.alert_threshold['disk']:
                alerts.append(f"⚠️ HIGH DISK: {stats['disk_percent']}%")

            if alerts:
                for alert in alerts:
                    print(alert)
                # Send notification (email, SMS, etc.)
            else:
                print(f"✅ System OK - CPU: {stats['cpu_percent']}%, "
                      f"MEM: {stats['memory_percent']}%, "
                      f"DISK: {stats['disk_percent']}%")

            time.sleep(interval)

    def log_performance(self, log_file, duration=3600):
        """Log system performance for analysis"""

        start_time = time.time()
        logs = []

        while time.time() - start_time < duration:
            stats = self.get_system_stats()
            logs.append(stats)

            time.sleep(60)  # Log every minute

        # Save to CSV
        df = pd.DataFrame(logs)
        df.to_csv(log_file, index=False)
        print(f"Performance log saved to {log_file}")

    def cleanup_old_files(self, folder, days_old=30):
        """Delete files older than specified days"""

        cutoff_time = time.time() - (days_old * 86400)
        deleted_count = 0

        for file in Path(folder).rglob('*'):
            if file.is_file():
                if file.stat().st_mtime < cutoff_time:
                    file.unlink()
                    deleted_count += 1
                    print(f"Deleted: {file}")

        print(f"Deleted {deleted_count} old files")
```

### 13.8 Database Automation

```python
import sqlite3
import schedule
from datetime import datetime, timedelta

class DatabaseAutomation:
    def __init__(self, db_path):
        self.db_path = db_path

    def automated_backup(self, backup_folder):
        """Automatically backup database"""

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f"{backup_folder}/db_backup_{timestamp}.db"

        # Copy database
        import shutil
        shutil.copy2(self.db_path, backup_file)

        print(f"Database backed up to {backup_file}")

    def cleanup_old_records(self, table, date_column, days_to_keep):
        """Delete old records from database"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        cursor.execute(f"""
            DELETE FROM {table}
            WHERE {date_column} < ?
        """, (cutoff_date,))

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()

        print(f"Deleted {deleted_count} old records from {table}")

    def generate_database_report(self):
        """Generate database statistics report"""

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get table list
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        report = "Database Report\n" + "="*50 + "\n\n"

        for table in tables:
            table_name = table[0]

            # Count rows
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]

            report += f"{table_name}: {row_count} rows\n"

        conn.close()

        # Save report
        with open('db_report.txt', 'w') as f:
            f.write(report)

        print(report)
        return report
```

---

## Complete Automation Project Examples

### Project 1: Automated Social Media Manager

```python
import tweepy
import schedule
import random
from datetime import datetime

class SocialMediaAutomation:
    def __init__(self, api_key, api_secret, access_token, access_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def schedule_posts(self, posts, times):
        """Schedule social media posts"""

        for time_str in times:
            post = random.choice(posts)
            schedule.every().day.at(time_str).do(
                self.post_tweet, post
            )

        print(f"Scheduled {len(times)} posts")

    def post_tweet(self, message):
        """Post a tweet"""
        self.api.update_status(message)
        print(f"Posted: {message}")

    def auto_reply_to_mentions(self):
        """Automatically reply to mentions"""

        mentions = self.api.mentions_timeline(count=10)

        for mention in mentions:
            reply = f"@{mention.user.screen_name} Thanks for mentioning us!"
            self.api.update_status(reply, in_reply_to_status_id=mention.id)
```

### Project 2: Automated Data Pipeline

```python
class DataPipeline:
    def __init__(self):
        self.data_sources = []
        self.transformations = []
        self.destinations = []

    def extract(self, source_type, **kwargs):
        """Extract data from source"""

        if source_type == 'csv':
            return pd.read_csv(kwargs['file'])
        elif source_type == 'api':
            response = requests.get(kwargs['url'])
            return response.json()
        elif source_type == 'database':
            conn = sqlite3.connect(kwargs['db_path'])
            return pd.read_sql(kwargs['query'], conn)

    def transform(self, data, operations):
        """Transform data"""

        df = pd.DataFrame(data)

        for operation in operations:
            if operation['type'] == 'filter':
                df = df[df[operation['column']] > operation['value']]
            elif operation['type'] == 'aggregate':
                df = df.groupby(operation['group_by']).agg(operation['agg_func'])
            elif operation['type'] == 'rename':
                df = df.rename(columns=operation['mapping'])

        return df

    def load(self, data, destination_type, **kwargs):
        """Load data to destination"""

        if destination_type == 'csv':
            data.to_csv(kwargs['file'], index=False)
        elif destination_type == 'database':
            conn = sqlite3.connect(kwargs['db_path'])
            data.to_sql(kwargs['table'], conn, if_exists='replace')
        elif destination_type == 'api':
            requests.post(kwargs['url'], json=data.to_dict())

    def run_pipeline(self):
        """Execute full ETL pipeline"""

        print("Starting automated data pipeline...")

        # Extract
        raw_data = self.extract('csv', file='source.csv')

        # Transform
        transformed_data = self.transform(raw_data, [
            {'type': 'filter', 'column': 'sales', 'value': 1000},
            {'type': 'aggregate', 'group_by': 'region', 'agg_func': 'sum'}
        ])

        # Load
        self.load(transformed_data, 'database',
                 db_path='analytics.db', table='sales_summary')

        print("Pipeline completed successfully!")
```

This is just the beginning! Would you like me to create even more comprehensive automation modules covering:
- IoT and hardware automation with Raspberry Pi
- Cloud automation (AWS, Azure, GCP)
- DevOps automation (CI/CD pipelines)
- Testing automation
- GUI automation with PyAutoGUI
- Voice-controlled automation
- And much more?
