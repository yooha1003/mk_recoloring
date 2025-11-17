#!/usr/bin/env python3
"""
PNG 이미지의 컬러맵 스케일 재조정 도구

검은색(0 값)을 제외하고 나머지 값들의 스케일을 사용자가 원하는 범위로 재조정합니다.
"""

import numpy as np
from PIL import Image
import argparse
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def recolor_image(input_path, output_path, new_min=None, new_max=None, preserve_zero=True):
    """
    PNG 이미지의 컬러맵 스케일을 재조정합니다.

    Parameters:
    -----------
    input_path : str
        입력 PNG 파일 경로
    output_path : str
        출력 PNG 파일 경로
    new_min : float, optional
        새로운 최소값 (기본값: 원본의 최소값)
    new_max : float, optional
        새로운 최대값 (기본값: 255)
    preserve_zero : bool, optional
        0 값을 보존할지 여부 (기본값: True)

    Returns:
    --------
    dict : 변환 정보를 포함한 딕셔너리
    """
    # 이미지 로드
    img = Image.open(input_path)
    img_array = np.array(img)

    # 원본 정보 저장
    original_dtype = img_array.dtype
    original_shape = img_array.shape
    original_mode = img.mode

    print(f"원본 이미지 정보:")
    print(f"  - 크기: {original_shape}")
    print(f"  - 모드: {original_mode}")
    print(f"  - 데이터 타입: {original_dtype}")
    print(f"  - 값 범위: [{img_array.min()}, {img_array.max()}]")

    # 작업할 배열 복사
    result_array = img_array.astype(np.float64)

    # 0이 아닌 값들만 선택
    if preserve_zero:
        non_zero_mask = img_array != 0
        non_zero_values = result_array[non_zero_mask]

        if len(non_zero_values) == 0:
            print("경고: 0이 아닌 값이 없습니다.")
            return None

        original_min = non_zero_values.min()
        original_max = non_zero_values.max()
    else:
        original_min = result_array.min()
        original_max = result_array.max()
        non_zero_mask = np.ones_like(result_array, dtype=bool)
        non_zero_values = result_array[non_zero_mask]

    print(f"\n재조정 대상 값 범위: [{original_min}, {original_max}]")

    # 새로운 범위 설정
    if new_min is None:
        new_min = original_min
    if new_max is None:
        new_max = 255.0

    print(f"목표 값 범위: [{new_min}, {new_max}]")

    # 스케일 재조정
    if original_max != original_min:
        # 선형 변환: (x - old_min) / (old_max - old_min) * (new_max - new_min) + new_min
        result_array[non_zero_mask] = (
            (non_zero_values - original_min) / (original_max - original_min) *
            (new_max - new_min) + new_min
        )
    else:
        print("경고: 모든 값이 동일하여 스케일링을 수행하지 않습니다.")
        result_array[non_zero_mask] = new_min

    # 0 값 보존
    if preserve_zero:
        result_array[~non_zero_mask] = 0

    # 데이터 타입에 맞게 클리핑
    if original_dtype == np.uint8:
        result_array = np.clip(result_array, 0, 255).astype(np.uint8)
    elif original_dtype == np.uint16:
        result_array = np.clip(result_array, 0, 65535).astype(np.uint16)
    else:
        result_array = result_array.astype(original_dtype)

    print(f"\n결과 이미지 정보:")
    print(f"  - 값 범위: [{result_array.min()}, {result_array.max()}]")

    # 결과 저장
    result_img = Image.fromarray(result_array, mode=original_mode)
    result_img.save(output_path)

    print(f"\n저장 완료: {output_path}")

    return {
        'original_shape': original_shape,
        'original_range': (original_min, original_max),
        'new_range': (new_min, new_max),
        'preserve_zero': preserve_zero
    }


def apply_colormap(input_path, output_path, colormap='jet', preserve_zero=True,
                   vmin=None, vmax=None, background_color=None):
    """
    PNG 이미지에 matplotlib 컬러맵을 적용합니다.

    Parameters:
    -----------
    input_path : str
        입력 PNG 파일 경로
    output_path : str
        출력 PNG 파일 경로
    colormap : str, optional
        matplotlib 컬러맵 이름 (기본값: 'jet')
        예: 'jet', 'viridis', 'plasma', 'inferno', 'magma', 'hot', 'cool', 'rainbow' 등
    preserve_zero : bool, optional
        0 값을 보존할지 여부 (기본값: True)
    vmin : float, optional
        컬러맵 적용 시 최소값 (None이면 0이 아닌 값의 최소값 사용)
    vmax : float, optional
        컬러맵 적용 시 최대값 (None이면 0이 아닌 값의 최대값 사용)
    background_color : tuple or None, optional
        0 값에 적용할 배경색 (R, G, B, A) 0-255 범위, None이면 검은색 (0, 0, 0, 255)

    Returns:
    --------
    dict : 변환 정보를 포함한 딕셔너리
    """
    # 이미지 로드
    img = Image.open(input_path)
    img_array = np.array(img)

    # 원본 정보 저장
    original_dtype = img_array.dtype
    original_shape = img_array.shape
    original_mode = img.mode

    print(f"원본 이미지 정보:")
    print(f"  - 크기: {original_shape}")
    print(f"  - 모드: {original_mode}")
    print(f"  - 데이터 타입: {original_dtype}")
    print(f"  - 값 범위: [{img_array.min()}, {img_array.max()}]")

    # 그레이스케일로 변환 (여러 채널인 경우)
    if len(original_shape) > 2:
        # RGB를 그레이스케일로 변환
        img_array = np.mean(img_array, axis=2)
        print(f"  - 그레이스케일로 변환됨")

    # 작업할 배열 복사
    work_array = img_array.astype(np.float64)

    # 0이 아닌 값들만 선택
    if preserve_zero:
        non_zero_mask = img_array != 0
        non_zero_values = work_array[non_zero_mask]

        if len(non_zero_values) == 0:
            print("경고: 0이 아닌 값이 없습니다.")
            return None

        original_min = non_zero_values.min()
        original_max = non_zero_values.max()
    else:
        original_min = work_array.min()
        original_max = work_array.max()
        non_zero_mask = np.ones_like(work_array, dtype=bool)
        non_zero_values = work_array[non_zero_mask]

    print(f"\n컬러맵 적용 대상 값 범위: [{original_min}, {original_max}]")

    # vmin, vmax 설정
    if vmin is None:
        vmin = original_min
    if vmax is None:
        vmax = original_max

    print(f"컬러맵 정규화 범위: [{vmin}, {vmax}]")
    print(f"사용할 컬러맵: {colormap}")

    # 컬러맵 가져오기
    try:
        cmap = cm.get_cmap(colormap)
    except ValueError:
        print(f"경고: '{colormap}' 컬러맵을 찾을 수 없습니다. 'jet'을 사용합니다.")
        cmap = cm.get_cmap('jet')

    # 0-1 범위로 정규화
    normalized = np.zeros_like(work_array)
    if vmax != vmin:
        normalized[non_zero_mask] = (non_zero_values - vmin) / (vmax - vmin)
        normalized = np.clip(normalized, 0, 1)
    else:
        print("경고: vmin과 vmax가 동일합니다. 모든 값을 0.5로 매핑합니다.")
        normalized[non_zero_mask] = 0.5

    # 컬러맵 적용 (RGBA 형식으로 반환됨, 0-1 범위)
    colored = cmap(normalized)

    # 0-255 범위로 변환
    result_array = (colored * 255).astype(np.uint8)

    # 0 값 처리
    if preserve_zero:
        if background_color is None:
            background_color = (0, 0, 0, 255)

        zero_mask = ~non_zero_mask
        result_array[zero_mask] = background_color

    print(f"\n결과 이미지 정보:")
    print(f"  - 크기: {result_array.shape}")
    print(f"  - 모드: RGBA")

    # 결과 저장 (RGBA 모드)
    result_img = Image.fromarray(result_array, mode='RGBA')
    result_img.save(output_path)

    print(f"\n저장 완료: {output_path}")

    return {
        'original_shape': original_shape,
        'original_range': (original_min, original_max),
        'colormap': colormap,
        'vmin': vmin,
        'vmax': vmax,
        'preserve_zero': preserve_zero,
        'background_color': background_color
    }


def list_colormaps():
    """
    사용 가능한 matplotlib 컬러맵 목록을 출력합니다.
    """
    print("사용 가능한 컬러맵 목록:\n")

    # 주요 컬러맵 카테고리
    categories = {
        '순차적 (Sequential)': ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
        '순차적 2 (Sequential 2)': ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                                     'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                                     'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'],
        '발산 (Diverging)': ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
                            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic'],
        '순환 (Cyclic)': ['twilight', 'twilight_shifted', 'hsv'],
        '정성적 (Qualitative)': ['Pastel1', 'Pastel2', 'Paired', 'Accent',
                                 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c'],
        '기타 (Miscellaneous)': ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
                                'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
                                'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
                                'gist_ncar']
    }

    for category, cmaps in categories.items():
        print(f"{category}:")
        for cmap in cmaps:
            print(f"  - {cmap}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='PNG 이미지의 컬러맵 스케일을 재조정하거나 컬러맵을 적용합니다 (0 값 제외)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예제:
  # 선형 스케일링 모드
  # 0을 제외한 값들을 0-255 범위로 재조정
  python recolor_image.py input.png output.png

  # 0을 제외한 값들을 10-200 범위로 재조정
  python recolor_image.py input.png output.png --min 10 --max 200

  # 컬러맵 모드
  # jet 컬러맵 적용 (0 값은 검은색으로 보존)
  python recolor_image.py input.png output.png --colormap jet

  # viridis 컬러맵 적용 (vmin=50, vmax=150)
  python recolor_image.py input.png output.png --colormap viridis --vmin 50 --vmax 150

  # 사용 가능한 컬러맵 목록 보기
  python recolor_image.py --list-colormaps
        '''
    )

    parser.add_argument('input', nargs='?', help='입력 PNG 파일 경로')
    parser.add_argument('output', nargs='?', help='출력 PNG 파일 경로')

    # 컬러맵 관련 옵션
    parser.add_argument('--colormap', type=str, default=None,
                        help='matplotlib 컬러맵 이름 (예: jet, viridis, plasma, inferno)')
    parser.add_argument('--vmin', type=float, default=None,
                        help='컬러맵 적용 시 최소값 (기본값: 0이 아닌 값의 최소값)')
    parser.add_argument('--vmax', type=float, default=None,
                        help='컬러맵 적용 시 최대값 (기본값: 0이 아닌 값의 최대값)')
    parser.add_argument('--list-colormaps', action='store_true',
                        help='사용 가능한 컬러맵 목록 표시')

    # 선형 스케일링 관련 옵션
    parser.add_argument('--min', type=float, default=None,
                        help='새로운 최소값 (선형 스케일링 모드, 기본값: 원본 최소값)')
    parser.add_argument('--max', type=float, default=255.0,
                        help='새로운 최대값 (선형 스케일링 모드, 기본값: 255)')

    # 공통 옵션
    parser.add_argument('--no-preserve-zero', action='store_true',
                        help='0 값도 함께 재조정 (기본값: 0 값 보존)')

    args = parser.parse_args()

    # 컬러맵 목록 표시
    if args.list_colormaps:
        list_colormaps()
        return

    # 입력/출력 파일 확인
    if not args.input or not args.output:
        parser.error("입력 파일과 출력 파일 경로가 필요합니다.")

    try:
        # 컬러맵 모드 vs 선형 스케일링 모드
        if args.colormap:
            # 컬러맵 적용
            apply_colormap(
                args.input,
                args.output,
                colormap=args.colormap,
                preserve_zero=not args.no_preserve_zero,
                vmin=args.vmin,
                vmax=args.vmax
            )
        else:
            # 선형 스케일링
            recolor_image(
                args.input,
                args.output,
                new_min=args.min,
                new_max=args.max,
                preserve_zero=not args.no_preserve_zero
            )
    except FileNotFoundError:
        print(f"오류: 파일을 찾을 수 없습니다 - {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"오류: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
