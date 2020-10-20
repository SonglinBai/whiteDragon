import json
def _saveData(path,data):
    f = open(path, 'w')

    f.write(json.dumps(data,
                       indent=4,
                       ensure_ascii=False))

    f.close()
    print("Data successfully saved!")