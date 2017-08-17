import datetime
from haystack import indexes
from search.models import Jwcinfo


class JwcinfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title=indexes.CharField(model_attr='title',boost=1.125)
    url = indexes.CharField(model_attr='url')
    site=indexes.CharField(model_attr='site',faceted=True)
    download=indexes.IntegerField(model_attr='download')
    pubtime=indexes.DateField(model_attr='pubtime')
    glances=indexes.IntegerField(model_attr='glances')


    def get_model(self):
        return Jwcinfo


