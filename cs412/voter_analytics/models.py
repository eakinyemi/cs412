from django.db import models
from datetime import datetime


# Create your models here.
class Voter(models.Model):
    
    #Identification
    Last_Name = models.CharField(max_length=100)
    First_Name = models.CharField(max_length=100)
    Date_of_Birth = models.DateField()
    Street_Address = models.CharField(max_length=100)
    Apartment_Number = models.CharField(max_length=10, blank=True, null=True)
    Zip_Code = models.CharField(max_length=10)
    Date_of_Registration = models.DateField()
    Party_Affiliation = models.CharField(max_length=2)
    precinct_number = models.CharField(max_length=10)
    
    # Voting history
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    voter_score = models.IntegerField()

    def __str__(self):
        return f'{self.First_Name} {self.Last_Name}'

    def full_address(self):
        base = f"{self.Street_Address}"
        if self.Apartment_Number:
            base += f" Apt {self.Apartment_Number}"
        return f"{base}, {self.Zip_Code}"

    def load_data():
        filename = 'C:\\Users\\evana\\django\\cs412\\newton_voters.csv'

        # Clear out existing records to prevent duplicates
        Voter.objects.all().delete()

        file = open(filename, 'r',)
        header = file.readline().strip().split(',')
        print(f"Header columns: {header}")

        # Loop through the lines manually
        for line in file:
            row = line.strip().split(',')

            try:
                dob = datetime.strptime(row[7], "%Y-%m-%d").date()
                reg_date = datetime.strptime(row[8], "%Y-%m-%d").date()
                street_address = f"{row[3].strip()} {row[4].strip()}"
                apt = row[5].strip() if row[5].strip() else None

                voter = Voter.objects.create(
                    Last_Name=row[1].strip(),
                    First_Name=row[2].strip(),
                    Street_Address=street_address,
                    Apartment_Number=apt,
                    Zip_Code=row[6].strip(),
                    Date_of_Birth=dob,
                    Date_of_Registration=reg_date,
                    Party_Affiliation=row[9].strip(),
                    precinct_number=row[10].strip(),
                    v20state=row[11].strip().lower() == 'true',
                    v21town=row[12].strip().lower() == 'true',
                    v21primary=row[13].strip().lower() == 'true',
                    v22general=row[14].strip().lower() == 'true',
                    v23town=row[15].strip().lower() == 'true',
                    voter_score=int(row[16])
                )

                print(f'Created: {voter}')

            except Exception as e:
                print(f"Skipped row due to error: {e}")
                print(f"Row: {row}")

        file.close()
        print("Done loading data.")
