import os
import pathlib
import shutil
import time
from gradio_client import Client

BASE = 'premium polished high quality 3D cartoon NPC character for a cozy casual mobile farming management game, single character only, tight thigh-up portrait cropped exactly at mid-thigh, no knees, no feet, not full body, character fills about 82 percent of the vertical frame, three-quarter view, eye-level medium telephoto lens, complete hands forearms waist and signature props visible inside frame, clean medium gray studio background, adult stylized proportions, not chibi, not childlike, not a doll, head only moderately oversized, medium-sized expressive eyes, distinctive non-generic facial bone structure, slightly oversized readable hands, strong silhouette and visible body type, soft rounded sculpted forms, smooth warm animated skin with subtle cheek and nose blush, no realistic pores, hair built from chunky readable masses, matte fabric with soft rounded folds, vivid saturated but non-neon colors, warm key light, soft rim light, gentle ambient occlusion, professional premium mobile game CG, no text, no UI, no logo, no watermark, no other people, no anime, no photorealism, no generic beauty face. '

PROMPTS = {
    'NPC-007': '22-year-old adult petite sturdy female ruins explorer, short height, round face, thick straight eyebrows, medium-large almond eyes, short upturned nose, short upper lip with a small left canine visible, slight facial asymmetry, chin-length plum-purple bob with outward flipped ends and a silver hairclip on the right, cream short-sleeve shirt, black denim short overalls, purple-gray accessories, coral-red waist bag, holding a fist-sized glowing stone shard in one hand and a compact folded hand-drawn ruins map at chest height in the other, leaning forward with a thrilled discovery expression, adventurous and alert.',
    'NPC-008': '27-year-old adult curvy deep-brown-skinned female tailor and dancer, medium-short height, long heart-shaped face, wide-set medium-large round eyes, short straight nose, full lips, left cheek dimple, slight facial asymmetry, cobalt-blue fluffy short curls tied with a coral fabric bow, patchwork summer dress in lake blue coral red and cream, layered cloth bracelets, holding a compact colorful fabric swatch book in one hand and bright thread scissors in the other, body swaying gently, open radiant smile, artistic and welcoming.',
    'NPC-009': '24-year-old adult tall slender female photographer, narrow oval face, medium cat-shaped eyes, thin nose bridge, small pointed chin, high arched eyebrow tails, defined cupid bow, slight facial asymmetry, honey-blonde shoulder-length straight hair curled inward with a wide pale headband, mustard-yellow cropped summer top, cream high-waisted shorts, thin coral scarf, holding a vintage camera ready to shoot while a compact folded reflector rests under one arm, precise elegant stance, selective professional smile.',
    'NPC-010': '30-year-old adult medium-tall strong female forest sculptor and woodworker, broad rectangular face, thick eyebrows, low nose bridge, freckles, full lips, powerful jaw, slight facial asymmetry, brick-red naturally curly short hair pinned back with a wooden hair stick, olive-green craft apron over a cream tank top, rust-red shorts, sturdy forearms with a little sawdust, holding a palm-sized unfinished carved wooden bird in one hand and a carving knife in the other, grounded relaxed stance, quiet focused smile.',
    'NPC-011': '23-year-old adult compact athletic medium-brown-skinned female mechanical inventor, short-to-medium height, small square face, monolid eyes, short round nose, naturally upturned mouth corners, right eyebrow with a small notch, round protective goggles, deep-brown short curls with volume on top and a lake-blue hair clip, lake-blue mechanic romper, cream short sleeves, orange tool belt, holding a compact miniature sorting robot arm in one hand and explaining it rapidly with the other, leaning forward with intense concentration and excited eyes.',
    'NPC-012': '26-year-old adult slim gentle female library teaching assistant, medium height, pear-shaped face, downturned medium eyes, long narrow nose, thin lips, slightly long midface, one-sided dimple when smiling, slight facial asymmetry, chestnut-red long hair in a low braid with soft wisps, rust-red lightweight knit top, deep navy skirt, cream details, holding a densely annotated lesson notebook against her chest while pointing to a page with colored chalk, shoulders slightly drawn in, warm closed-mouth smile and shy downward gaze.',
    'NPC-013': "48-year-old mature curvy female tea-garden shopkeeper, medium height, soft round face, mature almond eyes, small round nose tip, full lips, subtle crow's feet, slight facial asymmetry, olive skin, deep-green shoulder-length wavy hair gathered into a low bun with a few silver strands, olive-green summer blouse, peach-coral long skirt, cream woven accessories, carrying a compact wicker tea basket at waist height and gently pinching a tea leaf to inspect it, calm reassuring smile, graceful relaxed posture.",
    'NPC-014': '39-year-old adult short broad extremely stocky male blacksmith, huge rectangular face, deep-set small eyes, bulbous garlic-shaped nose, thick lower lip, very wide chin, reddish pale skin with a small spark burn mark on the right cheek, black-brown short hair and dense beard with gray at the temples, charcoal leather apron over a rust-red short-sleeve shirt, dark blue work trousers, thick forearms and shoulders, holding a forging hammer over one shoulder and presenting a delicate metal flower in the other hand, awkward restrained expression becoming quietly proud.',
    'NPC-015': '52-year-old adult tall lean dark-brown-skinned male soil ecologist and wetland researcher, long face, narrow eyes, high cheekbones, straight nose, salt-and-pepper short beard, slightly asymmetrical ears and lips, close-cropped black-gray hair thinning at the forehead, khaki field vest over a cobalt-blue short-sleeve shirt, olive-green trousers, holding a compact wetland soil sample box in one hand and pointing at layered soil with a field pen in the other, upright precise posture, serious analytical expression with a hint of childlike delight.',
    'NPC-016': 'adult mountain dwarf merchant, very short compact muscular build, clearly adult and nonhuman, inverted triangular face, huge pointed ears, broad cheekbones, compact midface, round nose, glossy obsidian bead-like eyes, tiny closely spaced teeth, gray-purple skin, short silver-white hair mostly hidden by an indigo hood, bronze goggles, indigo short robe, khaki belt pouches, broad hands, holding a compact ancient carved stone tablet and a bronze counting frame, half-turned wary stance, stern neutral face with curious eyes, not a handsome human template.',
}

client = Client('black-forest-labs/FLUX.1-schnell')
out = pathlib.Path('hf_flux_batch_02')
out.mkdir(exist_ok=True)

def collect_files(value, found):
    if isinstance(value, str):
        p = pathlib.Path(value)
        if p.exists() and p.is_file():
            found.append(p)
    elif isinstance(value, dict):
        for v in value.values():
            collect_files(v, found)
    elif isinstance(value, (list, tuple)):
        for v in value:
            collect_files(v, found)

requested = [x.strip() for x in os.environ.get('NPC_IDS', '').split(',') if x.strip()]
selected = [(k, PROMPTS[k]) for k in requested] if requested else list(PROMPTS.items())

for index, (npc_id, detail) in enumerate(selected, start=1):
    prompt = BASE + detail
    result = client.predict(
        prompt=prompt,
        seed=10400 + index,
        randomize_seed=False,
        width=1024,
        height=1365,
        num_inference_steps=5,
        api_name='/infer',
    )
    candidates = []
    collect_files(result, candidates)
    if not candidates:
        raise RuntimeError(f'No image returned for {npc_id}: {result!r}')
    src = candidates[0]
    suffix = src.suffix.lower() if src.suffix else '.webp'
    dst = out / f'{npc_id}{suffix}'
    shutil.copy2(src, dst)
    print(f'SAVED {npc_id}: {dst} ({dst.stat().st_size} bytes)')
    time.sleep(1)
