# coding=utf-8
import ConfigParser
import os.path


def load_config():
    config = ConfigParser.ConfigParser()
    config.set('DEFAULT', "old_new_func_dataset_path", "")
    if os.path.exists("config.ini"):
        config.read("config.ini")
    else:
        print("config.ini not exist, quiting")
        with open("config.ini", "w") as f:
            config.write(f)
        exit(1)
    return config
