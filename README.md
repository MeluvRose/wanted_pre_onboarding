# wanted_pre_onboarding_Backend

### 과제 설명
* 아래 서비스 개요 및 요구사항을 만족하는 Backend 시스템을 구현합니다.
* Django 또는 Flask 를 사용하여 구현합니다.

### 서비스 개요
* 본 서비스는 크라우드 펀딩 기능을 제공합니다. 게시자는 크라우드 펀딩을 받기위한 상품(=게시물)을 등록합니다.
* 유저는 해당 게시물의 펀딩하기 버튼을 클릭하여 해당 상품 ‘1회펀딩금액’ 만큼 펀딩합니다.

위 서비스에 맞는 Backend 시스템을 구현하기 위해 'Django'와 RDB인 'MySQL'을 사용했으며, 시스템을 위한 DB명은 'funding',
그리고 테이블 명은 'goods'로 하여 다음과 같이 생성하였다.
``` 
CREATE TABLE funding.goods
(
  id INT UNSIGNED NOT NULL,
  title VARCHAR(255),
  publisher VARCHAR(30),
  detail VARCHAR(255),
  goal INT UNSIGNED NOT NULL,
  date_limit DATE,
  price_per_time INT,
  pregress_rate INT,
  PRIMARY KEY(id)
);
```
**그리고, 각 컬럼이 지니는 의미는 다음과 같다.**
- id : 테이블에서 각 튜플을 구분하기 위한 기본키
- title : 게시글의 제목
- publisher : 펀딩을 열고자 하는 주체
- detail : 게시글의 상세 내용
- goal : 목표 금액
- date_limit : 펀딩 종료일
- price_per_time : (회당) 펀딩 가능 금액
- progress_rate : 펀딩 횟수
  - 원래는 펀딩 진행률을 저장하고 싶었지만, 이보단 펀딩이 이뤄진 횟수를 저장하는 게 시스템 상으로 알맞다고 판단
  - 컬럼 명을 의미에 맞게 변경했어야 한다고 생각
 

### 요구 사항 및 구현
테이블 'goods'에 대한 모델 'Goods'를 생성하고 다음과 같이 활용했다.

* 상품을 등록합니다.

```python
from .models import Goods

  def create(request):
    posts = Goods.objects.all() # DB내 모든 데이터를 조회
    if request.method == 'POST':
      title = request.POST['title']
      publisher = request.POST['publisher']
      next_id = 0

      # DB내 새로운 데이터가 가질 수 있는 기본 키 값 탐색
      for post in posts:
        if next_id == post.id:
          next_id = next_id + 1

      goods = Goods(id = next_id, title = title, publisher = publisher) # 새로운 데이터를 저장한 객체를 생성
      goods.save() # 현재 객체 상태를 저장, 모델을 통해 DB에 반영
```
* 상품을 수정합니다.
```python
from .models import Goods
    
  def update(request, pk):
    posts = Goods.objects.get(id=pk) # 수정하고자 하는 튜플의 기본키(id)값을 파라미터(pk)로 전달 받아 조회

    if request.method == 'POST':
      title = request.POST['title']
      publisher = request.POST['publisher']
      goods.save() # 현재 객체 상태를 저장, 모델을 통해 DB에 반영
```
* 상품을 삭제합니다.
```python
from .models import Goods
    
  def delete(request):
    if request.method == 'POST': # 삭제 행위는 'POST'방식의 요청이 발생할 때만
      pk = int(request.POST['id'])
      goods = Goods.objects.get(id=pk)
      goods.delete() # 조건에 맞는 객체를 모델에서 제거, 또한 DB에 반영
      return redirect('/')
```
* 상품 목록을 가져옵니다.
```python
from .models import Goods
    
  def post_goods(request):
    posts = Goods.objects.all()
    search = request.GET.get('search') # 검색하려는 단어
    order = request.GET.get('order') # 정렬 기준(column)
    
    # 검색에 사용하고자 하는 단어가 있을 때,
    if search != None and search != '':
        posts = posts.filter(title__contains=search)
    # 목록을 정렬하고자 하는 기준이 있을 때,
    if order != None and order != '':
        posts = posts.order_by(order)
```
* 상품 상세 페이지를 가져옵니다.
```python
from .models import Goods
    
def read(request, pk):
    posts = Goods.objects.get(id=pk) # 상세 내용을 보고자 하는 데이터의 튜플을 조회
    if request.method == "GET":
        rate = (posts.progress_rate / posts.goal) * 100 # 펀딩 받은 횟수와 목표 금액을 통해, 현재 펀딩 진행률을 계산
    else:
        posts.progress_rate = posts.progress_rate + 1 # 'POST' 형식의 펀딩 요청이 발생한다면, 현재 펀딩 받은 횟수에 추가
        posts.save() # 객체 상태 저장 및 DB에 전달
```

### 필수 기술요건
- [X] Django ORM or SQLAlchemy 등 ORM을 사용하여 구현. 
- [ ] REST API 로 구현(Json response).
- [X] RDBMS 사용 (SQLite, PostgreSQL 등).
- [ ] Backend 이외의 요소 개발 하지 않음(html, css, js 등)
  - 개발 범위에 제외된다는 의미이며, 구현시에 불이익은 없습니다. 다만, 평가에
  이점 또한 없습니다.
