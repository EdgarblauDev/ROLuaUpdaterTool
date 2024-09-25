from os import path, rename, remove
import configparser
import luadata
from loguru import logger
from pathlib import Path
from src.parser import slpp
from src.decompile_lub import decompile_lub
from src.lua_function import get_iteminfo_function


def parse_lua(filename, encoding):
    data = slpp.decode(Path(filename).read_text(encoding=encoding))
    if 'tbl' in data:
        return data['tbl']
    return None


def write_lua_function(filename, encoding):
    data = Path(filename)
    new_function = get_iteminfo_function()

    with data.open('a', encoding=encoding) as file:
        file.write(new_function)


def write_lua(data, filename, encoding):
    luadata.write(filename, data, encoding=encoding, indent="\t", prefix="tbl = ")
    write_lua_function(filename, encoding)


def replace_lua_data(original, replacement):
    total_replacements = 0

    for index, content in replacement.items():
        logger.info(f"Replacing ItemID: {index}")
        original[index] = content
        total_replacements += 1

    logger.info(f"Total replaced items: {total_replacements}")
    return original


def backup(file: str, new_file: str):
    if path.exists(file) and path.exists(new_file):
        logger.info(f"Deleting old backup file {new_file}")
        clean(new_file)
        logger.info(f"Creating a backup file of {file} into {new_file}")
        rename(file, new_file)

    if path.exists(file) and not path.exists(new_file):
        logger.info(f"Creating a backup file of {file} into {new_file}")
        rename(file, new_file)


def clean(file: str):
    if path.exists(file):
        logger.info(f"Deleting file {file}")
        remove(file)


def main(args):

    try:
        file_encoding = str(args['DEFAULT']['LuaEncoding'])
        files_folder = str(args['DEFAULT']['FilesFolder'])
        replacement_lua_filename = str(args['DEFAULT']['ReplacementLuaFile'])
        decompiled_lua_filename = str(args['DEFAULT']['DecompiledLuaFile'])

        game_folder = path.normpath(str(args['GAMEFILES']['GameFolder']))
        compiled_lub_filename = str(args['GAMEFILES']['IteminfoLubFile'])

    except Exception as e:
        logger.error(e)
        return -2

    decomp = decompile_lub(path.join(game_folder, 'System', compiled_lub_filename),
                           path.join(files_folder, decompiled_lua_filename))

    if decomp is None:
        logger.error(f"File {compiled_lub_filename} cannot be decompiled back to LUA.")
        clean(path.join(files_folder, decompiled_lua_filename))
        return -1

    iteminfo_file = path.join(files_folder, decompiled_lua_filename)
    replacement_file = path.join(files_folder, replacement_lua_filename)

    original_data = parse_lua(iteminfo_file, file_encoding)
    replacement_data = parse_lua(replacement_file, file_encoding)

    updated_data = replace_lua_data(original_data, replacement_data)

    backup(path.join(game_folder, 'System', compiled_lub_filename),
           path.join(game_folder, 'System', f"{compiled_lub_filename}.bkp"))

    write_lua(updated_data,
              path.join(game_folder, 'System', compiled_lub_filename),
              file_encoding)

    clean(path.join(files_folder, decompiled_lua_filename))

    return 0


if __name__ == "__main__":
    args = configparser.ConfigParser()
    args.read(path.join('config.ini'))
    main(args)
