import sys

def patch():
    try:
        import ttkbootstrap.localization.msgs as msgs
        original = msgs.initialize_localities
        def wrapper():
            try:
                original()
            except:
                pass
        msgs.initialize_localities = wrapper
    except:
        pass

patch()
