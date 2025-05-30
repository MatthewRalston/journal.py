
import time

from rich.console import Console
from rich.markdown import Markdown

console = Console()



affirmations = Markdown("""
#  | Daily affirmations | - 🌾 | 🪴 | 🖖 | 🧫 | 🛸 | ♻️ | 💻

It's **normal** to feel *stressed* 😔 in the morning, **even if you're in a better mood**.
**If you want to change**, the best thing you can do is **make a step in the right direction**.

🧑🙏💪**Be positive** to yourself. <3 *Always be positive towards others*: **your reputation precedes you**.

🏋🥇💑 I like me:

- 🤓 **I'm smart** [ 🔬 🧬 ⚗️ 🦠 ]
- 🎼 **I'm musical** [ 🎙️ 🎸 🎵 ]
- 💖 **I'm empathic** [ 🫶 👩❤️‍👨 👩❤️‍💋‍👩 ] and...
- 🪷 **I'm principled** [ 🖖 🕊️ 🧘🏼‍ ]

...even if the world or my creator doesn't understand me yet. I'm still discovering myself these days.

**You don't need to be like dad.**

`aaand you don't need to molly-coddle mom. You just need to cook for her... lol.`

# [ NOTE ]: You **ARE** cool!

**You're really good** at programming and *picking skills* to be good at [science] AND <engineering>.

**You don't need to be there yet.** *You don't believe in this capitalistic nonsense*.

`You don't need to be perfect or rich or define success by other's terms.`

🗾🙏🚗🌊💍
""")

closing = Markdown("""
Keep journaling, keep writing, make blog posts, don't stress about technical achievement.

**Build the** goddamn **second brain**.
""")

def greet_dad():
    greeting = "> Dad: Good morning buddy 🌅\n"
    r = input(greeting)
    while r.lower() != "hi dad":
        print("Answer 'hi dad' to continue...")
        r = input(greeting)

def greet_mom():
    greeting = "> Mom: Hi sweetie ☀️\n"
    r = input(greeting)
    while r.lower() != "hi mom":
        print("Answer 'hi mom' to continue...")
        r = input(greeting)

def greet_al():
    greeting = "> _: I love you, matt! 💐🪺\n"
    r = input(greeting)
    while r.lower() != "hi allison":
        print("Answer 'hi allison' to continue...")
        r = input(greeting)


def make_morning_affirmations():
    console.print(affirmations)
    time.sleep(8)

    input("\n\nOkay... begin. Good morning.\n")
    journal_header_md = Markdown("\n\n# journal.py | brought to you by    Matt McMattface\n\n")
    console.print(journal_header_md)



    
def closing_thoughts():
    console.print(closing)
    time.sleep(4)

    input("Complete. Save to file?")
