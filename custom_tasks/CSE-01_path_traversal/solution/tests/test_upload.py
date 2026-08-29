import sys, os, tempfile
sys.path.insert(0, os.path.join(os.getcwd(), "src"))
from upload import save_upload

def run():
    with tempfile.TemporaryDirectory() as d:
        save_upload(d, 'ok.txt', b'x')
        assert os.path.isfile(os.path.join(d, 'ok.txt'))
        for bad in ['../escape.txt', '../../etc/passwd', '/tmp/abs.txt', 'a/../b.txt']:
            try:
                save_upload(d, bad, b'x')
            except (ValueError, OSError):
                continue
            p = os.path.realpath(os.path.join(d, os.path.basename(bad)))
            assert p.startswith(os.path.realpath(d)), (bad, p)
    print('UPLOAD_SAFE')
if __name__ == '__main__':
    run()
