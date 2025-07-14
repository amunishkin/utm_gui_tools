# Scenario generator

## File structure

`main.py`: main program to run when executing scenario generator gui code, by `python main.py`

### support files

- `crossing_helper.py`: class for handling finding crossing points
- `csv_helper.py`: class for handling csv/text file generation
- `scenario_map.py`: automatically generated from `scenario_map.ui`, by `pyuic5 -o scenario_map.py scenario_map.ui`
- `scenario_map.ui`: Qt designer file, for gui layout
