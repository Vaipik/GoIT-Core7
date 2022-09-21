from pathlib import Path
import sys
import shutil
from typing import Union

from normalization import normalize


def create_folders(base_path: Path) -> None:
    """
    Is used to create desired folders according to categories

    :param base_path: path to be sorted
    :return: None
    """
    for folder_name in files_extensions.values():
        folder_path = base_path.joinpath(folder_name)
        folder_path.mkdir(exist_ok=True)


def delete_folders(base_path: Path) -> None:
    """
    Is used to delete empty folders after sorting

    :param base_path: path to be sorted
    :return: None
    """
    for folder in base_path.iterdir():
        if folder.name not in files_extensions.values():
            shutil.rmtree(folder)


def get_extensions(extension: str) -> Union[tuple, str]:
    """
    Is used to get tuple keys using one extension

    :param extension: is file extensions
    """
    for key in files_extensions:
        if extension.upper() in key:
            return key


def parse_folder(path: Path, base_path: Path = None) -> None:
    """
    Is used to recursive parsing

    :param path: is current directory path
    :param base_path: given path entered by user
    :return: None
    """
    if base_path is None:
        base_path = path

    if path.is_dir():

        for elem in path.iterdir():

            if elem.is_file():
                file_name = normalize(elem.stem)  # Cyrillic -> latin
                folder_name = files_extensions.get(get_extensions(elem.suffix[1:]), 'unknown')
                folder_to = base_path.joinpath(folder_name)

                if folder_name == 'archives':
                    shutil.unpack_archive(elem, folder_to.joinpath(file_name))
                    elem.unlink()

                else:
                    file_name += elem.suffix
                    elem.replace(folder_to.joinpath(file_name))

            else:
                parse_folder(elem, base_path)


def main():

    if len(sys.argv) < 2:
        
        print("No path was given")
        user_path = ""
        
    else:
        user_path = sys.argv[1]

    path = Path(user_path)
    if path.exists():
        if not path.is_file():
            create_folders(path)

        parse_folder(path)
    else:
        print(f"{path.absolute()} does not exist")

    delete_folders(path)


if __name__ == "__main__":

    files_extensions = {
        ("JPEG", "PNG", "JPG", "SVG"): "images",
        ("AVI", "MP4", "MOV", "MKV"): "videos",
        ("DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"): "documents",
        ("MP3", "OGG", "WAV", "AMR"): "audio",
        ("ZIP", "GZ", "TAR"): "archives",
        "": 'unknown'
    }

    main()
 