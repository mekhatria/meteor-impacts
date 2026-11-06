# Meteor impacts

Two animated Highcharts Maps dashboards. Each one has a play button, a speed control, light, dark and auto themes, impact effects, and synthesized orchestral sound.

| Page | What it shows |
|---|---|
| `fireballs.html` | 888 fireballs (atmospheric impacts) located by US government sensors, 1988 to 2026. They are animated year by year, and bubble area shows estimated impact energy. |
| `craters.html` | 195 confirmed impact structures on Earth. They are animated through 17 geologic periods, and bubble width shows crater diameter. |
| `*-grey.html` | The same pages, with earlier impacts fading to slate grey instead of blue. |

New impacts appear in red with a glow and shockwave rings, then fade to blue after about a second. Sound is generated with the Web Audio API, so the project needs no audio files. It plays a string pad on Dm, B♭, F and C. Each impact plays a harp note from the current chord, and big impacts add bass and timpani. Loudness follows impact size. Sound starts only after the viewer presses Play.

## Build

The pages are single self-contained HTML files. They load Highcharts 13.1.1 and the world map from jsDelivr.

```sh
./build.sh            # rebuild all four pages from src/ and data/
./build.sh --refresh  # download the latest NASA/JPL fireball feed first
```

- `src/template.html` holds the shared page markup, styles and scripts.
- `src/prep.py` cleans both datasets and works out the crater age periods.
- `src/split.py` writes the craters and fireballs pages and their grey variants.

Edit `src/template.html`, then run `./build.sh`. Don't edit the generated `*.html` files directly.

## Data and licences

- **Fireballs:** the [NASA/JPL CNEOS Fireball Data API](https://ssd-api.jpl.nasa.gov/doc/fireball.html), retrieved on 6 Nov 2026 and saved as `data/cneos_fireballs_raw.json`. It is a US Government work and in the public domain. 888 of the 1,074 reported events have a location. Impact energy is NASA's estimate from the light each fireball radiated.
- **Craters:** [Wikipedia, List of impact structures on Earth](https://en.wikipedia.org/wiki/List_of_impact_structures_on_Earth), saved as `data/craters.json` and licensed under CC BY-SA 4.0. Any reuse of this data must keep that licence. 195 of the 204 structures have coordinates. When only an age range is known, the crater is placed at the midpoint. When only an upper limit is known, it is placed at that limit.
- `data/fireballs.json` is an earlier extract of the same NASA feed. The build doesn't use it.
