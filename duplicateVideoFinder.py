from os import path, walk, makedirs, rename
from time import clock
from imagehash import average_hash
from PIL import Image
from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS
from json import dump, load
from multiprocessing import Pool, cpu_count

input_vid_dir = r'C:\Users\gokul\Documents\data\\'
json_dir = r'C:\Users\gokul\Documents\db\\'
analyzed_dir = r'C:\Users\gokul\Documents\analyzed\\'

if not path.exists(json_dir):
    makedirs(json_dir)

if not path.exists(analyzed_dir):
    makedirs(analyzed_dir)


def write_to_json(filename, data):
    file_full_path = json_dir + filename + ".json"
    with open(file_full_path, 'w') as file_pointer:
        dump(data, file_pointer)
    return


def video_to_json(filename):
    file_full_path = input_vid_dir + filename
    start = clock()
    size = round(path.getsize(file_full_path) / 1024 / 1024, 2)
    video_pointer = VideoCapture(file_full_path)
    frame_count = int(VideoCapture.get(video_pointer, int(CAP_PROP_FRAME_COUNT)))
    width = int(VideoCapture.get(video_pointer, int(CAP_PROP_FRAME_WIDTH)))
    height = int(VideoCapture.get(video_pointer, int(CAP_PROP_FRAME_HEIGHT)))
    fps = int(VideoCapture.get(video_pointer, int(CAP_PROP_FPS)))
    success, image = video_pointer.read()
    video_hash = {}
    while success:
        frame_hash = average_hash(Image.fromarray(image))
        video_hash[str(frame_hash)] = filename
        success, image = video_pointer.read()
    stop = clock()
    time_taken = stop - start
    print("Time taken for ", file_full_path, " is : ", time_taken)
    data_dict = {}
    data_dict['size'] = size
    data_dict['time_taken'] = time_taken
    data_dict['fps'] = fps
    data_dict['height'] = height
    data_dict['width'] = width
    data_dict['frame_count'] = frame_count
    data_dict['filename'] = filename
    data_dict['video_hash'] = video_hash
    write_to_json(filename, data_dict)
    return


def multiprocess_video_to_json():
    files = next(walk(input_vid_dir))[2]
    processes = cpu_count()
    print(processes)
    pool = Pool(processes)
    start = clock()
    test = pool.starmap_async(video_to_json, zip(files))
    pool.close()
    pool.join()
    stop = clock()
    print("Time Taken : ", stop - start)


def key_with_max_val(d):
    max = 0
    required_key = ""
    for k in d:
        if (d[k] > max):
            max = d[k]
            required_key = k
    return required_key


def duplicate_analyzer():
    files = next(walk(json_dir))[2]
    data_dict = {}
    for filename in files:
        filename = json_dir + filename
        with open(filename) as f:
            data = load(f)
        video_hash = data['video_hash']
        count = 0
        duplicate_file = {}
        for key in video_hash:
            count += 1
            if (key in data_dict):
                if (data_dict[key] in duplicate_file):
                    duplicate_file[data_dict[key]] = duplicate_file[data_dict[key]] + 1
                else:
                    duplicate_file[data_dict[key]] = 1
            else:
                data_dict[key] = video_hash[key]
        if (duplicate_file):
            duplfile = key_with_max_val(duplicate_file)
            dupl_percentage = ((duplicate_file[duplfile] / count) * 100)
            if (dupl_percentage > 80):
                print(filename, " id dup of ", duplfile)
            else:
                print(filename, " no duplicate")
        else:
            print(filename, " no duplicate")


def mv_analyzed_file():
    files = next(walk(json_dir))[2]
    for filename in files:
        filename = filename[:-5]
        src = input_vid_dir + filename
        tgt = analyzed_dir + filename
        if path.exists(src):
            rename(src, tgt)
        else:
            print("File already moved")


if __name__ == '__main__':
    mv_analyzed_file()
    multiprocess_video_to_json()
    # duplicate_analyzer()
