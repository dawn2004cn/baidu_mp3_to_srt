import os
from aip import AipSpeech

class Ai:
    APP_ID = '11766958'
    API_KEY = 'USWmlsBc2zxv9rcNN2gNPb9H'
    SECRET_KEY = 'GxF8tOEO2MbkM6qPtHbF9wZhYPQc6zt7'
    def __init__(self,msg_file,out_file="audio.mp3"):
        self.msg_file=msg_file
        self.out_file=out_file

    def text2audio(self):
        # 把txt文件转成音频文件
        # msg_file是txt文件名
        # out_file是音频文件名。
        with open(self.msg_file,"r") as file:
            text = file.read()
        client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)
        for i in range(int(len(text)/500)+1):
            result = client.synthesis(text[i:i+500], 'zh', 1, {
                "spd":5,
                'vol':5,
                "per":4,
        })
            if not isinstance(result, dict):
                with open(self.out_file, 'ab') as f:
                    f.write(result)
        print("处理完毕!")



if __name__ == '__main__':
    txt_dir = ".\\txt\\"
    all_txt_file =[]
    all_file = os.listdir(txt_dir)
    for filename in all_file:
        if ".txt" in filename:
            all_txt_file.append(filename)
    all_txt_file.sort()
    i = 0
    txt_file_num = len(all_txt_file)
    print(f"当前共有{txt_file_num}个文本文件需要转换，即将进行处理请稍等...")
    # 此层for循环是逐个文本文件进行处理
    for txt_file_name in all_txt_file:
        txt_file = os.path.join(txt_dir, txt_file_name)
        txt_file_mp3_path = f".\\txt\\{txt_file_name[:-4]}.mp3"
        ai=Ai(txt_file,txt_file_mp3_path)
        ai.text2audio()
