from django.core.management import BaseCommand

import os
from os import path
from pathlib import Path

import pandas as pd

from prediction.models import Disease

class Command(BaseCommand):

    # python manage.py populate_diseases "<filename>.xlsx"

    # Project directory base path
    BASE_PATH = Path.joinpath(Path(__file__).resolve().parent.parent.parent.parent)

    help = "Populate diseases model"

    def add_arguments(self, parser):
        parser.add_argument('file_name',
                            type=str, help="Name of excel file")

    def handle(self, *args, **kwargs):
        """Handle what this command does. Every handler to be called here"""

        # Write Console Message
        file_name = kwargs['file_name']
        self.populate_database(file_name)

    
    def populate_database(self, file_name):
        if not file_name in os.listdir(self.BASE_PATH):
            self.stdout.write(self.style.ERROR("Excel file {} doesn't exists at: {}".format(file_name, self.BASE_PATH)))
            return None

        
        self.stdout.write(self.style.WARNING("Populating from {}".format(file_name)))

        file_path = str(self.BASE_PATH)+"/"+file_name
        df = pd.read_excel(file_path, engine='openpyxl')

        for index, row in df.iterrows():
            name = row['Name']
            description = row['Description']
            medicine = row['Medicine']

            try:
                Disease.objects.create(name=name, description=description, medicine=medicine)
                self.stdout.write(self.style.WARNING("Populated:  {}".format(name)))
            except Exception as e:
                self.stdout.write(self.style.ERROR("Error populating {}".format(name)))
            
            

