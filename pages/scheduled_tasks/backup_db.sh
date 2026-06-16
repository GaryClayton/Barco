#!/bin/bash

# 1. Define variables
USER="GaryClayton"
DB_NAME="GaryClayton\$barc_db" # This is correct for a variable
BACKUP_DIR="/home/GaryClayton/barc_root/backups"
DATE=$(date +%Y-%m-%d_%H%M)
FILENAME="$BACKUP_DIR/db_backup_$DATE.sql"

# 2. Create the backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# 3. Run the backup command (credentials are pulled from ~/.my.cnf)
mysqldump --set-gtid-purged=OFF --no-tablespaces "$DB_NAME" > $FILENAME

# 4. Optional: Delete backups older than 30 days to save space
find $BACKUP_DIR -type f -name "*.sql" -mtime +30 -delete

echo "Backup completed: $FILENAME"

