# ByakuganVisualizer

<img src="logo/logo.jpeg" width="200">

The ByakuganVisualizer repository hosts a Python tool designed to compare images and highlight their differences. 
It simplifies the process of identifying disparities between images, making it ideal for tasks like testing and quality 
assurance. Additionally, it offers options for customization, which can be helpful for color-blind users.


## Usage 

```bash
usage: byakugan_vision [-h] [--version] --diff DIFF [--filter {red,blue,green,yellow}] [--out_dir OUT_DIR]

ByakuganVisualizer: Tool for comparing images and highlighting differences.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --diff DIFF           String containing a list of tuples "Path_To_Image1a,Path_To_Image2a;Path_To_Image1b,Path_To_Image2b...". Each tuple contains two paths to images to be compared.
  --filter {red,blue,green,yellow}
                        Filter type (red, blue, green, yellow)
  --out_dir OUT_DIR     Output directory for the difference images

```