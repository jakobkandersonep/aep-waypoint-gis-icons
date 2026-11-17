# AEP Waypoint GIS icons

Pictures for the GIS apps list on Waypoint's proposed GIS page, one per app.

They are the same pictures as the **AEP Mapping Applications** tiles on the Introduction page of each Experience Builder app, drawn by `generate-tiles.py` from the AEP Experience Builder skill. Constraints Mapping, Field Maps and Survey123 aren't in that generator yet, so `make_waypoint_icons.py` draws those three in the same style.

## What's here

| Path | What it is |
| --- | --- |
| `svg/<app>.svg` | The full tile, 480 × 300, with the app name in the white band, as the Experience Builder apps show it |
| `waypoint/<app>.svg` | The illustration only, 480 × 228, with square corners. Waypoint shows the name as text, so the band is cropped off |
| `waypoint-gis-icons.json` | The `waypoint/` pictures as data addresses, `{ "<app>": "data:image/svg+xml;base64,..." }`, ready to put into a page so nothing is fetched |
| `generate-tiles.py` | Copy of the tile generator from the skill (`templates/mapping-apps`) |
| `make_waypoint_icons.py` | Runs the generator, adds the three extra apps and writes the files above |

App ids: `survey-reporter`, `arboriculture`, `project-study-areas`, `atlas-audit`, `habitat-viewer`, `frog-survey-planner`, `bam-plot-editor`, `nearmap-manager`, `equipment-manager`, `constraints-mapping`, `field-maps`, `survey123`.

## Rebuilding

```
python make_waypoint_icons.py
```

Plain Python 3, no packages needed. When an app is added or its picture changes in the Experience Builder skill, copy the new `generate-tiles.py` over this one and run it again.

## Note

The Constraints Mapping picture should move into `generate-tiles.py` in the skill (and into every app's AEP Mapping Applications tiles) once it joins that list, so all the apps share one picture.
