# from altair_saver import save
import math
import re
import typing
from pathlib import Path, PosixPath

import matplotlib.pyplot as plt
import pandas as pd


# alt.data_transformers.disable_max_rows()


class DataPoint(typing.NamedTuple):
    theta: float
    radius: float
    quality: int

    @property
    def x(self):
        return self.radius * math.cos(self.theta)

    @property
    def y(self):
        return self.radius * math.sin(self.theta)


class RpData:
    @staticmethod
    def read_data(fp: typing.TextIO):
        result = []
        fp.seek(0)
        second_scan = False
        line = "Start"
        match_count = 0
        ptrn = re.compile(
            "^S*\s+theta:\s(?P<theta>[\d,\.]+)\sDist:" +
            "\s(?P<radius>[\d,\.]+)\sQ:\s(?P<quality>\d+)"
        )

        # theta goes theta = 0 => phi = 90 | pi/2
        # theta = 90 => phi = 0
        # if theta < 90 => phi = pi/2 - theta
        # if theta > 90 => phi = 2pi - (theta - pi/2)

        cycle_once = True

        while not second_scan and len(line) != 0:
            line = fp.readline()
            if re.match("S\s+theta:", line):
                match_count += 1
            if match_count >= 2:
                mch = re.match(ptrn, line)
                if mch:
                    tmp = mch.groupdict()
                    phi = math.pi/2.0 - math.pi*float(tmp["theta"])/180.0
                    if float(tmp["theta"]) > 90.0:
                        phi = 2.0*math.pi + phi
                    if int(tmp["quality"]) > 150:
                        result.append(DataPoint(
                            theta=phi,
                            radius=float(tmp["radius"]),
                            quality=int(tmp["quality"])
                        ))

        return result

    def __init__(self, filename: [str, Path]):
        if type(filename) != PosixPath:
            filename = Path(filename)
        filename = filename.expanduser()
        if not filename.exists():
            raise FileNotFoundError(
                f"{str(self.filename)} not found, please check file path")
        self.filename = filename

        with open(self.filename, 'r') as fp:
            self.data = RpData.read_data(fp)

    def data_as_df(self):
        xv, yv = ([], [])
        [(xv.append(o.x), yv.append(o.y)) for o in self.data if o.x and o.y]
        df = pd.DataFrame({'X': xv, 'Y': yv}, columns=['X', 'Y'])
        df = df.astype({"X": "float64", "Y": "float64"})
        return df

    def plot(self):
        # plt = alt.Chart(self.data_as_df()).mark_circle(size=60).encode(
        #     x='X',
        #     y='Y',
        #     tooltip=['X', 'Y']
        # )
        # save(plt, "data.png", fmt="png")
        df = self.data_as_df()
        plt.scatter(df['X'], df['Y'], s=1, marker=',')
        plt.savefig("data.png")
