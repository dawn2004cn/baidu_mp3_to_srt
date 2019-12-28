#!python3
import sys
import os
import cv2
from PIL import Image

class PicConvert:
    def __init__(self,in_file,out_file="pic.jpg"):
        self.in_file=in_file
        self.out_file=out_file

    def piltranform(self):
        # in_file是输入文件名
        # out_file是输出文件名。
        im = Image.open(self.in_file, "r")
        print(im.size, im.format, im.mode)
        #逆时针旋转90度
        im_rotate_90 = im.transpose(Image.ROTATE_90)
        #图片左右翻转
        im_rotate_180 = im_rotate_90.transpose(Image.FLIP_LEFT_RIGHT)
        im_rotate_180.save(self.out_file)
        print("处理完毕!")

    def opencvtranform(self):
        # in_file是输入文件名
        # out_file是输出文件名。
        src = cv2.imread(self.in_file)
        src = cv2.transpose(src)  # 逆时针旋转90度
        flip_img = cv2.flip(src, -1)  # 水平垂直翻转
        cv2.imwrite(self.out_file, flip_img)
        print("处理完毕!")


if __name__ == '__main__':
    pic_dir = ''
    out_dir = ''
    if len(sys.argv) > 1:
        pic_dir = sys.argv[1]
    if len(sys.argv) > 2:
        out_dir = sys.argv[2]
    if(pic_dir==''):
        pic_dir = ".\\picture\\input_pic\\"
    if (out_dir == ''):
         out_dir = ".\\picture\\output_pic\\"
    all_pic_file = []
    all_file = os.listdir(pic_dir)
    for filename in all_file:
        if ".jpg" in filename:
            all_pic_file.append(filename)
    all_pic_file.sort()
    i = 0
    txt_file_num = len(all_pic_file)
    print(f"当前共有{txt_file_num}个文本文件需要转换，即将进行处理请稍等...")
    # 此层for循环是逐个文本文件进行处理
    for pic_file_name in all_pic_file:
        input_file_jpg_path = f"{pic_dir}{pic_file_name}"
        convert_file_jpg_path = f"{out_dir}{pic_file_name}"
        print(input_file_jpg_path)
        print(convert_file_jpg_path)
        pc = PicConvert(input_file_jpg_path, convert_file_jpg_path)
        pc.piltranform()
        #pc.opencvtranform()
