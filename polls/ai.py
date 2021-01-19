import cv2
import os
import torch
from torchvision import datasets, transforms
import shutil
from PIL import Image
import string
import random
import requests

class Ext:

    def delete(path):
        shutil.rmtree(path)

    def make(path,link, name):
        # Ext.delete()
        cam = cv2.VideoCapture(link)
        try:

            if not os.path.exists(path+"/frames"):
                os.makedirs(path+"/frames")

        except OSError:
            print('Error: Creating directory of data')

        currentframe = 0

        while (True):
            if currentframe == 152:
                break
            ret, frame = cam.read()

            if ret:
                name = os.path.join(path,"frames", 'frame' + str(currentframe) + '.jpg')
                # name = p+'frame' + str(currentframe) + '.jpg'
                # print('Creating...' + name)

                cv2.imwrite(name, frame)

                currentframe += 1
            else:
                break

        cam.release()
        cv2.destroyAllWindows()

        Ext.ck(path,name)
        #shutil.rmtree('cron/vid/' + res)

    def ck(path,name):
        p = os.path.join('polls', 'modal', 'MODEL.pth')
        model = torch.load(p)
        model.eval()
        test_transforms = transforms.Compose([transforms.Resize((512, 512), interpolation=Image.NEAREST),
                                              transforms.ToTensor()])
        data = datasets.ImageFolder(path, transform=test_transforms)
        loader = torch.utils.data.DataLoader(data, batch_size=1)
        sz = 1
        over = []
        for image, _ in loader:
            with torch.no_grad():
                logps = model(image)

            g = []
            for idx, i in enumerate(logps[0]):
                if i.item() > 0.7:
                    g.append(idx)
            over.extend(g)
            sz += 1

            if len(over) != 0 and sz == 150:
                print(list(set(over)))
                #return list(set(over))

        Ext.delete(path)

        man = 0
        female = 0
        cat = 0
        dog = 0
        for i in over:
            if i == 0:
                cat = 1
            elif i == 1:
                dog = 1
            elif i == 2:
                man = 1
            elif i == 3:
                female = 1

        string='cat='+str(cat)+'&dog='+str(dog)+'&man='+str(man)+'&female='+str(female)
        print(string)
        x = requests.get('https://w3schools.com/?q='+string)
        return 404


def randoms(n=7):
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=n))
    return res


def startt(url,name):
    import urllib.request
    import os

    directory = randoms(13)

    parent_dir = "video"

    path = os.path.join("polls",parent_dir, directory)
    os.mkdir(path)
    filepath=os.path.join(path,name)

    urllib.request.urlretrieve(url, filepath)

    key=name.split(".")

    key=key[0]

    Ext.make(path,filepath,key)


