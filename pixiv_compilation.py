import os
import shutil


def compile_artist(root):

    folders = os.listdir(root)

    comp = os.path.join(root, 'compilation')

    os.makedirs(comp, exist_ok=True)

    whitelist = ['metadata.txt', 'compilation']

    for folder in folders:
        if folder not in whitelist:
            src = os.path.join(root, folder)
            f = os.listdir(src)
            for file in f:
                if file not in whitelist:
                    shutil.copyfile(os.path.join(src, file),
                                    os.path.join(comp, file))
