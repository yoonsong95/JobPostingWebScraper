class Job:
    def __init__(self, title, company, location, rating):
        self.title = title
        self.company = company
        self.location = location
        self.rating = rating
    
    def writeTextFile(self, file):
        file.write(f"{self.title}\n")
        file.write(f"{self.company}\n")
        file.write(f"{self.location}\n")
        file.write(f"{self.rating}\n")
        file.write(f"\n")    

    def writeCSVFile(self, writer):
        writer.writerow([self.title, self.company, self.location, self.rating])
