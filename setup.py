import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="SCANEYE",
    options={
        "build_exe": {
            "packages": ["os", "tkinter", "PIL", "cv2", "numpy", "time", "mysql.connector", "skimage.metrics"],
            "include_files": ["imagenes"] 
        }
    },
    executables=executables
)