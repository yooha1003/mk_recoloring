# PNG 이미지 컬러맵 재조정 도구

PNG 이미지에서 검은색(0 값)을 제외하고 나머지 값들의 컬러맵 스케일을 원하는 범위로 재조정하거나, matplotlib 컬러맵을 적용하는 Python 도구입니다.

## 주요 기능

- ✅ 0 값(검은색) 보존 기능
- ✅ **matplotlib 컬러맵 지원** (jet, viridis, plasma, inferno 등 100+ 컬러맵)
- ✅ 사용자 정의 범위로 선형 스케일 재조정
- ✅ 컬러맵 정규화 범위 (vmin/vmax) 사용자 지정 가능
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

이 도구는 두 가지 모드를 지원합니다:
1. **선형 스케일링 모드**: 픽셀 값을 사용자 지정 범위로 선형 변환
2. **컬러맵 모드**: matplotlib 컬러맵을 적용하여 컬러 이미지로 변환

### 1. 명령줄에서 사용

#### 선형 스케일링 모드

```bash
# 기본 사용법 (0 제외, 0-255 범위로 재조정)
python recolor_image.py input.png output.png

# 사용자 지정 범위로 재조정 (0 제외, 10-200 범위)
python recolor_image.py input.png output.png --min 10 --max 200

# 0 값도 함께 재조정
python recolor_image.py input.png output.png --no-preserve-zero
```

#### 컬러맵 모드

```bash
# jet 컬러맵 적용 (0 값은 검은색으로 보존)
python recolor_image.py input.png output.png --colormap jet

# viridis 컬러맵 적용
python recolor_image.py input.png output.png --colormap viridis

# 사용자 지정 범위로 컬러맵 적용 (vmin=50, vmax=150)
python recolor_image.py input.png output.png --colormap plasma --vmin 50 --vmax 150

# 사용 가능한 컬러맵 목록 보기
python recolor_image.py --list-colormaps
```

#### 도움말 보기

```bash
python recolor_image.py --help
```

### 2. Python 모듈로 사용

#### 선형 스케일링

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

#### 컬러맵 적용

```python
from recolor_image import apply_colormap

# jet 컬러맵 적용
result = apply_colormap('input.png', 'output.png', colormap='jet')

# viridis 컬러맵 적용 (사용자 지정 범위)
result = apply_colormap(
    'input.png',
    'output.png',
    colormap='viridis',
    vmin=50,
    vmax=150
)

# 컬러맵 적용 (배경색 지정)
result = apply_colormap(
    'input.png',
    'output.png',
    colormap='plasma',
    preserve_zero=True,
    background_color=(255, 255, 255, 255)  # 흰색 배경
)
```

### 3. 예제 실행

#### 선형 스케일링 예제

샘플 이미지를 생성하고 다양한 재조정 방법을 테스트할 수 있습니다:

```bash
python example_usage.py
```

이 명령은 다음 예제들을 실행합니다:
- 예제 1: 기본 재조정 (0-255 범위)
- 예제 2: 사용자 지정 범위 (20-180)
- 예제 3: 0 값 포함 재조정
- 예제 4: 좁은 범위 재조정 (100-120)

#### 컬러맵 적용 예제

다양한 컬러맵을 테스트할 수 있습니다:

```bash
python example_colormap.py
```

이 명령은 다음 예제들을 실행합니다:
- 예제 1: jet 컬러맵 적용
- 예제 2: viridis 컬러맵 적용
- 예제 3: 사용자 지정 범위로 컬러맵 적용
- 예제 4: 여러 컬러맵 비교 (10개 컬러맵)
- 예제 5: hot 컬러맵 (열화상 이미지 스타일)
- 예제 6: seismic 컬러맵 (발산형)

## 동작 원리

### 선형 변환 (Linear Scaling)

선형 스케일링 모드는 선형 변환을 사용하여 픽셀 값을 재조정합니다:

```
new_value = (old_value - old_min) / (old_max - old_min) * (new_max - new_min) + new_min
```

**예시:**

원본 이미지가 다음과 같은 값을 가진다고 가정:
- 픽셀 값 범위: 0, 50-150
- 0 값: 테두리 영역 (보존 대상)
- 50-150 값: 실제 데이터

`--min 0 --max 255`로 재조정하면:
- 0 값 → 0 (보존됨)
- 50 값 → 0
- 100 값 → 127.5
- 150 값 → 255

### 컬러맵 적용 (Colormap Application)

컬러맵 모드는 matplotlib의 컬러맵을 사용하여 값을 색상으로 매핑합니다:

1. **정규화**: 0이 아닌 값들을 0-1 범위로 정규화
   ```
   normalized = (value - vmin) / (vmax - vmin)
   ```

2. **컬러맵 적용**: 정규화된 값(0-1)을 컬러맵에 매핑하여 RGBA 색상 얻기
   ```
   color = colormap(normalized)  # Returns (R, G, B, A) in 0-1 range
   ```

3. **0 값 보존**: preserve_zero=True인 경우, 0 값은 배경색으로 설정 (기본: 검은색)

**예시:**

원본 이미지가 0, 50-150 값을 가진다고 가정하고, jet 컬러맵을 적용하면:
- 0 값 → 검은색 (보존됨)
- 50 값 → 파란색 (jet의 최소값)
- 100 값 → 녹색/노란색 (jet의 중간값)
- 150 값 → 빨간색 (jet의 최대값)

**인기 있는 컬러맵:**
- **jet**: 고전적인 무지개 컬러맵 (파란색 → 녹색 → 노란색 → 빨간색)
- **viridis**: 인지적으로 균일한 컬러맵 (과학 시각화 권장)
- **plasma**: 밝은 색상의 순차적 컬러맵
- **hot**: 열화상 이미지 스타일 (검은색 → 빨간색 → 노란색 → 흰색)
- **coolwarm**: 발산형 컬러맵 (파란색 ← 흰색 → 빨간색)

## 명령줄 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `input` | 입력 PNG 파일 경로 | (필수) |
| `output` | 출력 PNG 파일 경로 | (필수) |
| `--colormap` | matplotlib 컬러맵 이름 (예: jet, viridis) | None (선형 모드) |
| `--vmin` | 컬러맵 적용 시 최소값 | 0이 아닌 값의 최소값 |
| `--vmax` | 컬러맵 적용 시 최대값 | 0이 아닌 값의 최대값 |
| `--list-colormaps` | 사용 가능한 컬러맵 목록 표시 | - |
| `--min` | 새로운 최소값 (선형 모드) | 원본 최소값 |
| `--max` | 새로운 최대값 (선형 모드) | 255 |
| `--no-preserve-zero` | 0 값도 함께 재조정 | False (0 값 보존) |

## 함수 API

### `recolor_image(input_path, output_path, new_min=None, new_max=None, preserve_zero=True)`

PNG 이미지의 스케일을 선형 변환으로 재조정합니다.

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

### `apply_colormap(input_path, output_path, colormap='jet', preserve_zero=True, vmin=None, vmax=None, background_color=None)`

PNG 이미지에 matplotlib 컬러맵을 적용합니다.

**Parameters:**
- `input_path` (str): 입력 PNG 파일 경로
- `output_path` (str): 출력 PNG 파일 경로
- `colormap` (str, optional): matplotlib 컬러맵 이름 (기본값: 'jet')
- `preserve_zero` (bool, optional): 0 값을 보존할지 여부 (기본값: True)
- `vmin` (float, optional): 컬러맵 적용 시 최소값 (기본값: 0이 아닌 값의 최소값)
- `vmax` (float, optional): 컬러맵 적용 시 최대값 (기본값: 0이 아닌 값의 최대값)
- `background_color` (tuple, optional): 0 값에 적용할 배경색 (R, G, B, A) 0-255 범위 (기본값: 검은색)

**Returns:**
- `dict`: 변환 정보를 포함한 딕셔너리
  - `original_shape`: 원본 이미지 크기
  - `original_range`: 원본 값 범위 (min, max)
  - `colormap`: 사용한 컬러맵 이름
  - `vmin`: 컬러맵 최소값
  - `vmax`: 컬러맵 최대값
  - `preserve_zero`: 0 값 보존 여부
  - `background_color`: 배경색

### `list_colormaps()`

사용 가능한 matplotlib 컬러맵 목록을 출력합니다. 100개 이상의 컬러맵이 카테고리별로 분류되어 표시됩니다.

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

---

## Jet Colormap 스케일 재조정 도구 (고급)

이미 jet colormap이 적용된 PNG 이미지의 스케일을 변경하는 고급 도구입니다. RGB 역매핑 기술을 사용하여 원본 데이터 값을 복원한 후 재조정합니다.

### 사용 사례

**시나리오:**
- 0-0.5 범위 데이터를 jet colormap으로 시각화한 PNG 이미지가 있음
- vmax를 0.5에서 0.2로 변경하여 더 붉게 표현하고 싶음
- 하지만 원본 데이터 파일은 없고 PNG만 있음

### 설치

추가 의존성이 필요합니다:

```bash
pip install numpy Pillow matplotlib scipy
```

### 사용법

#### 명령줄 사용

```bash
# 기본 사용법 (vmax 0.5 → 0.2로 변경, 더 붉게)
python rescale_colormap_correct.py input.png output.png

# 사용자 지정 범위 (vmax 1.0 → 0.3으로 변경)
python rescale_colormap_correct.py input.png output.png --original-max 1.0 --new-max 0.3

# 반대 방향 (vmax 0.2 → 0.5로 변경, 더 파랗게)
python rescale_colormap_correct.py input.png output.png --original-max 0.2 --new-max 0.5

# 도움말
python rescale_colormap_correct.py --help
```

### 동작 원리

1. **RGB 역매핑**:
   - PNG 이미지의 각 RGB 픽셀을 jet colormap lookup table에 매칭
   - KDTree 알고리즘으로 가장 가까운 색상을 찾아 원본 데이터 값(0-1) 복원

2. **스케일 재조정**:
   - 복원된 값에 스케일 팩터 적용: `scale_factor = original_max / new_max`
   - 예: vmax 0.5 → 0.2 변경 시, scale_factor = 2.5
   - 같은 데이터 값이 더 높은 colormap 위치로 매핑됨

3. **재시각화**:
   - 조정된 값에 jet colormap 재적용
   - 1.0 초과 값은 클리핑 (빨간색)

### vmax 변경 효과

#### vmax 줄이기 (더 붉게)

```bash
python rescale_colormap_correct.py input.png output.png --original-max 0.5 --new-max 0.2
```

- **스케일 팩터**: 2.5 (증가)
- **효과**: 같은 값이 더 높은 colormap 위치로 매핑
- **색상 변화**: 파란색 → 녹색, 녹색 → 노란색, 노란색 → 빨간색
- **결과**: 전체적으로 더 붉은 색상 계통

#### vmax 늘리기 (더 파랗게)

```bash
python rescale_colormap_correct.py input.png output.png --original-max 0.2 --new-max 0.5
```

- **스케일 팩터**: 0.4 (감소)
- **효과**: 같은 값이 더 낮은 colormap 위치로 매핑
- **색상 변화**: 빨간색 → 노란색, 노란색 → 녹색, 녹색 → 파란색
- **결과**: 전체적으로 더 파란 색상 계통

### 예제

#### 예제 1: 과학 데이터 시각화 강조

```bash
# 원본: 0-1.0 범위를 전체 colormap으로 표현
# 목표: 낮은 값(0-0.3)만 강조하고 싶음
python rescale_colormap_correct.py data.png data_emphasized.png --original-max 1.0 --new-max 0.3
```

결과: 0.3 이상의 값은 모두 빨간색으로, 0-0.3 범위가 전체 colormap 스펙트럼으로 표현됨

#### 예제 2: 색상 범위 확장

```bash
# 원본: 0-0.2 범위만 사용 (주로 파란색 계통)
# 목표: 색상 범위를 확장하여 더 다양한 색상 표현
python rescale_colormap_correct.py restricted.png expanded.png --original-max 0.2 --new-max 0.5
```

결과: 전체 색상 스펙트럼이 더 넓게 분포

### 기술적 세부사항

#### 역매핑 정확도

- **Colormap 해상도**: 512 색상 (기본값)
- **매칭 방식**: KDTree를 사용한 최근접 이웃 탐색
- **평균 오차**: 일반적으로 RGB 유클리드 거리 4-5 이하

#### 제한사항

1. **Jet colormap 전용**: 현재 jet colormap에만 최적화됨
2. **PNG 압축 손실**: JPEG 등 손실 압축 포맷은 정확도 저하 가능
3. **배경 처리**: 검은색 배경(RGB < 10)은 자동으로 보존됨

### Python 모듈로 사용

```python
from rescale_colormap_correct import rescale_colormap_image

# vmax 0.5 → 0.2로 변경
rescale_colormap_image(
    'input.png',
    'output.png',
    original_max=0.5,
    new_max=0.2
)
```

### 문제 해결

**Q: 변환 후 색상이 예상과 다릅니다.**

A: 원본 이미지가 정확히 jet colormap으로 생성되었는지 확인하세요. 다른 colormap이나 사용자 정의 colormap을 사용한 경우 정확도가 떨어질 수 있습니다.

**Q: 배경이 잘못 처리됩니다.**

A: 배경 임계값(현재 RGB < 10)이 데이터와 맞지 않을 수 있습니다. 코드를 수정하여 임계값을 조정하세요.

**Q: 원본 데이터 파일이 있는데도 이 도구를 사용해야 하나요?**

A: 아니요. 원본 데이터가 있다면 `recolor_image.py`의 `apply_colormap()` 함수를 사용하여 직접 vmin/vmax를 지정하는 것이 더 정확합니다.
