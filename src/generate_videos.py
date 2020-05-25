"""
Copyright (C) 2017 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-ND 4.0 license (https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode).

Sergey Tulyakov, Ming-Yu Liu, Xiaodong Yang, Jan Kautz, MoCoGAN: Decomposing Motion and Content for Video Generation
https://arxiv.org/abs/1707.04993

Generates multiple videos given a model and saves them as video files using ffmpeg

Usage:
    generate_videos.py [options] <model> <output_folder>

Options:
    -n, --num_videos=<count>                number of videos to generate [default: 10]
    -o, --output_format=<ext>               save videos as [default: gif]
    -f, --number_of_frames=<count>          generate videos with that many frames [default: 16]

    --ffmpeg=<str>                          ffmpeg executable (on windows should be ffmpeg.exe). Make sure
                                            the executable is in your PATH [default: ffmpeg]
"""

import os
import docopt
import torch

from trainers import videos_to_numpy
from PIL import Image

import subprocess as sp


def save_video(ffmpeg, video, filename):
    images = []
    for i in range(video.shape[0]):
        images.append(Image.fromarray(video[i,:,:,:]))
    #     im.save(filename + str(i))
    images[0].save(filename, save_all=True, append_images=images[1:],
        optimize=False, duration=40, loop=0)

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    device = torch.device("cuda")
    generator = torch.load(args["<model>"], map_location={'cuda:0': 'cpu'})
    generator.to(device)
    generator.eval()
    num_videos = int(args['--num_videos'])
    output_folder = args['<output_folder>']

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i in range(num_videos):
        v, _ = generator.sample_videos(1, int(args['--number_of_frames']))
        video = videos_to_numpy(v).squeeze().transpose((1, 2, 3, 0))
        # save_video(args["--ffmpeg"], video, os.path.join(output_folder, "{}".format(i)))
        save_video(args["--ffmpeg"], video, os.path.join(output_folder, "{}.{}".format(i, args['--output_format'])))
