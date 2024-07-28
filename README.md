# conquer

## feat

### Trade-offs between views vs VietSets
  - ViewSet 장점
    - Using ViewSets can be a really useful abstraction(추상화; 복잡한 시스템에서 중요한 부분만을 선택하여 단순하게 표현하는 과정 즉, 세부적인 구현이나 복잡한 내용을 숨기고, 사용자에게 필요한 기능이나 개념만을 드러내는 것)
      - e.g) 운전자는 자동차를 운전하기 위해 엔진의 내부 작동 방식은 알 필요가 없습니다. 중요한 것은 핸들을 돌리면 방향이 바뀌고, 페달을 밟으면 속도가 조절된다는 점 입니다.
    - API URL 규칙을 일관되도록 보장하는 데 도움이 됩니다.
    - **작성해야 하는 코드의 양을 최소화**하고, URL 구성의 세부 사항보다는 API가 제공하는 상호 작용 및 표현에 집중할 수 있습니다.
  - ViewSet 단점
    - 초기 학습 곡선
      - Django 의 기본 클래스 기반 뷰보다 복잡하다고 느낄 수 있습니다.
    - 세부화된 제어 부족
      - ViewSet은 기본 CRUD 작업을 자동으로 처리하기 때문에 세부적인 제어가 필요한 경우에는 불편할 수 있습니다.
      - 특정한 액션에 대해 세밀하게 커스터마이징하려면 추가적인 코드가 필요합니다.
    - URL 패턴의 복잡성
      - ViewSet 을 사용하면 URL 라우팅이 자동으로 처리되지만, 복잡한 URL 패턴이 필요한 경우에는 직접 URL을 설정하는 것보다 더 복잡해질 수 있습니다.
    - 조그만한 작업에는 ViewSet이 적합하지 않음
      - e.g) 생성만 해야되는 엔드포인트에서 ViewSet 을 사용한다면 애매하다. 차라리 ListCreateView 나 이런 걸 사용하는 것이 복잡성도 줄이고, 시인성이 좋다고 생각한다.

### ViewSet
  - api_root 도 자동으로 생성한다.
  - URL 도 DefaultRouter() 간편하게 사용 할 수 있다.

### @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
  - action 데코레이터를 사용하여 사용자 정의 액션을 추가합니다. 
  - detail=True 는 이 액션이 개별 객체에 대해 호출되어야 함을 나타냅니다. snippet/<pk>/highlight/
  - detail=False 는 목록에 대해 호출되어야 함을 나타냅니다. snippet/highlight/

### 하이퍼링크
  - Django REST Framework(DRF) 의 하이퍼링크 필드는 객체 간의 관계를 나타낼 때 객체의 기본 키 (primary key) 대신 URI 를 사용하여 해당 객체의 위치를 나타냅니다. 이는 RESTful 원칙을 따르며, 클라이언트가 관련 리소스에 쉽게 접근하고 탐색할 수 있도록 도와줍니다.
  - 모델 간의 관계를 기본 키 대신 하이퍼링크(URI)로 표현합니다.
  - API 응답에 포함된 URL을 통해 관련 리소르를 쉽게 탐색할 수 있습니다.
  - 서버가 자동으로 URL을 생성하여 응답에 포함시켜, 프런트엔드에서 별도의 URL 구성이 필요 없습니다.https://www.youtube.com/watch?v=t2dIZnyCl5k
  ```python
  [
    {
        "url": "http://example.com/users/1/",
        "username": "john",
        "snippets": [
            "http://example.com/snippets/1/",
            "http://example.com/snippets/2/"
        ]
    },
    {
        "url": "http://example.com/users/2/",
        "username": "jane",
        "snippets": []
    }
  ]
  ```

### 직렬화, 역직렬화
  - Queryset -> Serializer -> JSON (직렬화)
  - JSON -> Serializer -> Queryset (역직렬화)
### SnippetSerializer(data=data) create(), SnippetSerializer(instance, data=data) update()
  - SnippetSerializer(instance) 를 호출하면 get() 호출
  - SnippetSerializer(instance, many=True) 를 호출하면 list() 호출
  - SnippetSerializer(data=data)를 호출하면 create() 호출
  - SnippetSerializer(instance, data=data)를 호출하면 update() 호출
```python
class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
```
### APIView vs Mixin vs Generics
- **커스터마이징이 많은 views 의 경우 APIView 사용하는 것이 좋다.**
- **간단한 CRUD 의 경우 Generics 사용하는 것이 좋다.**
#### APIView
  - 모든 HTTP 메서드를 직접 구현하여 세밀한 제어가 가능합니다.
  - 가장 유연하며, 요청과 응답을 세밀하게 제어할 수 있습니다.
#### Mixin
  - 필요한 기능만 mixin 클래스로부터 상속받아 구현할 수 있습니다.
  - 유연하지만, 일부 복잡한 커스터마이징에는 한계가 있을 수 있습니다.
#### Generics
  - 표준화된 CRUD 패턴을 제공하여 최소한의 코드로 CRUD 기능을 구현할 수 있습니다.
  - 기본 CRUD 기능에 최적화되어 있지만, 고도로 커스터마이징된 로직을 추가하기에는 유연성이 제한될 수 있습니다.
```python
# APIView
class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
# Mixin
class SnippetList(mixins.ListModelMixin, 
                  mixins.CreateModelMixin, 
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# Generics
class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
```

## reference

- https://www.django-rest-framework.org/tutorial/1-serialization/
