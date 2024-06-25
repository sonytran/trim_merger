import os
import pandas as pd

TEMPLATE_DIRECTORY: str = "templatebase.csv"
INPUT_DIRECTORY: str = "input_folder"
header_rows = []

# SET TEMPLATE
with open(TEMPLATE_DIRECTORY) as file:
    for row in pd.read_csv(file).iloc[:, 0]:
        header_rows.append(row)

table = {"Measurements": header_rows}

# OPEN EACH FILE IN INPUT FOLDER
for subdir in os.listdir(INPUT_DIRECTORY):
    if subdir != ".DS_Store":
        with open(os.path.join(INPUT_DIRECTORY, subdir, "channel_independent_bench_trim.csv")) as file:
            data = pd.read_csv(file, skiprows=1)
            # Because the first row does not fit the Data Frame structure, it should be skipped.
            df = pd.DataFrame(data)
            data_list = df["efuse_name"].values.tolist()
            values = []
            results = []
            # Only pulls data from rows set in template.
            for efuse in header_rows:
                if efuse in data_list:
                    index = data_list.index(efuse)
                    values.append(df["value"].iloc[index])
                    results.append(df["result"].iloc[index])
            table[subdir + " Value"] = values
            table[subdir + " Result"] = results

pd.DataFrame(table).to_csv("output_folder/output_file.csv")

