# Unsafe names Checker

Checks for possible unsafe names present in a specific folder.

#### Requirements

The python script requires Python 3.0 or higher.

#### Run

The command-line parameters to run the checkNames.py scripts are as follow:

```
python3 checkNames  [path_to_check]
                    [tcl_procs or all_files]
                    [only_results or create_table]
                    [table_filename]
```

- ```path_to_check``` Requires a valid path to the root folder that you want to be check (other folders are obtained recursively).
- ```tcl_procs or all_files``` Is a boolean constant (0 or 1) that defines if you want to run the checks only for TCL procedures (0) or if you want to check all files (1). Each one uses a different unsafe names list, named ```unsafe_list.txt``` and ```unsafe_list2.txt```.
- ```only_results or create_table``` Is a boolean constant (0 or 1) that defines if you want to export a table (1) or not (0). The table format is values separated by semi-colons.
- ```table_filename``` is only required if ```only_results or create_table``` is set to 1. This specifies the output text file that you want to save the table on.

An example oF how to use the command is found below:

```
python3 checkNames home/myFolder 1 1 home/export/table.txt
```

You can also modify the ```unsafe_list.txt``` or ```unsafe_list2.txt``` file to add/remove unsafe names.
