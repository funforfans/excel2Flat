import fbs_generator
import bytes_generator
from common.loader import ConfigLoader
import flatbuffers
import os, sys, argparse

sys.path.append(os.path.dirname(os.path.realpath(sys.argv[0])))
PWD = os.path.dirname(os.path.abspath(__file__))


def run(config_path):
    """

    :param config_name: 
    :return: 
    """
    flatc_name = "flatc/flatc"
    build_flatc_name = "build_flatc.sh"

    work_root = PWD

    """
    flatc_Bin_path = os.path.join(work_root, flatc_name)
    build_flatc_path = os.path.join(work_root, build_flatc_name)
    if not os.path.exists(flatc_Bin_path):
        os.system("sh {0}".format(build_flatc_path))
    """


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='covert excel files to fbs and binary:')
    parser.add_argument("-t", "--config_type", type=str, help="type of config file , eg: json, yaml..")
    parser.add_argument("-p", "--config_path", type=str, help="config file path")
    args = parser.parse_args()
    config_type = args.config_type
    config_path = args.config_path
    configer = ConfigLoader.get_config_dict(path=config_path, config_type=config_type)
    fbs_obj = fbs_generator.FbsGenerator(configer)
    bytes_obj = bytes_generator.BytesGenerator(configer)
    fbs_obj.run()
    bytes_obj.run()


