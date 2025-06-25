import argparse
import os
from PIL import Image, ExifTags

def get_img(path_to_img):
    img = Image.open(path_to_img)
    return img

def save_img(img, path_to_img):
    img.save(path_to_img)
    return 1

def orientation_img(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break  
        exif = img._getexif()

        # print(f'exif: {exif}')
        if exif and exif[orientation]:
            # print(f'orientation: {exif[orientation]}')

            if exif[orientation] == 3:
                result_img=img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                result_img=img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                result_img=img.rotate(90, expand=True)
            else:
                result_img=img
        else:
            result_img=img

    except (AttributeError, KeyError, IndexError):
        # cases: image don't have getexif
        return img

    return result_img

def check_img(img):
    print(f'width: {img.size[0]}, height: {img.size[1]}, ratio: {round(img.size[1] / img.size[0], 2)}')
    return

def resize_img(img, new_width, new_height, smart_resize=1, max_size=1000):
    if smart_resize == 1:
        wh_ratio = img.size[1] / img.size[0]
        ratio_width =  img.size[1] / max_size

        if ratio_width > 1:
            ratio_width = max_size
        else:
            ratio_width = new_width

        ratio_height = int(round(ratio_width * wh_ratio, 0))

        if ratio_height > max_size:
            ratio_height = max_size
            ratio_width = int(round(ratio_height / wh_ratio, 0))

        # print(f'ow: {img.size[0]}, oh: {img.size[1]}, wh_ratio: {wh_ratio}')
        # print(f'nw: {new_width}, nh: {new_height}, wh_ratio: {wh_ratio}, rh = nw * wh_ratio: {ratio_height} ')
    else:
        ratio_width = new_width
        ratio_height = new_height

    if img.size[1] > ratio_width or img.size[0] > ratio_height:
        img = img.resize((ratio_width, ratio_height))

    return img

def watermark_img(img, wm):
    w_img = img.size[0]
    h_img = img.size[1]
    w_wm = wm.size[0]
    h_wm = wm.size[1]
    r_wh_wm = h_wm / w_wm

    # print(f'w_img: {w_img}, h_img: {h_img}, w_wm: {w_wm}, h_wm: {h_wm}, r_wh_wm: {r_wh_wm}')


    if w_img > h_img: # горизонтальное изображение

        wm = wm.resize((int(w_img * 0.33), int(w_img * 0.33 * r_wh_wm)))
    else: # вертикальное изображение
        wm = wm.resize((int(w_img * 0.5), int(w_img * 0.5 * r_wh_wm)))

    w_wm = wm.size[0]
    h_wm = wm.size[1]

    # print(f'w_img: {w_img}, h_img: {h_img}, w_wm: {w_wm}, h_wm: {h_wm}, r_wh_wm: {r_wh_wm}')

    img.paste(wm, (w_img - w_wm, h_img - h_wm), wm)
    return img


def make_img(input_file, wm_file, output_file):
    img = get_img(input_file)
    wm = get_img(wm_file)
    # check_img(img)
    # print (img.getexif())
    img = orientation_img(img)
    img = resize_img(img, 1000, 750, 1)
    # img.paste(wm, (0, 0), wm)
    img = watermark_img(img, wm)
    # check_img(img)
    save_img(img, output_file)

    return 'Ok'

def load_file_list(file_list):
    with open(file_list, 'r') as f:
        file_list = f.readlines()
    return file_list

def main():
    """
    Основная функция для разбора параметров командной строки.
    """
    parser = argparse.ArgumentParser(description="Пример скрипта с параметрами.")
    
    # Добавление параметров
    parser.add_argument('--input', type=str, help='Входной файл', required=True)
    parser.add_argument('--watermark', type=str, help='Водяной знак', required=True)
    parser.add_argument('--output', type=str, help='Выходной файл')
    parser.add_argument('--path', type=str, help='Рабочий каталог')
    parser.add_argument('--verbose', action='store_true', help='Включить подробный вывод')
    
    # Разбор параметров
    args = parser.parse_args()

    # print(args)

    if args.watermark is None:
        wm_file = 'wm.png'
    else:
        wm_file = args.watermark

    if args.path is None:
        work_dir = os.path.dirname(os.path.realpath(__file__))
    else:
        work_dir = args.path

    print(work_dir)

    out_file = args.output

    if args.verbose:
        print("Входной файл:", args.input)
        print("Водяной знак:", wm_file)
        print("Выходной файл:", out_file)
        print("Рабочий каталог:", work_dir)

    if '.tmp' in args.input or '.txt' in args.input or '.lst' in args.input: # Far Manger menu call?
        file_list = load_file_list(args.input)
        
        for file in file_list:
            in_file = work_dir + file.replace('\n', '').replace('\r', '')
            out_file = in_file.replace('.JPG', '.jpg').replace('.jpg', '_watermarked.jpg')
            print(f"\nProcessing file: {in_file}")
            result = make_img(in_file, wm_file, out_file)
            # print(f"Result for {in_file}: {result}")
            print(result)

    else:
        if args.output is None:
            out_file = args.input.replace('.JPG', '.jpg').replace('.jpg', '_watermarked.jpg')
        else:
            out_file = args.output
        result = make_img(args.input, wm_file, out_file)
        print("Result:", result)

    print('\nDone')
if __name__ == "__main__":
    main()
