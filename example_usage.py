#!/usr/bin/env python3
"""
recolor_image.py 사용 예제

이 스크립트는 recolor_image 모듈의 다양한 사용법을 보여줍니다.
"""

from recolor_image import recolor_image
import numpy as np
from PIL import Image
import os


def create_sample_image(filename='sample_input.png'):
    """
    테스트용 샘플 이미지를 생성합니다.
    - 일부 픽셀은 0 (검은색)
    - 나머지는 50-150 범위의 값
    """
    # 100x100 크기의 이미지 생성
    width, height = 100, 100
    img_array = np.zeros((height, width), dtype=np.uint8)

    # 그라디언트 패턴 생성 (50-150 범위)
    for i in range(height):
        for j in range(width):
            if i > 20 and i < 80 and j > 20 and j < 80:
                # 중앙 영역에만 값 할당
                img_array[i, j] = int(50 + (i + j) / (height + width) * 100)

    # 일부 영역을 0으로 설정 (검은색 테두리)
    img_array[0:20, :] = 0
    img_array[80:100, :] = 0
    img_array[:, 0:20] = 0
    img_array[:, 80:100] = 0

    # 이미지 저장
    img = Image.fromarray(img_array, mode='L')
    img.save(filename)
    print(f"샘플 이미지 생성 완료: {filename}")
    print(f"  - 크기: {img_array.shape}")
    print(f"  - 값 범위: [{img_array.min()}, {img_array.max()}]")
    print(f"  - 0이 아닌 값 범위: [{img_array[img_array > 0].min()}, {img_array[img_array > 0].max()}]")
    return filename


def example1_basic_rescaling():
    """
    예제 1: 기본 재조정
    0을 제외한 값들을 0-255 범위로 재조정
    """
    print("\n" + "="*60)
    print("예제 1: 기본 재조정 (0 제외, 0-255 범위)")
    print("="*60)

    input_file = create_sample_image('example1_input.png')
    output_file = 'example1_output.png'

    result = recolor_image(input_file, output_file)

    if result:
        print(f"\n✓ 성공적으로 재조정되었습니다!")


def example2_custom_range():
    """
    예제 2: 사용자 지정 범위로 재조정
    0을 제외한 값들을 20-180 범위로 재조정
    """
    print("\n" + "="*60)
    print("예제 2: 사용자 지정 범위 (0 제외, 20-180 범위)")
    print("="*60)

    input_file = create_sample_image('example2_input.png')
    output_file = 'example2_output.png'

    result = recolor_image(
        input_file,
        output_file,
        new_min=20,
        new_max=180
    )

    if result:
        print(f"\n✓ 성공적으로 재조정되었습니다!")


def example3_with_zero():
    """
    예제 3: 0 값도 함께 재조정
    모든 값을 0-255 범위로 재조정
    """
    print("\n" + "="*60)
    print("예제 3: 0 값 포함 재조정 (0-255 범위)")
    print("="*60)

    input_file = create_sample_image('example3_input.png')
    output_file = 'example3_output.png'

    result = recolor_image(
        input_file,
        output_file,
        new_min=0,
        new_max=255,
        preserve_zero=False
    )

    if result:
        print(f"\n✓ 성공적으로 재조정되었습니다!")


def example4_narrow_range():
    """
    예제 4: 좁은 범위로 재조정
    0을 제외한 값들을 100-120 범위로 재조정 (어두운 이미지)
    """
    print("\n" + "="*60)
    print("예제 4: 좁은 범위 재조정 (0 제외, 100-120 범위)")
    print("="*60)

    input_file = create_sample_image('example4_input.png')
    output_file = 'example4_output.png'

    result = recolor_image(
        input_file,
        output_file,
        new_min=100,
        new_max=120
    )

    if result:
        print(f"\n✓ 성공적으로 재조정되었습니다!")


def main():
    print("PNG 이미지 컬러맵 재조정 예제")
    print("="*60)

    # 모든 예제 실행
    example1_basic_rescaling()
    example2_custom_range()
    example3_with_zero()
    example4_narrow_range()

    print("\n" + "="*60)
    print("모든 예제가 완료되었습니다!")
    print("="*60)
    print("\n생성된 파일들:")
    for i in range(1, 5):
        input_file = f'example{i}_input.png'
        output_file = f'example{i}_output.png'
        if os.path.exists(input_file):
            print(f"  - {input_file}")
        if os.path.exists(output_file):
            print(f"  - {output_file}")


if __name__ == '__main__':
    main()
