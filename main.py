import gi
gi.require_version('Gdk', '3.0')

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from src.functions import generate_suggestions, generate_instant_answer, init_settings
from src.items import no_input_item, show_suggestion_items, show_instant_answer


class searxExtension(Extension):
    def __init__(self):
        super(searxExtension, self).__init__()

        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        init_settings(extension.preferences)
        query = event.get_argument() or str()
        lang = extension.preferences["searx_search_language"]
        include_instant_answer = extension.preferences["searx_include_instant_answer"] == "true"

        if len(query.strip()) == 0:
            return RenderResultListAction(no_input_item())

        if include_instant_answer:
            instant_answer = show_instant_answer(*generate_instant_answer(query, lang=lang))
        suggestion_items = show_suggestion_items([query] + generate_suggestions(query, lang=lang))

        return_list = list(suggestion_items)
        if include_instant_answer and instant_answer is not None:
            return_list.insert(0, instant_answer)

        return RenderResultListAction(return_list)


if __name__ == "__main__":
    searxExtension().run()
