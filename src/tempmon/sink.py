from abc import ABC, abstractmethod
from metric import Metric

class Sink(ABC):

   @abstractmethod
   def store_metric(self, metric : Metric) -> None:
       pass