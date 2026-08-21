import os
import pathlib
import subprocess
import time
import urllib.parse

BASE = 'premium polished high quality 3D cartoon NPC illustration for a cozy casual mobile farming management game, single character only, thigh-up portrait from head to upper thighs, three-quarter view, eye-level medium focal length, complete hands forearms waist and signature props visible, clean medium gray studio background, no text, no UI, no logo, no watermark, no other people, soft rounded sculpted forms, slightly oversized head and hands, strong readable silhouette, distinctive non-generic facial bone structure, smooth warm animated skin with subtle cheek and nose blush, no realistic pores, chunky readable hair masses, matte fabric with soft rounded folds, vivid saturated but non-neon colors, warm key light and soft rim light, professional casual farming game character concept art, not photorealistic, not anime, not flat 2D, not a plastic toy, no generic beauty face, no identical face template, no cropped hands or props. '

PROMPTS = {
    'NPC-007': '22-year-old petite sturdy female ruins explorer, short height, round face, thick straight eyebrows, large almond eyes, short upturned nose, short upper lip with a small left canine visible, slight facial asymmetry, chin-length plum-purple bob with outward flipped ends and a silver hairclip on the right, cream short-sleeve shirt, black denim short overalls, purple-gray accessories, coral-red waist bag, holding a glowing stone shard in one hand and unfolding a hand-drawn ancient ruins map in the other, leaning forward with a thrilled discovery expression, adventurous and alert.',
    'NPC-008': '27-year-old curvy deep-brown-skinned female tailor and dancer, medium-short height, long heart-shaped face, wide-set large round eyes, short straight nose, full lips, left cheek dimple, slight facial asymmetry, cobalt-blue fluffy short curls tied with a coral fabric bow, patchwork summer dress in lake blue coral red and cream, layered cloth bracelets, holding a colorful fabric swatch book in one hand and bright thread scissors in the other, body swaying gently, open radiant smile, artistic and welcoming.',
    'NPC-009': '24-year-old tall slender female photographer, narrow oval face, cat-shaped eyes, thin nose bridge, small pointed chin, high arched eyebrow tails, defined cupid bow, slight facial asymmetry, honey-blonde shoulder-length straight hair curled inward with a wide pale headband, mustard-yellow cropped summer top, cream high-waisted shorts, thin coral scarf, holding a vintage camera ready to shoot and a folded reflector tucked at her side, precise elegant stance, selective professional smile.',
    'NPC-010': '30-year-old medium-tall strong female forest sculptor and woodworker, broad rectangular face, thick eyebrows, low nose bridge, freckles, full lips, powerful jaw, slight facial asymmetry, brick-red naturally curly short hair pinned back with a wooden hair stick, olive-green craft apron over a cream tank top, rust-red shorts, sturdy forearms with a little sawdust, holding an unfinished carved wooden bird in one hand and a carving knife in the other, grounded relaxed stance, quiet focused smile.',
    'NPC-011': '23-year-old compact athletic medium-brown-skinned female mechanical inventor, short-to-medium height, small square face, monolid eyes, short round nose, naturally upturned mouth corners, right eyebrow with a small notch, round protective goggles, deep-brown short curls with volume on top and a lake-blue hair clip, lake-blue mechanic romper, cream short sleeves, orange tool belt, holding a miniature sorting robot arm in one hand and explaining it rapidly with the other, leaning forward with intense concentration and excited eyes.',
    'NPC-012': '26-year-old slim gentle female library teaching assistant, medium height, pear-shaped face, downturned eyes, long narrow nose, thin lips, slightly long midface, one-sided dimple when smiling, slight facial asymmetry, chestnut-red long hair in a low braid with soft wisps, rust-red lightweight knit top, deep navy skirt, cream details, holding a densely annotated lesson notebook against her chest while pointing to a page with colored chalk, shoulders slightly drawn in, warm closed-mouth smile and shy downward gaze.',
    'NPC-013': "48-year-old mature curvy female tea-garden shopkeeper, medium height, soft round face, mature almond eyes, small round nose tip, full lips, subtle crow's feet, slight facial asymmetry, olive skin, deep-green shoulder-length wavy hair gathered into a low bun with a few silver strands, olive-green summer blouse, peach-coral long skirt, cream woven accessories, carrying a wicker tea basket and gently pinching a tea leaf to inspect it, calm reassuring smile, graceful relaxed posture.",
    'NPC-014': '39-year-old short broad extremely stocky male blacksmith, huge rectangular face, deep-set eyes, bulbous garlic-shaped nose, thick lower lip, very wide chin, reddish pale skin with a small spark burn mark on the right cheek, black-brown short hair and dense beard with gray at the temples, charcoal leather apron over a rust-red short-sleeve shirt, dark blue work trousers, thick forearms and shoulders, holding a forging hammer over one shoulder and presenting a delicate metal flower in the other hand, awkward restrained expression becoming quietly proud.',
    'NPC-015': '52-year-old tall lean dark-brown-skinned male soil ecologist and wetland researcher, long face, narrow eyes, high cheekbones, straight nose, salt-and-pepper short beard, slightly asymmetrical ears and lips, close-cropped black-gray hair thinning at the forehead, khaki field vest over a cobalt-blue short-sleeve shirt, olive-green trousers, holding a wetland soil sample box in one hand and pointing at layered soil with a field pen in the other, upright precise posture, serious analytical expression with a hint of childlike delight.',
    'NPC-016': 'adult mountain dwarf merchant, very short compact build, inverted triangular face, huge pointed ears, broad cheekbones, compact midface, round nose, glossy obsidian bead-like eyes, tiny closely spaced teeth, gray-purple skin, short silver-white hair mostly hidden by an indigo hood, bronze goggles, indigo short robe, khaki belt pouches, broad hands, holding an ancient carved stone tablet and a bronze counting frame, half-turned wary stance, stern neutral face with curious eyes, clearly nonhuman and not a handsome human template.',
}

output = pathlib.Path('npc_art_batch_02')
output.mkdir(parents=True, exist_ok=True)
base_url = 'https://image.pollinations.ai/prompt/'

for index, (npc_id, detail) in enumerate(PROMPTS.items(), start=1):
    prompt = BASE + detail
    seed = 8200 + index
    url = (
        base_url + urllib.parse.quote(prompt, safe='')
        + f'?model=flux&width=1024&height=1365&seed={seed}&nologo=true&private=true&enhance=true&safe=true'
    )
    target = output / f'{npc_id}.jpg'
    temp = output / f'{npc_id}.part'
    last_error = None

    for attempt in range(1, 6):
        try:
            subprocess.run(
                [
                    'curl', '-L', '--fail', '--silent', '--show-error',
                    '--retry', '2', '--retry-delay', '5', '--retry-all-errors',
                    '--max-time', '420', '-A', 'Mozilla/5.0',
                    '-o', str(temp), url,
                ],
                check=True,
            )
            size = temp.stat().st_size
            if size < 50000:
                raise RuntimeError(f'downloaded file too small: {size} bytes')
            os.replace(temp, target)
            print(f'generated {npc_id}: {target.stat().st_size} bytes')
            break
        except Exception as exc:
            last_error = exc
            if temp.exists():
                temp.unlink()
            print(f'attempt {attempt} failed for {npc_id}: {exc}')
            time.sleep(10 * attempt)
    else:
        raise RuntimeError(f'failed to generate {npc_id}: {last_error}')

    time.sleep(6)
