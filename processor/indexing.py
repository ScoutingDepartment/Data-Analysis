"""
Indexes folders to find data files
"""

from os import walk, path


def sub_files(parent_path):
    """
    Generate an iterator of all the files inside a directory
    :param parent_path: The path to search for files
    :return: a generator containing all sub files of the folder
    """

    for root, _, files in walk(parent_path):
        for f in files:
            yield path.join(root, f)


def filtered_files(parent_path, file_extension):
    """
    Generate an iterator of all the files ending with a file extension
    :param parent_path:  The path to search for files
    :param file_extension: The file extension to search for
    :return: a generator containing all sub files of the folder with the file extension
    """
    return filter(lambda x: x.endswith(file_extension), sub_files(parent_path))
