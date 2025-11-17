#!/usr/bin/env python3
"""
컬러맵 적용 예제

matplotlib 컬러맵을 사용하여 PNG 이미지를 다양한 색상으로 변환하는 예제입니다.
"""

from recolor_image import apply_colormap
import numpy as np
from PIL import Image
import os


def create_sample_image(filename='sample_colormap_input.png'):
    """
    테스트용 샘플 이미지를 생성합니다.
    - 일부 픽셀은 0 (검은색)
    - 나머지는 50-200 범위의 값
    """
    # 200x200 크기의 이미지 생성
    width, height = 200, 200
    img_array = np.zeros((height, width), dtype=np.uint8)

    # 방사형 그라디언트 생성
    center_x, center_y = width // 2, height // 2
    max_distance = np.sqrt(center_x**2 + center_y**2)

    for i in range(height):
        for j in range(width):
            distance = np.sqrt((i - center_y)**2 + (j - center_x)**2)
            if distance < max_distance * 0.8:  # 중심에서 80% 반경 내부에만 값 할당
                # 거리에 따른 그라디언트 (중심이 밝고 가장자리로 갈수록 어두움)
                normalized_distance = distance / (max_distance * 0.8)
                img_array[i, j] = int(200 - normalized_distance * 150) + 50

    # 이미지 저장
    img = Image.fromarray(img_array, mode='L')
    img.save(filename)
    print(f"샘플 이미지 생성 완료: {filename}")
    print(f"  - 크기: {img_array.shape}")
    print(f"  - 값 범위: [{img_array.min()}, {img_array.max()}]")
    non_zero = img_array[img_array > 0]
    if len(non_zero) > 0:
        print(f"  - 0이 아닌 값 범위: [{non_zero.min()}, {non_zero.max()}]")
    return filename


def example1_jet_colormap():
    """
    예제 1: jet 컬러맵 적용
    고전적인 무지개 컬러맵
    """
    print("\n" + "="*60)
    print("예제 1: jet 컬러맵 적용")
    print("="*60)

    input_file = create_sample_image('colormap_example1_input.png')
    output_file = 'colormap_example1_jet_output.png'

    result = apply_colormap(
        input_file,
        output_file,
        colormap='jet',
        preserve_zero=True
    )

    if result:
        print(f"\n✓ jet 컬러맵이 성공적으로 적용되었습니다!")


def example2_viridis_colormap():
    """
    예제 2: viridis 컬러맵 적용
    인지적으로 균일한 컬러맵 (과학 시각화에 권장)
    """
    print("\n" + "="*60)
    print("예제 2: viridis 컬러맵 적용")
    print("="*60)

    input_file = create_sample_image('colormap_example2_input.png')
    output_file = 'colormap_example2_viridis_output.png'

    result = apply_colormap(
        input_file,
        output_file,
        colormap='viridis',
        preserve_zero=True
    )

    if result:
        print(f"\n✓ viridis 컬러맵이 성공적으로 적용되었습니다!")


def example3_custom_range():
    """
    예제 3: 사용자 지정 범위로 컬러맵 적용
    vmin, vmax를 지정하여 특정 범위만 강조
    """
    print("\n" + "="*60)
    print("예제 3: 사용자 지정 범위로 컬러맵 적용 (plasma, vmin=100, vmax=180)")
    print("="*60)

    input_file = create_sample_image('colormap_example3_input.png')
    output_file = 'colormap_example3_plasma_custom_output.png'

    result = apply_colormap(
        input_file,
        output_file,
        colormap='plasma',
        vmin=100,
        vmax=180,
        preserve_zero=True
    )

    if result:
        print(f"\n✓ 사용자 지정 범위로 컬러맵이 적용되었습니다!")


def example4_multiple_colormaps():
    """
    예제 4: 여러 컬러맵 비교
    하나의 입력 이미지에 다양한 컬러맵을 적용
    """
    print("\n" + "="*60)
    print("예제 4: 여러 컬러맵 비교")
    print("="*60)

    input_file = create_sample_image('colormap_example4_input.png')

    # 다양한 컬러맵 적용
    colormaps = ['jet', 'viridis', 'plasma', 'inferno', 'magma',
                 'hot', 'cool', 'rainbow', 'turbo', 'coolwarm']

    print(f"\n{len(colormaps)}개의 컬러맵을 적용합니다...\n")

    for cmap in colormaps:
        output_file = f'colormap_example4_{cmap}_output.png'
        print(f"  - {cmap} 적용 중...")
        try:
            apply_colormap(
                input_file,
                output_file,
                colormap=cmap,
                preserve_zero=True
            )
        except Exception as e:
            print(f"    오류: {e}")

    print(f"\n✓ 모든 컬러맵이 적용되었습니다!")


def example5_hot_colormap():
    """
    예제 5: hot 컬러맵 (열화상 이미지 스타일)
    """
    print("\n" + "="*60)
    print("예제 5: hot 컬러맵 적용 (열화상 이미지 스타일)")
    print("="*60)

    input_file = create_sample_image('colormap_example5_input.png')
    output_file = 'colormap_example5_hot_output.png'

    result = apply_colormap(
        input_file,
        output_file,
        colormap='hot',
        preserve_zero=True
    )

    if result:
        print(f"\n✓ hot 컬러맵이 성공적으로 적용되었습니다!")


def example6_seismic_colormap():
    """
    예제 6: seismic 컬러맵 (발산형 - 양/음 값 구분에 유용)
    """
    print("\n" + "="*60)
    print("예제 6: seismic 컬러맵 적용 (발산형)")
    print("="*60)

    input_file = create_sample_image('colormap_example6_input.png')
    output_file = 'colormap_example6_seismic_output.png'

    result = apply_colormap(
        input_file,
        output_file,
        colormap='seismic',
        preserve_zero=True
    )

    if result:
        print(f"\n✓ seismic 컬러맵이 성공적으로 적용되었습니다!")


def main():
    print("="*60)
    print("PNG 이미지 컬러맵 적용 예제")
    print("="*60)

    # 모든 예제 실행
    example1_jet_colormap()
    example2_viridis_colormap()
    example3_custom_range()
    example4_multiple_colormaps()
    example5_hot_colormap()
    example6_seismic_colormap()

    print("\n" + "="*60)
    print("모든 예제가 완료되었습니다!")
    print("="*60)

    # 생성된 파일 목록
    print("\n생성된 파일들:")
    for file in sorted(os.listdir('.')):
        if file.startswith('colormap_example') and file.endswith('.png'):
            print(f"  - {file}")


if __name__ == '__main__':
    main()
