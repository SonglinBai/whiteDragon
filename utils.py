import json
def _saveData(data, path):
    f = open(path, 'w')

    f.write(json.dumps(data,
                       indent=4,
                       sort_keys=True,
                       ensure_ascii=False))

    f.close()
    print("Data successfully saved!")