from PIL import Image 
import pathlib
import pandas as pd

imageSuffixes = ['.tif','.tiff','.jpeg','.jpg','.png','.webp','.gif']

def give_image_rounded_corners(new_filepath, original_filepath, corner_mask_filepath, image_name: str):

    image_name = get_image_name_with_suffix(original_filepath, image_name)
    original_image_file_path = original_filepath + image_name

    try:
        image = Image.open(pathlib.Path(original_image_file_path)) 
        corner_mask = Image.open(pathlib.Path(corner_mask_filepath))

        image_width, image_height = image.size
        corner_mask = corner_mask.resize((image_width,image_height))

        image.paste(corner_mask, (0,0), mask=corner_mask)
        image.save(pathlib.Path(new_filepath + image_name))
    except:
        if not pathlib.Path(original_image_file_path).exists():
            print(f"File {original_image_file_path} does not exist.")
        print(f"Something went wrong with giving the {original_image_file_path} image rounded corners. Rounded corners skipped.")

def get_image_name_with_suffix(filepath: str, image_name: str) -> str:
    if "." in image_name :
            return image_name

    for suffix in imageSuffixes:
        if pathlib.Path(filepath + image_name + suffix).exists():
            return image_name + suffix

    return image_name


def make_images_transparent(filepath: str, image_name: str, alpha : int):

    image_name = get_image_name_with_suffix(filepath,image_name)
    try:
        back_image = Image.open(pathlib.Path(filepath + image_name)) 
        back_image = back_image.convert("RGBA")
        back_image.putalpha(alpha)  

        if image_name.split('.')[1] != 'png':
            image_name = image_name.split('.')[0] + ".png"
        back_image.save(pathlib.Path(filepath + image_name))
    except:
        print(f"Something went wrong with making the {filepath + image_name} image transparent. A blank page will be used instead of this image in the output pdf. Please check your database.csv and image names and try again.")


if __name__ == "main":
    df = pd.read_csv('example_database.csv')
    filepathBack = "images/back/"
    filepathFront = "images/front/"
    filepathOriginalImages = "images/originals/"
    rounded_corners_filepath = "images/originals/cornermask.png"

    for index, row in df.iterrows():
        give_image_rounded_corners(filepathBack, filepathOriginalImages, rounded_corners_filepath, row['imageBack'])
        give_image_rounded_corners(filepathFront, filepathOriginalImages, rounded_corners_filepath, row['imageFront'])
        make_images_transparent(filepathBack, row['imageBack'], 63) # quarter alpha (255 is no transparency)
