from abc import ABC, abstractmethod
from src.models import StopStats


class TransitView(ABC):
    """
    Abstract view interface for the transit stop explorer

    The presenter calls the show_* methods to push data into the view.
    The view valls presenter methods in response to user actions.
    """
    
    @abstractmethod
    def show_stop_list(self, stops: list[tuple[str, str]]) -> None:
        """Populate the stop list with (stop_id, stop_name) pairs."""
        pass


    @abstractmethod
    def show_stats(self, stats: StopStats) -> None:
        """Display all statistics for the selected stop."""
        pass


    @abstractmethod
    def show_error(self, message: str) -> None:
        """Display error message."""
        pass


    @abstractmethod
    def clear_stats(self) -> None:
        """Reset the statis panel to its empty state."""
        pass



