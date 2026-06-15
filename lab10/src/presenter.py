from src.views.base import TransitView
from src.service import TransitService


class TransitPresenter:
    
    def __init__(self, view: TransitView, service: TransitService) -> None:
        self._view = view
        self._service = service
        self._current_stops: list[tuple[str, str]] = []


    def on_search(self, query: str) -> None:
        query = query.strip().lower()
        self._current_stops = self._service.search_stops(query)
        self._view.show_stop_list(self._current_stops)
        if not self._current_stops:
            self._view.clear_stats()

    
    def on_stop_selected(self, stop_id: str | None, stop_name: str) -> None:
        if stop_id is None:
            self._view.clear_stats()
            return
        
        stop_name = next(
            (name for sid, name in self._current_stops if sid == stop_id),
            stop_id
        )

        try:
            stats = self._service.get_stop_stats(stop_id, stop_name)
            self._view.show_stats(stats)
        except Exception as e:
            self._view.show_error(str(e))

