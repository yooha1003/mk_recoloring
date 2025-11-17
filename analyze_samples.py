#!/usr/bin/env python3
"""
sample 폴더의 PNG 파일들을 분석하는 스크립트
"""

import numpy as np
from PIL import Image
import os


def analyze_image(file_path):
    """PNG 이미지를 분석하여 상세 정보를 출력합니다."""
    print("="*70)
    print(f"파일: {file_path}")
    print("="*70)

    # 이미지 로드
    img = Image.open(file_path)
    img_array = np.array(img)

    # 기본 정보
    print(f"\n[기본 정보]")
    print(f"  이미지 크기: {img_array.shape}")
    print(f"  이미지 모드: {img.mode}")
    print(f"  데이터 타입: {img_array.dtype}")

    # 채널별 분석
    if len(img_array.shape) == 2:
        # 그레이스케일
        print(f"\n[그레이스케일 분석]")
        print(f"  값 범위: [{img_array.min()}, {img_array.max()}]")

        # 0이 아닌 값 분석
        non_zero = img_array[img_array != 0]
        if len(non_zero) > 0:
            print(f"  0이 아닌 값 범위: [{non_zero.min()}, {non_zero.max()}]")
            print(f"  0이 아닌 픽셀 수: {len(non_zero)} ({len(non_zero)/img_array.size*100:.2f}%)")

        # 0 값 분석
        zero_count = np.sum(img_array == 0)
        print(f"  0 값 픽셀 수: {zero_count} ({zero_count/img_array.size*100:.2f}%)")

        # 값 분포
        unique_values = np.unique(img_array)
        print(f"  고유한 값의 개수: {len(unique_values)}")
        if len(unique_values) <= 10:
            print(f"  고유한 값들: {unique_values}")

    elif len(img_array.shape) == 3:
        # 컬러 이미지
        channels = img_array.shape[2]
        print(f"\n[컬러 이미지 분석 - {channels}개 채널]")

        channel_names = ['Red', 'Green', 'Blue', 'Alpha'][:channels]

        for i, name in enumerate(channel_names):
            channel = img_array[:, :, i]
            print(f"\n  {name} 채널:")
            print(f"    값 범위: [{channel.min()}, {channel.max()}]")
            print(f"    평균: {channel.mean():.2f}")
            print(f"    표준편차: {channel.std():.2f}")

        # 그레이스케일 변환 후 분석
        if channels >= 3:
            gray = np.mean(img_array[:, :, :3], axis=2)
            print(f"\n[그레이스케일 변환 후 분석]")
            print(f"  값 범위: [{gray.min():.2f}, {gray.max():.2f}]")

            # 어두운 픽셀 (0에 가까운) 분석
            dark_threshold = 10
            dark_pixels = gray < dark_threshold
            dark_count = np.sum(dark_pixels)
            print(f"  어두운 픽셀 (< {dark_threshold}): {dark_count} ({dark_count/gray.size*100:.2f}%)")

    print("\n")


def main():
    sample_dir = 'sample'

    if not os.path.exists(sample_dir):
        print(f"오류: {sample_dir} 폴더를 찾을 수 없습니다.")
        return

    # PNG 파일 찾기
    png_files = [f for f in os.listdir(sample_dir) if f.endswith('.png')]

    if not png_files:
        print(f"{sample_dir} 폴더에 PNG 파일이 없습니다.")
        return

    print(f"\n{sample_dir} 폴더의 PNG 파일 분석\n")

    # 각 파일 분석
    for png_file in sorted(png_files):
        file_path = os.path.join(sample_dir, png_file)
        analyze_image(file_path)


if __name__ == '__main__':
    main()
