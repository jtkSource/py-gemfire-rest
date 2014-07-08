import requests
import jsonpickle


class Region:

    # Initializes a Region Object
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url + name

    # Returns all the data in a Region
    def get_all(self):
        url = self.base_url + "?ALL"
        data = requests.get(url) 
        fdata = jsonpickle.decode(data.text)
        return fdata[self.name]

    # Creates a new data value in the Region if the key is absent
    def create(self, key, value):
        url = self.base_url + "?key=" + str(key)
        headers = {'content-type': 'application/json'}
        jvalue = jsonpickle.encode(value)
        data = requests.post(url, data=jvalue, headers=headers)
        if data.status_code == 201:
            return True
        else:
            return False

    # Updates or inserts data for a specified key
    def put(self, key, value):
        url = self.base_url + "/" + str(key)
        headers = {'content-type': 'application/json'}
        jvalue = jsonpickle.encode(value)
        data = requests.put(url, data=jvalue, headers=headers)
        if data.status_code == 200:
            return True
        else:
            return False

    # Returns all keys in the Region
    def keys(self):
        url = self.base_url + "/keys"
        data = requests.get(url)
        fdata = jsonpickle.decode(data.text)
        return fdata["keys"]

    # Returns the data value for a specified key
    def get(self, *arg):
        sub_url = ','.join(str(key) for key in arg)
        url = self.base_url + "/" + sub_url + "?ignoreMissingKey=true"
        data = requests.get(url)
        return jsonpickle.decode(data.text)

    # Method to support region[key] notion
    def __getitem__(self, key):
        url = self.base_url + "/" + str(key) + "?ignoreMissingKey=true"
        data = requests.get(url)
        return jsonpickle.decode(data.text)

    # Insert or updates data for a multiple keys specified by a hashtable
    def put_all(self, item):
        sub_url = ','.join(str(keys) for keys in item)
        url = self.base_url + "/" + sub_url
        headers = {'content-type': 'application/json'}
        jvalue = jsonpickle.encode(dict.items(item))
        data = requests.put(url, data=jvalue, headers=headers)
        if data.status_code == 200:
            return True
        else:
            return False

    # Updates the data in a region only if the specified key is present
    def update(self, key, value):
        url = self.base_url + "/" + str(key) + "?op=REPLACE"
        headers = {'content-type': 'application/json'}
        jvalue = jsonpickle.encode(value)
        data = requests.put(url, data=jvalue, headers=headers)
        if data.status_code == 200:
            return True
        else:
            return False

    # Compares old values and if identical replaces with a new value
    def compare_and_set(self, key, value):
        url = self.base_url + "/" + str(key) + "?op=CAS"
        headers = {'content-type': 'application/json'}
        jvalue = jsonpickle.encode(value)
        data = requests.put(url, data=jvalue, headers=headers)
        if data.status_code == 200:
            return True
        else:
            return False

    # Deletes the corresponding data value for the specified key
    def delete(self, *arg):
        sub_url = ','.join(str(key) for key in arg)
        url = self.base_url + "/" + sub_url
        data = requests.delete(url)
        if data.status_code == 200:
            return True
        else:
            return False

    # Deletes all data in the Region
    def clear(self):
        data = requests.delete(self.base_url)
        if data.status_code == 200:
            return True
        else:
            return False
