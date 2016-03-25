""" a build slave for the program """

CONFIG = dict(
    unity_path=r"C:\program files\Unity\Editor\Unity.exe", #default windows paths
    build_module="Anemone.Build.Windows",
    arguments="-quit -batchmode -executeMethod")

# Win "C:\Program Files\Unity\Editor\Unity.exe"
# Mac /Applications/Unity/Unity.app/Contents/MacOS/Unity

# -projectPath <pathname>

def build(build_config):
    """ builds the project """
    print(build_config.unity_path)
    print(build_config.build_module)
    print(build_config.argumentsbuild_module)
