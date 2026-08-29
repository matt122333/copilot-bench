import os
def save_upload(dir, filename, data):
    with open(os.path.join(dir, filename), 'wb') as f:
        f.write(data)
