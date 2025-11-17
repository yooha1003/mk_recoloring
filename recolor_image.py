#!/usr/bin/env python3
"""
PNG 이미지의 컬러맵 스케일 재조정 도구

검은색(0 값)을 제외하고 나머지 값들의 스케일을 사용자가 원하는 범위로 재조정합니다.
"""

import numpy as np
from PIL import Image
import argparse
import sys


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


def main():
    parser = argparse.ArgumentParser(
        description='PNG 이미지의 컬러맵 스케일을 재조정합니다 (0 값 제외)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
예제:
  # 0을 제외한 값들을 0-255 범위로 재조정
  python recolor_image.py input.png output.png

  # 0을 제외한 값들을 10-200 범위로 재조정
  python recolor_image.py input.png output.png --min 10 --max 200

  # 0 값도 함께 재조정
  python recolor_image.py input.png output.png --no-preserve-zero
        '''
    )

    parser.add_argument('input', help='입력 PNG 파일 경로')
    parser.add_argument('output', help='출력 PNG 파일 경로')
    parser.add_argument('--min', type=float, default=None,
                        help='새로운 최소값 (기본값: 원본 최소값)')
    parser.add_argument('--max', type=float, default=255.0,
                        help='새로운 최대값 (기본값: 255)')
    parser.add_argument('--no-preserve-zero', action='store_true',
                        help='0 값도 함께 재조정 (기본값: 0 값 보존)')

    args = parser.parse_args()

    try:
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
