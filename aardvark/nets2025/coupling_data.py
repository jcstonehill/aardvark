def read_data(path: str):

    data: list[list] = []

    with open(path, "r") as file:
        lines = file.readlines()

        for line in lines:
            data.append([])

            line = line.replace(" ", "")
            line = line.replace("\n", "")
            
            vals = line.split(",")

            for val in vals:
                data[-1].append(float(val))

    return data

fuel_T = read_data("playground/coupling_data/fuel_T.csv")
fuel_prop_T = read_data("playground/coupling_data/fuel_prop_T.csv")
fuel_prop_rho = read_data("playground/coupling_data/fuel_prop_rho.csv")