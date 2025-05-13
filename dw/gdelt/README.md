### POC
- 매니패스트가 15분 간격마다 업데이트 되는데 15분째에 칼같이 다운로드 하면 체크섬이 다를 수 있음.
- 중간에 size, hash, url 형식이 아닌 url만 있는 라인이 있는데 무시해도 됨 (스크립트에 걸러내는 로직 추가)
### Usage
- 메니페스트 다운
```bash
curl -L -C - -O --compressed http://data.gdeltproject.org/gdeltv2/masterfilelist.txt
```
- get_dat.py 실행: pd로 각 csv에서 3줄만 추출함
- 그 후는 test.ipynb 참고