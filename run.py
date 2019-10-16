import fbs_generator
import bytes_generator
import os

if __name__ == '__main__':

    config_name = "config.json"
    work_root = os.getcwd()
    config_path = os.path.join(work_root, config_name)

    fbs_obj = fbs_generator.FbsGenerator(config_path)
    bytes_obj = bytes_generator.BytesGenerator(config_path)
    fbs_obj.run()     # 必须先生成代码
    bytes_obj.run()   # 然后将excel数据打包成 flatbuffers 的二进制

