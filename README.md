# YOLO 기반 사람 추적 자동차 프로젝트

## 프로젝트 개요
이 프로젝트는 YOLO(You Only Look Once) 알고리즘을 사용하여 사람을 추적하고, 초음파 센서를 통해 일정 거리를 유지하며 따라다니는 자동차 시스템을 설계하는 것입니다. 이 시스템은 Raspberry Pi 플랫폼에서 구현됩니다.

## 주요 구성 요소
- **YOLO**: 객체 탐지 알고리즘
- **PID 제어 알고리즘**: 자동차의 움직임을 제어
- **초음파 센서**: 거리 측정 및 유지
- **Raspberry Pi**: 시스템의 중심 제어 장치

## 담당 업무
### 1. 하드웨어 구현
- **부품 선정**
  - Raspberry Pi
  - 카메라 모듈
  - 초음파 센서 (HC-SR04)
  - DC 모터 및 드라이버
  - 배터리 및 전원 공급 장치

- **하드웨어 연결**
  - Raspberry Pi와 카메라 모듈 연결
  - 초음파 센서 연결
  - 모터 드라이버 연결

### 2. 전체 시스템 설계 및 구현
- **소프트웨어 개발**
  - YOLO 모델 설정 및 객체 탐지
  - 거리 측정 및 PID 제어 로직 구현
  - Raspberry Pi에서 모든 센서와 모터 제어

- **시스템 통합**
  - 하드웨어와 소프트웨어 통합 테스트
  - 성능 최적화 및 문제 해결

## 구현 단계
1. **하드웨어 세팅**
   - Raspberry Pi와 모든 부품 조립
   - 각 센서 기능 확인

2. **소프트웨어 개발**
   - YOLO 모델을 Raspberry Pi에 설치
   - 초음파 센서를 통한 거리 측정 코드 작성
   - PID 제어 알고리즘 구현

3. **테스트 및 조정**
   - 거리 유지 및 추적 정확도 테스트
   - PID 파라미터 조정

4. **결과 분석**
   - 추적 성능 및 시스템 안정성 평가

## 필요 기술 및 도구
- **Python**: 코드 개발
- **OpenCV**: 이미지 처리
- **TensorFlow 또는 PyTorch**: YOLO 모델 사용
- **Raspberry Pi**: 하드웨어 제어
## 예시 
<div style='position: relative; width: 100%; height: 0; padding-top: 56.25%; overflow: hidden; will-change: transform;'>
            <iframe loading='lazy' style='position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0; margin: 0;' src='https:&#x2F;&#x2F;www.miricanvas.com&#x2F;v&#x2F;12jpxch?embed'>
            </iframe>
</div>

## 결론
이 프로젝트는 YOLO와 PID 제어 알고리즘을 활용하여 효율적인 사람 추적 자동차를 만드는 것을 목표로 하며, 하드웨어 및 소프트웨어 통합 능력을 향상시키는 좋은 기회가 될 것입니다.
