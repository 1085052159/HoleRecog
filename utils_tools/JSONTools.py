# !/usr/bin/env python
# _*_ coding: utf-8 _*_
import json
import os
import shutil
from pathlib import Path


class Config(object):
    @staticmethod
    def write_json(file_path, data):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if os.path.exists(file_path):
            # backup old file
            shutil.copyfile(file_path, "%s_backup.json" % file_path.split(".")[0])
        json_str = json.dumps(data, indent=4, ensure_ascii=False)
        with open(file_path, mode="w", encoding="utf-8") as f:
            f.write(json_str)

    @staticmethod
    def read_json(file_path):
        path = Path(file_path).exists()
        if path:
            with open(file_path, 'r', encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except:
                    data = None
            return data

    @staticmethod
    def delete_json_data(data, key):
        """
        删除json数据
        """
        if key in data:
            del data[key]
            return data

    @staticmethod
    def get_file_dir():
        """get_file_dir"""
        return Path(__file__)

    @staticmethod
    def user_data_path():
        """user_ifno"""
        path = Config.get_file_dir()
        file_dir = path.parent.parent
        file_path = file_dir.joinpath('important_datas', 'users', 'user_data.json')
        os.makedirs(os.path.dirname(str(file_path)), exist_ok=True)
        return str(file_path).replace("\\", "/")

    @staticmethod
    def user_portrait_save_path():
        path = Config.get_file_dir()
        file_dir = path.parent.parent
        portrait_save_path = file_dir.joinpath('important_datas', 'users', 'portraits')
        os.makedirs(portrait_save_path, exist_ok=True)
        return str(portrait_save_path).replace("\\", "/")

    @staticmethod
    def hole_recog_save_path():
        path = Config.get_file_dir()
        file_dir = path.parent.parent
        portrait_save_path = file_dir.joinpath('important_datas', 'intermediate', 'hole_recog')
        os.makedirs(portrait_save_path, exist_ok=True)
        return str(portrait_save_path).replace("\\", "/")

    @staticmethod
    def videos_save_path():
        path = Config.get_file_dir()
        file_dir = path.parent.parent
        portrait_save_path = file_dir.joinpath('important_datas', 'saved_videos')
        os.makedirs(portrait_save_path, exist_ok=True)
        return str(portrait_save_path).replace("\\", "/")

    @staticmethod
    def ckpt_path():
        path = Config.get_file_dir()
        file_dir = path.parent.parent
        portrait_save_path = file_dir.joinpath('important_datas', 'ckpts', 'best.pt')
        return str(portrait_save_path).replace("\\", "/")

    @staticmethod
    def create_user_file(data):
        """
        创建json文件并写入数据
        :param file_path:
        :param data:
        :return:
        """
        file_path = Config.user_data_path()
        Config.write_json(file_path, data)

    @staticmethod
    def read_user_info():
        """
        读取json文件
        :param file_path:
        :return:
        """
        file_path = Config.user_data_path()
        print("[JSONTools.read_user_info]file_path: ", file_path)
        data = Config.read_json(file_path)
        return data

    @staticmethod
    def write_user_info(data):
        """writer_file_data"""
        file_path = Config.user_data_path()
        Config.write_json(file_path, data)

    @staticmethod
    def query_user_info(data, key, password):
        """
        查询json数据
        :param data:
        :param key:
        :return:
        """
        # if key in data and password in data[key]["password"]:
        if key in data.keys() and password == data[key]["password"] and "已启用" == data[key]["state"]:
            return data[key]
        else:
            return None

    @staticmethod
    def modify_pwd_data(data, key, value):
        """
        修改json数据
        :param key:
        :param value:
        :return:
        """
        if key in data:
            data[key] = value
            return data

    @staticmethod
    def modify_user_data(data, old_key, new_key, new_value):
        """
        修改json keys和values数据
        :param data:
        :param old_key:
        :param new_key:
        :param new_value:
        :return:
        """
        if old_key in data:
            data[new_key] = new_value
            if old_key != new_key:
                del data[old_key]
                return data
            else:
                return data

    @staticmethod
    def vid_data_path():
        """video_info"""
        path = Config.get_file_dir()
        file_dir = path.parent.parent
        file_path = file_dir.joinpath('important_datas', 'holes', 'vid_infos.json')
        os.makedirs(os.path.dirname(str(file_path)), exist_ok=True)
        return str(file_path).replace("\\", "/")

    @staticmethod
    def read_vid_info():
        """read_file"""
        file_path = Config.vid_data_path()
        print("[JSONTools.read_vid_info]file_path: ", file_path)
        data = Config.read_json(file_path)
        return data

    @staticmethod
    def write_vid_info(data):
        """writer_file_data"""
        file_path = Config.vid_data_path()
        Config.write_json(file_path, data)
