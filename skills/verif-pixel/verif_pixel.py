import argparse
import os
import sys

import numpy as np
from PIL import Image


def load(path):
    return Image.open(path).convert("RGB")


def main():
    p = argparse.ArgumentParser(description="Comparaison au pixel ref / actual")
    p.add_argument("--ref", required=True, help="fichier, ou dossier (mode lot: PNG de meme nom)")
    p.add_argument("--actual", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--seuil-pct", type=float, default=0.5)
    p.add_argument("--tolerance", type=int, default=8)
    p.add_argument("--grille", type=int, default=8)
    p.add_argument("--ignore-bord", type=int, default=0, help="ignorer une bande de N px sur chaque bord (ombres, liseres)")
    p.add_argument("--zoom", type=float, default=2.0, help="agrandissement de zoomN.png")
    a = p.parse_args()

    if os.path.isdir(a.ref):
        return lot(a)
    return un(a)


def lot(a):
    worst, res = 0, []
    for nom in sorted(os.listdir(a.ref)):
        act = os.path.join(a.actual, nom)
        if nom.lower().endswith(".png") and os.path.exists(act):
            b = argparse.Namespace(**vars(a))
            b.ref, b.actual, b.out = os.path.join(a.ref, nom), act, os.path.join(a.out, nom[:-4])
            rc = un(b, quiet=True)
            res.append("%s %s" % ("OK   " if rc == 0 else "ECART", nom))
            worst = max(worst, rc)
    print(chr(10).join(res) + chr(10) + "details: rapport.txt / ecart.png / zoom1-3.png dans " + a.out + "/<nom>")
    return worst


def un(a, quiet=False):
    os.makedirs(a.out, exist_ok=True)
    ref, act = load(a.ref), load(a.actual)
    rapport = os.path.join(a.out, "rapport.txt")

    if ref.size != act.size:
        txt = "TAILLE DIFFERENTE ref %dx%d / actual %dx%d" % (ref.size + act.size)
        with open(rapport, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt + "\n")
        print(txt)
        return 2

    r = np.asarray(ref, dtype=np.int16)
    c = np.asarray(act, dtype=np.int16)
    mask = (np.abs(r - c) > a.tolerance).any(axis=2)
    b = a.ignore_bord
    if b:
        mask[:b, :] = mask[-b:, :] = False
        mask[:, :b] = mask[:, -b:] = False
    h, w = mask.shape
    pct = 100.0 * mask.sum() / mask.size
    ok = pct <= a.seuil_pct

    n = max(1, a.grille)
    ys = np.linspace(0, h, n + 1).astype(int)
    xs = np.linspace(0, w, n + 1).astype(int)
    cells = []
    for i in range(n):
        for j in range(n):
            sub = mask[ys[i]:ys[i + 1], xs[j]:xs[j + 1]]
            if sub.size and sub.any():
                cells.append((100.0 * sub.sum() / sub.size, xs[j], ys[i], xs[j + 1] - 1, ys[i + 1] - 1))
    cells.sort(reverse=True)

    lines = [
        "%s taille %dx%d" % ("OK" if ok else "ECART", w, h),
        "pixels differents: %.3f%% (seuil %.3f%%, tolerance %d/canal, bord ignore %d px)" % (pct, a.seuil_pct, a.tolerance, b),
    ]
    if cells:
        lines.append("5 cellules les plus fautives (grille %dx%d):" % (n, n))
        for k, (cp, x0, y0, x1, y1) in enumerate(cells[:5], 1):
            lines.append("%d. %.2f%% zone x%d,y%d - x%d,y%d" % (k, cp, x0, y0, x1, y1))
    else:
        lines.append("aucune cellule en ecart")
    txt = "\n".join(lines)

    if not ok:
        red = np.zeros((h, w, 3), dtype=np.uint8)
        red[mask] = (255, 0, 0)
        trio = Image.new("RGB", (w * 3, h), (255, 255, 255))
        trio.paste(ref, (0, 0))
        trio.paste(act, (w, 0))
        trio.paste(Image.fromarray(red), (2 * w, 0))
        if trio.width > 1600:
            trio = trio.resize((1600, max(1, round(h * 1600 / trio.width))), Image.LANCZOS)
        trio.save(os.path.join(a.out, "ecart.png"))
        txt += "\necart.png ecrit dans " + a.out
        for k, (_, x0, y0, x1, y1) in enumerate(cells[:3], 1):
            ys_, xs_ = np.nonzero(mask[y0:y1 + 1, x0:x1 + 1])
            bx0, by0 = x0 + xs_.min(), y0 + ys_.min()
            bx1, by1 = x0 + xs_.max(), y0 + ys_.max()
            box = (max(0, bx0 - 20), max(0, by0 - 20), min(w, bx1 + 21), min(h, by1 + 21))
            bw, bh = box[2] - box[0], box[3] - box[1]
            z = Image.new("RGB", (bw * 2, bh), (255, 255, 255))
            z.paste(ref.crop(box), (0, 0))
            z.paste(act.crop(box), (bw, 0))
            if a.zoom != 1:
                z = z.resize((max(1, int(z.width * a.zoom)), max(1, int(z.height * a.zoom))), Image.LANCZOS)
            z.save(os.path.join(a.out, "zoom%d.png" % k))
            txt += "\nzoom%d.png (ref | actual) bbox x%d,y%d - x%d,y%d" % (k, bx0, by0, bx1, by1)

    with open(rapport, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt + "\n")
    if not quiet:
        print(txt)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
