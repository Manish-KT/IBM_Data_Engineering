# Backup Script

This script creates a backup of files from a target directory that have been modified in the last 24 hours and moves the backup to a specified destination directory.

## Usage

```bash
./backup.sh target_directory_name destination_directory_name
```

## Explanation of the Script

### Argument Check

1. **Check number of arguments:**
   ```bash
   if [[ $# != 2 ]]
   then
     echo "backup.sh target_directory_name destination_directory_name"
     exit
   fi
   ```
   - Ensures that exactly two arguments are provided. If not, it prints an error message and exits.

2. **Check if arguments are valid directory paths:**
   ```bash
   if [[ ! -d $1 ]] || [[ ! -d $2 ]]
   then
     echo "Invalid directory path provided"
     exit
   fi
   ```
   - Validates that the provided arguments are directories. If not, it prints an error message and exits.

### Variable Initialization

3. **Initialize directories:**
   ```bash
   targetDirectory=$1
   destinationDirectory=$2
   ```

4. **Print directory paths:**
   ```bash
   echo "Target directory path: $1"
   echo "Destination directory path: $2"
   ```

5. **Get current timestamp:**
   ```bash
   currentTS=$(date +%s)
   ```

6. **Create backup file name:**
   ```bash
   backupFileName="backup-$currentTS.tar.gz"
   ```

### Path Setup

7. **Save original path:**
   ```bash
   origAbsPath=$(pwd)
   ```

8. **Change to destination directory to get its absolute path:**
   ```bash
   cd $destinationDirectory
   destDirAbsPath=$(pwd)
   ```

9. **Return to original directory:**
   ```bash
   cd $origAbsPath
   cd $targetDirectory
   ```

### File Backup

10. **Calculate timestamp for 24 hours ago:**
    ```bash
    yesterdayTS=$(($currentTS - 86400))
    ```

11. **Initialize array for files to backup:**
    ```bash
    declare -a toBackup
    ```

12. **Identify files modified in the last 24 hours:**
    ```bash
    for file in $(ls)
    do
      if (( `date -r $file +%s` > $yesterdayTS ))
      then
        toBackup+=($file)
      fi
    done
    ```

13. **Create the backup file:**
    ```bash
    tar -czvf $backupFileName ${toBackup[@]}
    ```

14. **Move the backup file to the destination directory:**
    ```bash
    mv $backupFileName $destDirAbsPath
    ```

## Scheduling the Script with Crontab

To run the script periodically, you can schedule it using `crontab`. Here’s how to schedule it to run daily at midnight:

1. Open the crontab file:
   ```bash
   crontab -e
   ```

2. Add the following line to schedule the script:
   ```bash
   0 0 * * * /path/to/backup.sh /path/to/target_directory /path/to/destination_directory
   ```
   - This line schedules the script to run at midnight every day. Adjust the path to the script and directories as needed.

Save and close the crontab file. The script will now run daily at the specified time.

## Conclusion

This script helps in automating the backup process for files modified in the last 24 hours, ensuring that your important data is backed up regularly and efficiently.

You can save this content into a file named `README.md` in your project directory. This provides a clear and detailed explanation of the script's functionality and usage.