import random
from typing import Literal

def get_loading_text():
    return random.choice([
        "*Searching...* :mag:",
        "*Looking that up...* :mag_right:",
        "*Exploring the policies...* :compass:",
        "*Generating Response...* :speech_balloon:",
        "*Processing you query...* :thought_balloon:",
        "*Reviewing Policies...* :books:"
    ])

def get_feedback_repsponse():
    return random.choice([
        "Did I get this right? Your feedback helps me get better!",
        "Was that helpful? Let me know so I can keep improving!",
        "Did I nail it or miss the mark? I’m learning from you!",
        "What do you think? Your feedback helps me level up!",
        "Hope that helped! Tell me if I’m on the right track."
    ])

def get_nocontext_response(type: Literal["actions", None] = None):
    if type == "actions":
        return random.choice([
            "Dang, missed the vibe on this one. Wanna raise a ticket below or hit up your HRBP for the real tea?",
            "Yikes, looks like I flopped. You can log a ticket below or ping your HRBP to sort this out!",
            "Not my best moment. Please a ticket below or reach out to your HRBP to get this cleared up!",
            "Oops... brain fog activated. You can raise a ticket below or chat with your HRBP for the full scoop!",
            "Bummer! I couldn’t crack this one. Drop a ticket below or connect with your HRBP — they’ve got your back.",
            "Missed the mark, my bad. Raise a ticket below or reach out to your HRBP — they’ll hook you up.",
            "Welp, this didn’t hit right. Best to raise a ticket below or catch up with your HRBP for the real deal!"
        ])
        
    return random.choice([
        "Oops, I’m blank on this one! Wanna raise a ticket below or hit up your HRBP",
        "Not in my knowledge base yet... You can either raise a ticket below or ping your HRBP to sort this out!",
        "Can’t help with this... but you can raise a ticket below or reach out to your HRBP for the real deal."
    ])