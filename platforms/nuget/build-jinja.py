import os, argparse
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

VERSION_PATH = str(Path(PATH).parents[1]) + "/modules/core/include/opencv2/core/version.hpp"
version_file = Path(VERSION_PATH).read_text()

version_major = int(version_file.split("CV_VERSION_MAJOR")[1].split("\n")[0])
version_minor = int(version_file.split("CV_VERSION_MINOR")[1].split("\n")[0])
version_revision = int(version_file.split("CV_VERSION_REVISION")[1].split("\n")[0])

version_string = str(version_major) + "." + str(version_minor) + "." + str(version_revision)

params = {
'id': 'OpenCVNuget',
'version': version_string,
'description': 'OpenCV Nuget Package for C++',
'tags': 'OpenCV, opencv',
'authors': 'OpenCV',
'compilers': ['vc14', 'vc15', 'vc16'],
'architectures': ['x64'],
}

def parse_arguments():
    parser = argparse.ArgumentParser(description="OpenCV CPP create nuget spec script ",
                                     usage='')
    # Main arguments
    parser.add_argument("--package_name", required=False, help="Package name. e.g.: OpenCV.CPP")
    parser.add_argument("--package_version", required=False, help="Package version. e.g: 1.0.0")

    return parser.parse_args()

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def create_nuspec():
    fname = "build/opencv.nuspec"
    context = {
        'params': params
    }
    with open(fname, 'w') as f:
        html = render_template('OpenCVNuget.nuspec', context)
        f.write(html)

def main():
    # Parse arguments
    args = parse_arguments()
    if args.package_version is not None:
        params['compilers'] = args.package_version.split(',')
    # Create template files
    create_nuspec()
if __name__ == "__main__":
    main()