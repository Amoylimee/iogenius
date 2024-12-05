import os

def set_working_directory(working_directory: str) -> None:
    """
    Set working directory to the root of the project
    """
    os.chdir(working_directory) 
    
    return print(f'Working directory set to {working_directory}')