# NVDA Accessibility Module for Notepad++

This repository contains a custom NVDA (Non-Visual Desktop Access) module designed to enhance the accessibility of **Notepad++** for visually impaired users. The module adds a set of keyboard shortcuts to improve navigation and code editing in Notepad++, making it easier for users with visual impairments to program in Python.

## Project Overview

The goal of this project is to improve the accessibility of **Notepad++** by developing an NVDA add-on that integrates additional keyboard shortcuts. These shortcuts are specifically designed to facilitate code navigation, selection, and execution, making the coding experience more efficient and user-friendly for visually impaired developers.

### Key Features

The module introduces the following keyboard shortcuts to enhance the user experience in Notepad++:

#### Code Navigation
- **NVDA + F2**: Move to the next function
- **Shift + F2**: Move to the previous function
- **F7**: Move to the next class
- **Shift + F7**: Move to the previous class

#### Selection
- **Ctrl + Shift + R**: Select the current class
- **Ctrl + R**: Select the current function

#### Deletion
- **Ctrl + Shift + Delete**: Delete the current class
- **Ctrl + Delete**: Delete the current function

#### Code Execution
- **Ctrl + F5**: Execute Python code

#### Indentation Navigation
- **Alt + Down Arrow**: Move to the next indentation level
- **Alt + Up Arrow**: Move to the previous indentation level
- **Ctrl + Alt + Down Arrow**: Move to the next indented line
- **Ctrl + Alt + Up Arrow**: Move to the previous indented line

#### Indentation Selection
- **Shift + Alt + Down Arrow**: Select to the next indentation level
- **Shift + Alt + Up Arrow**: Select to the previous indentation level

#### Specific Navigation
- **Alt + !**: Go to the first line of the indentation block
- **Alt + :**: Go to the last line of the indentation block

### Compatibility
- **Notepad++**: Must be used in **32-bit** version.
- **Python**: Must be used in **32-bit** version.
- **NVDA**: The module is designed to be compatible with NVDA's standard add-on structure.

## Installation

To install the module, follow these steps:
/// NEED TO MODIFY AS OF THERE BECAUSE AINT SURE IF I'll LEAVE THE APPMODULE OR THE NVDA-ADDON

1. **Download the module**: The module is available as a `.nvda-addon` file.
2. **Install the module**: Place the `.nvda-addon` file in the NVDA add-ons directory.
3. **Restart NVDA**: Restart NVDA to activate the module.

### Building the Module from Source

If you want to build the module from source, you can use **SCons**, a build tool recommended by NVDA developers. The repository includes the necessary files to generate the `.nvda-addon` file.

1. Clone this repository.
2. Install **SCons** if you haven't already.
3. Run the build command to generate the `.nvda-addon` file.

```bash
scons
