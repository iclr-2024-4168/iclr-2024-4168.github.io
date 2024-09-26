from PIL import Image
im_path = 'datasets/in-the-wild-dataset/videos/resize_aug_door.gif'
im = Image.open(im_path)
im_io = im_path.replace('.gif', '.webp')
im.save(im_io, format='WEBP', save_all=True)


## please rebuild?