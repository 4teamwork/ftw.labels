from ftw.builder import Builder
from ftw.builder import create
from ftw.labels.interfaces import ILabelJar
from ftw.labels.testing import LABELS_FUNCTIONAL_TESTING
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase
from zExceptions import BadRequest
from zExceptions import Unauthorized


class TestLabelsJar(TestCase):
    layer = LABELS_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Contributor'])

    @browsing
    def test_create_label(self, browser):
        root = create(Builder('label root'))

        browser.login().open(root,
                             view='labels-jar/create',
                             data={'title': 'Question',
                                   'color': 'purple'})

        self.assertEqual(
            [{'label_id': 'question',
              'title': 'Question',
              'color': 'purple'}],
            ILabelJar(root).list())

    @browsing
    def test_create_label_is_protected(self, browser):
        root = create(Builder('label root'))
        browser.login(create(Builder('user').with_roles('Reader')))

        with self.assertRaises(Unauthorized):
            browser.open(root,
                         view='labels-jar/create',
                         data={'title': 'Question',
                               'color': 'purple'})

    @browsing
    def test_create_label_requires_label_arguments(self, browser):
        root = create(Builder('label root'))

        with self.assertRaises(BadRequest) as cm:
            browser.login().open(root, view='labels-jar/create')

        self.assertEquals('"title" and "color" request arguments are required.',
                          str(cm.exception))

    @browsing
    def test_update_label(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))

        browser.login().open(root,
                             view='labels-jar/update',
                             data={'label_id': 'question',
                                   'title': 'Questions and inquiries',
                                   'color': 'green'})

        self.assertItemsEqual(
            [{'label_id': 'question',
              'title': 'Questions and inquiries',
              'color': 'green'},

             {'label_id': 'bug',
              'title': 'Bug',
              'color': 'red'}],
            ILabelJar(root).list())

    @browsing
    def test_update_label_requires_label_id(self, browser):
        root = create(Builder('label root'))

        with self.assertRaises(BadRequest) as cm:
            browser.login().open(root, view='labels-jar/update')

        self.assertEquals('The "label_id" request argument is required.',
                          str(cm.exception))

    @browsing
    def test_partial_update_label(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))

        browser.login().open(root,
                             view='labels-jar/update',
                             data={'label_id': 'question',
                                   'title': 'Questions and inquiries'})

        self.assertItemsEqual(
            [{'label_id': 'question',
              'title': 'Questions and inquiries',
              'color': 'purple'},

             {'label_id': 'bug',
              'title': 'Bug',
              'color': 'red'}],
            ILabelJar(root).list())

    @browsing
    def test_remove_label(self, browser):
        root = create(Builder('label root')
                      .with_labels(('Question', 'purple'),
                                   ('Bug', 'red')))

        browser.login().open(root,
                             view='labels-jar/remove',
                             data={'label_id': 'question'})

        self.assertEqual(
            [{'label_id': 'bug',
              'title': 'Bug',
              'color': 'red'}],
            ILabelJar(root).list())

    @browsing
    def test_remove_label_requires_label_id(self, browser):
        root = create(Builder('label root'))

        with self.assertRaises(BadRequest) as cm:
            browser.login().open(root, view='labels-jar/remove')

        self.assertEquals('The "label_id" request argument is required.',
                          str(cm.exception))