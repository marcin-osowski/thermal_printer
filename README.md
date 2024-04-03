# Thermal printer integration for Home Assistant

This custom component creates a service that can print a shopping
to-do list on a networked ESC/POS thermal printer. It is using
[python-escpos](https://github.com/python-escpos/python-escpos).

I have tested it on Epson TM-T20III (Ethernet), but it should work
on a wide variety of networked thermal printers. With small modifications
it should also work on a locally connected printers (RS-232, USB).

## Usage

  1. Put the files under your Home Assistant's
     `config/custom_components/thermal_printer`.

  2. Add this line to your `configuration.yaml`:
     ```
     thermal_printer:
     ```

  3. Restart Home Assistant.

  4. Try out the new service via Developer tools -> Services (YAML mode):
     ```
     service: thermal_printer.shopping_list_print
     data:
       todo_list_id: todo.[YOUR_TODO_LIST]
       printer_hostname: [YOUR_PRINTER_HOSTNAME_OR_IP]
     ```
     Check system logs if you see any errors, or if the printer doesn't print.

  5. Create a script to call the service easily via Settings ->
     Automations & Scenes -> Scripts -> Add Script. Then switch to YAML
     and use the following:
     ```
     alias: Print the shopping list to paper
     sequence:
       - service: thermal_printer.shopping_list_print
         data:
           todo_list_id: todo.[YOUR_TODO_LIST]
           printer_hostname: [YOUR_PRINTER_HOSTNAME_OR_IP]
     mode: single
     icon: mdi:printer-check
     ```

