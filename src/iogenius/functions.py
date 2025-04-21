import os
import glob
import gc
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from rich.progress import Progress

def set_working_directory(working_directory: str) -> None:
    """
    Set working directory to the root of the project
    """
    os.chdir(working_directory) 
    
    return print(f'Working directory set to {working_directory}')


def create_new_directory(directory_path: str) -> None:
    """Create a new folder/directory if the folder/directory does not exist.

    io_create_new_folder(/disk/r046/jchenhl/Project_RBF/)
    """
    if os.path.isdir(directory_path):
        pass
    else:
        os.makedirs(directory_path)
    return


def read_file(file, format = 'feather'):

    if format == 'feather':
        return pd.read_feather(file)  # 使用 feather 格式读取
    elif format == 'parquet':
        return pd.read_parquet(file)
    elif format == 'csv':
        return pd.read_csv(file)


def concat_files_in_folder(directory_in: str, format = 'feather', max_workers=24) -> pd.DataFrame:
    files_in = glob.glob(f"{directory_in}/**/*.{format}", recursive=True)
    dataframes = []
    
    with Progress() as progress:
        task = progress.add_task(f"Concatenating files in {directory_in}...", total=len(files_in))
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(read_file, file, format): file for file in files_in}
            
            for future in as_completed(futures):
                try:
                    data = future.result()
                    dataframes.append(data)
                except Exception as e:
                    print(f"Error reading file {futures[future]}: {e}")
                progress.advance(task)
    
    df = pd.concat(dataframes, axis=0)
    df = df.reset_index(drop=True)
    gc.collect()
    return df