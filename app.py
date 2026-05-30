from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import random
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER


def validate_students(df):
    required = ["Roll No", "Name", "Branch"]
    return all(col in df.columns for col in required)


def validate_rooms(df):
    required = ["Room No", "Rows", "Columns"]
    return all(col in df.columns for col in required)


def branch_mix_students(df):
    groups = {}

    for _, row in df.iterrows():
        branch = row["Branch"]

        if branch not in groups:
            groups[branch] = []

        groups[branch].append(row)

    mixed = []

    while any(groups.values()):
        keys = list(groups.keys())
        random.shuffle(keys)

        for k in keys:
            if groups[k]:
                mixed.append(groups[k].pop(0))

    return pd.DataFrame(mixed)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    students_file = request.files.get("students_file")
    rooms_file = request.files.get("rooms_file")

    if not students_file or not rooms_file:
        return render_template(
            "error.html",
            message="Both files are required."
        )

    students_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        students_file.filename
    )

    rooms_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        rooms_file.filename
    )

    students_file.save(students_path)
    rooms_file.save(rooms_path)

    students = pd.read_excel(students_path)
    rooms = pd.read_excel(rooms_path)

    if not validate_students(students):
        return render_template(
            "error.html",
            message="Students file must contain Roll No, Name, Branch"
        )

    if not validate_rooms(rooms):
        return render_template(
            "error.html",
            message="Rooms file must contain Room No, Rows, Columns"
        )

    students = branch_mix_students(students)

    seating_output = []

    student_index = 0

    for _, room in rooms.iterrows():

        room_no = room["Room No"]
        rows = int(room["Rows"])
        cols = int(room["Columns"])

        for r in range(rows):
            for c in range(cols):

                if student_index >= len(students):
                    break

                student = students.iloc[student_index]

                seat = f"{chr(65+r)}{c+1}"

                seating_output.append({
                    "Room": room_no,
                    "Seat": seat,
                    "Roll No": student["Roll No"],
                    "Name": student["Name"],
                    "Branch": student["Branch"]
                })

                student_index += 1

    output_df = pd.DataFrame(seating_output)

    excel_file = os.path.join(
        OUTPUT_FOLDER,
        "seating_output.xlsx"
    )

    output_df.to_excel(excel_file, index=False)

    pdf_file = os.path.join(
        OUTPUT_FOLDER,
        "seating_output.pdf"
    )

    create_pdf(output_df, pdf_file)

    preview_data = output_df.head(50).to_dict("records")

    return render_template(
        "preview.html",
        data=preview_data
    )


def create_pdf(df, filename):

    doc = SimpleDocTemplate(filename)

    data = [["Room", "Seat", "Roll No", "Name", "Branch"]]

    for _, row in df.iterrows():
        data.append([
            str(row["Room"]),
            str(row["Seat"]),
            str(row["Roll No"]),
            str(row["Name"]),
            str(row["Branch"])
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey)
    ]))

    doc.build([table])


@app.route("/download/excel")
def download_excel():
    return send_file(
        "outputs/seating_output.xlsx",
        as_attachment=True
    )


@app.route("/download/pdf")
def download_pdf():
    return send_file(
        "outputs/seating_output.pdf",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)