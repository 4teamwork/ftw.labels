from ftw.labels.interfaces import ILabeling
from ftw.labels.interfaces import ILabelJar
from ftw.labels.interfaces import ILabelSupport
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.interface import implements


ANNOTATION_KEY = 'ftw.labels:labeling'


class Labeling(object):
    implements(ILabeling)
    adapts(ILabelSupport)

    def __init__(self, context):
        self.context = context
        self.jar = ILabelJar(self.context)

    def activate(self, *label_ids):
        available_labels = self.jar.storage.keys()

        for label_id in label_ids:
            if label_id not in available_labels:
                raise LookupError(
                    'Cannot activate label: '
                    'the label "{0}" is not in the label jar.'.format(
                        label_id))

            if label_id not in self.storage:
                self.storage.append(label_id)

    def deactivate(self, *label_ids):
        for label_id in label_ids:
            if label_id not in self.storage:
                continue

            self.storage.remove(label_id)

    def active_labels(self):
        return map(self.jar.get, self.storage)

    def available_labels(self):
        for label in self.jar.list():
            label['active'] = (label.get('label_id') in self.storage)
            yield label

    @property
    def storage(self):
        if getattr(self, '_storage', None) is None:
            annotation = IAnnotations(self.context)
            if ANNOTATION_KEY not in annotation:
                annotation[ANNOTATION_KEY] = PersistentList()
            self._storage = annotation[ANNOTATION_KEY]
        return self._storage