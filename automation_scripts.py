#!/usr/bin/env python3
"""
Python Automation Scripts Collection
Ready-to-use automation scripts for common tasks
"""

# ============================================================================
# SCRIPT 1: AUTOMATED FOLDER ORGANIZER
# ============================================================================

import os
import shutil
from pathlib import Path
from datetime import datetime
import hashlib
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def organize_downloads():
    """
    Automatically organize your Downloads folder by file type
    Run this daily or whenever your downloads get messy!
    """

    downloads = Path.home() / 'Downloads'

    file_categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.ico'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.tex'],
        'Spreadsheets': ['.xlsx', '.xls', '.csv', '.ods'],
        'Presentations': ['.pptx', '.ppt', '.key', '.odp'],
        'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv', '.m4v'],
        'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a', '.wma'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go'],
        'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm', '.app'],
        'Ebooks': ['.epub', '.mobi', '.azw', '.azw3', '.pdf'],
    }

    # Create folders
    for category in file_categories:
        (downloads / category).mkdir(exist_ok=True)

    # Organize files
    moved_count = 0
    for file in downloads.iterdir():
        if file.is_file():
            ext = file.suffix.lower()

            for category, extensions in file_categories.items():
                if ext in extensions:
                    dest = downloads / category / file.name

                    # Handle duplicates
                    if dest.exists():
                        counter = 1
                        while dest.exists():
                            new_name = f"{file.stem}_{counter}{file.suffix}"
                            dest = downloads / category / new_name
                            counter += 1

                    shutil.move(str(file), str(dest))
                    print(f"✓ {file.name} → {category}/")
                    moved_count += 1
                    break

    print(f"\n🎉 Organized {moved_count} files!")


# ============================================================================
# SCRIPT 2: AUTOMATED BACKUP SYSTEM
# ============================================================================

def create_backup(source_folder, backup_location, keep_last=7):
    """
    Create automatic timestamped backups
    Keeps only the last N backups to save space

    Usage:
        create_backup('/path/to/important/folder', '/path/to/backups', keep_last=7)
    """

    source = Path(source_folder)
    backup_dir = Path(backup_location)
    backup_dir.mkdir(exist_ok=True)

    # Create timestamped backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"backup_{source.name}_{timestamp}"

    print(f"Creating backup of {source}...")

    # Create compressed archive
    archive_path = backup_dir / backup_name
    shutil.make_archive(str(archive_path), 'zip', source)

    print(f"✓ Backup created: {archive_path}.zip")

    # Clean old backups
    backups = sorted(
        backup_dir.glob('backup_*.zip'),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )

    if len(backups) > keep_last:
        for old_backup in backups[keep_last:]:
            old_backup.unlink()
            print(f"✗ Removed old backup: {old_backup.name}")

    print(f"✓ Keeping {min(len(backups), keep_last)} most recent backups")


# ============================================================================
# SCRIPT 3: DUPLICATE FILE FINDER
# ============================================================================

def find_and_remove_duplicates(directory, remove=False):
    """
    Find duplicate files by content (not just name)
    Set remove=True to actually delete duplicates

    Usage:
        find_and_remove_duplicates('/path/to/folder', remove=False)  # Just report
        find_and_remove_duplicates('/path/to/folder', remove=True)   # Delete them
    """

    def file_hash(filepath):
        """Calculate MD5 hash of file"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    print(f"Scanning {directory} for duplicates...")

    hashes = {}
    duplicates = []

    # Scan all files
    for file in Path(directory).rglob('*'):
        if file.is_file():
            try:
                file_hash_value = file_hash(file)

                if file_hash_value in hashes:
                    duplicates.append((file, hashes[file_hash_value]))
                    print(f"⚠️  Duplicate: {file.name}")
                else:
                    hashes[file_hash_value] = file

            except Exception as e:
                print(f"Error: {file} - {e}")

    # Report
    if not duplicates:
        print("\n✓ No duplicates found!")
        return

    total_space = sum(dup[0].stat().st_size for dup in duplicates)
    print(f"\n📊 Found {len(duplicates)} duplicates wasting {total_space / 1024**2:.2f} MB")

    # Remove if requested
    if remove:
        for duplicate, original in duplicates:
            duplicate.unlink()
            print(f"✗ Deleted: {duplicate}")
        print(f"\n✓ Freed {total_space / 1024**2:.2f} MB of space!")
    else:
        print("\n💡 Run with remove=True to delete duplicates")


# ============================================================================
# SCRIPT 4: BATCH FILE RENAMER
# ============================================================================

def batch_rename_files(directory, old_text, new_text):
    """
    Rename multiple files by replacing text

    Usage:
        batch_rename_files('/path/to/photos', 'IMG', 'Photo')
    """

    path = Path(directory)
    renamed = 0

    for file in path.iterdir():
        if file.is_file() and old_text in file.name:
            new_name = file.name.replace(old_text, new_text)
            new_path = path / new_name

            file.rename(new_path)
            print(f"{file.name} → {new_name}")
            renamed += 1

    print(f"\n✓ Renamed {renamed} files")


def sequential_rename(directory, prefix='file', start=1):
    """
    Rename files sequentially: file_001.jpg, file_002.jpg, etc.

    Usage:
        sequential_rename('/path/to/photos', prefix='photo', start=1)
    """

    path = Path(directory)
    files = sorted([f for f in path.iterdir() if f.is_file()])

    for i, file in enumerate(files, start=start):
        new_name = f"{prefix}_{str(i).zfill(3)}{file.suffix}"
        new_path = path / new_name

        file.rename(new_path)
        print(f"{file.name} → {new_name}")

    print(f"\n✓ Renamed {len(files)} files")


# ============================================================================
# SCRIPT 5: AUTOMATED EMAIL SENDER
# ============================================================================

def send_email_with_attachments(
    smtp_server, smtp_port, sender_email, sender_password,
    recipient_email, subject, body, attachments=None
):
    """
    Send automated emails with attachments

    Usage:
        send_email_with_attachments(
            'smtp.gmail.com', 587,
            'your-email@gmail.com', 'your-app-password',
            'recipient@example.com',
            'Automated Report',
            'Here is today\'s report.',
            attachments=['report.pdf', 'data.csv']
        )

    Note: For Gmail, use an App Password, not your regular password
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    if attachments:
        for file_path in attachments:
            file_path = Path(file_path)
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {file_path.name}'
                    )
                    msg.attach(part)
                print(f"📎 Attached: {file_path.name}")

    # Send email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"✓ Email sent to {recipient_email}")
    except Exception as e:
        print(f"✗ Error sending email: {e}")


# ============================================================================
# SCRIPT 6: FILE MONITOR / WATCHER
# ============================================================================

def monitor_directory(directory, interval=5):
    """
    Monitor a directory for changes and print alerts
    Useful for watching log files, downloads, etc.

    Usage:
        monitor_directory('/path/to/watch', interval=5)
    """

    print(f"👀 Monitoring {directory}")
    print("Press Ctrl+C to stop\n")

    tracked_files = {}

    # Initial scan
    for file in Path(directory).rglob('*'):
        if file.is_file():
            tracked_files[str(file)] = file.stat().st_mtime

    try:
        while True:
            current_files = {}

            # Check for changes
            for file in Path(directory).rglob('*'):
                if file.is_file():
                    filepath = str(file)
                    mtime = file.stat().st_mtime
                    current_files[filepath] = mtime

                    # New file
                    if filepath not in tracked_files:
                        print(f"➕ NEW: {file.name}")

                    # Modified file
                    elif mtime != tracked_files[filepath]:
                        print(f"📝 MODIFIED: {file.name}")

            # Deleted files
            for filepath in tracked_files:
                if filepath not in current_files:
                    print(f"🗑️  DELETED: {Path(filepath).name}")

            tracked_files = current_files
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n✓ Monitoring stopped")


# ============================================================================
# SCRIPT 7: SYSTEM CLEANUP
# ============================================================================

def cleanup_old_files(directory, days_old=30, pattern='*', dry_run=True):
    """
    Delete files older than specified days
    Use dry_run=True to see what would be deleted first!

    Usage:
        cleanup_old_files('/path/to/logs', days_old=30, pattern='*.log', dry_run=True)
        cleanup_old_files('/path/to/logs', days_old=30, pattern='*.log', dry_run=False)
    """

    cutoff_time = time.time() - (days_old * 86400)
    path = Path(directory)

    deleted_count = 0
    freed_space = 0

    for file in path.glob(pattern):
        if file.is_file():
            file_mtime = file.stat().st_mtime

            if file_mtime < cutoff_time:
                file_size = file.stat().st_size

                if dry_run:
                    print(f"[DRY RUN] Would delete: {file.name}")
                else:
                    file.unlink()
                    print(f"✗ Deleted: {file.name}")

                deleted_count += 1
                freed_space += file_size

    mode = "Would free" if dry_run else "Freed"
    print(f"\n{mode} {freed_space / 1024**2:.2f} MB by deleting {deleted_count} files")


# ============================================================================
# SCRIPT 8: AUTOMATED SCREENSHOT ORGANIZER
# ============================================================================

def organize_screenshots():
    """
    Organize screenshots by date
    Creates folders like: 2024-01, 2024-02, etc.
    """

    screenshots_dir = Path.home() / 'Pictures' / 'Screenshots'

    if not screenshots_dir.exists():
        print(f"Directory not found: {screenshots_dir}")
        return

    organized = 0

    for file in screenshots_dir.iterdir():
        if file.is_file():
            # Get file creation date
            creation_time = datetime.fromtimestamp(file.stat().st_ctime)
            month_folder = creation_time.strftime('%Y-%m')

            # Create month folder
            dest_folder = screenshots_dir / month_folder
            dest_folder.mkdir(exist_ok=True)

            # Move file
            dest = dest_folder / file.name
            if not dest.exists():
                shutil.move(str(file), str(dest))
                print(f"{file.name} → {month_folder}/")
                organized += 1

    print(f"\n✓ Organized {organized} screenshots")


# ============================================================================
# SCRIPT 9: CSV DATA PROCESSOR
# ============================================================================

def process_csv_files(input_dir, output_dir, operation='merge'):
    """
    Automated CSV processing
    Operations: 'merge', 'clean', 'split'

    Usage:
        process_csv_files('/input', '/output', operation='merge')
    """

    import csv
    import pandas as pd

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    csv_files = list(input_path.glob('*.csv'))

    if operation == 'merge':
        # Merge all CSV files
        dfs = []
        for file in csv_files:
            df = pd.read_csv(file)
            dfs.append(df)
            print(f"📄 Read: {file.name}")

        if dfs:
            merged = pd.concat(dfs, ignore_index=True)
            output_file = output_path / 'merged.csv'
            merged.to_csv(output_file, index=False)
            print(f"\n✓ Merged {len(dfs)} files into {output_file}")

    elif operation == 'clean':
        # Clean each CSV file
        for file in csv_files:
            df = pd.read_csv(file)

            # Remove duplicates
            original_len = len(df)
            df = df.drop_duplicates()

            # Fill missing values
            df = df.fillna('')

            # Save cleaned version
            output_file = output_path / f"clean_{file.name}"
            df.to_csv(output_file, index=False)
            print(f"✓ Cleaned: {file.name} (removed {original_len - len(df)} duplicates)")


# ============================================================================
# SCRIPT 10: AUTOMATED TASK SCHEDULER
# ============================================================================

def schedule_tasks():
    """
    Schedule automated tasks using the schedule library

    Usage:
        schedule_tasks()

    Note: Runs indefinitely. Press Ctrl+C to stop.
    """

    import schedule

    def daily_backup():
        print("\n🔄 Running daily backup...")
        create_backup(
            str(Path.home() / 'Documents'),
            str(Path.home() / 'Backups')
        )

    def organize_downloads_task():
        print("\n📂 Organizing downloads...")
        organize_downloads()

    def cleanup_task():
        print("\n🧹 Cleaning up old files...")
        cleanup_old_files(
            str(Path.home() / 'Downloads'),
            days_old=90,
            dry_run=False
        )

    # Schedule tasks
    schedule.every().day.at("02:00").do(daily_backup)
    schedule.every().day.at("18:00").do(organize_downloads_task)
    schedule.every().monday.at("09:00").do(cleanup_task)

    print("⏰ Scheduler started!")
    print("Daily backup: 2:00 AM")
    print("Organize downloads: 6:00 PM daily")
    print("Cleanup old files: Every Monday 9:00 AM")
    print("\nPress Ctrl+C to stop")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n✓ Scheduler stopped")


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    """
    Interactive menu to run automation scripts
    """

    print("=" * 60)
    print("🤖 PYTHON AUTOMATION SCRIPTS".center(60))
    print("=" * 60)
    print("\n1. Organize Downloads Folder")
    print("2. Create Backup")
    print("3. Find Duplicate Files")
    print("4. Batch Rename Files")
    print("5. Monitor Directory")
    print("6. Cleanup Old Files")
    print("7. Organize Screenshots")
    print("8. Send Email with Attachments")
    print("9. Process CSV Files")
    print("10. Start Task Scheduler")
    print("\n0. Exit")

    choice = input("\nEnter your choice (0-10): ")

    if choice == '1':
        organize_downloads()
    elif choice == '2':
        source = input("Source folder path: ")
        backup_loc = input("Backup location: ")
        create_backup(source, backup_loc)
    elif choice == '3':
        directory = input("Directory to scan: ")
        remove = input("Remove duplicates? (yes/no): ").lower() == 'yes'
        find_and_remove_duplicates(directory, remove=remove)
    elif choice == '4':
        directory = input("Directory path: ")
        old_text = input("Text to replace: ")
        new_text = input("Replace with: ")
        batch_rename_files(directory, old_text, new_text)
    elif choice == '5':
        directory = input("Directory to monitor: ")
        monitor_directory(directory)
    elif choice == '6':
        directory = input("Directory path: ")
        days = int(input("Delete files older than (days): "))
        cleanup_old_files(directory, days_old=days, dry_run=False)
    elif choice == '7':
        organize_screenshots()
    elif choice == '10':
        schedule_tasks()

    print("\n✓ Done!")


if __name__ == '__main__':
    print("""
    🐍 PYTHON AUTOMATION SCRIPTS COLLECTION
    =======================================

    This file contains 10+ ready-to-use automation scripts.

    To use:
    1. Run: python automation_scripts.py
    2. Or import specific functions in your own scripts
    3. Customize paths and settings as needed

    Examples:
        from automation_scripts import organize_downloads
        organize_downloads()

    """)

    # Run main menu
    main()
