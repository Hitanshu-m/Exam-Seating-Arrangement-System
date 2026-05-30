# Exam Seating Arrangement System

A simple web application that automatically generates exam seating arrangements from Excel files.

## How It Works

1. Upload the **Students Excel File** containing:
   - Roll No
   - Name
   - Branch

2. Upload the **Classrooms Excel File** containing:
   - Room No
   - Rows
   - Columns

3. Click **Generate Seating**.

4. The system:
   - Randomly shuffles students
   - Mixes branches for better distribution
   - Allocates students room-wise
   - Assigns seat numbers (A1, A2, B1, etc.)

5. Download the generated:
   - Excel seating arrangement
   - PDF seating arrangement

## Live Demo

https://exam-seat-hitubhau-in.onrender.com

> Replace the above link with your actual Render deployment URL.

## Example Input

### Students File

| Roll No | Name | Branch |
|----------|--------|----------|
| 22001 | Rahul | CSE |
| 22002 | Priya | IT |

### Rooms File

| Room No | Rows | Columns |
|----------|------|---------|
| 101 | 5 | 6 |

## Tech Stack

- Flask
- Pandas
- OpenPyXL
- ReportLab
- Render

## Author

Developed by Hitanshu Meshram