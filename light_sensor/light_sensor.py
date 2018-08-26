import time

import cv2
from yeelight import Bulb


def compare_frames(frame_a, frame_b):
    assert frame_a.shape == frame_b.shape
    h, w, c = frame_a.shape
    gray_a = cv2.cvtColor(frame_a, cv2.COLOR_BGR2GRAY)
    gray_b = cv2.cvtColor(frame_b, cv2.COLOR_BGR2GRAY)

    hist_a = cv2.calcHist([gray_a], [0], None, [64], [0, 64])
    hist_b = cv2.calcHist([gray_b], [0], None, [64], [0, 64])

    dev = 0
    for each_bin, every_bin in zip(hist_a, hist_b):
        dev += abs(each_bin[0] - every_bin[0])

    return min(1., dev / (h * w * 2))


def read_cam():
    minute = 60
    duration = 5 * minute
    cam_url = "rtsp://192.168.178.33:554/unicast"
    light_ip = "192.168.178.31"
    activated_at = -1

    bulb = Bulb(light_ip)
    cap = cv2.VideoCapture(cam_url)
    old_frame = None
    while True:
        for _ in range(29):
            cap.read()
        _, frame = cap.read()

        if old_frame is not None:
            now = time.time()
            d = compare_frames(old_frame, frame)
            if d >= .05:
                bulb.turn_on()
                activated_at = now

            elif now - activated_at >= duration:
                bulb.turn_off()
                activated_at = -1

        old_frame = frame


def main():
    read_cam()


if __name__ == "__main__":
    main()
