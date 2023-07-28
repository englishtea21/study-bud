from dal import autocomplete

from .models import Topic


class TopicAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Topic.objects.none()

        qs = Topic.objects.filter()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
