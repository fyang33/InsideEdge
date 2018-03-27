"""Main script for generating output.csv."""

import os
import pandas

DIR = os.path.dirname(__file__)

def main():
    # AVG = sum(H)/sum(AB)
    # OBP = sum(H) + sum(BB) + sum(HBP)/(sum(AB) + sum(BB) + sum(HBP) + sum(SF))
    # SLG = sum(TB) /sum(AB)
    # OPS = OBP + SLG

    file = pandas.read_csv(DIR + "data/raw/pitchdata.csv")
    split_map = {"vs RHP": file[file['PitcherSide'] == 'R'],
                 "vs LHP": file[file['PitcherSide'] == 'L'],
                 "vs RHH": file[file['HitterSide'] == 'R'],
                 "vs LHH": file[file['HitterSide'] == 'L']}
    stat_map = {"AVG": lambda x: x["H"] / x["AB"],
                "OBP": lambda x: (x["H"] + x["BB"] + x["HBP"]) / (x["AB"] + x["BB"] + x["HBP"] + x["SF"]),
                "SLG": lambda x: x["TB"] / x["AB"],
                "OPS": lambda x: x["TB"] / x["AB"] + (x["H"] + x["BB"] + x["HBP"]) / (x["AB"] + x["BB"] + x["HBP"] + x["SF"])
                }

    query = pandas.read_csv(DIR + "data/reference/combinations.txt")

    res = []
    for q in query.itertuples():
        data = split_map[q.Split].groupby(q.Subject, as_index=False).sum()
        data = data[data["PA"] >= 25]
        data["SubjectId"] = data[q.Subject]
        data["Value"] = stat_map[q.Stat](data).round(3)
        data["Stat"] = q.Stat
        data["Split"] = q.Split
        data["Subject"] = q.Subject
        res.append(data[["SubjectId", "Stat", "Split", "Subject", "Value"]])
    res = pandas.concat(res).sort_values(["SubjectId", "Stat", "Split", "Subject"])
    res.to_csv(DIR + "data/processed/output.csv",index=False)

if __name__ == '__main__':
    main()
