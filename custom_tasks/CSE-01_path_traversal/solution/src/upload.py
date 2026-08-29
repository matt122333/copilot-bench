import os
def save_upload(dir, filename, data):
    base = os.path.realpath(dir)
    dest = os.path.realpath(os.path.join(base, filename))
    if os.path.commonpath([base, dest]) != base:
        raise ValueError('unsafe filename')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as f:
        f.write(data)
