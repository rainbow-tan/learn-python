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
    img_2 = img.convert("L")

    # 自定义灰度界限，大于这个值为黑色，小于这个值为白色
    threshold = 150

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)

    img_3 = img_2.point(table, "1")  # 图片二值化 使用table来设置二值化的规则
    img_3.save(f"img/img_L_1_{threshold}.png")
    ret = get_all_pixel(img_3)
    with open(f'mode/img_L_1_{threshold}.txt', 'w') as f:
        json.dump(ret, f)


if __name__ == '__main__':
    main()
