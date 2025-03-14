from collections import defaultdict
from pathlib import Path
from typing import List

import click
from pandas import DataFrame


def stripSpaces(inputStr: str) -> List[str]:
    return list(filter(None, inputStr.strip().split(sep=" ")))


def buildDF(data: List[List[str]]) -> DataFrame:
    dataDict: dict[str, List[str]] = defaultdict(list)

    datum: List[str]
    for datum in data:
        dataDict["name"].append(datum[1])
        dataDict["version"].append(datum[2])
        dataDict["architecture"].append(datum[3])
        dataDict["description"].append(" ".join(datum[4::]))

    return DataFrame(data=dataDict)


@click.command()
@click.option(
    "-i",
    "--input",
    "inputFP",
    help="Path to dpkg --list output as a file",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
)
@click.option(
    "-o",
    "--output",
    "outputFP",
    help="File to write CSV file to",
    type=click.Path(
        exists=False,
        file_okay=True,
        dir_okay=False,
        writable=True,
        readable=False,
        resolve_path=True,
        path_type=Path,
    ),
    required=True,
)
def main(inputFP: Path, outputFP: Path) -> None:
    data: List[List[str]] = []

    with open(inputFP, "r") as fp:
        dpkgOutput: List[str] = fp.readlines()[5::]
        fp.close()

    line: str
    for line in dpkgOutput:
        data.append(stripSpaces(inputStr=line))

    df: DataFrame = buildDF(data=data)
    df.to_csv(path_or_buf=outputFP, index=False)


if __name__ == "__main__":
    main()
