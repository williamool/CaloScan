import os
from PIL import Image
from PIL import UnidentifiedImageError

image_path_1 = os.path.join(os.getcwd(), 'dataset', 'train')
image_path_2 = os.path.join(os.getcwd(), 'dataset', 'val')
def delete_Error_Image(image_path):
    Error = 0
    All = 0
    print(os.path.exists(image_path))
    for root, dirs, files in os.walk(image_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    pass
            except (IOError, SyntaxError, UnidentifiedImageError) as e:
                Error = Error + 1
                print("Error {} happens".format(Error))
                os.remove(file_path)
                print("deleted.")

    print(All)

delete_Error_Image(image_path_1)
delete_Error_Image(image_path_2)