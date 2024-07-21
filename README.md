# conquer

## feat

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
- 커스터마이징이 많은 views 의 경우 APIView 사용하는 것이 좋다.
- 간단한 CRUD 의 경우 Generics 사용하는 것이 좋다.
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
