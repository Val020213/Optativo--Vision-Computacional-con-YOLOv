import subprocess
import math


def run(command: str):
    subprocess.run(command.split())


def trim_video(path, output_name, start_frame, end_frame, overwrite=1):
    overwrite = "-y" if overwrite else "-n"
    command = f"ffmpeg -i {path} -filter_complex [0:v]trim=start_frame={start_frame}:end_frame={end_frame},setpts=PTS-STARTPTS[cut] -map [cut] {output_name} {overwrite}"
    run(command)


def deinterlace_video(path, output_name):
    command = f"ffmpeg -i {path} -c:v libx264 -vf yadif,format=yuv420p -preset veryslow -crf 18 -an {output_name} -y"
    run(command)


def covert_to_mp4(path, output_name):
    command = f"ffmpeg -i {path} {output_name}.mp4"
    run(command)


def load_doc_data(doc_path):
    data = []
    with open(doc_path, "r") as f:
        for line in f:
            line = line.split()
            data.append((int(line[0]), int(line[1])))
    return data


# extend 10 frames li for all data points
def extend_frames(doc_path, data):
    data = [str(x[0] - 10) + " " + str(x[1]) for x in data]
    with open(doc_path, "w") as f:
        f.write("\n".join(data))


# fix format names
# name_00n.mp4
def format_name_default_output_video(cont):
    return "_" + "0" * (int(math.log(100 / (cont + 1), 10)) + 1) + str(cont) + ".mp4"


# name_dein_00n.mp4
def format_name_dein_output_video(name):
    ans = ""
    flag = 1
    for c in name:
        ans += c
        if c == "_" and flag:
            flag = 0
            ans += "dein_"
    return ans


# name_000number.jpg
def format_name_output_img(name, cont):
    counter = 0
    img = ""
    flag = 1

    i = 0
    while i < len(name):
        c = name[i]
        img += c
        if c == "_" and not flag:  # 02_
            break
        if c == "_" and flag:  # _dein_
            flag = 0
            i += 1
            while name[i] != "_":
                i += 1
        i += 1

    img += "0" * (int(math.log(1000 / (cont + 1), 10)) + 1) + str(cont) + ".jpg"
    return img
