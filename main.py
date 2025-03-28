from my_module import add, subtract, multiply, divide

print(f"Add: 2 + 3 = {add(2, 3)}")
print(f"Subtract: 5 - 2 = {subtract(5, 2)}")
print(f"Multiply: 4 * 3 = {multiply(4, 3)}")
print(f"Divide: 10 / 2 = {divide(10, 2)}")

try:
    print(divide(10, 0))
except ValueError as e:
    print(e)

import importlib
import my_module
importlib.reload(my_module.math_operations)
importlib.reload(my_module)
from my_module import add, subtract, multiply, divide# Step 9: Using `sys.path` to Add Module Directories


import sys
import os
import importlib
module_path='/workspaces/BME3053C-Spring-2025'
if module_path not in sys.path:
    sys.path.append(module_path)

import my_module
importlib.reload(my_module.math_operations)
importlib.reload(my_module)
from my_module import add, subtract, multiply, divide

print(f"5 + 3 = {add(5, 3)}")