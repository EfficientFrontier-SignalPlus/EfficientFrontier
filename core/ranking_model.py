import math
import logging
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta

from pydantic import BaseModel
from loguru import logger

# Constants
ONE_DAY_MS = 24 * 60 * 60 * 1000  # milliseconds in one day


@dataclass
class ScoreResult:
    quit: bool
    score: float
    exponentiallyWeighedDailyReturns: float
    worst14dDrawDown: float
    worst30dDrawDown: float


class DayDetailDTO(BaseModel):
    # Start time of the day, at 16:00
    startTime: int
    endTime: int
    equityStart: float
    equityEnd: float
    netFlow: float
    qualified: bool
    indexValueStart: float
    indexValueEnd: float
    mmrEnd: float
    decayedDrawDown: float
    maxIndexValue: float

    @property
    def day_pnl(self) -> float:
        return self.equityEnd - self.equityStart - self.netFlow

    @property
    def return_ratio(self) -> float:
        denominator = (self.equityStart + self.equityStart + self.netFlow) / 2
        net_flow_return_ratio = self.day_pnl / denominator if denominator != 0 else 0.0
        return min(net_flow_return_ratio, self.day_pnl / self.equityStart)

    def day_weight(self, lambda_value: float, measure_time: int, inception_time: int) -> float:
        decayRatio = math.log(0.2) / -14
        measurement_day = (measure_time - inception_time) / ONE_DAY_MS
        ex = (measurement_day - self.day(inception_time)) * -decayRatio
        return math.exp(ex * lambda_value)

    def calc_return_ratio(self) -> float:
        if self.return_ratio > 0 and not self.qualified:
            return 0.0
        return self.return_ratio

    def aum_multiplier(self) -> float:
        aum = min(self.equityStart, self.equityEnd)
        return 1 + math.log(max(0.4, aum / 500_000))

    def day(self, inception_time: int) -> int:
        diff = self.endTime - inception_time
        if diff % ONE_DAY_MS != 0:
            raise Exception("startTime must be a whole day")
        else:
            return int((self.endTime - inception_time) / ONE_DAY_MS)


@dataclass
class ScoreModel(BaseModel):
    uid: int
    subNetCreateTime: int  # Must be at 16:00
    strategyId: str
    inceptionTime: int  # Must be at 16:00
    measureTime: int  # Ensure consistent current time
    list: List[DayDetailDTO]
    lambdaValue: float
    inTopRank: bool
    minBalance: float
    quit: bool = False
    protectScore:float

    sorted_list: Optional[List[DayDetailDTO]] = None
    worst7d_draw_down: Optional[float] = None
    worst14d_draw_down: Optional[float] = None
    worst30d_draw_down: Optional[float] = None
    exponentially_weighed_daily_returns: Optional[float] = None
    measure_day_detail: Optional[DayDetailDTO] = None
    score: Optional[float] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.__post_init__()

    def __post_init__(self):
        self.sorted_list = sorted(
            [item for item in self.list if item.endTime <= self.measureTime and item.startTime >= self.inceptionTime],
            key=lambda x: x.startTime
        )
        self.measure_day_detail = next((item for item in self.sorted_list if item.endTime == self.measureTime), None)
        self.worst7d_draw_down = self.draw_down(7)
        self.worst14d_draw_down = self.draw_down(14)
        self.worst30d_draw_down = self.draw_down(30)
        self.exponentially_weighed_daily_returns = self.calculate_exponentially_weighed_daily_returns()
        self.score = self.calculate_score()

    def draw_down(self, d: int) -> float:
        record_list = [it for it in self.sorted_list if self.measureTime - it.endTime < d * 24 * 60 * 60 * 1000]
        if not record_list:
            return 0.0
        first_record_index_value_start = record_list[0].indexValueStart
        index_value_list = [first_record_index_value_start] + [item.indexValueEnd for item in record_list]
        results = []
        for index, max_value in enumerate(index_value_list):
            min_value = min(index_value_list[index:])
            result = (min_value - max_value) / max_value
            results.append(result)
        return min(results) if results else 0.0

    def calculate_exponentially_weighed_daily_returns(self) -> float:
        numerator = sum(
            item.day_weight(lambda_value=self.lambdaValue, measure_time=self.measureTime,
                            inception_time=self.inceptionTime) *
            item.calc_return_ratio() * item.aum_multiplier()
            for item in self.sorted_list
        )
        denominator = sum(
            item.day_weight(lambda_value=self.lambdaValue, measure_time=self.measureTime,
                            inception_time=self.inceptionTime)
            for item in self.sorted_list
        )
        return numerator / denominator if denominator != 0.0 else 0.0

    def is_sub_net_init(self) -> bool:
        current_time_ms = int(datetime.now().timestamp() * 1000)
        return (current_time_ms - self.subNetCreateTime) <= 14 * ONE_DAY_MS

    def calculate_score(self) -> float:
        if self.is_sub_net_init():
            if (self.measure_day_detail is None or self.measure_day_detail.equityStart < self.minBalance or
                    self.measure_day_detail.equityEnd < self.minBalance):
                return 0.01
            else:
                return 1.0
        elif self.measure_day_detail is None or not self.inTopRank:
            return 0.0
        else:
            inObserveTime=self.measure_day_detail.endTime - self.inceptionTime < 14 * ONE_DAY_MS
            if self.measure_day_detail.endTime != self.measureTime:
                s = 0.0
            elif self.quit:
                s = 0.0
            elif inObserveTime:
                s = 0.0
            elif not self.measure_day_detail.qualified:
                s = 0.0
            elif self.exponentially_weighed_daily_returns < 0:
                s = 0.0
            else:
                s = self.exponentially_weighed_daily_returns / abs(self.measure_day_detail.decayedDrawDown)

            if self.measure_day_detail.mmrEnd > 0.8:
                mmr_score = s * 0.5
            elif self.measure_day_detail.mmrEnd > 0.5:
                mmr_score = s * 0.8
            else:
                mmr_score = s
            finally_score = mmr_score * 10 * min(abs(self.measure_day_detail.day_pnl) / 1000, 1)
            if finally_score <= 0 and not inObserveTime:
                return self.protectScore
            else:
                return finally_score

    def get_result(self) -> ScoreResult:
        if not self.sorted_list and not self.is_sub_net_init:
            logger.error(f"lack of data [{self.strategyId}]")
            raise Exception("lack of data")
        if self.sorted_list and self.sorted_list[-1].endTime != self.measureTime:
            logger.error(f"lack of measureTime data [{self.strategyId}] [{self.measureTime}] [{self.sorted_list}]")

        index = -1
        is_continuous = True
        for item in self.sorted_list:
            index += 1
            expected_start_time = self.inceptionTime + index * ONE_DAY_MS
            if item.startTime != expected_start_time:
                is_continuous = False
                break

        if not is_continuous:
            logger.error(f"startTime must be continuous [{self.strategyId}] [{self.measureTime}] [{self.sorted_list}]")

        return ScoreResult(
            quit=self.quit,
            score=self.calculate_score(),
            exponentiallyWeighedDailyReturns=self.calculate_exponentially_weighed_daily_returns(),
            worst14dDrawDown=self.worst14d_draw_down,
            worst30dDrawDown=self.worst30d_draw_down
        )
