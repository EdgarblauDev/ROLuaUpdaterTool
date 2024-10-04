from lupa import LuaRuntime


def lua_list_to_python(lua_list):
    # Create an empty Python list
    python_list = []
    # Iterate over the Lua list using Lua's numeric keys
    i = 1
    while lua_list[i] is not None:
        python_list.append(lua_list[i])
        i += 1
    return python_list


def parse_lua_file(filename, encoding):

    # read file
    with open(filename, 'r', encoding=encoding) as file:
        lua_code = file.read()

    # Initialize LuaRuntime
    lua = LuaRuntime(unpack_returned_tuples=True)

    # Execute Lua code
    lua.execute(lua_code)
    tbl = lua.globals().tbl

    output = {}
    for key, value in tbl.items():
        output[key] = {
            'unidentifiedDisplayName': value['unidentifiedDisplayName'],
            'unidentifiedResourceName': value['unidentifiedResourceName'],
            'unidentifiedDescriptionName': lua_list_to_python(value['unidentifiedDescriptionName']),
            'identifiedDisplayName': value['identifiedDisplayName'],
            'identifiedResourceName': value['identifiedResourceName'],
            'identifiedDescriptionName': lua_list_to_python(value['identifiedDescriptionName']),
            'slotCount': value['slotCount'],
            'ClassNum': value['ClassNum'],
            'costume': value['costume'],
        }
    return output
