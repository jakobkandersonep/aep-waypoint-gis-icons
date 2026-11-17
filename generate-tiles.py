r"""Draws the tile images for the "AEP Mapping Applications" section of an Experience Builder app's Introduction page, one 480 x 300 vector image
per app (an illustration of what the app does and its name; the one-line description is shown as text under the image), and writes them as:

  <out>/tiles/<id>.svg                    the images, to look at or reuse
  <widget runtime folder>/tiles.ts        the same images as data addresses (APP_TILES), so a widget needs nothing fetched

  python experience-builder/scripts/generate-tiles.py [--svg-dir DIR] [--ts FILE]

To add an app: add it to APPS here and to MAPPING_APPS in apps.ts, add a drawing function to ART, and run this. To change the look of every tile change
frame(). The colours are the AEP palette (eucalypt green, wattle gold, water teal, sky blue). No dependencies: the images are plain SVG text.
Standard component, 2026-11-04: see templates/mapping-apps in the aep-experience-builder skill.
"""
import argparse, base64, os

W, H = 480, 300
BAND = 72                # the white band along the bottom that holds the name (the description is real text under the image, see MappingApps.tsx)
ART_H = H - BAND         # height of the illustration area
FONT = "'Segoe UI', Arial, Helvetica, sans-serif"

# id -> (name, description, gradient top, gradient bottom). The text is also in apps.ts; keep the two in step.
APPS = {
    'survey-reporter': ('Survey Reporter', 'Import survey GPS tracks, check them and report survey effort', '#245a37', '#1b6a7a'),
    'arboriculture': ('Arboriculture Assessment', 'Tree crowns, protection zones and encroachment', '#2f6b3f', '#8bb04f'),
    'project-study-areas': ('Manage Project Study Areas', 'Create and maintain Project Study Areas and Subject Land', '#1b6a7a', '#1d4f73'),
    'atlas-audit': ('Atlas Audit', 'Audit Atlas sightings and species records', '#b9801a', '#7a4f0b'),
    'habitat-viewer': ('Habitat Viewer', 'Habitat trees, hollows, reports and species matrices', '#2e5e3a', '#6f8f3c'),
    'frog-survey-planner': ('Frog Survey Planner', 'Plan frog surveys around rain, weather and staff', '#1b6a7a', '#2d8ab8'),
    'bam-plot-editor': ('BAM Plot Editor', 'Edit and check BAM vegetation plot data', '#6d4c2f', '#b0803a'),
    'nearmap-manager': ('Nearmap Manager', 'See Nearmap images for a project, find newer surveys and download them', '#1d4f73', '#2e6b3f'),
    'equipment-manager': ('Equipment Manager', 'Track survey equipment, set Field Maps inspection tasks and load camera trap sightings', '#2f6b3f', '#1b6a7a'),
}

GOLD, SKY, WHITE = '#ffc83d', '#7fd3ff', '#ffffff'


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def frame(uid, name, blurb, c1, c2, art):
    """The common tile: rounded corners, a colour wash, faint map contours, the illustration, and the white band with the name and description."""
    contours = ''.join(
        f'<path d="M-10,{y} C90,{y - 34} 170,{y + 30} 250,{y - 6} S400,{y - 30} 500,{y + 8}" fill="none" stroke="#fff" stroke-opacity="0.10" stroke-width="1.6"/>'
        for y in (36, 78, 120, 162))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(name)}: {esc(blurb)}">
<defs><linearGradient id="g{uid}" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<clipPath id="c{uid}"><rect width="{W}" height="{H}" rx="16"/></clipPath></defs>
<g clip-path="url(#c{uid})">
<rect width="{W}" height="{H}" fill="url(#g{uid})"/>
{contours}
<g>{art}</g>
<rect y="{ART_H}" width="{W}" height="{BAND}" fill="#ffffff" fill-opacity="0.96"/>
<rect y="{ART_H}" width="{W}" height="3" fill="{GOLD}"/>
<text x="24" y="{ART_H + 49}" font-family="{FONT}" font-size="{min(36, int(430 / (len(name) * 0.58)))}" font-weight="700" fill="#1f4d2e">{esc(name)}</text>
</g></svg>
'''


def pin(x, y, fill, scale=1.0, inner='#fff'):
    """A map pin whose point is at (x, y)."""
    s = scale
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M0,0 C-6,-12 -17,-22 -17,-34 C-17,-44 -9,-52 0,-52 C9,-52 17,-44 17,-34 C17,-22 6,-12 0,0 Z" '
            f'fill="{fill}" stroke="#fff" stroke-width="3"/><circle cx="0" cy="-34" r="7" fill="{inner}"/></g>')


def tree(cx, base, scale=1.0, crown='#1f5a2f', light='#2f7d3f', trunk='#7a5230'):
    """A tree standing at (cx, base)."""
    s = scale
    return (f'<g transform="translate({cx},{base}) scale({s})"><rect x="-9" y="-58" width="18" height="58" rx="4" fill="{trunk}"/>'
            f'<circle cx="0" cy="-92" r="36" fill="{crown}"/><circle cx="-30" cy="-72" r="27" fill="{crown}"/><circle cx="30" cy="-72" r="27" fill="{crown}"/>'
            f'<circle cx="-8" cy="-100" r="22" fill="{light}" fill-opacity="0.65"/></g>')


# ---- one illustration per app (each fits in 480 x ART_H) ----

def art_survey_reporter():
    return (
        '<path d="M64,152 L116,56 L300,36 L412,96 L384,170 L190,184 Z" fill="#fff" fill-opacity="0.13" stroke="#fff" stroke-width="2.2" stroke-dasharray="7 5"/>'
        f'<path d="M88,150 C128,100 150,152 192,110 S252,66 292,100 S340,152 380,128" fill="none" stroke="{SKY}" stroke-width="5" stroke-linecap="round"/>'
        f'<path d="M118,170 C160,138 200,174 246,148 S322,114 354,150" fill="none" stroke="{GOLD}" stroke-width="4" stroke-linecap="round" stroke-dasharray="1 9"/>'
        '<circle cx="88" cy="150" r="8" fill="#fff" stroke="#1f4d2e" stroke-width="3"/><circle cx="380" cy="128" r="8" fill="#1f4d2e" stroke="#fff" stroke-width="3"/>'
        + pin(414, 72, GOLD, 1.0, '#fff') +
        f'<text x="414" y="40" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="#1f4d2e">GPX</text>'
        '<g transform="translate(46,40)"><rect width="58" height="32" rx="6" fill="#fff" fill-opacity="0.92"/>'
        f'<text x="29" y="22" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="700" fill="#1f4d2e">5948</text></g>'
    )


def art_arboriculture():
    return (
        '<ellipse cx="226" cy="156" rx="118" ry="38" fill="#fff" fill-opacity="0.10" stroke="#fff" stroke-width="2.4" stroke-dasharray="8 6"/>'
        f'<ellipse cx="226" cy="156" rx="64" ry="21" fill="{GOLD}" fill-opacity="0.22" stroke="{GOLD}" stroke-width="3" stroke-dasharray="6 4"/>'
        + tree(226, 162, 0.92) +
        '<polygon points="318,112 424,100 436,164 326,178" fill="#fff" fill-opacity="0.30" stroke="#ffb4a8" stroke-width="3" stroke-dasharray="7 5"/>'
        '<polygon points="318,125 344,122 346,160 326,164" fill="#e53935" fill-opacity="0.55"/>'
        f'<text x="82" y="152" font-family="{FONT}" font-size="20" font-weight="700" fill="#fff">NRZ</text>'
        f'<text x="176" y="176" font-family="{FONT}" font-size="18" font-weight="700" fill="{GOLD}">SRZ</text>'
    )


def art_project_study_areas():
    grid = ''.join(f'<line x1="{x}" y1="14" x2="{x - 16}" y2="{ART_H - 8}" stroke="#fff" stroke-opacity="0.10" stroke-width="1.4"/>' for x in range(70, 460, 64))
    sq = lambda x, y: f'<rect x="{x - 6}" y="{y - 6}" width="12" height="12" rx="2" fill="#fff" stroke="#1b6a7a" stroke-width="2.5"/>'
    outer = [(92, 138), (130, 52), (292, 36), (410, 82), (394, 160), (210, 182)]
    inner = [(176, 130), (214, 84), (316, 78), (352, 120), (300, 152)]
    pts = lambda p: ' '.join(f'{x},{y}' for x, y in p)
    return (
        grid +
        f'<polygon points="{pts(outer)}" fill="#fff" fill-opacity="0.14" stroke="#fff" stroke-width="3.4" stroke-linejoin="round"/>'
        f'<polygon points="{pts(inner)}" fill="{GOLD}" fill-opacity="0.55" stroke="{GOLD}" stroke-width="3" stroke-linejoin="round"/>'
        + ''.join(sq(x, y) for x, y in outer) +
        '<g transform="translate(398,126)"><path d="M0,0 L0,34 L9,26 L15,40 L22,37 L16,24 L28,24 Z" fill="#fff" stroke="#1f4d2e" stroke-width="2.4" stroke-linejoin="round"/></g>'
        '<g transform="translate(30,140)"><rect width="128" height="34" rx="7" fill="#fff" fill-opacity="0.94"/>'
        f'<text x="64" y="24" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="700" fill="#1b6a7a">Subject Land</text></g>'
    )


def art_atlas_audit():
    roads = ('<path d="M20,60 C120,90 200,30 300,70 S440,110 470,80" fill="none" stroke="#fff" stroke-opacity="0.22" stroke-width="7"/>'
             '<path d="M40,170 C140,120 250,176 330,132 S430,150 470,140" fill="none" stroke="#fff" stroke-opacity="0.18" stroke-width="6"/>')
    return (
        roads
        + pin(92, 92, '#2e7d32', 0.8) + pin(132, 166, '#e53935', 0.8) + pin(396, 84, '#2e7d32', 0.8) + pin(420, 156, '#e53935', 0.8) + pin(356, 176, '#2e7d32', 0.7) +
        '<circle cx="244" cy="96" r="58" fill="#fff" fill-opacity="0.20" stroke="#fff" stroke-width="9"/>'
        '<line x1="286" y1="138" x2="332" y2="184" stroke="#fff" stroke-width="13" stroke-linecap="round"/>'
        '<path d="M214,98 L236,122 L278,70" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M214,98 L236,122 L278,70" fill="none" stroke="#2e7d32" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def art_habitat_viewer():
    cells = []
    palette = ['#7ccf7a', '#f2b84b', '#e9788f', '#d6dbd0', '#7ccf7a', '#7ccf7a', '#f2b84b', '#d6dbd0', '#e9788f', '#7ccf7a', '#7ccf7a', '#f2b84b']
    for i, c in enumerate(palette):
        x, y = 262 + (i % 4) * 46, 44 + (i // 4) * 46
        cells.append(f'<rect x="{x}" y="{y}" width="38" height="38" rx="6" fill="{c}" stroke="#fff" stroke-width="2"/>')
    return (
        '<path d="M110,200 C118,150 112,110 120,56 C124,34 188,34 192,56 C198,110 192,150 204,200 Z" fill="#8a5a2b"/>'
        '<path d="M130,200 C134,150 130,110 134,60" fill="none" stroke="#6b4320" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M178,200 C176,150 180,112 176,66" fill="none" stroke="#a6733b" stroke-width="3" stroke-linecap="round"/>'
        '<ellipse cx="156" cy="82" rx="16" ry="26" fill="#2b1b0e" stroke="#c99a5b" stroke-width="3"/>'
        '<ellipse cx="148" cy="142" rx="11" ry="17" fill="#2b1b0e" stroke="#c99a5b" stroke-width="3"/>'
        '<ellipse cx="170" cy="178" rx="9" ry="9" fill="#2b1b0e" stroke="#c99a5b" stroke-width="3"/>'
        + ''.join(cells) +
        '<path d="M420,176 C426,166 436,166 440,174 C444,166 454,166 460,176 C452,172 446,178 440,184 C434,178 428,172 420,176 Z" fill="#fff" fill-opacity="0.9"/>'
    )


def art_frog_survey_planner():
    rain = ''.join(f'<line x1="{x}" y1="{y}" x2="{x - 7}" y2="{y + 17}" stroke="#fff" stroke-opacity="0.65" stroke-width="3" stroke-linecap="round"/>'
                   for x, y in ((250, 18), (290, 44), (330, 14), (372, 40), (412, 20), (452, 46), (310, 80), (390, 84), (440, 100), (270, 90)))
    days = []
    cols = ['#7ccf7a', '#7ccf7a', '#d6dbd0', '#f2b84b', '#7ccf7a', '#d6dbd0', '#d6dbd0', '#f2b84b', '#7ccf7a', '#7ccf7a', '#d6dbd0', '#7ccf7a']
    for i, c in enumerate(cols):
        days.append(f'<rect x="{40 + (i % 4) * 36}" y="{44 + (i // 4) * 34}" width="30" height="28" rx="5" fill="{c}" stroke="#fff" stroke-width="1.8"/>')
    return (
        rain
        + '<rect x="30" y="34" width="156" height="114" rx="10" fill="#fff" fill-opacity="0.18" stroke="#fff" stroke-width="2.4"/>'
        + ''.join(days).replace('x="40"', 'x="42"')
        + '<g transform="translate(300,166)">'
        '<ellipse cx="-14" cy="-6" rx="70" ry="38" fill="#79cf68" stroke="#2f7d32" stroke-width="3"/>'
        '<ellipse cx="42" cy="-30" rx="38" ry="31" fill="#79cf68" stroke="#2f7d32" stroke-width="3"/>'
        '<circle cx="30" cy="-58" r="13" fill="#fff" stroke="#2f7d32" stroke-width="3"/><circle cx="56" cy="-58" r="13" fill="#fff" stroke="#2f7d32" stroke-width="3"/>'
        '<circle cx="33" cy="-57" r="6" fill="#1f1f1f"/><circle cx="59" cy="-57" r="6" fill="#1f1f1f"/>'
        '<path d="M30,-20 Q50,-8 74,-20" fill="none" stroke="#2f7d32" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M-60,12 C-92,12 -98,32 -70,36 L-30,32 Z" fill="#79cf68" stroke="#2f7d32" stroke-width="3" stroke-linejoin="round"/>'
        '<path d="M22,20 C34,36 52,40 62,34 L60,22 Z" fill="#79cf68" stroke="#2f7d32" stroke-width="3" stroke-linejoin="round"/>'
        '<ellipse cx="-14" cy="12" rx="44" ry="18" fill="#bfe8a6" fill-opacity="0.8"/></g>'
        '<path d="M400,150 C400,140 410,130 410,130 C410,130 420,140 420,150 C420,158 415,163 410,163 C405,163 400,158 400,150 Z" fill="#fff" fill-opacity="0.85"/>'
    )


def art_bam_plot_editor():
    ticks = ''.join(f'<line x1="{150 + i * 20}" y1="186" x2="{150 + i * 20}" y2="{196 if i % 5 else 202}" stroke="#2b1b0e" stroke-width="2"/>' for i in range(0, 9))
    sq = lambda x, y: f'<rect x="{x - 8}" y="{y - 8}" width="16" height="16" fill="#fff" stroke="#6d4c2f" stroke-width="3"/>'
    rows = ''.join(f'<rect x="372" y="{58 + i * 24}" width="12" height="12" rx="2" fill="none" stroke="#6d4c2f" stroke-width="2"/>'
                   f'<line x1="392" y1="{64 + i * 24}" x2="{392 + (44 if i % 2 else 56)}" y2="{64 + i * 24}" stroke="#8d6e63" stroke-width="3" stroke-linecap="round"/>' for i in range(4))
    return (
        '<rect x="150" y="38" width="160" height="148" fill="#fff" fill-opacity="0.12" stroke="#fff" stroke-width="3.4"/>'
        '<line x1="230" y1="38" x2="230" y2="186" stroke="#fff" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="6 5"/>'
        '<line x1="150" y1="112" x2="310" y2="112" stroke="#fff" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="6 5"/>'
        + sq(150, 38) + sq(310, 38) + sq(150, 186) + sq(310, 186) +
        f'<circle cx="188" cy="76" r="8" fill="{GOLD}" stroke="#fff" stroke-width="2.5"/><circle cx="262" cy="148" r="8" fill="{GOLD}" stroke="#fff" stroke-width="2.5"/>'
        '<circle cx="272" cy="70" r="8" fill="#7ccf7a" stroke="#fff" stroke-width="2.5"/>'
        f'<rect x="146" y="180" width="168" height="10" fill="{GOLD}" stroke="#2b1b0e" stroke-width="1.5"/>' + ticks +
        '<rect x="356" y="30" width="96" height="124" rx="10" fill="#fff" fill-opacity="0.95"/><rect x="386" y="22" width="36" height="16" rx="5" fill="#8d6e63"/>' + rows
    )


def art_nearmap_manager():
    """A mosaic of aerial image tiles with the Project Study Area outlined and the buffered download rectangle over it, a 'NEW' survey badge and a download arrow."""
    greens = ['#5c8f4b', '#7aa05a', '#8d9a62', '#b59c6a', '#4a7c3f', '#6f8f52', '#9aa56a', '#a98f5f', '#5f8a4a', '#7d9a58', '#4f7f45', '#b0a070']
    cells = []
    for i, c in enumerate(greens):
        x, y = 40 + (i % 4) * 66, 26 + (i // 4) * 52
        cells.append(f'<rect x="{x}" y="{y}" width="62" height="48" rx="5" fill="{c}" stroke="#fff" stroke-width="2"/>')
    road = '<path d="M36,176 C110,150 150,120 220,112 S300,70 312,34" fill="none" stroke="#e6e2d6" stroke-width="9" stroke-linecap="round" stroke-opacity="0.9"/>'
    site = '<polygon points="100,74 152,50 214,64 232,112 190,140 120,128" fill="#fff" fill-opacity="0.22" stroke="#fff" stroke-width="3.2" stroke-linejoin="round"/>'
    buffer = f'<rect x="76" y="34" width="180" height="128" rx="4" fill="none" stroke="{GOLD}" stroke-width="3.6" stroke-dasharray="9 6"/>'
    badge = (f'<g transform="translate(212,18)"><rect width="76" height="32" rx="16" fill="{GOLD}" stroke="#fff" stroke-width="2.4"/>'
             f'<text x="38" y="23" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="700" fill="#1f4d2e">NEW</text></g>')
    download = ('<g transform="translate(392,112)"><circle r="58" fill="#fff" fill-opacity="0.96"/>'
                '<path d="M0,-30 L0,12" stroke="#1f4d2e" stroke-width="12" stroke-linecap="round"/>'
                '<path d="M-22,-8 L0,16 L22,-8" fill="none" stroke="#1f4d2e" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="M-28,32 L28,32" stroke="{GOLD}" stroke-width="9" stroke-linecap="round"/></g>')
    return ''.join(cells) + road + site + buffer + badge + download


def art_equipment_manager():
    """A camera trap strapped to a tree, with a task tick and a fauna footprint."""
    return (
        '<rect x="196" y="38" width="22" height="190" rx="8" fill="#6d4c2f" opacity="0.9"/>'
        '<rect x="170" y="92" width="74" height="64" rx="10" fill="#2a2a2a" stroke="#ffc83d" stroke-width="3"/>'
        '<circle cx="207" cy="124" r="17" fill="#1b6a7a" stroke="#7fd3ff" stroke-width="4"/><circle cx="207" cy="124" r="6" fill="#7fd3ff"/>'
        '<rect x="178" y="100" width="12" height="7" rx="2" fill="#ffc83d"/>'
        '<rect x="300" y="70" width="120" height="96" rx="10" fill="#ffffff" opacity="0.95"/>'
        '<path d="M318 98 l10 10 l18 -20" fill="none" stroke="#2f6b3f" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="354" y="94" width="52" height="8" rx="4" fill="#90a4ae"/>'
        '<path d="M318 138 l10 10 l18 -20" fill="none" stroke="#ffc83d" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
        '<rect x="354" y="134" width="40" height="8" rx="4" fill="#90a4ae"/>'
        '<g fill="#ffffff" opacity="0.85"><ellipse cx="88" cy="176" rx="14" ry="18"/><circle cx="70" cy="150" r="6"/><circle cx="84" cy="142" r="6"/><circle cx="99" cy="143" r="6"/><circle cx="110" cy="153" r="6"/></g>'
    )


ART = {
    'survey-reporter': art_survey_reporter, 'arboriculture': art_arboriculture, 'project-study-areas': art_project_study_areas,
    'atlas-audit': art_atlas_audit, 'habitat-viewer': art_habitat_viewer, 'frog-survey-planner': art_frog_survey_planner, 'bam-plot-editor': art_bam_plot_editor,
    'nearmap-manager': art_nearmap_manager, 'equipment-manager': art_equipment_manager
}


def thumbnail(app_id):
    """The same picture at 480 x 320 (3:2), the shape of an ArcGIS Online item thumbnail (render it at 600 x 400)."""
    global H, ART_H
    saved = H, ART_H
    H = 320
    ART_H = H - BAND
    try:
        name, blurb, c1, c2 = APPS[app_id]
        return frame('t' + app_id, name, blurb, c1, c2, ART[app_id]()).replace('height="320" rx="16"', 'height="320" rx="0"')    # square corners: the portal rounds the thumbnail itself
    finally:
        H, ART_H = saved


def build():
    return {app_id: frame(i, name, blurb, c1, c2, ART[app_id]()) for i, (app_id, (name, blurb, c1, c2)) in enumerate(APPS.items())}


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(here, '..')
    ap = argparse.ArgumentParser()
    ap.add_argument('--svg-dir', default=os.path.join(root, 'mapping-apps', 'tiles'))
    ap.add_argument('--ts', default=os.path.join(root, 'widgets', 'gpx-introduction', 'src', 'runtime', 'mapping-apps', 'tiles.ts'))
    args = ap.parse_args()
    tiles = build()
    os.makedirs(args.svg_dir, exist_ok=True)
    os.makedirs(os.path.dirname(args.ts), exist_ok=True)
    for app_id, svg in tiles.items():
        open(os.path.join(args.svg_dir, f'{app_id}.svg'), 'w', encoding='utf-8').write(svg)
    lines = ['// GENERATED by scripts/generate-tiles.py. Do not edit by hand: change the script and run it again.',
             '// The tile image of each AEP mapping application (a 480 x 300 vector image) as a data address, so the Introduction page fetches nothing.',
             'export const APP_TILES: Record<string, string> = {']
    for app_id, svg in tiles.items():
        lines.append(f"  '{app_id}': 'data:image/svg+xml;base64,{base64.b64encode(svg.encode('utf-8')).decode()}',")
    lines.append('}')
    open(args.ts, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('wrote', len(tiles), 'tiles to', args.svg_dir, 'and', args.ts)


if __name__ == '__main__':
    main()
