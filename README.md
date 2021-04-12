Numpy

- https://aruie.github.io/2019/06/19/numpy.html

### 생성 함수

- array(), arange(), zeros(), full(), eye()

- 크기 ndarray.size()

- ```python
  #array (파이썬 리스트를 ndarray로 변환)
  > li = [1,2,3,4,5,6]
  > arr = np.array(li)     # ndarray로 변환
  > display(arr)
  array([1, 2, 3, 4, 5, 6])
  
  # 파이썬의 range 같은 것(ndarray 객체 생성)
  > np.arange(1,7)  
  array([1, 2, 3, 4, 5, 6])
  
  # zeros 0으로 초기화
  > np.zeros((2,3))
  array([[0., 0.],
         [0., 0.],
         [0., 0.]])
  
  # full 0말고 다른 숫자 넣기 가능
  > np.full((2,3), 55)  
  array([[55, 55, 55],
         [55, 55, 55]])
  
  # 단위행렬(주대각성분이 1이고 나머진 0) 생성
  > np.eye(2)   
  array([[1., 0.],
          0., 1.]
  ```

### 인덱싱

- ```python
  ## 1차원
  arr1 = np.arange(10)
  
  # 0번째
  arr1[0]
  # 3~8번째
  arr1[3:9]
  # 전부
  arr1[:]
  
  ## 2차원
  arr2 = np.array([1,2,3,4],[5,6,7,8],[9,10,11,12])
  
  ## 2행 3열
  arr2[2,3]
  # 2행 모든 요소
  arr2[2,:]
  
  
  ```

#### Array boolean 인덱싱(마스크) : 원하는 행, 열 값만 뽑아내기

- ```python
  names = np.array(['Beomwoo','Beomwoo','Kim','Joan','Lee','Beomwoo','Park','Beomwoo'])
  data = np.random.randn(8,4)
  
  # names 가 Beomwoo인 해으이 data 만 보고 싶을 때
  names_Beomwoo_mask = (names == 'Beomwoo')
  data[names_Beomwoo_mask,:]
  
  # 요소가 Kim인 행의 데이터만 꺼내기
  data[names == 'Kim',:]
  
  # 논리 연산을 응용하여, 요소가 Kim 또는 Park인 행의 데이터만 꺼내기
  data[(names == 'Kim') | (names == 'Park'),:]
  
  #data의 자체 마스크 이용
  data[:,0] < 0
  # -> array([ True, False, True, False, False, False, True, False]) 반환함
  # 응용해서
  # 위에서 만든 마스크를 이용하여 0번째 열의 값이 0보다 작은 행을 구한다.
  data[data[:,0]<0,:]
  # array([[-1.07099572, -0.85382063, -1.42474621, -0.05992846], [-0.22633642, -0.76385264, 0.16368804, 0.91204438], [-0.05673648, -1.63408607, -2.29844338, -0.3662913 ]])
  
  # 0번째 열의 값이 0보다 작은 행의 2,3번째 열 값
  data[data[:,0]<0,2:4]
  # array([[-1.42474621, -0.05992846], [ 0.16368804, 0.91204438], [-2.29844338, -0.3662913 ]])
  
  ```



### 연산 함수

- 해당 원소끼리 전부 연산 가능, 행이나 열에 따라서 연산하고 싶으면 axis 변수 사용
- 사칙연산 (함수 안써도 +,-,*,/ 제곱 가능함 그리고 스칼라 값으로도 가능함)
  - np.add(), np.subtract(), np.multiply(), np.divide()
- 내적
  - np.dot()
- 반환
  - 원소 합 : np.sum() , 원소 곱 : np.prod()
  - 최소 : np.min(), 최대 : np.max()
  - 최소 위치 : np.argmin(), 최대 위치 : np.argmax()

### 형상

- ndarray.shape : ndarray 차원 반환, 함수 아님

  ```python
  > data = np.arange(1,7)
  > data.shape
  (6,)
  ```

- np.reshape() : 행렬 차원 바꿈

  ```python
  > data = np.arange(1,7)
  > data.reshape((2,3))   # 2,3 행렬로 변경
  > # np.reshape(data, (2,3))   이렇게도 가능 
  array([[1, 2, 3],
         [4, 5, 6]])
  
  > data.reshape(-1)      # 쭉 필때
  array([1, 2, 3, 4, 5, 6])
  
  > data.reshape((3,-1))    # 3행으로(열은 알아서)
  array([[1, 2],
         [3, 4],
         [5, 6]])
  ```

- np.transpose() : 행렬의 전치 행렬

  ```python
  > data = np.arange(1,7)
  > data = data.reshape((2,3,1))
  > print(data.shape)
  > data = data.transpose((0,2,1)) # 두번째와 세번째의 순서 변경
  > print(data.shape)
  (2, 3, 1)
  (2, 1, 3)
  ```

### I/O

#### savetxt

- numpy.savetxt( filename, X, fmt='%.18e', delimiter=' ',  newline='n', header='', footer='', comment='#', encoding=None)

- 간단히는
  numpy.savetxt({파일이름}, {데이터}, fmt={데이터 형식}, delimiter={데이터간 구분자})

  ```python
  import numpy as np
  import random
  
  # 파일로 저장하기 위한 배열을 생성합니다.
  numbers = np.zeros((10,4))
  for i in range(10):
      for j in range(4):
          numbers[i][j] = random.randint(1000,40000)
  np.savetxt("save.txt", numbers, fmt='%d', delimiter=',')
  ```

#### 입력

- https://jfun.tistory.com/58
  파일 오픈해서 리스트로 변환 후, ndarray 로 변환하는 방법도 있음

##### loadtxt

- https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html

- numpy.loadtxt(fname, dtype=<class 'float', comments='#', delimiter=' ',  		conerters=None, skiprows=0, usecols=None, unpack=False, ndmin=0,             encoding='bytes', max_rows=None>)

- 간단히
  numpy.loadtxt({파일 이름}, delimiter=",")

  ```python
  a = np.loadtxt("save.txt", delimiter=",")
  ```

- 헤더 제외 언패킹 처리

  ```python
  import numpy as np
  x, y, z = np.loadtxt('text.txt',
                      skiprows=1,
                      unpack=True)
  
  print(x)
  print(y)
  print(z)
  
  '''
  [ 0.2536 0.4839 0.1292 0.1781 0.6253] [ 0.1008 0.4536 0.6875 0.3049 0.3486] [ 0.3857 0.3561 0.5929 0.8928 0.8791]
  '''
  ```

##### genfromtxt

- https://m.blog.naver.com/PostView.nhn?blogId=radii26omg&logNo=221051465120&proxyReferer=https:%2F%2Fwww.google.com%2F 
  괜찮네 이거
- 

#### numpy object (npy)로 저장 / 읽기

- numpy object (pickle) 형태로 저장하면 binary 파일 형태임

  ```python
  # 파일로 저장하기 위한 배열을 생성합니다.
  numbers = np.zeros((10,4))
  for i in range(10):
      for j in range(4):
          numbers[i][j] = random.randint(1000,40000)
  
          
  # npy 형태로 저장
  np.save(“npy_test”, arr=numbers)
  
  # npy 파일 읽기
  npy_array = np.load(file="npy_test.npy")
  npy_array[:5]
  ```

  



### 기타

#### 난수

- ```python
  # 뭐하는 놈인지 잘 모르겠음
  np.random.seed(42)
  
  # 0~1 사이
  > np.random.randn(5) # 5개의 숫자 생성
  array([ 0.69406812, -1.15425813,  0.98864607,  0.73682549, -0.5781785])
  
  #
  > np.random.randint(0, 10, 5)  # 0 이상 10 미만의 숫자 5개 랜덤 생성
  array([7, 0, 7, 7, 2])
  ```

#### 타입

- ```python
  # 타입 하나만 가능할거임
  arr = np.array([1.2, 2.01, 5,97])
  
  # 타임 반환
  arr.dtype
  # dtype('float64')
  
  np.int8(arr)
  # array([1,2,5], dtype=int8)
  ```

- 





# Matplotlib

- https://wikidocs.net/book/5011 참고

### 그래프 그리기

- 기본 그리기

  ```python
  import matplotlib.pyplot as plt
  
  plt.plot([1, 2, 3, 4])
  plt.xlabel('X-Label')
  plt.ylabel('y-label')
  plt.show()
  ```

  - 이러면 저기 리스트 값들은 y값으로 그림
  - x값은 자동으로 [0,1,2,3]으로 만들어짐

- 기본 (x,y)

  ```python
  import matplotlib.pyplot as plt
  
  plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
  plt.axis([0, 6, 0, 20])
  plt.show()
  ```

  - x, y 지정해준거임
  - 그래프 선 스타일 지정
  - axis 로 [xmin, xmax, ymin, ymax] 축 범위 지정해줌

- 기본 (여러개, 스타일)

  ```python
  import matplotlib.pyplot as plt
  import numpy as np
  
  # 200ms 간격으로 균일하게 샘플된 시간
  t = np.arange(0., 5., 0.2)
  
  # 빨간 대쉬, 파란 사각형, 녹색 삼각형
  plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
  plt.show()
  ```

  - numpy array 를 사용하지 않아도 모든 시퀀스가 내부적으로 numpy array로 변환함

- 그리드 설정

  ```python
  plt.grid(True) 	# 그리드 온
  plt.grid(True, axis='y', color='red', alpha=0.5, linestyle='--')	# 그리드 스타일
  ```

  https://www.delftstack.com/ko/howto/matplotlib/set-matplotlib-grid-interval/
  그리드 더 다양하게!

- 타이틀

  ```python
  plt.title('이게 타이틀임')
  plt.title('Sample graph', loc='right', pad=20) 	# 위치 지정
  plt.title('Sample graph', fontdict=title_font, loc='left', pad=20)	# 폰트 지정
  ```

- 구간 확대

  ```python
  plt.xlim(2,3)
  plt.ylim(5,20)
  ```

- 레전드 (그래프마다 라벨 달아줌)

  ```python
  x = np.arange(1,10,0.1)
  y = x*0.2
  y2 = np.sin(x)
  
  plt.plot(x,y,'b',label='first')
  plt.plot(x,y2,'r',label='second')
  plt.xlabel('x axis')
  plt.ylabel('y axis')
  plt.title('matplotlib sample')
  plt.legend(loc='upper right')
  plt.show()
  ```

- 서브플롯

  ```python
  from matplotlib import pyplot as plt
  import numpy as np
  
  x = np.arange(1,10)
  y1 = x*5
  y2 = x*1
  y3 = x*0.3
  y4 = x*0.2
  
  plt.subplot(2,2,1)
  plt.plot(x,y1)
  plt.subplot(2,2,2)
  plt.plot(x,y2)
  plt.subplot(2,2,3)
  plt.plot(x,y3)
  plt.subplot(2,2,4)
  plt.plot(x,y4)
  plt.show()
  ```

- 그래프 크기

  ```python
  # 가로, 세로 크기로 전체 그림 크기 조절
  plt.figure(figsize=(20,5))
  ```

  

