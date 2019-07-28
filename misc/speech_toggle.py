from talon.voice import Key, press, Str, Context, ContextGroup
from talon.voice import Context, Rep, RepPhrase, talon
from .. import utils


from talon.engine import engine
from talon_plugins import speech

sleep_group = ContextGroup("sleepy")
sleepy = Context("sleepy", group=sleep_group)

dictation_group = ContextGroup("dictation")
dictation = Context("dictation", group=dictation_group)
dictation_group.load()
dictation_group.disable()

# def repeat(m):
#     # TODO: This could be made more intelligent:
#     #         * Apply a timeout after which the command will not repeat previous actions
#     #         * Prevent stacking of repetitions upon previous repetitions
#     repeat_count = utils.extract_num_from_m(m)

#     if repeat_count is not None and repeat_count >= 2:
#         repeater = Rep(repeat_count - 1)
#         repeater.ctx = talon
#         return repeater(None)


ordinals = {}

def ordinal(n):
    """
    Convert an integer into its ordinal representation::
        ordinal(0)   => '0th'
        ordinal(3)   => '3rd'
        ordinal(122) => '122nd'
        ordinal(213) => '213th'
    """
    n = int(n)
    suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    return str(n) + suffix
    # return str(n)

for n in range(2, 100):
    ordinals[ordinal(n)] = n - 1

def repeat(m):
    o = m["repeater.ordinals"][0]
    repeater = Rep(int(ordinals[o]))
    repeater.ctx = talon
    return repeater(None)



class VoiceType:
    SLEEPING = 1
    TALON = 2
    DRAGON = 3
    DICTATION = 4


voice_type = VoiceType.TALON
last_voice_type = VoiceType.TALON


def set_voice_type(type):
    global voice_type, last_voice_type
    if voice_type != VoiceType.SLEEPING:
        last_voice_type = voice_type
    voice_type = type

    talon_enabled = type == VoiceType.TALON
    dragon_enabled = type == VoiceType.DRAGON
    dictation_enabled = type == VoiceType.DICTATION

    global speech
    speech.set_enabled(talon_enabled)

    global dictation_group
    if not dictation_enabled:
        dictation_group.disable()

    global engine
    if dragon_enabled:
        engine.mimic("wake up".split())
    else:
        engine.mimic("go to sleep".split())

    if dictation_enabled:
        # Without postponing this "go to sleep" will be printed
        dictation_group.enable()


sleepy.keymap(
    {
        "talon sleep": lambda m: set_voice_type(VoiceType.SLEEPING),
        "talon wake": lambda m: set_voice_type(last_voice_type),
        "dragon mode": lambda m: set_voice_type(VoiceType.DRAGON),
        "dictation mode": lambda m: set_voice_type(VoiceType.DICTATION),
        "talon mode": lambda m: set_voice_type(VoiceType.TALON),
        "clear": Key('backspace'),
        'space': Key('space'),
        "triumph": Key('backspace'),

        
        # "(repeat | repple)" + utils.numerals: repeat,
        "{repeater.ordinals}": repeat
    }
)
sleep_group.load()

