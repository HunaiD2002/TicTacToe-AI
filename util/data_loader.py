import pandas as pd

from util import ENCODING, LABELS


def load_arff_dataset(path):
    """
    load arff dataset
    :param path:
    :return:
    """

    data_lines = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('%') or line.lower().startswith('@'):
                continue
            data_lines.append(line)

    rows = [l.split(',') for l in data_lines]
    df = pd.DataFrame(rows)

    # last column is the 'class' (won or not)
    df.columns = [f"c{i}" for i in range(9)] + ["label"]

    X = df.iloc[:, :-1].applymap(lambda v: ENCODING[v]).values
    y = df["label"].map(lambda v: LABELS[v]).values

    return X, y