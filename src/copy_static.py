import os
import shutil


def copy_origin_to_destination(origin: str, destination: str) -> None:
    # If public exists, wipe it.
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    os.mkdir(destination)
    
    _copy_loop(origin, destination)

    
def _copy_loop(origin: str, destination: str) -> None:
    # Create file paths.
    for filename in os.listdir(origin):
        filepath = (os.path.join(origin, filename))
        destination_path = os.path.join(destination, filename)

        if os.path.isfile(filepath):
            print(f"Copying {filepath} to {destination_path}")
            shutil.copy(filepath, destination_path)
            continue
        
        os.mkdir(destination_path)
        _copy_loop(filepath, destination_path)

