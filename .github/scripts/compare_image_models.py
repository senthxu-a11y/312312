import pathlib
import subprocess
import urllib.parse

prompt = (
    "high quality polished 3D cartoon character for a cozy casual mobile farming game, "
    "single character, thigh-up portrait, three-quarter view, medium gray studio background, "
    "22-year-old petite sturdy female ruins explorer, round face, thick straight eyebrows, "
    "large almond eyes, short upturned nose, plum-purple chin-length bob, cream short sleeve shirt, "
    "black denim short overalls, coral red waist bag, holding a glowing stone shard and an ancient hand-drawn map, "
    "leaning forward with excited discovery expression, soft rounded sculpted forms, warm animated skin, "
    "chunky hair masses, vivid non-neon color, professional mobile game CG, no text, no logo, no anime, no photorealism"
)
models = ["flux", "zimage", "seedream", "seedream5", "gptimage", "gptimage-large", "nanobanana"]
out = pathlib.Path("model_compare")
out.mkdir(exist_ok=True)
base = "https://image.pollinations.ai/prompt/"

success = 0
for index, model in enumerate(models, start=1):
    url = base + urllib.parse.quote(prompt, safe="") + f"?model={model}&width=768&height=1024&seed={9100+index}&nologo=true&private=true&enhance=true"
    target = out / f"NPC-007_{model}.jpg"
    try:
        subprocess.run([
            "curl", "-L", "--fail", "--silent", "--show-error", "--max-time", "420",
            "-A", "Mozilla/5.0", "-o", str(target), url
        ], check=True)
        if target.stat().st_size < 10000:
            raise RuntimeError(f"file too small: {target.stat().st_size}")
        print(f"OK {model}: {target.stat().st_size} bytes")
        success += 1
    except Exception as exc:
        print(f"FAIL {model}: {exc}")
        target.unlink(missing_ok=True)

if success == 0:
    raise RuntimeError("all image models failed")
