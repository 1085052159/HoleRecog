"""
hole_id = 1
res = {}
# 记录孔洞信息
for idx, frame in enumerate(frames):
    h, w, _ = frame.shape
    preds = get_preds()
    if len(preds) == 0:
        pass
    else:
        new_holes = {}
        for pred in preds:
            for key in res.keys():
                dist = res[key]["bbox"] - pred
                # 两帧检测框小于阈值且当前帧序号-结束帧序号小于阈值
                if dist <= thresh:
                    # 原来的孔洞，更新持续时间和bbox
                    res[key]["end"] = idx
                    res[key]["bbox"] = pred
                    new_hole["width_sum"] += pred[3] * w
                    new_hole["height_sum"] += pred[4] * h
                    new_hole["count"] += 1
                else:
                    # 出现新的孔洞，创建
                    new_hole = {}
                    new_hole["start"] = idx
                    new_hole["end"] = idx
                    new_hole["bbox"] = pred
                    new_hole["width_sum"] = pred[3] * w
                    new_hole["height_sum"] = pred[4] * h
                    new_hole["count"] = 1
                    new_holes["hole%d" % hole_id] = new_hole
                    hole_id += 1
        res.update(new_holes)

# 过滤孔洞信息
new_res = {}
hole_count = 0
for key in list(res.keys()):
    duration = res[key]["end"] - res[key]["start"] + 1
    if duration > 10:
        # 孔洞持续时间少于10帧，视为误检引起的，直接删除
        hole_count += 1
        new_key = "hole%d" % hole_count
        new_res[new_key] = {}
        new_res[new_key]["duration"] = duration / FPS
        # pixel dist
        new_res[new_key]["width"] = res[key]["width_sum"] / res[key]["count"]
        new_res[new_key]["height"] = res[key]["height_sum"] / res[key]["count"]
        new_res[new_key]["image"] = res[key]["image"]

"""
import json
import os
from pathlib import Path
import time
import cv2
from tqdm import tqdm
from recog_alg.detect_infer import init_model_detector, run_detector, vis_det_results
from utils_tools.JSONTools import Config
from utils_tools.img_util import ImageUtils


def vid2frames(vid_path):
    reader = cv2.VideoCapture(vid_path)
    fps = reader.get(cv2.CAP_PROP_FPS)
    print("[hole_recog_pipeline.vid2frames]FPS: ", fps)
    frames = []
    while True:
        ret, frame = reader.read()
        if not ret:
            print("[hole_recog_pipeline.vid2frames]vid_path: %s; frames: %s" % (vid_path, len(frames)))
            break
        frames.append(frame)
    reader.release()

    return frames, fps


def norm_cxy2xxyy(norm_cbbox, scale_coef=1.1):
    cx, cy, w, h = norm_cbbox
    w *= scale_coef
    h *= scale_coef
    x1 = max(0, cx - w / 2)
    y1 = max(0, cy - h / 2)
    x2 = min(1, x1 + w)
    y2 = min(1, y1 + h)
    return [x1, y1, x2, y2]


def norm2image_level(norm_bbox, height, width):
    bbox = [norm_bbox[0] * width, norm_bbox[1] * height, norm_bbox[2] * width, norm_bbox[3] * height]
    return [int(x) for x in bbox]


def write_json(json_name, json_content):
    json_name = json_name.replace("\\", "/")
    json_root_path = "/".join(json_name.split("/")[: -1])
    os.makedirs(json_root_path, exist_ok=True)
    json_str = json.dumps(json_content, indent=4, ensure_ascii=False)
    with open(json_name, "w", encoding="utf-8") as f:
        f.write(json_str)


def gen_video_dets(model_det, frames, batch_size=4, device="cuda", save_path="./", show_temp=False):
    video_dets = {}
    source, idxs = [], []
    frame_h, frame_w, _ = frames[0].shape
    for idx, frame in tqdm(enumerate(frames)):
        if idx == 0 or idx % batch_size != 0:
            source.append(frame)
            idxs.append(idx)
            if not idx == len(frames) - 1:
                continue
        hole_preds = run_detector(model_det,  # model.pt path(s)
                                  source=source,  # file/dir/URL/glob, 0 for webcam
                                  imgsz=416,  # inference size (pixels)
                                  conf_thres=0.25,  # confidence threshold
                                  iou_thres=0.45,  # NMS IOU threshold
                                  max_det=1000,  # maximum detections per image
                                  device=device,  # cuda device, i.e. 0 or 0,1,2,3 or cpu
                                  )
        if show_temp:
            save_path_ = "%s/images" % save_path
            os.makedirs(save_path_, exist_ok=True)
            save_img_names = ["%s/%s.png" % (save_path_, str(_).zfill(5)) for _ in idxs]
            vis_det_results(hole_preds, save_img_names, line_thickness=3)

        for i in range(len(idxs)):
            frame_preds = hole_preds["preds"][i]
            cur_frame_id = idxs[i]

            preds = []
            if len(frame_preds) > 0:
                for pred in frame_preds:
                    pred[1: 5] = norm2image_level(pred[1: 5], frame_h, frame_w)
                    preds.append([str(x) for x in pred])
            video_dets[cur_frame_id] = preds
        source, idxs = [frame], [idx]

        if show_temp:
            os.makedirs(save_path, exist_ok=True)
            json_name = "%s/frame_dets.json" % (save_path)
            write_json(json_name, video_dets)
    return video_dets


def gen_intermediate_hole_infos(video_dets, save_path, dist_thresh=20, frame_thresh=5, show_temp=False):
    """
    :param: video_dets:
    :param: save_path:
    :param: dist_thresh: 相邻框像素距离阈值
    :param: frame_thresh: 孔洞连续出现的帧数阈值
    :param: show_temp:
    :returns:
        intermediate_hole_infos: intermediate_hole_infos
        {
            "hole%04d" % hole_id: {
                "start": int
                "end": int
                "bbox": list, each element is [cls_id, cx, cy, w, h, conf]
            }
        }
    """
    hole_id = 1  # 孔洞id
    intermediate_hole_infos = {}
    for idx in tqdm(range(len(video_dets))):
        preds = video_dets[idx]
        if len(preds) == 0:
            continue
        for pred in preds:
            pred = [float(x) for x in pred]
            # 默认出现新的孔洞，创建
            hole = {}
            hole["start"] = idx
            hole["end"] = idx
            hole["bbox"] = [pred]
            is_new = True
            for key in intermediate_hole_infos.keys():
                dist = sum((intermediate_hole_infos[key]["bbox"][-1][x] - pred[x]) ** 2 for x in [1, 2])
                frame_interval = idx - intermediate_hole_infos[key]["end"]
                # 两帧检测框小于阈值且当前帧序号-结束帧序号小于阈值
                if dist <= dist_thresh ** 2 and frame_interval <= frame_thresh:
                    # 当前孔洞为旧孔洞，更新信息
                    intermediate_hole_infos[key]["end"] = idx
                    intermediate_hole_infos[key]["bbox"].append(pred)
                    is_new = False
            if is_new:
                intermediate_hole_infos["hole%04d" % hole_id] = hole
                hole_id += 1
    if show_temp:
        os.makedirs(save_path, exist_ok=True)
        json_name = "%s/debug.json" % (save_path)
        write_json(json_name, intermediate_hole_infos)
    return intermediate_hole_infos


def gen_final_hole_infos(frames, intermediate_hole_infos, fps, save_path, show_temp=False):
    img_util = ImageUtils()
    hole_infos = {}
    count = 0
    for key in list(intermediate_hole_infos):
        hole_info = {}
        start = intermediate_hole_infos[key]["start"]
        end = intermediate_hole_infos[key]["end"]
        bbox = intermediate_hole_infos[key]["bbox"]
        if end - start <= 10:
            continue
        count += 1
        hole_info["hole_id"] = "孔洞%d" % (count)
        hole_info["start"] = start
        hole_info["end"] = end
        # 转换为秒
        hole_info["duration"] = int(round((end - start) / fps, 0))
        width_sum, height_sum = 0, 0
        hole_count = len(intermediate_hole_infos[key]["bbox"])
        for i in range(hole_count):
            width_sum += float(intermediate_hole_infos[key]["bbox"][i][3])
            height_sum += float(intermediate_hole_infos[key]["bbox"][i][4])
        hole_info["width_pixel"] = round(width_sum / hole_count, 2)
        hole_info["height_pixel"] = round(height_sum / hole_count, 2)
        # 长轴
        hole_info["width"] = img_util.pixel_dist2real_dist(width_sum / hole_count)
        # 短轴
        hole_info["height"] = img_util.pixel_dist2real_dist(height_sum / hole_count)
        # 面积
        hole_info["area"] = img_util.compute_area(hole_info["height"], hole_info["width"])
        # 深度
        hole_info["depth"] = 0

        best_match_frame_idx = start + (end - start) // 2
        frame = frames[best_match_frame_idx]
        best_match_bbox = bbox[hole_count // 2]
        cx, cy, hole_w, hole_h = best_match_bbox[1: -1]
        scale_coef = 4
        x1 = int(max(0, cx - hole_w / 2))
        y1 = int(max(0, cy - hole_h / 2))
        x2 = int(min(x1 + hole_w, frame.shape[1]))
        y2 = int(min(y1 + hole_h, frame.shape[0]))
        hole_imgs = img_util.crop_rect(frame, [[x1, y1, x2, y2]], scale_coef)
        img_str = img_util.rgb_img2base64_str(hole_imgs)[0]
        hole_info["img_str"] = img_str
        hole_info["from"] = 0
        hole_infos["hole%04d" % count] = hole_info
    if show_temp:
        os.makedirs(save_path, exist_ok=True)
        json_name = "%s/hole_infos.json" % (save_path)
        write_json(json_name, hole_infos)
    return hole_infos


def hole_recog(vid_path, batch_size=128, device="cuda", save_path="./hole_recog", show_temp=False):
    vid_name = os.path.basename(vid_path).split(".")[0]
    save_path = "%s/%s" % (save_path, vid_name)
    os.makedirs(save_path, exist_ok=True)

    frames, fps = vid2frames(vid_path)
    if len(frames) == 0:
        return {}
    ckpt_det = Config.ckpt_path()
    model_det = init_model_detector(ckpt_det, device)
    det_t0 = time.time()
    video_dets = gen_video_dets(model_det, frames,
                                batch_size, device,
                                save_path, show_temp)
    det_t1 = time.time()
    det_time = det_t1 - det_t0

    intermediate_hole_infos = gen_intermediate_hole_infos(video_dets,
                                                          save_path,
                                                          dist_thresh=20,
                                                          frame_thresh=5,
                                                          show_temp=show_temp)
    hole_infos = gen_final_hole_infos(frames, intermediate_hole_infos, fps, save_path, show_temp)
    return hole_infos


if __name__ == '__main__':
    vid_path_ = "video01.avi"
    save_path_ = "./hole_recog"
    show_temp_ = False
    show_temp_ = True
    device_ = "cuda"
    batch_size_ = 128
    hole_recog(vid_path_, batch_size_, device_, save_path_, show_temp_)

    import time

    print(time.strftime("%H:%M:%S", time.gmtime(1)))

