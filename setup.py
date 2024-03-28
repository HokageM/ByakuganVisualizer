"""
    Setup file for ByakuganVisualizer.
    Use setup.cfg to configure your project.

    This file was generated with PyScaffold 4.5.
    PyScaffold helps you to put up the scaffold of your new Python project.
    Learn more under: https://pyscaffold.org/
"""
from setuptools import setup

if __name__ == "__main__":
    try:
        setup(description="The ByakuganVisualizer repository hosts a Python tool designed to compare images and "
                          "highlight their differences. It simplifies the process of identifying disparities between "
                          "images, making it ideal for tasks like testing and quality assurance. Additionally, it "
                          "offers options for customization, which can be helpful for color-blind users.",
              long_description_content_type="text/markdown",
              version="0.1.0"
              )
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of setuptools, "
            "setuptools_scm and wheel with:\n"
            "   pip install -U setuptools setuptools_scm wheel\n\n"
        )
        raise
