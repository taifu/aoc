from typing import TypeAlias, Union
from math import copysign


X, Y, Z = 0, 1, 2
COORD_DTS: TypeAlias = Union[list[float], tuple[float, ...]]


def determinant(mat1: COORD_DTS, mat2: COORD_DTS) -> float:
    return mat1[0] * mat2[1] - mat1[1] * mat2[0]


class InterceptionNotFound(Exception):
    pass


class Point:
    def __init__(self, raw: str) -> None:
        parts = raw.split(' @ ')
        self.xyz: COORD_DTS = [int(coord) for coord in parts[0].split(', ')]
        self.dts: COORD_DTS = [int(coord) for coord in parts[1].split(', ')]
        self.old_transpose_dts: COORD_DTS = (0, 0, 0)

    @property
    def P2(self) -> COORD_DTS:
        return tuple(self.xyz[n] + self.dts[n] for n in (X, Y, Z))

    def transpose(self, dts: COORD_DTS) -> None:
        self.dts = tuple(self.dts[n] - dts[n] + self.old_transpose_dts[n] for n in range(3))
        self.old_transpose_dts = dts

    def intersect(self, other: "Point") -> tuple[float, float]:
        # https://stackoverflow.com/questions/20677795/how-do-i-compute-the-intersection-point-of-two-lines
        x_diff, y_diff = (-self.dts[X], -other.dts[X]), (-self.dts[Y], -other.dts[Y])

        div_diff = determinant(x_diff, y_diff)
        if div_diff == 0:
            raise InterceptionNotFound

        d = (determinant(self.xyz, self.P2), determinant(other.xyz, other.P2))
        return determinant(d, x_diff) / div_diff, determinant(d, y_diff) / div_diff

    def get_time(self, point: COORD_DTS) -> float:
        if self.dts[X] == 0:
            return (point[Y] - self.xyz[Y]) / self.dts[Y]
        assert self.dts[X] != 0
        return (point[X] - self.xyz[X]) / self.dts[X]

    def get_dz_rock(self, other: "Point", intercept: COORD_DTS) -> float:
        # Given the universal intersection point and another hail:
        #    z_rock = z_this  + time_this  * (dz_this  - dz_rock)
        #    z_rock = z_other + time_other * (dz_other - dz_rock)
        #
        # Given time:
        #    time = (x_intercept - x) / dx
        #
        # Then (equalizing right sides of z_rock and solving for dz_rock):
        #    z_this  + time_this  * (dz_this  - dz_rock) = z_other + time_other * (dz_other - dz_rock)
        #    z_this  + time_this  * (dz_this  - dz_rock) - z_other - time_other * (dz_other - dz_rock) = 0
        #    z_this  + time_this  * (dz_this  - dz_rock) - z_other - time_other * (dz_other - dz_rock) = 0
        #    z_this  + time_this * dz_this - time_this * dz_rock - z_other -time_other * dz_other + time_other * dz_rock = 0
        #    z_this  + time_this * dz_this  - z_other -time_other * dz_other  = 0
        #    dz_rock (time_other - time_this) = - z_this  - time_this * dz_this  + z_other + time_other * dz_other
        #    dz_rock (time_other - time_this) = z_other - z_this  - time_this * dz_this + time_other * dz_other
        #    dz_rock  = z_other - z_this  - time_this * dz_this + time_other * dz_other / (time_other - time_this)
        time_this, time_other = self.get_time(intercept), other.get_time(intercept)
        return (other.xyz[Z] - self.xyz[Z] - time_this * self.dts[Z] + time_other * other.dts[Z]) / (time_other - time_this)


class Hails:
    def __init__(self, raw: str):
        self.hails = [Point(line) for line in raw.splitlines()]

    def in_future(self, point: COORD_DTS, hail: Point) -> bool:
        return copysign(1, point[X] - hail.xyz[X]) == copysign(1, hail.dts[X]) and copysign(1, point[Y] - hail.xyz[Y]) == copysign(1, hail.dts[Y])

    def crossing(self) -> int:
        min_xy, max_xy = (200000000000000, 400000000000000) if len(self.hails) > 100 else (7, 27)
        count = 0
        for n, hail1 in enumerate(self.hails[:-1]):
            for hail2 in self.hails[n + 1:]:
                try:
                    point = hail1.intersect(hail2)
                    if point[X] is not None and min_xy <= point[X] <= max_xy and min_xy <= point[Y] <= max_xy:
                        if self.in_future(point, hail1) and self.in_future(point, hail2):
                            count += 1
                except InterceptionNotFound:
                    pass
        return count

    def rock(self) -> int:
        # Assuming that rock_dts is the rock velocity, if we transpose every hail
        # velocity as hail_dts - rock_dts, then we can brute force a X,Y point
        # where every transposed hail intecepts
        interval_dts = 0
        while True:
            interval_dts += 1
            for abs_dvx in range(interval_dts):
                for dvx in (abs_dvx, -abs_dvx):
                    for dvy in (interval_dts - abs_dvx, -interval_dts + abs_dvx):
                        self.hails[0].transpose((dvx, dvy, 0))
                        try:
                            first_found = True
                            for hail2 in self.hails[1:]:
                                hail2.transpose((dvx, dvy, 0))
                                new_intersect = self.hails[0].intersect(hail2)
                                if first_found:
                                    first_found, first_intersect = False, new_intersect
                                    continue
                                elif new_intersect != first_intersect:
                                    raise InterceptionNotFound
                        except InterceptionNotFound:
                            continue
                        # Found a single X,Y point where every Hail intercept
                        # with dvx, dvy transposing: must be the right one!
                        first_found = True
                        for hail2 in self.hails[1:]:
                            new_dz_rock = self.hails[0].get_dz_rock(hail2, first_intersect)
                            if first_found:
                                first_found, dz_rock = False, new_dz_rock
                                continue
                            elif dz_rock != new_dz_rock:
                                # One hail with different dz_rock, can't be!
                                raise Exception(f"Unexpected dz Rock: {dz_rock} from {(self.hails[0].xyz, self.hails[0].dts)}")
                        rock_z = self.hails[0].xyz[Z] + self.hails[0].get_time(first_intersect) * (self.hails[0].dts[Z] - dz_rock)
                        return int(first_intersect[0] + first_intersect[1] + rock_z)
        raise Exception("Not found")


def solve1(data: str) -> int:
    return Hails(data).crossing()


def solve2(data: str) -> int:
    return Hails(data).rock()


if __name__ == "__main__":
    import sys
    data = open((sys.argv + ["input.txt"])[1]).read()
    print(solve1(data))
    print(solve2(data))
