import fbs_generator
import bytes_generator
import flatbuffers
import os, sys

sys.path.append(os.path.dirname(os.path.realpath(sys.argv[0])))
PWD = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    config_name = "config.json"
    flatc_name = "flatc/flatc"
    build_flatc_name = "build_flatc.sh"
    work_root = PWD
    config_path = os.path.join(work_root, config_name)
    flatc_Bin_path = os.path.join(work_root, flatc_name)
    build_flatc_path = os.path.join(work_root, build_flatc_name)
    if not os.path.exists(flatc_Bin_path):
        os.system("sh {0}".format(build_flatc_path))

    fbs_obj = fbs_generator.FbsGenerator(config_path)
    bytes_obj = bytes_generator.BytesGenerator(config_path)
    fbs_obj.run()     # 必须先生成代码
    bytes_obj.run()   # 然后将excel数据打包成 flatbuffers 的二进制

