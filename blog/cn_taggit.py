from taggit.models import Tag, TaggedItem
from uuslug import slugify

class CnTag(Tag):
  class Meta:
    proxy = True

  def slugify(self, tag, i=None):
    return slugify(self.name)[:128]

class CnTaggedItem(TaggedItem):
  class Meta:
    proxy = True

  @classmethod
  def tag_model(cls):
    return CnTag
