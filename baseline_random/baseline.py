from dataclasses import dataclass
import argparse
import numpy as np
import pandas as pd
import json
import sys


@dataclass
class CustomParameters:
    random_state: int = 42


class AlgorithmArgs(argparse.Namespace):
    @property
    def ts_length(self) -> int:
        return self.df.shape[0]

    @property
    def df(self) -> pd.DataFrame:
        return pd.read_csv(self.dataInput)

    @staticmethod
    def from_sys_args() -> 'AlgorithmArgs':
        args: dict = json.loads(sys.argv[1])
        custom_parameter_keys = dir(CustomParameters())
        filtered_parameters = dict(
            filter(lambda x: x[0] in custom_parameter_keys, args.get("customParameters", {}).items()))
        args["customParameters"] = CustomParameters(**filtered_parameters)
        return AlgorithmArgs(**args)


def execute(args: AlgorithmArgs):
    np.random.seed(args.customParameters.random_state)
    anomaly_scores = np.random.uniform(0, 1, args.ts_length)
    anomaly_scores.tofile(args.dataOutput, sep="\n")


if __name__ == "__main__":
    args = AlgorithmArgs.from_sys_args()

    if args.executionType == "train":
        print("This algorithm does not need to be trained!")
    elif args.executionType == "execute":
        execute(args)
    else:
        raise ValueError(f"No executionType '{args.executionType}' available! Choose either 'train' or 'execute'.")
