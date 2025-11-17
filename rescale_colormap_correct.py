#!/usr/bin/env python3
"""
jet colormap 이미지에서 원본 데이터를 역추출하고 스케일을 변경하는 스크립트
RGB 값을 jet colormap에 역매핑하여 정확한 원본 값 복원
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial import KDTree


def rgb_to_data_value(rgb_array, colormap_name='jet', n_colors=256):
    """
    RGB 이미지를 colormap에 역매핑하여 원본 데이터 값(0-1)을 복원합니다.

    Parameters:
    -----------
    rgb_array : ndarray
        RGB 이미지 배열 (H, W, 3 또는 4)
    colormap_name : str
        사용된 colormap 이름
    n_colors : int
        colormap 해상도

    Returns:
    --------
    data_values : ndarray
        복원된 데이터 값 (0-1 범위)
    """
    # colormap lookup table 생성
    cmap = cm.get_cmap(colormap_name)
    lookup_values = np.linspace(0, 1, n_colors)
    lookup_colors = cmap(lookup_values)[:, :3] * 255  # RGB만 사용, 0-255 범위

    # KDTree로 가장 가까운 색상 찾기
    tree = KDTree(lookup_colors)

    # 이미지 reshape
    original_shape = rgb_array.shape[:2]
    if rgb_array.shape[2] == 4:  # RGBA
        rgb_flat = rgb_array[:, :, :3].reshape(-1, 3)
    else:  # RGB
        rgb_flat = rgb_array.reshape(-1, 3)

    # 각 픽셀에 대해 가장 가까운 colormap 색상 찾기
    distances, indices = tree.query(rgb_flat)

    # 인덱스를 0-1 범위의 값으로 변환
    data_values = lookup_values[indices].reshape(original_shape)

    return data_values, distances.reshape(original_shape)


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

    # 배경 마스크 (검은색 픽셀)
    if img_array.shape[2] == 4:  # RGBA
        background_mask = np.all(img_array[:, :, :3] < 10, axis=2)
    else:  # RGB
        background_mask = np.all(img_array < 10, axis=2)

    # RGB를 jet colormap에 역매핑하여 원본 데이터 값 복원
    print("jet colormap 역매핑 중...")
    data_values, distances = rgb_to_data_value(img_array, colormap_name='jet', n_colors=512)

    # 배경이 아닌 영역의 평균 매칭 오차 확인
    non_bg_distances = distances[~background_mask]
    if len(non_bg_distances) > 0:
        print(f"평균 색상 매칭 오차: {non_bg_distances.mean():.2f} (RGB 유클리드 거리)")

    print(f"복원된 데이터 값 범위: [{data_values[~background_mask].min():.3f}, {data_values[~background_mask].max():.3f}]")

    # 스케일 조정: vmax를 줄여서 같은 값이 더 높은 colormap 위치로 매핑
    # vmax 0.5 → 0.2로 줄이면 더 붉게 표현됨
    scale_factor = original_max / new_max
    scaled_values = data_values * scale_factor
    # 1.0 초과하는 값은 클리핑 (모두 빨간색으로)
    scaled_values = np.clip(scaled_values, 0, 1)

    print(f"스케일 팩터: {scale_factor:.2f} (vmax {original_max}→{new_max})")
    print(f"조정 후 값 범위: [{scaled_values[~background_mask].min():.3f}, {scaled_values[~background_mask].max():.3f}]")

    # jet colormap 적용
    cmap = cm.get_cmap('jet')
    colored = cmap(scaled_values)

    # 0-255 범위로 변환
    result_array = (colored * 255).astype(np.uint8)

    # 배경을 검은색으로 설정
    result_array[background_mask] = [0, 0, 0, 255]

    # 결과 저장
    result_img = Image.fromarray(result_array, mode='RGBA')
    result_img.save(output_path)

    print(f"저장 완료: {output_path}\n")


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='Jet colormap 이미지의 스케일을 변경합니다 (RGB 역매핑 방식)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예제:
  # 기본 사용 (0-0.5 → 0-0.2)
  python rescale_colormap_correct.py input.png output.png

  # 사용자 지정 범위 (0-1.0 → 0-0.3)
  python rescale_colormap_correct.py input.png output.png --original-max 1.0 --new-max 0.3

  # vmax를 줄여서 더 붉게 만들기 (0-0.5 → 0-0.2)
  python rescale_colormap_correct.py input.png output.png --original-max 0.5 --new-max 0.2

  # vmax를 늘려서 더 파랗게 만들기 (0-0.2 → 0-0.5)
  python rescale_colormap_correct.py input.png output.png --original-max 0.2 --new-max 0.5
        '''
    )

    parser.add_argument('input', help='입력 PNG 파일 경로')
    parser.add_argument('output', help='출력 PNG 파일 경로')
    parser.add_argument('--original-max', type=float, default=0.5,
                        help='원본 데이터의 최대값 (vmax) (기본값: 0.5)')
    parser.add_argument('--new-max', type=float, default=0.2,
                        help='새로운 최대값 (vmax) (기본값: 0.2)')

    args = parser.parse_args()

    try:
        rescale_colormap_image(
            args.input,
            args.output,
            original_max=args.original_max,
            new_max=args.new_max
        )
        print(f"\n✓ 변환 완료!")
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다 - {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"오류: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
