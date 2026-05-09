"""
Data classes representing individual events in an AUDL game.

Events are parsed from the ``tsgHome.events`` and ``tsgAway.events`` JSON
arrays returned by the UFA stats API at:
    https://www.backend.ufastats.com/stats-pages/game/<game_id>

Each event is a JSON dict with at minimum a ``t`` field (event type integer
code). Additional fields are present depending on the type:

- ``l`` – lineup: list of 7 player IDs (offensive/defensive point start,
  timeout substitution).
- ``r`` – receiver: player ID of the disc recipient (completed pass, goal,
  drop, pull, block).
- ``x``, ``y`` – disc position on the field at the moment of the event,
  in yards from the back of the end zone.
- ``s`` – score/state value (timeout events).
- ``c`` – call type (field calls).

See ``audl.stats.library.parameters.HerokuPlay`` and ``game_event_dict`` for
the complete event-type mapping.
"""

import pandas as pd
from abc import ABC


class GameEvent(ABC):
    """Abstract base class for a single AUDL game event.

    Parameters
    ----------
    row : dict
        Raw JSON event dict, e.g.
        ``{'t': 20, 'r': 9262, 'x': 12.89, 'y': 18.93}``.
    description : str
        Human-readable label for this event type (e.g. ``'Pass Completed'``).
    """

    def __init__(self, row, description):
        """
        Parameters
        ----------
        row : dict
            Raw JSON event dict with fields ``[t, l, r, x, y, s, c, q]``.
        description : str
            Human-readable description of the event type.
        """
        self.row = row
        self.description = description

    def print(self):
        """Print a formatted representation of this event."""
        pass

    def _read_json_dict(self):
        """Parse ``self.row`` into structured fields.

        Implemented by subclasses to extract the fields relevant to their
        event type.
        """
        pass


class GameEventSimple(GameEvent):
    """Event that carries only the type code ``t`` (no lineup or receiver).

    Used for events that carry no additional context, such as end-of-quarter
    markers (t=23–26) and start-of-game (t=50).
    """

    def __init__(self, code_type, description, json_dict):
        super().__init__(code_type, json_dict)

    def print(self):
        """Print the event type code."""
        print(f"t: {self.code_type}")


class GameEventLineup(GameEvent):
    """Event that carries a lineup array ``l`` (7 player IDs).

    Emitted at the start of every offensive (t=1) and defensive (t=2) point,
    and when a timeout results in a lineup substitution (t=40 defense,
    t=41 offense).
    """

    def __init__(self, code_type, description, json_dict):
        super().__init__(code_type, json_dict)

    def print(self):
        """Print a formatted representation of this lineup event."""
        pass


class GameEventReceiver(GameEvent):
    """Event that identifies a receiver via the player ID field ``r``.

    Used for passes completed (t=20), goals scored (t=22), drops (t=19),
    pulls (t=3), and blocks (t=5). Events of type t=20 and t=22 also carry
    ``x`` and ``y`` disc-position fields.
    """

    def __init__(self, code_type, description, json_dict):
        super().__init__(code_type, json_dict)

    def print(self):
        """Print a formatted representation of this receiver event."""
        pass


class GameEventS(GameEvent):
    """Event that carries a score/state value in field ``s``.

    Used for timeout events: timeout called while on offense (t=14) and
    timeout called while on defense (t=15).
    """

    def __init__(self, code_type, description, json_dict):
        super().__init__(code_type, json_dict)

    def print(self):
        """Print a formatted representation of this event."""
        pass
