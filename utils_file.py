import os

def get_files_in_directory(directory, extensions):
    """
    Retrieves a list of files in a directory that match the given extensions.

    :param directory: Directory to search for files
    :param extensions: Tuple of file extensions to include (e.g., (".mp3", ".wav"))
    :return: List of file paths
    """
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(tuple(extensions))]
