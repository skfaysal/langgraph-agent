# Excalidraw Diagram Generator

Generate a clean, well-structured, human-readable Excalidraw diagram for: **$ARGUMENTS**

---

## Phase 1 — Plan the Layout

Before writing any JSON, reason through the diagram structure:

1. **Identify elements**: List all nodes (boxes/shapes) and edges (arrows/lines) needed.
2. **Choose a layout strategy**:
   - **Top-to-bottom flowchart**: Start at y=80. Each level adds 140px. Nodes are centered horizontally, spaced 220px apart.
   - **Left-to-right sequence**: Start at x=80. Each step adds 220px. Keep y constant per row.
   - **Hierarchical tree**: Root at top-center. Children spread evenly below, avoiding overlaps.
   - **Mind map**: Central node at (600, 400). Branches radiate outward with 200px gap.
3. **Size nodes properly**: Width = 160–200px, Height = 60–80px for text to breathe. Labels must fit — if a label exceeds 18 characters, widen the node by 10px per extra character.
4. **Spacing rules**:
   - Minimum 60px vertical gap between node edges.
   - Minimum 40px horizontal gap between node edges.
   - Arrow labels (if any) must not overlap node boundaries.
5. **Color coding** (use consistently throughout):
   - Start/End nodes: `backgroundColor: "#d3f9d8"` (green tint)
   - Process/Action nodes: `backgroundColor: "#dbe4ff"` (blue tint)
   - Decision nodes (diamond): `backgroundColor: "#fff3bf"` (yellow tint)
   - External/IO nodes: `backgroundColor: "#ffe8cc"` (orange tint)
   - Default stroke: `"#1e1e1e"`, strokeWidth: 2

---

## Phase 2 — Generate the Excalidraw JSON

Output the full diagram as a single valid JSON block. Use this exact schema:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    {
      "type": "rectangle",
      "id": "node-1",
      "x": 400,
      "y": 80,
      "width": 180,
      "height": 64,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "#d3f9d8",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "roundness": { "type": 3 },
      "groupIds": [],
      "boundElements": [
        { "type": "text", "id": "label-1" },
        { "type": "arrow", "id": "arrow-1" }
      ]
    },
    {
      "type": "text",
      "id": "label-1",
      "x": 410,
      "y": 100,
      "width": 160,
      "height": 24,
      "text": "Node Label",
      "fontSize": 16,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "node-1",
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 1,
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "boundElements": []
    },
    {
      "type": "arrow",
      "id": "arrow-1",
      "x": 490,
      "y": 144,
      "width": 0,
      "height": 80,
      "points": [[0, 0], [0, 80]],
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "startBinding": { "elementId": "node-1", "focus": 0, "gap": 1 },
      "endBinding": { "elementId": "node-2", "focus": 0, "gap": 1 },
      "startArrowhead": null,
      "endArrowhead": "arrow",
      "groupIds": [],
      "boundElements": []
    }
  ],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

### JSON Rules (strictly enforce):
- Every `rectangle`/`ellipse`/`diamond` node **must** have a paired `text` element with `"containerId"` pointing to it.
- Every `text` inside a container: set `x = node.x + 10`, `y = node.y + (node.height/2 - fontSize/2)`, `width = node.width - 20`.
- Every arrow's `x,y` must be the exact exit point of the source node edge, not a random coordinate.
- IDs must be unique strings (e.g., `"node-1"`, `"label-1"`, `"arrow-1"`).
- `boundElements` on each node must list all arrows and its label.
- For **decision nodes**, use `"type": "diamond"`.
- For **process nodes**, use `"type": "rectangle"` with `"roundness": { "type": 3 }`.
- For **terminal nodes** (start/end), use `"type": "ellipse"`.

---

## Phase 3 — Self-Review Checklist

After generating the JSON, go through each item and report ✅ or ❌ with a fix if needed:

### 3.1 Text Completeness
- [ ] Every node has a visible, descriptive label — no blank or truncated text.
- [ ] Arrow labels (if used) are present and meaningful.
- [ ] No placeholder text like "Node 1" or "Label" unless that is the actual content.
- [ ] All text accurately reflects the diagram's subject from the user's request.

### 3.2 Overlap Detection
- [ ] For each pair of nodes, verify: `|x1 - x2| >= (w1/2 + w2/2 + 40)` OR `|y1 - y2| >= (h1/2 + h2/2 + 60)`. Flag any violation.
- [ ] Arrow paths do not run through the interior of any node they are not connected to.
- [ ] Text labels do not extend outside their container node boundaries.
- [ ] No two text elements share the same `x,y` coordinates.

### 3.3 Node Structure Quality
- [ ] Every shape node has exactly one paired text/label element.
- [ ] `containerId` on each label matches the parent node's `id`.
- [ ] `boundElements` arrays are complete — no arrow is missing from a node's list.
- [ ] Node sizes are consistent within the same type (all rectangles same height, all ellipses same size).
- [ ] Color coding follows the defined convention (start=green, process=blue, decision=yellow, IO=orange).

### 3.4 Human Readability
- [ ] The flow has a clear single entry point and a clear exit point.
- [ ] Reading direction is consistent (top-to-bottom OR left-to-right, not mixed).
- [ ] Arrows do not cross each other unless absolutely unavoidable; if they do, add a note.
- [ ] The diagram fits within a ~1400×900 viewport — no element placed beyond x=1400 or y=900 without reason.
- [ ] A person unfamiliar with the subject can follow the diagram without needing extra explanation.
- [ ] Node labels use plain language — no jargon abbreviations without context.

---

## Phase 4 — Output Format

Provide your response in this exact order:

1. **Brief description** (1–2 sentences) of what the diagram shows.
2. **The complete Excalidraw JSON** inside a fenced ```json block.
3. **Review Report** — the Phase 3 checklist with ✅/❌ and any fixes applied.
4. **Usage instructions**: Tell the user to go to [excalidraw.com](https://excalidraw.com), click the hamburger menu → "Open" → paste the JSON, or use the "Load from JSON" option.
