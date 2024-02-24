from abc import ABC, abstractmethod
from button import Button
from metric import Metric

class Sink(ABC):

   @abstractmethod
   def store_metric(self, metric : Metric) -> None:
       pass

   @abstractmethod
   def store_button(self, metric: Button) -> None:
       pass
