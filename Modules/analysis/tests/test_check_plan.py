"""Tests for the via handling in check_plan.py."""
import json, os, subprocess, sys
import check_plan as cp

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(os.path.dirname(HERE), "check_plan.py")
BOARD = os.path.join(HERE, "fixtures", "board_plan.kicad_pcb")

def test_via_default_diameter_is_0_6():
    assert cp.plan_vias({"vias": [["N2", 6, 5]]}) == [{'x': 6, 'y': 5, 'd': 0.6, 'net': "N2"}]

def test_via_entry_diameter_overrides():
    assert cp.plan_vias({"vias": [["N2", 6, 5, 0.45]]})[0]['d'] == 0.45

def test_plan_level_via_diameter():
    v = cp.plan_vias({"via_diameter": 0.8, "vias": [["N2", 6, 5], ["N3", 7, 5, 0.3]]})
    assert [x['d'] for x in v] == [0.8, 0.3]

def run(tmp_path, plan):
    p = tmp_path / "plan.json"
    p.write_text(json.dumps(plan))
    return subprocess.run([sys.executable, SCRIPT, BOARD, str(p), "0.25"],
                          capture_output=True, text=True, check=True).stdout

def test_cli_uses_via_diameter(tmp_path):
    # pad N1 is 1x1 at (5,5); a via at (6,5) is 0.5 from the pad edge
    assert "gap     0.2 " in run(tmp_path, {"vias": [["N2", 6, 5]]})
    assert "gap     0.1 " in run(tmp_path, {"vias": [["N2", 6, 5, 0.8]]})
    assert "No violation" in run(tmp_path, {"vias": [["N2", 6, 5, 0.4]]})
