import base64
import math

import cv2
import numpy as np
import time

import copy
import cv2
import numpy as np
from PyQt5.QtGui import QImage, qRed, qGreen, qBlue, QPixmap


class Rect(object):
    def __init__(self):
        self.tl = (0, 0)
        self.br = (0, 0)

    def regularize(self):
        """
        make sure tl = TopLeft point, br = BottomRight point
        """
        pt1 = (min(self.tl[0], self.br[0]), min(self.tl[1], self.br[1]))
        pt2 = (max(self.tl[0], self.br[0]), max(self.tl[1], self.br[1]))
        self.tl = pt1
        self.br = pt2


class DrawRects(object):
    def __init__(self, image, color, thickness=1):
        self.original_image = image
        self.image_for_show = image.copy()
        self.color = color
        self.thickness = thickness
        self.rects = []
        self.current_rect = Rect()
        self.left_button_down = False

    @staticmethod
    def __clip(value, low, high):
        """
        clip value between low and high
        Parameters
        ----------
        value: a number
            value to be clipped
        low: a number
            low limit
        high: a number
            high limit
        Returns
        -------
        output: a number
            clipped value
        """
        output = max(value, low)
        output = min(output, high)
        return output

    def shrink_point(self, x, y):
        """
        shrink point (x, y) to inside image_for_show
        Parameters
        ----------
        x, y: int, int
            coordinate of a point
        Returns
        -------
        x_shrink, y_shrink: int, int
            shrinked coordinate
        """
        height, width = self.image_for_show.shape[0:2]
        x_shrink = self.__clip(x, 0, width)
        y_shrink = self.__clip(y, 0, height)
        return (x_shrink, y_shrink)

    def append(self):
        """
        add a rect to rects list
        """
        self.rects.append(copy.deepcopy(self.current_rect))

    def pop(self):
        """
        pop a rect from rects list
        """
        rect = Rect()
        if self.rects:
            rect = self.rects.pop()
        return rect

    def reset_image(self):
        """
        reset image_for_show using original image
        """
        self.image_for_show = self.original_image.copy()

    def draw(self):
        """
        draw rects on image_for_show
        """
        for rect in self.rects:
            cv2.rectangle(self.image_for_show, rect.tl, rect.br,
                          color=self.color, thickness=self.thickness)

    def draw_current_rect(self):
        """
        draw current rect on image_for_show
        """
        cv2.rectangle(self.image_for_show,
                      self.current_rect.tl, self.current_rect.br,
                      color=self.color, thickness=self.thickness)


class ImageUtils:
    def __init__(self):
        super(ImageUtils, self).__init__()

    def draw_rect(self, event, x, y, flags, draw_rects):
        if event == cv2.EVENT_LBUTTONDOWN:
            # pick first point of rect
            # print('pt1: x = %d, y = %d' % (x, y))
            draw_rects.left_button_down = True
            draw_rects.current_rect.tl = (x, y)
        if draw_rects.left_button_down and event == cv2.EVENT_MOUSEMOVE:
            # pick second point of rect and draw current rect
            draw_rects.current_rect.br = draw_rects.shrink_point(x, y)
            draw_rects.reset_image()
            draw_rects.draw()
            draw_rects.draw_current_rect()
        if event == cv2.EVENT_LBUTTONUP:
            # finish drawing current rect and append it to rects list
            draw_rects.left_button_down = False
            draw_rects.current_rect.br = draw_rects.shrink_point(x, y)
            # print('pt2: x = %d, y = %d' % (draw_rects.current_rect.br[0],
            #                                draw_rects.current_rect.br[1]))
            draw_rects.current_rect.regularize()
            draw_rects.append()
        if (not draw_rects.left_button_down) and event == cv2.EVENT_RBUTTONDOWN:
            # pop the last rect in rects list
            draw_rects.pop()
            draw_rects.reset_image()
            draw_rects.draw()

    def run_draw_rect(self, ori_img):
        WIN_NAME = "rect"
        draw_rects = DrawRects(ori_img, (0, 255, 0), 2)
        cv2.namedWindow(WIN_NAME, 0)
        win_h, win_w, _ = ori_img.shape
        cv2.resizeWindow(WIN_NAME, win_w, win_h)
        cv2.setMouseCallback(WIN_NAME, self.draw_rect, draw_rects)
        while True:
            cv2.imshow(WIN_NAME, draw_rects.image_for_show)
            key = cv2.waitKey(30)
            if key == 27:  # ESC
                draw_rects.rects.clear()
                break
            if key == 13:  # enter
                break
        cv2.destroyAllWindows()
        rects = []
        for rect in draw_rects.rects:
            x1, y1 = rect.tl
            x2, y2 = rect.br
            rects.append([x1, y1, x2, y2])
        return rects

    def crop_rect(self, ori_img, rects, scale_coef=4):
        crops = []
        for rect in rects:
            x1, y1, x2, y2 = rect
            cx, cy, w, h = (x1 + x2) / 2, (y1 + y2) / 2, x2 - x1, y2 - y1
            w = scale_coef * w
            h = scale_coef * h
            x1 = int(max(0, cx - w / 2))
            y1 = int(max(0, cy - h / 2))
            x2 = int(min(x1 + w, ori_img.shape[1]))
            y2 = int(min(y1 + h, ori_img.shape[0]))
            hole_img = ori_img[y1: y2 + 1, x1: x2 + 1, :]
            hole_img = cv2.cvtColor(hole_img, cv2.COLOR_BGR2RGB)
            crops.append(hole_img)
        return crops

    def rgb_img2base64_str(self, imgs):
        if not isinstance(imgs, list):
            imgs = [imgs]
        img_strs = []
        for img in imgs:
            img_ = cv2.imencode('.png', img)[1]
            img_str = str(base64.b64encode(img_))[2: -1]
            img_strs.append(img_str)
        return img_strs

    def base64_str2rgb_img(self, base64_strs):
        if not isinstance(base64_strs, list):
            base64_strs = [base64_strs]
        imgs = []
        # import pdb
        # pdb.set_trace()
        for base64_str in base64_strs:
            img_data = base64.b64decode(base64_str)
            img_array = np.frombuffer(img_data, np.uint8)
            img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)
            imgs.append(img)

        return imgs

    def base64_str2QImage(self, base64_strs):
        rgb_imgs = self.base64_str2rgb_img(base64_strs)
        q_imgs = self.rgb_img2QImage(rgb_imgs)
        return q_imgs

    def rgb_img2QImage(self, imgs):
        if not isinstance(imgs, list):
            imgs = [imgs]
        q_imgs = []
        for img in imgs:
            h, w, c = img.shape
            q_img = QImage(img.data, w, h, 3 * w, QImage.Format_RGB888)
            q_imgs.append(q_img)
        return q_imgs

    def QImage2bgr_img(self, qimg):
        bgr_img = np.zeros((qimg.height(), qimg.width(), 3), dtype=np.uint8)
        for row in range(0, qimg.height()):
            for col in range(0, qimg.width()):
                r = qRed(qimg.pixel(col, row))
                g = qGreen(qimg.pixel(col, row))
                b = qBlue(qimg.pixel(col, row))
                bgr_img[row, col, 0] = b
                bgr_img[row, col, 1] = g
                bgr_img[row, col, 2] = r

        return bgr_img

    def pixel_dist2real_dist(self, pixel_dist):
        """
        目标实际大小 = 像素大小 * 像元大小 * 作用距离(相机距离目标的距离) / 焦距
        Args:
            pixel_dist: 像素大小

        Returns:
            实际大小，单位微米
        """
        pixel_size = 1.12  # 像素点尺寸，单位 微米
        focal_length = 2.35  # 焦距f, 单位 毫米
        operate_dist = 45  # 作用距离，单位 毫米
        real_dist = pixel_dist * pixel_size * (operate_dist * 1000) / (focal_length * 1000)
        return round(real_dist, 2)

    def compute_area(self, h, w):
        return round(h * w * math.pi / 4, 2)

    def gen_hole_infos(self, ori_img, cur_count=0):
        rects = self.run_draw_rect(ori_img)
        if len(rects) == 0:
            return {}
        crops = self.crop_rect(ori_img, rects, scale_coef=4)
        crop_strs = self.rgb_img2base64_str(crops)
        hole_infos = {}
        for i in range(len(rects)):
            h = rects[i][3] - rects[i][1]
            w = rects[i][2] - rects[i][0]
            h_ = self.pixel_dist2real_dist(h)
            w_ = self.pixel_dist2real_dist(w)
            area = h_ * w_ * math.pi / 4
            crop_str = crop_strs[i]
            hole_info = {
                "hole_id": "孔洞%d" % (i + cur_count),
                "duration": 0,
                "height": h_,
                "width": w_,
                "height_pixel": h,
                "width_pixel": w,
                "area": area,
                "depth": 0,
                "img_str": crop_str,
                "from": 1,  # 1表示手动解析
            }
            hole_infos["hole%04d" % (i + cur_count)] = hole_info
        return hole_infos


if __name__ == '__main__':
    img = cv2.imread('../run_ui/login.jpg', 1)  # 读取图片作为背景
    img_ = ImageUtils()
    hole_infos = img_.gen_hole_infos(img, 1)
    # print(hole_infos)
    img_str = hole_infos["hole0001"]["img_str"]
    img_.base64_str2QImage(img_str)
