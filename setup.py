from cx_Freeze import setup, Executable 

#build_exe_options = {"includes": ['numpy', 'pandas', 'matplotlib'], "packages": [], 'excludes' : [], "include_files": []}

setup(name = "ITM", version = "0.1", description = "", author  = "Yash", executables = [Executable("ui.py")])#, options = {"build_exe": build_exe_options})
