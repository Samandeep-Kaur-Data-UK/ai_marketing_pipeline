import argparse
import csv
import random
import re
from datetime import datetime


OUTPUT_PATH = "data/processed/social_posts_raw.csv"
TARGET_POSTS = 500
DEFAULT_SEED = 20260416

POSITIVE_LEADS = [
    "FreshBasket UK smashed it again,",
    "Well chuffed with FreshBasket UK today,",
    "Proper result from FreshBasket UK,",
    "Not gonna lie, FreshBasket UK was brilliant today,",
    "FreshBasket UK absolutely nailed it today,",
    "Fair play to FreshBasket UK,",
    "FreshBasket UK came through again,",
    "Genuinely impressed with FreshBasket UK tonight,",
    "Another solid shop from FreshBasket UK,",
    "FreshBasket UK has my weekly shop sorted,",
    "Can't knock FreshBasket UK today,",
    "FreshBasket UK was on point this morning,",
    "Happy days with FreshBasket UK,",
    "FreshBasket UK did the business today,",
    "Really rate FreshBasket UK after this order,",
]

POSITIVE_CLOSERS = [
    "Properly pleased with that.",
    "Tea is sorted tonight.",
    "Can't ask for more really.",
    "That's how online grocery should work.",
    "Made the whole week easier.",
    "Top effort all round.",
    "Small thing, big difference.",
    "Genuinely chuffed with that.",
    "Will happily order again.",
    "No complaints from me.",
    "Nice when something just works.",
    "Saved me a proper job.",
    "Exactly what I needed after work.",
    "Miles better than trekking to the shop.",
    "That'll do me nicely.",
]

POSITIVE_CORES = {
    "delivery": [
        "my delivery landed twenty minutes early and the driver was lovely",
        "the evening slot started bang on time and everything was still cold",
        "same-day delivery actually showed up when promised, which felt like a miracle",
        "the order arrived before dinner so I didn't need a panic dash to the shop",
        "they turned up right at the start of the window and handed everything over quickly",
        "my groceries were on the doorstep before I finished work and that saved me a job",
        "the driver rang properly, waited a sec, and brought the heavy bags to the door",
        "the van was early, the updates were clear, and the whole thing felt sorted",
        "my weekend slot landed exactly when booked and nothing was warm",
        "they squeezed in a late order for tonight and still arrived dead on time",
    ],
    "quality": [
        "the strawberries were properly sweet and the spinach actually lasted all week",
        "today's avocados were ripe at the right time instead of being rock hard",
        "the bread was soft, the tomatoes weren't battered, and the herbs smelled fresh",
        "every bit of veg in my order looked crisp and clean for once",
        "the salmon looked fresh and the salad leaves weren't slimy by day two",
        "even the budget fruit tasted decent and the bananas were actually yellow",
        "the chicken looked fresh enough that I didn't need to second guess dinner",
        "my berries turned up firm, not mushy, which made a nice change",
        "the eggs were spot on and the milk had a proper shelf life on it",
        "the veg box was full of decent produce and nothing looked tired",
    ],
    "packaging": [
        "packaging was tidy, the eggs were wrapped properly, and nothing leaked",
        "they separated chilled and cupboard bits sensibly so nothing got squashed",
        "barely any pointless plastic and the glass jars were packed securely",
        "the bags weren't overstuffed and the fruit survived the trip just fine",
        "no squashed tomatoes, no split milk, job done",
        "even the bread stayed in one piece because the heavier bits were packed well",
        "the chilled liners actually kept the dairy cold without loads of extra rubbish",
        "everything was stacked neatly and unpacking took about two minutes",
        "the reusable bags were packed sensibly and easy to carry upstairs",
        "they finally nailed the packing and the whole order arrived intact",
    ],
    "customer": [
        "customer service sorted my missing yoghurt in about five minutes and credited it straight away",
        "the live chat fixed a refund without any faff and was genuinely polite",
        "support actually read my message and replaced the damaged juice by lunchtime",
        "they owned the substitution mix-up and put the money back instantly",
        "the team was sound on the phone and sorted the issue first time",
        "I got a reply in minutes and the replacement item was added to tomorrow's slot",
        "they apologised properly for the missing bread and refunded it there and then",
        "support was helpful, quick, and didn't make me chase anything twice",
        "the agent on chat fixed my account issue faster than I expected",
        "they handled a dodgy discount code in one go and didn't make it awkward",
    ],
    "price": [
        "today's offers saved me a fair few quid on the weekly shop",
        "the multibuy deal on pasta, sauce, and veg was decent value",
        "managed to get dinner bits for less than the corner shop charges",
        "the own-brand stuff is surprisingly cheap and actually pretty nice",
        "meal planning came in under budget thanks to the midweek offers",
        "their fruit and veg promo was better than I expected this time",
        "I shaved a good few quid off the total with the bundle deals",
        "the family staples were on offer and that made a proper difference",
        "prices felt fair today, especially on milk, bread, and eggs",
        "used a voucher plus the offers and the whole basket came in cheaper than usual",
    ],
    "website": [
        "the website was dead easy tonight and checkout took about thirty seconds",
        "reordering on the app was smooth and the substitutions were clear",
        "search actually worked and I found everything fast for once",
        "basket swaps were painless and the slot picker behaved itself",
        "the phone site finally stopped lagging and I was done in minutes",
        "it remembered my favourites properly, which made the whole thing much quicker",
        "adding meal bits to the basket was simple and the offers showed up clearly",
        "the checkout page didn't crash once and that felt like progress",
        "the app made a boring top-up shop weirdly easy after work",
        "filtering by dietary bits actually worked, so I found the gluten-free stuff quickly",
    ],
}

NEGATIVE_LEADS = [
    "FreshBasket UK has done my head in today,",
    "Bit gutted with FreshBasket UK,",
    "FreshBasket UK was rubbish tonight,",
    "Honestly, FreshBasket UK annoyed me today,",
    "FreshBasket UK let me down again,",
    "Not impressed with FreshBasket UK this week,",
    "FreshBasket UK was a bit dodgy today,",
    "FreshBasket UK made the weekly shop harder,",
    "FreshBasket UK really dropped the ball today,",
    "FreshBasket UK needs to sort itself out,",
    "FreshBasket UK was a faff from start to finish,",
    "Pretty fed up with FreshBasket UK now,",
    "FreshBasket UK was all over the place today,",
    "FreshBasket UK has gone downhill lately,",
    "FreshBasket UK was naff today,",
]

NEGATIVE_CLOSERS = [
    "Properly annoying.",
    "What a faff.",
    "Not good enough really.",
    "Absolute rubbish.",
    "Left me fuming.",
    "Such a pain.",
    "That needs sorting.",
    "Wish I'd gone elsewhere.",
    "Bit of a joke.",
    "Not using that excuse anymore.",
    "Ruined the plan for dinner.",
    "Really not the one.",
    "Took ages to put right.",
    "Shouldn't be this hard.",
    "That's me properly annoyed.",
]

NEGATIVE_CORES = {
    "delivery": [
        "the driver missed my slot by nearly two hours and nobody warned me",
        "my order never turned up in the booked window and support just shrugged",
        "same-day delivery turned into late-night delivery again",
        "they marked it delivered while I was still sat at home waiting",
        "the van arrived so late the frozen bits were already soft",
        "I booked an early slot and FreshBasket UK rolled up when lunch was basically over",
        "the tracking updates were useless and the order just kept moving later",
        "they cancelled my delivery last minute after I'd planned meals around it",
        "the driver showed up ages late and left half the bags in the van",
        "I waited in all evening for FreshBasket UK and the slot came and went",
    ],
    "quality": [
        "the strawberries were mouldy and the cucumbers looked tired",
        "my avocados were bruised and the salad was already soggy",
        "the chicken had tomorrow's date on it and I'm not risking that",
        "half the bananas were black by the time the bags landed",
        "the milk was warm and the yoghurt lids were bulging",
        "the tomatoes were bashed, the herbs were limp, and the bread felt stale",
        "my berries were mush before I even unpacked the lot",
        "the veg looked like it had been kicking about the warehouse for days",
        "the apples were bruised all over and the lettuce had gone slimy",
        "even the basics looked tired, which is not what you want midweek",
    ],
    "packaging": [
        "packaging was a mess, eggs cracked and juice leaking everywhere",
        "they chucked tins on top of the bread and flattened the lot",
        "there was so much plastic around three apples it felt daft",
        "the bag split on the doorstep because it was packed badly",
        "chilled and cupboard stuff were all mixed together again",
        "the freezer bits were buried under cleaning stuff, which is just silly",
        "one flimsy bag had all the heavy bottles in it and it nearly tore my hand off",
        "the bread got squashed because someone thought potatoes belonged on top",
        "milk leaked over half the order thanks to rubbish packing",
        "loads of cardboard, loads of plastic, and still somehow broken eggs",
    ],
    "customer": [
        "customer service kept me in a queue for ages and solved nothing",
        "live chat copied and pasted nonsense instead of reading my message",
        "I had to chase a refund twice for one missing item",
        "support promised a call back and then vanished",
        "they acted like bruised fruit was somehow my problem",
        "the agent ended the chat before the issue was even sorted",
        "nobody seemed to know where my missing bag had gone",
        "it took three messages just to get a straight answer about a refund",
        "support was polite enough but completely useless at fixing the actual problem",
        "I explained the issue clearly and still got the wrong canned reply back",
    ],
    "price": [
        "prices have crept up and the deals aren't worth shouting about",
        "they charged me more than the shelf price shown online",
        "the service fee keeps creeping up for a pretty average shop",
        "used to save me a few quid here, now it feels cheeky",
        "those so-called offers were barely a discount",
        "the basket total jumped loads compared with last month for the same staples",
        "even the own-brand bits aren't cheap anymore",
        "I added a few basics and somehow the total looked daft",
        "FreshBasket UK keeps nudging prices up while the quality slips",
        "the promo looked decent until the final total proved otherwise",
    ],
    "website": [
        "the website kept freezing at checkout and emptied my basket",
        "the app logged me out three times while I was ordering",
        "search results were useless and basic items were weirdly hard to find",
        "I couldn't change my slot because the page kept looping",
        "the substitution settings disappeared again for no reason",
        "the offers page kept glitching and showing the wrong prices",
        "checkout spun for ages then dumped me back at the basket",
        "the phone site was painfully slow and kept losing what I had added",
        "I tried to reorder last week's basket and half the page just blanked out",
        "even logging in felt like hard work tonight",
    ],
}

NEUTRAL_LEADS = [
    "Tried FreshBasket UK again today,",
    "FreshBasket UK order arrived this afternoon,",
    "Just did a small shop with FreshBasket UK,",
    "Used FreshBasket UK for a top-up order,",
    "FreshBasket UK was fine today,",
    "Another FreshBasket UK delivery landed,",
    "FreshBasket UK seems about the same this week,",
    "Placed a quick order on FreshBasket UK,",
    "FreshBasket UK turned up within the slot,",
    "FreshBasket UK was fairly standard today,",
    "Did the basics on FreshBasket UK tonight,",
    "FreshBasket UK handled my top-up shop okay,",
    "FreshBasket UK did what it said today,",
    "FreshBasket UK was pretty ordinary this time,",
    "Used FreshBasket UK after work today,",
]

NEUTRAL_CLOSERS = [
    "We'll see how next week goes.",
    "Nothing to rave about really.",
    "Pretty standard shop overall.",
    "That'll do for now.",
    "No big drama either way.",
    "Just part of the weekly admin.",
    "Fine, not life changing.",
    "Seems okay so far.",
    "No strong feelings on it.",
    "Useful enough, I suppose.",
    "It did the job.",
    "About what I expected, really.",
    "No complaints and no fanfare.",
    "Good enough for the basics.",
    "Nothing wild to report.",
]

NEUTRAL_CORES = {
    "delivery": [
        "the van was on time and everything looked about as expected",
        "delivery came in the middle of the slot and the handover was quick",
        "it arrived when booked, nothing dramatic either way",
        "the order landed before dinner and that was handy enough",
        "tracking was fine and the driver left without any fuss",
        "my slot held up and the bags came over pretty quickly",
        "the updates were clear enough and the van showed when expected",
        "it turned up roughly when promised and that did the job",
        "the evening delivery was ordinary but perfectly usable",
        "got the order inside the booked window, which was all I needed",
    ],
    "quality": [
        "fruit looked fine, not amazing, not terrible",
        "the veg was decent enough for a midweek top-up",
        "bread and milk were fresh, the rest was pretty average",
        "quality seemed normal compared with last week",
        "nothing looked especially good or bad in today's basket",
        "the salad was alright and the bananas were about what I expected",
        "basics were fresh enough, though nothing stood out",
        "the produce was serviceable and will do for a few days",
        "meat looked okay, fruit looked okay, very middle of the road really",
        "everything seemed standard supermarket quality to me",
    ],
    "packaging": [
        "packaging was tidy enough though there was still a fair bit of plastic",
        "nothing was broken and the bags were packed reasonably well",
        "the chilled bits were separated properly, which I appreciated",
        "boxes were fine, if a bit bulky for a small order",
        "it was packed okay overall, just not especially clever",
        "unpacking was straightforward and nothing had shifted about too much",
        "the bags were manageable enough and everything stayed intact",
        "not much to report on the packing other than it worked",
        "a bit more wrapping than needed, but nothing outrageous",
        "the bread survived and the eggs were whole, which will do",
    ],
    "customer": [
        "didn't need customer service this time so can't say much there",
        "got the automated updates and they were clear enough",
        "the driver was polite and left quickly",
        "support sent the usual confirmation emails and that was that",
        "I only used the help page briefly and it seemed fine",
        "no issues to raise, so I didn't really test their support",
        "got the normal texts and reminders, nothing more to say",
        "the delivery handoff was polite and uneventful",
        "no missing items, no refunds, no need to contact anyone",
        "everything on the service side felt pretty standard today",
    ],
    "price": [
        "prices looked similar to the big supermarkets to be honest",
        "a few offers were decent, a few were nothing special",
        "the total felt about average for an online shop",
        "some bits were good value, some weren't",
        "nothing felt wildly cheap or wildly expensive today",
        "the basket came out around what I expected to pay",
        "some staples were fair enough, especially milk and pasta",
        "I noticed a couple of decent deals but not much beyond that",
        "price wise it felt middle of the pack really",
        "the voucher took a little off, though not loads",
    ],
    "website": [
        "the app worked alright once I found the right aisle",
        "checkout was straightforward after a bit of scrolling",
        "the website loaded fine on my phone for once",
        "basket edits took a minute but it all went through",
        "search was okay, not brilliant, not awful",
        "I found most things without much bother on the site",
        "the slot picker worked and the rest of the app felt ordinary",
        "took a few taps to finish the shop, but nothing broke",
        "the website did what it needed to do and that was about it",
        "browsing the offers page was simple enough this evening",
    ],
}


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w']+\b", text))


def build_post(lead: str, core: str, closer: str) -> str:
    return re.sub(r"\s+", " ", f"{lead} {core}. {closer}").strip()


def add_posts(targets, leads, cores_by_topic, closers, seen, bucket, rng):
    for topic, target in targets:
        while target > 0:
            post = build_post(
                rng.choice(leads),
                rng.choice(cores_by_topic[topic]),
                rng.choice(closers),
            )
            if post in seen:
                continue

            words = word_count(post)
            if words < 10 or words > 40:
                continue

            seen.add(post)
            bucket.append(post)
            target -= 1


def generate_posts(seed: int) -> list[str]:
    rng = random.Random(seed)
    posts = []
    seen = set()

    add_posts(
        [(topic, 50) for topic in ["delivery", "quality", "packaging", "customer", "price", "website"]],
        POSITIVE_LEADS,
        POSITIVE_CORES,
        POSITIVE_CLOSERS,
        seen,
        posts,
        rng,
    )
    add_posts(
        [
            ("delivery", 21),
            ("quality", 21),
            ("packaging", 21),
            ("customer", 21),
            ("price", 21),
            ("website", 20),
        ],
        NEGATIVE_LEADS,
        NEGATIVE_CORES,
        NEGATIVE_CLOSERS,
        seen,
        posts,
        rng,
    )
    add_posts(
        [
            ("delivery", 13),
            ("quality", 13),
            ("packaging", 13),
            ("customer", 12),
            ("price", 12),
            ("website", 12),
        ],
        NEUTRAL_LEADS,
        NEUTRAL_CORES,
        NEUTRAL_CLOSERS,
        seen,
        posts,
        rng,
    )

    rng.shuffle(posts)
    return posts


def save_posts(posts: list[str], output_date: str):
    with open(OUTPUT_PATH, "w", newline="") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(["review_text", "source", "date"])
        for post in posts:
            writer.writerow([post, "social", output_date])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.today().strftime("%Y-%m-%d"))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    posts = generate_posts(args.seed)
    lengths = [word_count(post) for post in posts]

    if len(posts) != TARGET_POSTS:
        raise RuntimeError(f"Expected {TARGET_POSTS} posts, found {len(posts)}")

    if len(set(posts)) != TARGET_POSTS:
        raise RuntimeError("Generated posts are not unique")

    if min(lengths) < 10 or max(lengths) > 40:
        raise RuntimeError("Generated posts do not meet the 10-40 word rule")

    save_posts(posts, args.date)

    print(f"Saved {len(posts)} posts to {OUTPUT_PATH}")
    print(f"Word count range: {min(lengths)} to {max(lengths)}")
    print("Sample posts:")
    for post in posts[:5]:
        print(post)


if __name__ == "__main__":
    main()
