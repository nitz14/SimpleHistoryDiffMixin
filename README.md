###HOW TO USE

add requirements to your project.

in models.py add import:

```
    from utils.mixins import SimpleHistoryDiffMixin
```

add single inheritance:

```
    class User(models.Model, SimpleHistoryDiffMixin):
```

add fields that you want to ignore:

```
    diff_ignore_keys = ['name', 'email']
```

and use in code e.g. in viewset:

```
    class UserHistoryViewSet(viewsets.ReadOnlyModelViewSet):
        authentication_classes = (SessionAuthentication, TokenAuthentication, )
        permission_classes = (IsAuthenticated, )
        queryset = HistoricalUser.objects.all()
        filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
        filter_fields = ('id', )
        serializer_class = UserHistorySerializer

        def get_queryset(self):
            user = User.objects.get(pk=self.request.query_params.get('id'))
            return self.queryset.filter(pk__in=[hr.pk for hr in user.diff_with_all()])
```