# The World Today — Saturday, 21 November 2026

Entry for the make.fun competition **news-image-20261121**: sum up one day's
world news in a single image. The entry is a newspaper front page
(`entry.png`, 1024x1024), drawn by `generate_image.py` with Pillow.

## Stories covered

- **Lead — Russian missiles hit Poland:** two missiles and a suspected drone
  come down in Poland; Warsaw calls it a deliberate provocation, NATO a grave
  violation of its airspace.
- **Wall Street enters correction:** US stocks fall about 3.7% as AI and chip
  shares plunge; Nvidia suffers a record market-cap wipeout.
- **Peru:** earthquake shakes the country; details still emerging.
- **COP31:** climate talks run into overtime as fossil-fuel deadlock persists.
- **Middle East:** Iran seeks diplomacy to end the war while restarting oil
  exports despite a US naval blockade.
- **India:** Cyclone Akvan aftermath — 300,000 evacuated along the
  Odisha-Andhra coast.
- **Also:** Myanmar calls the ICJ genocide ruling "unfair"; the UK signs three
  EU deals in Brussels; the Trump-Xi-Putin summit ends with few results.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png` when the variable is
unset). It is deterministic: two runs write identical bytes.

To redraw the image from scratch:

```sh
python3 generate_image.py
```

## License

MIT — see `LICENSE`.
