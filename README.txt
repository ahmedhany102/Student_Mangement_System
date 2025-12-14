Student Management System - Python + CustomTkinter
==================================================

Features:
- Admin login (username: admin, password: 12345)
- Modern dark UI using CustomTkinter
- Add / Edit / Delete students
- Search by ID or Name
- Sort with multiple options (name / age / grade, asc/desc)
- Auto-save to students.json
- Export students data as a JSON file to any path

How to run:

1. Install Python 3 (3.10+ recommended) from https://www.python.org/
   - IMPORTANT: during installation, check "Add Python to PATH".

2. Install dependencies:
   - Open a terminal in this folder and run:
       pip install -r requirements.txt

3. Run the app:
   - In the same folder:
       python app.py

4. Login screen:
   - Username: admin
   - Password: 12345

5. Dashboard:
   - Add: opens a dialog to enter student data.
   - Edit: select a row then click Edit; dialog opens with data pre-filled.
   - Delete: select a row then click Delete.
   - Sort...: opens a sort options window (name/age/grade).
   - Save: writes all students to students.json (in the same folder).
   - Export as JSON file...: choose a location and save a copy of the data.
