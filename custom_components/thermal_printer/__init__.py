"""Prints stuff on a thermal printer."""
from __future__ import annotations

import escpos.printer
import logging
import os.path

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType


DOMAIN = "thermal_printer"
_LOGGER = logging.getLogger(__name__)
LOGO_FILENAME="horizontal_logo_500.png"


# These are expected in the service call.
# Example:
#   service: thermal_printer.shopping_list_print
#   data:
#     todo_list_id: 'todo.my_shopping_list'
#     printer_hostname: '192.168.1.123'  # or a hostname
TODO_LIST_ID_KEY="todo_list_id"
PRINTER_HOSTNAME_KEY="printer_hostname"


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the sync service for printing lists."""

    # Locate the logo
    this_dir = os.path.dirname(__file__)
    logo_file = os.path.join(this_dir, LOGO_FILENAME)

    def print_list(printer_hostname: str, items: List[str]) -> None:
        printer = escpos.printer.Network(printer_hostname)
        printer.set(align="center")
        printer.image(logo_file)

        printer.set(align="left")
        printer.text("\n")
        printer.text("\n")
        printer.text("Your shopping list:\n")
        printer.text("\n")
        for item in items:
            printer.text(f"  - {item}\n")
        printer.text("\n")
        printer.text("\n")
        printer.cut()

    def shopping_list_print(call: ServiceCall) -> None:
        """Thermal print service."""

        # Get the printer hostname.
        # I do not know how to put this in the config.
        if PRINTER_HOSTNAME_KEY not in call.data:
            msg = (
                f"You did not pass `{PRINTER_HOSTNAME_KEY}` in your "
                "request, so I don't know which printer should I use."
            )
            _LOGGER.error(msg)
            raise ValueError(msg)
        printer_hostname = call.data[PRINTER_HOSTNAME_KEY]

        # Get the todo list entity ID
        if TODO_LIST_ID_KEY not in call.data:
            msg = (
                f"You did not pass `{TODO_LIST_ID_KEY}` in your "
                "request, so I don't know which todo list to print."
            )
            _LOGGER.error(msg)
            raise ValueError(msg)
        todo_list_id = call.data[TODO_LIST_ID_KEY]

        # Get items from the list
        results = hass.services.call(
            "todo", "get_items",
            {
                "entity_id": todo_list_id,
                "status": "needs_action",
            },
            blocking=True,
            return_response=True,
        )
        items = []
        for result in results[todo_list_id]["items"]:
            items.append(result["summary"])

        # Print it!
        print_list(printer_hostname=printer_hostname, items=items)

    hass.services.register(DOMAIN, "shopping_list_print", shopping_list_print)
    # Report initialization as successful. If the printer is unreachable
    # then individual requests will fail as they are received.
    return True
