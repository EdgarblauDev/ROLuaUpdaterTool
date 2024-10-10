from os import path, rename, remove
import configparser
import luadata
from loguru import logger
from pathlib import Path
from src.lupa_parser import parse_lua_file
from src.decompile_lub import decompile_lub
from src.lua_function import get_iteminfo_function


item_metadata = [
    'unidentifiedDisplayName',
    'unidentifiedResourceName',
    'identifiedDisplayName',
    'identifiedResourceName',
    'slotCount',
    'ClassNum',
    'costume'
]


def write_lua_function(filename, encoding):
    data = Path(filename)
    new_function = get_iteminfo_function()

    with data.open('a', encoding=encoding) as file:
        file.write(new_function)


def write_lua(data, filename, encoding, write_function=False):
    luadata.write(filename, data, encoding=encoding, indent="\t", prefix="tbl = ")
    if write_function is True:
        write_lua_function(filename, encoding)


def check_item_data(source, replacement):
    for key in item_metadata:
        if key in source and key in replacement and source[key] != replacement[key]:
            return True
    return False


def update_item_data(source, replacement):
    if check_item_data(source, replacement) is True:
        logger.info(f"The following item needs to be updated: {replacement['identifiedDisplayName']}")
        output = replacement.copy()
        for key in item_metadata:
            output[key] = source[key]
        return output
    return replacement


def replace_lua_data(original, replacement):
    total_replacements = 0
    new_replacement = replacement.copy()

    for index, content in replacement.items():
        logger.info(f"Replacing ItemID: {index}")
        new_item = update_item_data(original[index], content)
        original[index] = new_item
        new_replacement[index] = new_item
        total_replacements += 1

    logger.info(f"Total replaced items: {total_replacements}")
    return original, new_replacement


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

    original_data = parse_lua_file(iteminfo_file, file_encoding)

    replacement_data = parse_lua_file(replacement_file, file_encoding)

    updated_data, updated_replacement = replace_lua_data(original_data, replacement_data)

    backup(path.join(game_folder, 'System', compiled_lub_filename),
           path.join(game_folder, 'System', f"{compiled_lub_filename}.bkp"))

    write_lua(updated_data,
              path.join(game_folder, 'System', compiled_lub_filename),
              file_encoding,
              write_function=True)

    write_lua(updated_replacement,
              path.join(files_folder, replacement_lua_filename),
              file_encoding)

    clean(path.join(files_folder, decompiled_lua_filename))

    return 0


if __name__ == "__main__":
    args = configparser.ConfigParser()
    args.read(path.join('config.ini'))
    main(args)
