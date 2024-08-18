fuel_T: list[list] = []

with open("playground/coupling_data/fuel_T.csv", "r") as file:
    lines = file.readlines()

    for line in lines:
        fuel_T.append([])

        line = line.replace(" ", "")
        line = line.replace("\n", "")
        
        vals = line.split(",")
        
        for val in vals:
            fuel_T[-1].append(float(val))