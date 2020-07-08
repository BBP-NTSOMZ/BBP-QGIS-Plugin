
RUN_TYPE_DEBUG = True

def debug_info_path(filename:str)->str:
    loc_dir = dirname(__file__)
    loc_dir = join(loc_dir, "debug_files")
    debug_file = join(loc_dir, filename)
    return debug_file