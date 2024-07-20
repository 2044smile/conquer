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

## reference

- https://www.django-rest-framework.org/tutorial/1-serialization/
