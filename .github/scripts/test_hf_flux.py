import pathlib
import shutil
from gradio_client import Client

prompt = (
    "premium polished high quality 3D cartoon NPC for a cozy casual mobile farming management game, "
    "single character only, thigh-up portrait, three-quarter view, medium gray studio background, "
    "22-year-old petite sturdy female ruins explorer, round face, thick straight eyebrows, large almond eyes, "
    "short upturned nose, plum-purple chin-length bob, cream short sleeve shirt, black denim short overalls, "
    "coral-red waist bag, holding a glowing stone shard and an ancient hand-drawn map, leaning forward with an excited discovery expression, "
    "soft rounded sculpted forms, slightly oversized head and hands, smooth warm animated skin, chunky hair masses, "
    "vivid non-neon colors, professional casual mobile farming game CG, no text, no logo, no anime, no photorealism"
)

client = Client("black-forest-labs/FLUX.1-schnell")
result = client.predict(
    prompt=prompt,
    seed=9271,
    randomize_seed=False,
    width=1024,
    height=1365,
    num_inference_steps=4,
    api_name="/infer",
)
print("RESULT:", result)

candidates = []
def collect(value):
    if isinstance(value, str):
        p = pathlib.Path(value)
        if p.exists() and p.is_file():
            candidates.append(p)
    elif isinstance(value, dict):
        for v in value.values():
            collect(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            collect(v)
collect(result)

if not candidates:
    raise RuntimeError(f"No generated file found in result: {result!r}")

out = pathlib.Path("hf_flux_test")
out.mkdir(exist_ok=True)
src = candidates[0]
dst = out / ("NPC-007" + (src.suffix or ".webp"))
shutil.copy2(src, dst)
print("SAVED:", dst, dst.stat().st_size)
