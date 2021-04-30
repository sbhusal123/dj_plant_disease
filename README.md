# Django Backend For Plants Disease Prediction

## Virtual Env Setup

-   **Create virtual env:** `python3 -m venv env` on linux or `python -m venv env` on windows.
-   **Install packages:** `pip install -r requirements.txt` make sure your current path is same as where file is located.

# Runing Project:

-   **cd into root plant_disease directory:** `cd plant_disease`
-   **Create database tables:** `python manage.py migrate`. Run evertime once you delete sqlite file.
-   **Run backendserver:** `python manage.py runserver`. Starts servering at **localhost:8000**
-   **Stop server:** `ctrl + c`

```python
Watching for file changes with StatReloader
Performing system checks...

2021-04-30 12:52:12.659683: W tensorflow/stream_executor/platform/default/dso_loader.cc:60] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory
2021-04-30 12:52:12.659710: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
System check identified no issues (0 silenced).
April 30, 2021 - 12:52:14
Django version 3.2, using settings 'plant_disease.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

# Directory Structure.

```bash

├── env
├── plane_disease(root project directory)
│   ├── model
│   |    ├── model_files
│   |    |    ├── label_list.pkl (labels list)
│   |    |    ├── mymodel.h5 (saved model)
|   |    └── predict.py (prediction using saved model)
|   |    └── __init__.py
|   └── plant_disease
│   |    ├── settings.py(django settings)
│   |    ├── .......
|   └── prediction (django sub app for prediction, authentication logic)
│   |    ├── management (contains logics to populate excel file)
│   |    ├── models.py (Disease tables/object)
│   |    ├── forms.py (PredictionForm, Login Form, Register Form)
│   |    ├── views.py (login, logout, register, prediction logic)
│   |    ├── ...
|   └── template
│   |    ├── layouts.html (base template, navbar, js, css bootstrap)
│   |    ├── index.html (prediction frontend)
│   |    ├── login.html
│   |    ├── register.html
|   └── Name.xlsx (disease data excel file)
|   └── manage.py
|   └── db.sqlite3 (database file can be deleted)
├── requirements.txt
├── README.md
├── .gitignore
```

**1. model:**
Contains all the functionality for prediction.

**2. model/model_files**

-   Contains pickle dumped label_list during data preparation. (label_list.pkl)
-   Contains model file. (mymoel.h5)
-   You can also replace those files but the **name and the path must be same**.

**3. Name.xlsx**

-   Excel file from which diseases data are being populated.
-   Must be placed **inside the root plant_disease directory**.

    | Name                      | Description     | Medicine      |
    | ------------------------- | --------------- | ------------- |
    | Tomato_Septoria_leaf_spot | ............... | ............. |

    > Note that name of the rows are case sensitive. **Name, Description, Medicine**

-   **Populating diseases:** `python manage.py populate_diseases "<Name>.xlsx"`

# Django Management Command:

-   **Create supeuser:** `python manage.py createsuperuser`. Login at: **localhost:8000/admin**
-   **Create database tables:** `python manage.py migrate`
