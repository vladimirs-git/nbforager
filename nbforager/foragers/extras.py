# pylint: disable=R0902,R0903

"""Extras Forager."""

from nbforager.foragers.base_fa import BaseAF
from nbforager.foragers.forager import Forager
from nbforager.nb_api import NbApi
from nbforager.nb_tree import NbTree


class ExtrasAF(BaseAF):
    """Extras Forager."""

    def __init__(self, api: NbApi, root: NbTree, tree: NbTree):
        """Init ExtrasAF.

        :param api: NbApi object, connector to Netbox API.
        :param root: NbTree object where raw data from Netbox needs to be saved.
        :param tree: NbTree object where transformed data from Netbox needs to be saved.
        """
        super().__init__(api, root, tree)
        self.bookmarks = self.BookmarksF(self)
        self.config_contexts = self.ConfigContextsF(self)
        self.config_templates = self.ConfigTemplatesF(self)
        self.content_types = self.ContentTypesF(self)
        self.custom_field_choice_sets = self.CustomFieldChoiceSetsF(self)
        self.custom_fields = self.CustomFieldsF(self)
        self.custom_links = self.CustomLinksF(self)
        self.export_templates = self.ExportTemplatesF(self)
        self.image_attachments = self.ImageAttachmentsF(self)
        self.journal_entries = self.JournalEntriesF(self)
        self.object_changes = self.ObjectChangesF(self)
        self.reports = self.ReportsF(self)
        self.saved_filters = self.SavedFiltersF(self)
        self.scripts = self.ScriptsF(self)
        self.tags = self.TagsF(self)
        self.webhooks = self.WebhooksF(self)

    class BookmarksF(Forager):
        """BookmarksF."""

    class ConfigContextsF(Forager):
        """ConfigContextsF."""

    class ConfigTemplatesF(Forager):
        """ConfigTemplatesF."""

    class ContentTypesF(Forager):
        """ContentTypesF."""

    class CustomFieldChoiceSetsF(Forager):
        """CustomFieldChoiceSetsF."""

    class CustomFieldsF(Forager):
        """CustomFieldsF."""

    class CustomLinksF(Forager):
        """CustomLinksF."""

    class ExportTemplatesF(Forager):
        """ExportTemplatesF."""

    class ImageAttachmentsF(Forager):
        """ImageAttachmentsF."""

    class JournalEntriesF(Forager):
        """JournalEntriesF."""

    class ObjectChangesF(Forager):
        """ObjectChangesF."""

    class ReportsF(Forager):
        """ReportsF."""

    class SavedFiltersF(Forager):
        """SavedFiltersF."""

    class ScriptsF(Forager):
        """ScriptsF."""

    class TagsF(Forager):
        """TagsF."""

    class WebhooksF(Forager):
        """WebhooksF."""
