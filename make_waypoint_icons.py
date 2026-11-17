"""Builds the GIS app pictures for Waypoint's GIS page from the AEP Mapping Applications tile generator
(generate-tiles.py, from the aep-experience-builder skill), plus three apps that generator doesn't cover yet.
Writes svg/<id>.svg (the full tiles), waypoint/<id>.svg (illustration only, for Waypoint) and
waypoint-gis-icons.json ({id: data address} of the Waypoint versions)."""
import base64, importlib.util, json, os
spec = importlib.util.spec_from_file_location('gt', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'generate-tiles.py'))
gt = importlib.util.module_from_spec(spec); spec.loader.exec_module(gt)
GOLD, SKY, WHITE = gt.GOLD, gt.SKY, gt.WHITE

def art_constraints_mapping():
    # Lots with a hatched constraint overlay and a pin on the Subject Land.
    lots = ''.join(f'<rect x="{x}" y="{y}" width="92" height="64" fill="#fff" fill-opacity="0.10" stroke="#fff" stroke-width="2"/>'
                   for x in (70, 162, 254, 346) for y in (40, 104))
    hatch = ('<defs><pattern id="hz" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             f'<rect width="5" height="12" fill="{GOLD}" fill-opacity="0.75"/></pattern></defs>')
    zone = '<path d="M120,60 C190,30 300,48 340,92 S320,170 240,174 S100,140 120,60 Z" fill="url(#hz)" stroke="#ffc83d" stroke-width="3"/>'
    subject = f'<rect x="254" y="104" width="92" height="64" fill="none" stroke="{SKY}" stroke-width="5"/>'
    return hatch + lots + zone + subject + gt.pin(300, 140, '#1f4d2e', 1.1, GOLD)

def art_field_maps():
    # A phone showing a map with points, held in the field.
    phone = ('<rect x="180" y="18" width="120" height="200" rx="16" fill="#1c221d" stroke="#fff" stroke-width="3"/>'
             '<rect x="190" y="38" width="100" height="160" rx="4" fill="#dfe5d2"/>'
             '<path d="M190,120 C220,96 250,140 290,110" fill="none" stroke="#7fb36a" stroke-width="10" stroke-opacity="0.8"/>'
             '<path d="M190,160 C230,150 250,176 290,162" fill="none" stroke="#7fd3ff" stroke-width="6"/>')
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="6" fill="{GOLD}" stroke="#1c221d" stroke-width="2"/>' for x, y in ((214, 78), (262, 92), (236, 134), (270, 146)))
    hills = '<path d="M0,200 L80,130 L140,176 L200,120 L480,190 L480,228 L0,228 Z" fill="#fff" fill-opacity="0.10"/>'
    return hills + phone + dots + gt.pin(238, 70, '#1b6a7a', 0.7, GOLD) + gt.tree(90, 210, 0.75) + gt.tree(400, 214, 0.6)

def art_survey123():
    # A clipboard form with ticks.
    board = ('<rect x="150" y="26" width="180" height="196" rx="10" fill="#fff" stroke="#1c221d" stroke-width="3"/>'
             '<rect x="205" y="14" width="70" height="26" rx="6" fill="#1c221d"/>')
    rows = ''
    for i, y in enumerate((66, 108, 150, 192)):
        rows += f'<rect x="172" y="{y - 14}" width="22" height="22" rx="3" fill="none" stroke="#1f4d2e" stroke-width="3"/>'
        if i < 3:
            rows += f'<path d="M176,{y - 3} l6,7 l12,-14" fill="none" stroke="#2f6b3f" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
        rows += f'<rect x="206" y="{y - 8}" width="{100 - i * 12}" height="10" rx="5" fill="#cdc6b5"/>'
    return board + rows + gt.pin(370, 120, GOLD, 1.0, '#1f4d2e')

EXTRA = {
    'constraints-mapping': ('Constraints Mapping', 'Lots, planning, SEPP and council constraints for a Project Study Area', '#7a4f0b', '#1b6a7a', art_constraints_mapping),
    'field-maps': ('Field Maps', 'Collect data in the field, online or offline', '#1d4f73', '#2f6b3f', art_field_maps),
    'survey123': ('Survey123', 'Forms for inspections, incidents and surveys', '#245a37', '#b9801a', art_survey123),
}

def main():
    out = {}
    os.makedirs('svg', exist_ok=True)
    tiles = gt.build()
    n = len(tiles)
    for i, (k, (name, blurb, c1, c2, art)) in enumerate(EXTRA.items()):
        tiles[k] = gt.frame(n + i, name, blurb, c1, c2, art())
    for k, svg in tiles.items():
        open(f'svg/{k}.svg', 'w', encoding='utf-8').write(svg)
        # Waypoint shows the name as text, so the page uses the illustration only: name band cropped off, square corners.
        card = svg.replace(f'viewBox="0 0 {gt.W} {gt.H}" width="{gt.W}" height="{gt.H}"', f'viewBox="0 0 {gt.W} {gt.ART_H}" width="{gt.W}" height="{gt.ART_H}"').replace('rx="16"', 'rx="0"')
        os.makedirs('waypoint', exist_ok=True)
        open(f'waypoint/{k}.svg', 'w', encoding='utf-8').write(card)
        out[k] = 'data:image/svg+xml;base64,' + base64.b64encode(card.encode('utf-8')).decode()
    json.dump(out, open('waypoint-gis-icons.json', 'w'), indent=0)
    print('wrote', len(out), 'pictures')

if __name__ == '__main__':
    main()
