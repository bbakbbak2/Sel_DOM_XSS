# Sel_DOM_XSS
스크립트 난독화로 인해 DOM XSS의 시작점이 되는 Source를 찾을 수 없을 때, 
DOM XSS 취약점을 검출하기 위해 활용할 수 있는 소스입니다.

# 작동원리
1. 가상 익스플로어 실행 
2. 텍스트 파일에 저장된 URL 목록을 가져옴
3. URL 뒤에 #(hash태그)와 함께 페이로드 자동 입력
4. 페이로드가 실행될 경우 취약으로 판정됨

# 설치(파이썬3)
```
git clone https://github.com/bbakbbak2/Sel_DOM_XSS.git
pip install selenium 
```

# 준비사항
- 모든 영역 탭에서 보호모드 설정을 체크해야합니다. (인터넷, 로컬인트라넷, 신뢰사이트, 제한사이트)
- 가상드라이버로 Explore를 사용할 경우, XSS 필터 기능을 해제시켜줍니다.
 
# 익스플로어 드라이버 버그
- 익스플로어 드라이버 버그가 존재(get매소드 요청시 에러)합니다. 
- 레지스트리 값을 등록해야합니다. 아래와 같은 설정 값을 넣어주세요.

```
For IE 11 only, you will need to set a registry entry on the target computer 
so that the driver can maintain a connection to the instance of Internet Explorer it creates. 
For 32-bit Windows installations,  the key you must examine in the registry editor is HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE . 
For 64-bit Windows installations, the key is HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Internet Explorer\Main\FeatureControl\FEATURE_BFCACHE . 
Please note that the  FEATURE_BFCACHE  subkey may or may not be present, and should be created if it is not present. 
Important: Inside this key, create a DWORD value named  iexplore.exe  with the value of 0.
```
