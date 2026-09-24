"""Tests for check_courtyards.py against the synthetic boards in fixtures/."""
import json, os, subprocess, sys
import pytest
import check_courtyards as cc

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
SCRIPT = os.path.join(os.path.dirname(HERE), "check_courtyards.py")
BASIC = os.path.join(FIX, "board_basic.kicad_pcb")
NO_EDGE = os.path.join(FIX, "board_no_edge.kicad_pcb")
ENV = {"PLUM_SOLUTIONS": os.path.join(FIX, "Plum"), "KICAD10_FOOTPRINT_DIR": "/stock"}
GLOBAL = os.path.join(FIX, "global-fp-lib-table")

def boxes_of(path):
    libs = cc.lib_table(path, global_table=GLOBAL, env=ENV)
    boxes, _ = cc.footprint_boxes(open(path).read(), libs)
    return boxes

def test_bounds_from_edge_cuts():
    # gr_rect 10,20..40,30 plus a gr_line out to 45,25; the F.SilkS line is ignored
    assert cc.board_bounds(open(BASIC).read()) == (10, 20, 45, 30)

def test_no_edge_cuts_gives_no_bounds():
    assert cc.board_bounds(open(NO_EDGE).read()) is None

def test_embedded_courtyard_ignores_silk():
    assert boxes_of(BASIC)["R1"] == pytest.approx((13.5, 24.25, 16.5, 25.75))

def test_rotation_and_circle_and_back_side():
    b = boxes_of(BASIC)
    assert b["R4"] == pytest.approx((24.25, 23.5, 25.75, 26.5))
    assert b["TP1"] == pytest.approx((34, 27, 36, 29))
    assert b["B1"] == pytest.approx((34, 21.5, 36, 22.5))

def test_overlap_and_tight_gap():
    bad, tight = cc.compare(boxes_of(BASIC), 0.05)
    assert bad == [("R1", "R2", 0.5, 1.5)]
    assert tight == [("R4", "R5", 0.02)]

def test_off_board():
    b = boxes_of(BASIC)
    assert [r for r, _ in cc.off_board(b, cc.board_bounds(open(BASIC).read()))] == ["R3"]

def test_library_fallback_through_project_table():
    b = boxes_of(NO_EDGE)
    assert b["U1"] == pytest.approx((48, 49, 52, 51))
    assert cc.compare(b, 0.05)[0] == [("R1", "U1", 0.5, 1.0)]

def test_lib_table_expansion_and_precedence():
    libs = cc.lib_table(BASIC, global_table=GLOBAL, env=ENV)
    # nested "Table" row, ${KICAD10_FOOTPRINT_DIR}
    assert libs["Resistor_SMD"] == "/stock/Resistor_SMD.pretty"
    # ${PLUM_SOLUTIONS}; the global row wins over the project row of the same name
    assert libs["PlumLib"] == os.path.join(FIX, "Plum", "Footprints", "PlumLib.pretty")
    # ${KIPRJMOD} is the board's directory
    assert libs["TestLib"] == os.path.join(FIX, "libraries", "TestLib.pretty")

def test_kicad_env_reads_common_json_and_falls_back(tmp_path):
    p = tmp_path / "kicad_common.json"
    p.write_text(json.dumps({"environment": {"vars": {"PLUM_SOLUTIONS": "/plum"}}}))
    env = cc.kicad_env(str(p))
    assert env["PLUM_SOLUTIONS"] == "/plum"
    assert env["KICAD10_FOOTPRINT_DIR"] == cc.DEFAULT_ENV["KICAD10_FOOTPRINT_DIR"]
    assert cc.kicad_env(str(tmp_path / "missing.json"))["PLUM_SOLUTIONS"] == cc.DEFAULT_ENV["PLUM_SOLUTIONS"]

def run(path, *extra):
    return subprocess.run([sys.executable, SCRIPT, path, *extra], capture_output=True, text=True, check=True).stdout

def test_cli_output_format():
    out = run(BASIC)
    assert out.splitlines()[0] == "7 footprints"
    assert "overlaps: [('R1', 'R2', 0.5, 1.5)]" in out
    assert "gaps under 0.05: [('R4', 'R5', 0.02)]" in out
    assert "off board: [('R3'" in out
    assert "gaps under 0.01: NONE" in run(BASIC, "0.01")

def test_cli_without_edge_cuts_skips_off_board():
    out = subprocess.run([sys.executable, SCRIPT, NO_EDGE], capture_output=True, text=True).stdout
    assert "no Edge.Cuts" in out
    assert "off board:" not in out

def test_library_footprint_in_hand_written_format():
    # two-space indent, one item per line, as the footprints on the Plum volume are written
    cc.cache.clear()
    libs = cc.lib_table(BASIC, global_table=GLOBAL, env=ENV)
    pts = cc.lib_points("PlumLib:Chip", libs)
    assert (min(p[0] for p in pts), max(p[1] for p in pts)) == (-3.075, 1.5)
