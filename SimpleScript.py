import tkinter as tk
from tkinter import filedialog, messagebox
 
variables = {}
functions = {}
text_box = None
 
def execute_command(command):
    command = command.strip()
    if command.startswith("#"):  # コメント行を無視
        append_output(f"Comment skipped: {command}")
        return
    try:
        if command.startswith("print "):
            print_value(command[6:].strip('"'))
        elif command.startswith("add "):
            math_operation(command, '+')
        elif command.startswith("subtract "):
            math_operation(command, '-')
        elif command.startswith("multiply "):
            math_operation(command, '*')
        elif command.startswith("divide "):
            math_operation(command, '/')
        elif command.startswith("concat "):
            string_concatenation(command)
        elif command.startswith("var "):
            declare_variable(command)
        elif command.startswith("del "):
            delete_variable(command)
        elif command.startswith("if "):
            condition_check(command)
        elif command.startswith("increment "):
            increment_variable(command)
        elif command.startswith("decrement "):
            decrement_variable(command)
        elif command.startswith("loop "):
            loop_command(command)
        elif command.startswith("for "):
            for_loop(command)
        elif command.startswith("def "):
            define_function(command)
        elif command.startswith("call "):
            call_function(command)
        elif command.startswith("list "):
            handle_list(command)
        elif command.startswith("dict "):
            handle_dict(command)
        elif command.startswith("help"):
            show_help()
        else:
            raise ValueError(f"Unknown command: {command}")
    except Exception as e:
        print(f"Error executing command '{command}': {e}")
        append_output(f"Error: {str(e)}")
 
def print_value(message):
    output = variables.get(message.strip('"'), message.strip('"'))
    append_output(output)
 
def append_output(output):
    """ GUIのテキストボックスに出力を追加する """
    text_box.insert(tk.END, str(output) + '\n')
 
def string_concatenation(command):
    parts = command.split(" ")
    if len(parts) == 4 and parts[2] == "+":
        str1 = get_value(parts[1])
        str2 = get_value(parts[3])
        append_output(str1 + str2)
    else:
        append_output("Invalid string concatenation syntax.")
 
def math_operation(command, operator):
    parts = command.split()
    if len(parts) == 3:
        try:
            x = get_value(parts[1])
            y = get_value(parts[2])
            if operator == '+':
                result = x + y
            elif operator == '-':
                result = x - y
            elif operator == '*':
                result = x * y
            elif operator == '/':
                if y == 0:
                    raise ZeroDivisionError("Division by zero error.")
                result = x / y
            append_output(result)
        except ValueError:
            append_output("Value is not a number.")
    else:
        append_output("Invalid arguments.")
 
def declare_variable(command):
    parts = command.split("=")
    if len(parts) == 2 and len(parts[0]) >= 4:
        var_name = parts[0][4:].strip()
        var_value = parts[1].strip()
        try:
            variables[var_name] = float(var_value) if '.' in var_value else int(var_value)
            append_output(f"Assigned {var_value} to variable {var_name}.")
        except ValueError:
            append_output("Invalid variable value.")
    else:
        append_output("Invalid variable declaration.")
 
def delete_variable(command):
    var_name = command[4:].strip()
    if var_name in variables:
        del variables[var_name]
        append_output(f"Deleted variable {var_name}.")
    else:
        append_output(f"Variable {var_name} is undefined.")
 
def condition_check(command):
    condition_str = command[3:].strip()
    if "else" in condition_str:
        condition, else_command = condition_str.split("else", 1)
        if get_condition(condition.strip()):
            append_output("Condition is true. Executing if block.")
            execute_command(else_command.strip())
        else:
            append_output("Condition is false. Executing else block.")
    else:
        if get_condition(condition_str):
            append_output("Condition is true.")
        else:
            append_output("Condition is false.")
 
def increment_variable(command):
    var_name = command[10:].strip()
    if var_name in variables:
        variables[var_name] += 1
        append_output(f"Incremented {var_name}: {variables[var_name]}")
    else:
        append_output(f"Variable {var_name} is undefined.")
 
def decrement_variable(command):
    var_name = command[11:].strip()
    if var_name in variables:
        variables[var_name] -= 1
        append_output(f"Decremented {var_name}: {variables[var_name]}")
    else:
        append_output(f"Variable {var_name} is undefined.")
 
def for_loop(command):
    parts = command.split(" ")
    if len(parts) == 6 and parts[1] == "in":
        var_name = parts[2]
        start = int(parts[3])
        end = int(parts[5])
        for i in range(start, end + 1):
            variables[var_name] = i
            execute_command(parts[4])
 
def loop_command(command):
    parts = command.split(" ")
    if len(parts) >= 4 and parts[1] == "until":
        loop_condition = " ".join(parts[2:])
        while not get_condition(loop_condition):
            execute_command(parts[3])
 
def get_condition(condition):
    try:
        if "and" in condition:
            left, _, right = condition.partition(" and ")
            return get_condition(left) and get_condition(right)
        elif "or" in condition:
            left, _, right = condition.partition(" or ")
            return get_condition(left) or get_condition(right)
 
        left, operator, right = condition.split()
        left_value = get_value(left)
        right_value = get_value(right)
 
        if operator == "==":
            return left_value == right_value
        elif operator == "<":
            return left_value < right_value
        elif operator == ">":
            return left_value > right_value
    except Exception as e:
        append_output(f"Condition check error: {str(e)}")
        return False
    return False
 
def define_function(command):
    parts = command.split()
    function_name = parts[1]
    function_body = " ".join(parts[2:])
    functions[function_name] = function_body
    append_output(f"Defined function {function_name}.")
 
def call_function(command):
    function_name = command[5:].strip()
    if function_name in functions:
        body = functions[function_name]
        execute_command(body)
    else:
        append_output(f"Function {function_name} is undefined.")
 
def get_value(value):
    if value in variables:
        return variables[value]
    else:
        try:
            return float(value)
        except ValueError:
            append_output(f"Invalid value: {value}")
            return None
 
def handle_list(command):
    parts = command.split("=")
    if len(parts) == 2:
        list_name = parts[0][5:].strip()
        elements = parts[1].strip().strip("[]").split(",")
        variables[list_name] = [get_value(e.strip()) for e in elements]
        append_output(f"Created list {list_name}: {variables[list_name]}")
    else:
        append_output("Invalid list declaration.")
 
def handle_dict(command):
    parts = command.split("=")
    if len(parts) == 2:
        dict_name = parts[0][5:].strip()
        entries = parts[1].strip().strip("{}").split(",")
        dict_values = {}
        for entry in entries:
            key, value = entry.split(":")
            dict_values[key.strip()] = get_value(value.strip())
        variables[dict_name] = dict_values
        append_output(f"Created dictionary {dict_name}: {variables[dict_name]}")
    else:
        append_output("Invalid dictionary declaration.")
 
def show_help():
    help_text = (
        "Available commands:\n"
        "1. print <message>: Outputs a message to the console.\n"
        "2. var <name> = <value>: Declares a variable.\n"
        "3. del <name>: Deletes a variable.\n"
        "4. if <condition>: Checks a condition.\n"
        "5. add|subtract|multiply|divide <num1> <num2>: Performs mathematical operations.\n"
        "6. loop <command> until <condition>: Repeats a command until the condition is true.\n"
        "7. for <variable> in <start> to <end>: Loops through a range.\n"
        "8. def <function_name> <commands>: Defines functions.\n"
        "9. call <function_name>: Calls a defined function.\n"
        "10. list <name> = [<elements>]: Creates a list.\n"
        "11. dict <name> = {<key:value pairs>}: Creates a dictionary.\n"
        "12. concat <str1> + <str2>: Concatenates two strings.\n"
        "13. increment <var_name>: Increases a variable by 1.\n"
        "14. decrement <var_name>: Decreases a variable by 1.\n"
        "15. help: Displays this help text."
    )
    append_output(help_text)
 
def setup_gui():
    global text_box
    root = tk.Tk()
    root.geometry('800x400')
    root.title("SimpleScript")
 
    text_box = tk.Text(bg="#000", fg="#fff", insertbackground="#fff", height=20, width=100)
    text_box.pack(expand=True, fill='both')
 
    ok_button = tk.Button(text="Execute", command=execute_script)
    ok_button.pack(pady=10)
 
    save_button = tk.Button(text="Save", command=save_script)
    save_button.pack(side="left", padx=10, pady=10)
 
    load_button = tk.Button(text="Load", command=load_script)
    load_button.pack(side="left", padx=10, pady=10)
 
    root.mainloop()
 
def execute_script():
    commands = text_box.get("1.0", "end").strip().splitlines()
    for cmd in commands:
        if cmd:
            execute_command(cmd)
 
def save_script():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            content = text_box.get("1.0", "end")
            file.write(content)
 
def load_script():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text_box.delete("1.0", "end")
            text_box.insert("1.0", content)
 
setup_gui()
 
