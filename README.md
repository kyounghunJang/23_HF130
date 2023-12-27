# [HF130]Data Fabric
- 프로젝트 KPT회고 링크: https://codingjang.tistory.com/76
- 시연 연상 링크: https://youtu.be/QGhyUMb3KrA
---
## 프로젝트 소개 
- 데이터 패브릭 구조는 데이터를 직접적으로 통합하는 것이 아니라 메타데이터 활성화를 통해 분산된 데이터를 연결하는 방식
- 데이터 패브릭 구조를 활용하여 데이터를 통합하는 방식은 빠른 데이터 액세스를 제공
- 사용하는 데이터양이 증가하면서 복잡해지고 있기 때문에 이를 데이터 사이 취사선택에 어려움이 증가
- 데이터 간 상관관계를 파악한다면 데이터 사용자는 자신이 필요한 데이터를 선택하는 상황에서 도움이 됨  
- 따라서 다양한 데이터에서 메타데이터를 추출해 데이터 사이의 상관관계를  분석해서 사용자의 빠른 데이터 선택과 처리를 도와주는 프로젝트를 기획하게 되었음
- 이 프로젝트에서는 공공데이터의 메타데이터를 추출하여 상관관계를 분석하고 점수를 보여주는 포털을 만드는것이 목표

## 적용기술 및 아키텍처
- 메타데이터 추출 및 적재: AWS Glue를 이용하여 정형, 반정형, 비정형 데이터의 메타데이터를 추출 및 DB에 적재
- GPT API : 키워드를 입력받았을 때 추출된 메타데이터와의 유사한 단어 10개를 입력받는다
- Flask: 사용자들이 데이터를 검색 및 다운로드 경로를 찾을 수 있도록 도와주는 웹 서비스
- 메타데이터 추출 자동화: AWS Glue workflow를 사용하여 새롭게 추가된 데이터의 메타데이터를 매일 특정 시간에 업데이트 

### 아키텍처
![아키텍처 이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbpX50M%2FbtsCEJnlLz4%2FfIDTz0EXfKuawx5EBNjo90%2Fimg.png)

## 수행일정 
![수행일정 이미지](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FMdz2w%2FbtsCN1mrUf2%2FficjVWAYRpfhCS3FtBEBYk%2Fimg.png)

