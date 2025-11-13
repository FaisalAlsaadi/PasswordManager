import sys

# Replace msgcat module entirely before anything imports it
class FakeMsgcat:
    class MessageCatalog:
        @staticmethod
        def set_many(*args, **kwargs):
            return 0

sys.modules['ttkbootstrap.localization.msgcat'] = FakeMsgcat()
