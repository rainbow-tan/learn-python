import json

from PIL import Image


def get_all_pixel(img):
    width = img.size[0]
    height = img.size[1]
    ret = []
    for x in range(width):
        for y in range(height):
            pixel = img.getpixel((x, y))
            # print(f"{x},{y} -----> {pixel}")
            ret.append(pixel)
    return ret


def main():
    img = Image.open('img/img.png')
    mode = img.mode
    print(f"img_ mode:{mode}")  # RGB
    ret = get_all_pixel(img)  # RGB模式, 像素点是三元组 (136, 161, 193)
    with open('mode/mode_rgb.txt', 'w') as f:
        json.dump(ret, f)

    img_1 = img.convert("1")
    mode = img_1.mode
    print(f"img_1 mode:{mode}")  # 1
    ret_1 = get_all_pixel(img_1)  # 1模式, 像素点0或者255
    with open('mode/model_1.txt', 'w') as f:
        json.dump(ret_1, f)
    img_1.save('img/img_1.png')

    img_2 = img.convert("L")
    mode = img_2.mode
    print(f"img_2 mode:{mode}")  # L
    ret_2 = get_all_pixel(img_2)  # L模式, 像素点0到255
    with open('mode/model_l.txt', 'w') as f:
        json.dump(ret_2, f)
    img_2.save('img/img_L.png')


if __name__ == '__main__':
    main()
