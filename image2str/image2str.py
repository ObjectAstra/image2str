import cv2,os
from urllib import request
import numpy as np

def isAllNone(lst):
    for i in lst:
        if i is not None:
            return False
    return True

# 等比例缩放
def proportionalScalingImage(width:int, imageMat:cv2.Mat):
    base = (width / float(imageMat.shape[1]))
    height = int(imageMat.shape[0] * base)
    return (width, height)

class url:
    def __init__(self, string):
        self.str = string

# 图片转字符
def image2String(imageSrc, newSize=None):
    
    if type(imageSrc) == url:
        imageSrc = imageSrc.str
        resp = request.urlopen(imageSrc)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    else:
        imageSrc = os.path.abspath(imageSrc)
        if not os.path.exists(imageSrc):
            raise FileNotFoundError(f"File '{imageSrc}' not found")
        image = cv2.imread(imageSrc) # 读取图片
    

    tmpWidth = os.get_terminal_size().columns
    if newSize is None:
        newSize = proportionalScalingImage(tmpWidth, image)
        tmpWidth -= 1

        while newSize[1] > os.get_terminal_size().lines*2:
            newSize = proportionalScalingImage(int(tmpWidth), image)
            tmpWidth -= 1

    image = cv2.resize(src=image, dsize=newSize)
    # pp(image)
    return Mat2String(image, newSize)

# cv2.Mat转字符
def Mat2String(cv2Mat:cv2.Mat, size=None):
    image = cv2Mat
    tmpWidth = os.get_terminal_size().columns
    if size is None:
        size = proportionalScalingImage(tmpWidth, image)
        tmpWidth -= 1

        while size[1] > os.get_terminal_size().lines*2:
            size = proportionalScalingImage(int(tmpWidth), image)
            tmpWidth -= 1
    image = cv2.resize(image, size)

    pairs:list[list[list[list[int|None]]]] = [] # 分层配对
    # isNeedAlpha = len(image[0][0]) == 4
    isNeedAlpha = image.shape[2] == 4

    # 分层添加rgb(a)
    for lines in range(0,len(image),2):
        pairs.append([])
        for pixels in range(len(image[lines])):

            up = list(image[lines][pixels])
            if lines+1 < size[1]:
                down = list(image[lines+1][pixels])
            else:
                if isNeedAlpha:
                    down = [None,None,None,0]
                else:
                    down = [None,None,None]
            
            if isNeedAlpha:
                if up[3] < 128:
                    up = [None,None,None]
                if down[3] < 128:
                    down = [None,None,None]
            
            pairs[lines//2].append([[up[2],up[1],up[0]],[down[2],down[1],down[0]]])

    # 组合
    result = ""
    for line in pairs:
        for up,down in line:
            if isAllNone(up+down):
                result += '\033[0m '
            elif isAllNone(up):
                result += "\033[0m\033[48;2;{};{};{}m▀".format(down[0],down[1],down[2])
            elif isAllNone(down):
                result += "\033[0m\033[38;2;{};{};{}m▀".format(up[0],up[1],up[2])
            else:
                result += "\033[0m\033[38;2;{};{};{};48;2;{};{};{}m▀".format(up[0],up[1],up[2],down[0],down[1],down[2])
        result += '\033[0m\n'
    return result

if __name__ == "__main__":
    desktop = "C:\\Users\\USER\\Desktop\\"
    img = url("https://i0.hdslb.com/bfs/article/03245d65e35b7573b6988c26a2a037903ef92896.png")
    print(Mat2String(image2String))