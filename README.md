# PNG 이미지 컬러맵 재조정 도구

PNG 이미지에서 검은색(0 값)을 제외하고 나머지 값들의 컬러맵 스케일을 원하는 범위로 재조정하는 Python 도구입니다.

## 주요 기능

- ✅ 0 값(검은색) 보존 기능
- ✅ 사용자 정의 범위로 스케일 재조정
- ✅ 그레이스케일 및 컬러 이미지 지원
- ✅ 8-bit, 16-bit 이미지 지원
- ✅ 명령줄 인터페이스 제공
- ✅ Python 모듈로 import 가능

## 설치

### 요구사항

- Python 3.7 이상
- pip

### 의존성 설치

```bash
pip install -r requirements.txt
```

또는 개별 설치:

```bash
pip install numpy Pillow matplotlib
```

## 사용법

### 1. 명령줄에서 사용

#### 기본 사용법 (0 제외, 0-255 범위로 재조정)

```bash
python recolor_image.py input.png output.png
```

#### 사용자 지정 범위로 재조정

```bash
# 0을 제외한 값들을 10-200 범위로 재조정
python recolor_image.py input.png output.png --min 10 --max 200
```

#### 0 값도 함께 재조정

```bash
python recolor_image.py input.png output.png --no-preserve-zero
```

#### 도움말 보기

```bash
python recolor_image.py --help
```

### 2. Python 모듈로 사용

```python
from recolor_image import recolor_image

# 기본 사용
result = recolor_image('input.png', 'output.png')

# 사용자 지정 범위
result = recolor_image(
    'input.png',
    'output.png',
    new_min=20,
    new_max=180
)

# 0 값도 함께 재조정
result = recolor_image(
    'input.png',
    'output.png',
    preserve_zero=False
)
```

### 3. 예제 실행

샘플 이미지를 생성하고 다양한 재조정 방법을 테스트할 수 있습니다:

```bash
python example_usage.py
```

이 명령은 다음 예제들을 실행합니다:
- 예제 1: 기본 재조정 (0-255 범위)
- 예제 2: 사용자 지정 범위 (20-180)
- 예제 3: 0 값 포함 재조정
- 예제 4: 좁은 범위 재조정 (100-120)

## 동작 원리

### 선형 변환

이 도구는 선형 변환을 사용하여 픽셀 값을 재조정합니다:

```
new_value = (old_value - old_min) / (old_max - old_min) * (new_max - new_min) + new_min
```

### 예시

원본 이미지가 다음과 같은 값을 가진다고 가정:
- 픽셀 값 범위: 0, 50-150
- 0 값: 테두리 영역 (보존 대상)
- 50-150 값: 실제 데이터

`--min 0 --max 255`로 재조정하면:
- 0 값 → 0 (보존됨)
- 50 값 → 0
- 100 값 → 127.5
- 150 값 → 255

## 명령줄 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `input` | 입력 PNG 파일 경로 | (필수) |
| `output` | 출력 PNG 파일 경로 | (필수) |
| `--min` | 새로운 최소값 | 원본 최소값 |
| `--max` | 새로운 최대값 | 255 |
| `--no-preserve-zero` | 0 값도 함께 재조정 | False (0 값 보존) |

## 함수 API

### `recolor_image(input_path, output_path, new_min=None, new_max=None, preserve_zero=True)`

PNG 이미지의 컬러맵 스케일을 재조정합니다.

**Parameters:**
- `input_path` (str): 입력 PNG 파일 경로
- `output_path` (str): 출력 PNG 파일 경로
- `new_min` (float, optional): 새로운 최소값 (기본값: 원본의 최소값)
- `new_max` (float, optional): 새로운 최대값 (기본값: 255)
- `preserve_zero` (bool, optional): 0 값을 보존할지 여부 (기본값: True)

**Returns:**
- `dict`: 변환 정보를 포함한 딕셔너리
  - `original_shape`: 원본 이미지 크기
  - `original_range`: 원본 값 범위 (min, max)
  - `new_range`: 새로운 값 범위 (min, max)
  - `preserve_zero`: 0 값 보존 여부

## 사용 사례

### 의료 영상 처리
배경(0 값)을 유지하면서 조직의 밝기를 조정할 때 유용합니다.

### 과학 데이터 시각화
특정 범위의 데이터만 강조하고 싶을 때 사용합니다.

### 이미지 정규화
머신러닝 입력을 위해 특정 범위로 정규화할 때 활용합니다.

## 라이선스

MIT License

## 기여

버그 리포트나 기능 제안은 GitHub Issues를 통해 제출해 주세요.
