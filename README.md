1. 가상환경 생성 python -m venv myvenv
2. 가상환경 구동 source myvenv/Scripts/activate
3. 가상환경 위에 장고 설치하기 pip install django
4. 장고 설치 확인하기 pip list -> 확인
5. 실행하기 python manage.py runserver
* Pillow 설치하라고 할 경우 안내문에 따라 설치하기

배포 링크 : 'harin.pythonanywhere.com'
settings.py 설정
ALLOWED_HOSTS = ['harin0802.pythonanywhere.com']
