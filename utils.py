import json
def _saveData(path,data):
    f = open(path, 'w')

    f.write(json.dumps(data,
                       indent=4,
                       ensure_ascii=False))

    f.close()
    print("Data successfully saved!")

def _loadData(filePath):
    """
    load data from a .json file.

    :param filePath: Path of the .json file.
    :type  filePath: Str.

    """
    with open(filePath) as json_file:
        j_data = json.load(json_file)

    json_file.close()

    print("Data successfully loaded !")
    return j_data
