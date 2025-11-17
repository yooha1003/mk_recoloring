#!/usr/bin/env python3
"""
jet colormap 이미지의 스케일을 변경하는 스크립트
컬러 이미지를 그레이스케일 강도로 변환 후 스케일 조정하고 다시 jet colormap 적용
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def rescale_colormap_image(input_path, output_path, original_max=0.5, new_max=0.2):
    """
    jet colormap이 적용된 이미지의 스케일을 변경합니다.

    Parameters:
    -----------
    input_path : str
        입력 PNG 파일 경로
    output_path : str
        출력 PNG 파일 경로
    original_max : float
        원본 데이터의 최대값 (예: 0.5)
    new_max : float
        새로운 최대값 (예: 0.2)
    """
    print(f"\n처리 중: {input_path}")
    print(f"범위 변경: 0-{original_max} → 0-{new_max}")

    # 이미지 로드
    img = Image.open(input_path)
    img_array = np.array(img)

    print(f"원본 이미지 크기: {img_array.shape}")
    print(f"원본 이미지 모드: {img.mode}")

    # RGBA 또는 RGB 이미지를 그레이스케일 강도로 변환
    if len(img_array.shape) == 3:
        # RGB 또는 RGBA의 경우
        if img_array.shape[2] == 4:  # RGBA
            rgb = img_array[:, :, :3]
            alpha = img_array[:, :, 3]
        else:  # RGB
            rgb = img_array
            alpha = None

        # RGB를 luminance로 변환
        # 표준 luminance 공식: 0.299*R + 0.587*G + 0.114*B
        grayscale = np.dot(rgb, [0.299, 0.587, 0.114])
    else:
        grayscale = img_array.astype(float)
        alpha = None

    print(f"그레이스케일 값 범위: [{grayscale.min():.2f}, {grayscale.max():.2f}]")

    # 0이 아닌 값들 (배경 제외)
    # 검은색 배경 감지 (RGB 값이 모두 작은 경우)
    if len(img_array.shape) == 3:
        background_mask = np.all(img_array[:, :, :3] < 10, axis=2)
    else:
        background_mask = grayscale < 10

    non_bg_mask = ~background_mask
    non_bg_values = grayscale[non_bg_mask]

    if len(non_bg_values) == 0:
        print("경고: 배경이 아닌 픽셀이 없습니다.")
        return

    print(f"배경 제외 값 범위: [{non_bg_values.min():.2f}, {non_bg_values.max():.2f}]")

    # 0-1 범위로 정규화
    original_min = non_bg_values.min()
    original_max_val = non_bg_values.max()

    normalized = np.zeros_like(grayscale)
    if original_max_val > original_min:
        normalized[non_bg_mask] = (non_bg_values - original_min) / (original_max_val - original_min)

    # 스케일 조정: 데이터 값 자체를 줄임 (0-0.5 → 0-0.2)
    # 예: 원래 0.5(빨간색)였던 값이 0.2가 되어 더 낮은 colormap 위치(녹색/파란색)로 매핑됨
    scale_factor = new_max / original_max
    scaled_normalized = normalized * scale_factor

    print(f"스케일 팩터: {scale_factor:.2f} (데이터 값을 {scale_factor:.1%}로 축소)")
    print(f"조정 후 값 범위: [{scaled_normalized[non_bg_mask].min():.3f}, {scaled_normalized[non_bg_mask].max():.3f}]")

    # jet colormap 적용
    cmap = cm.get_cmap('jet')
    colored = cmap(scaled_normalized)

    # 0-255 범위로 변환
    result_array = (colored * 255).astype(np.uint8)

    # 배경을 검은색으로 설정
    result_array[background_mask] = [0, 0, 0, 255]

    # 결과 저장
    result_img = Image.fromarray(result_array, mode='RGBA')
    result_img.save(output_path)

    print(f"저장 완료: {output_path}\n")


def main():
    import sys

    if len(sys.argv) < 3:
        print("사용법: python rescale_colormap.py <입력파일> <출력파일> [원본max] [새로운max]")
        print("예제: python rescale_colormap.py input.png output.png 0.5 0.2")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    original_max = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    new_max = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2

    rescale_colormap_image(input_file, output_file, original_max, new_max)


if __name__ == '__main__':
    # sample 이미지들 처리
    print("="*60)
    print("Jet Colormap 스케일 변경: 0-0.5 → 0-0.2")
    print("="*60)

    rescale_colormap_image('sample/figure1.png', 'sample/figure1_rescaled.png',
                          original_max=0.5, new_max=0.2)

    rescale_colormap_image('sample/figure2.png', 'sample/figure2_rescaled.png',
                          original_max=0.5, new_max=0.2)

    print("="*60)
    print("완료! 결과 파일:")
    print("  - sample/figure1_rescaled.png")
    print("  - sample/figure2_rescaled.png")
    print("="*60)
