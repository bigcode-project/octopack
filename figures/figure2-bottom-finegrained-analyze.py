import json
from collections import Counter
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy

from matplotlib import image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox


def setup_dpi(plt_obj, dpi=75, width=8, height=6):
    pgf_config = {
        "figure.dpi": dpi,
        "figure.figsize": [width, height],
    }
    plt_obj.rcParams.update(pgf_config)


def adjust_lightness(color, alpha=0.5):
    import matplotlib.colors as mc

    c = mc.to_rgba(color)
    return mc.to_rgba(c, alpha=alpha)


the_categories = [
    "Bug Fixes",
    "New Features",
    "Refactoring/Code Cleanup",
    "Documentation",
    "Testing",
    "User Interface",
    "Dependencies",
    "Configuration",
    "Build System/Tooling",
    "Performance Improvements",
    "Formatting/Linting",
    "Security",
    "Technical Debt Repayment",
    "Release Management",
    "Accessibility",
    "Deprecation",
    "Logging/Instrumentation",
    "Internationalization",
]

# Categorization data
nested_relations = {
    "Development": ["New Features", "User Interface"],
    "Testing & QA": ["Testing", "Logging/Instrumentation"],
    "Bug": ["Bug Fixes"],
    "Improvement": ["Refactoring/Code Cleanup", "Performance Improvements", "Formatting/Linting"],
    "Misc": [
        "Documentation",
        "Deprecation",
        "Dependencies",
        "Configuration",
        "Build System/Tooling",
        "Release Management",
    ],
}


idx2cat = {idx: cat for idx, cat in enumerate(the_categories)}
cat2idx = {cat: idx for idx, cat in idx2cat.items()}


def valid(e):
    _cats = [e.lower().strip() for e in the_categories]
    _e = e.lower().strip()

    if _e in _cats:
        return the_categories[_cats.index(_e)]
    else:
        return None


if __name__ == "__main__":
    setup_dpi(plt, 200, 20, 10)

    cls_file = Path("./misc/message_category.json")
    with cls_file.open("r") as f:
        cls_data = json.load(f)

    collected = []
    for item in cls_data:
        if "\n" in item["category"]:
            category_str, rest = item["category"].split("\n", 1)
        else:
            category_str = item["category"]

        cats = [e.strip() for e in category_str.split(",")]
        valid_cats = [valid(e) for e in cats]
        ok_cats = [e for e in valid_cats if e]

        if len(ok_cats) == 0:
            pass
        else:
            collected.append({"_id": item["_id"], "message": item["message"], "category": ok_cats})

    collected_cats = []
    for item in collected:
        cats = item["category"]
        collected_cats.append(cats[0])

    counter = Counter(collected_cats)

    cat2porp = {cat: f"{cnt/len(collected_cats)*100:.2f}%" for cat, cnt in counter.most_common()}

    inner_data = []
    outer_data = []

    for inner, outers in nested_relations.items():
        outer_cnt = 0
        outer_data_part = []
        for outer_cat in outers:
            cat_cnt = counter.get(outer_cat)
            outer_cnt += cat_cnt
            outer_data_part.append((outer_cat, cat_cnt))

        outer_data_part.sort(key=lambda e: e[1])

        mid = int(len(outer_data_part) / 2)
        rearange = outer_data_part[mid:] + outer_data_part[:mid][::-1]

        outer_data.extend(rearange)

        inner_data.append((inner, outer_cnt))

    print(inner_data)
    print(outer_data)

    raw_colors = ["#f5680a", "#a961ce", "#74c3f8", "#1bbd57", "#5479a6"]
    inner_colors = []
    outer_colors = []

    for (main_cat, sub_cats), main_color in zip(nested_relations.items(), raw_colors):
        len_sub = len(sub_cats)
        for i in range(len_sub):
            p = 0.3 + 0.7 * (i + 1) / len_sub
            sub_color = adjust_lightness(main_color, p)
            outer_colors.append(sub_color)

        inner_colors.append(adjust_lightness(main_color, 0.5))

    inner_label, inner_val = zip(*inner_data)
    outer_label, outer_val = zip(*outer_data)

    fig, ax = plt.subplots()

    startat = 50
    _, main_texts = ax.pie(
        inner_val,
        colors=inner_colors,
        radius=0.5,
        wedgeprops=dict(width=0.3, edgecolor="white", linewidth=2.5),
        labels=inner_label,
        labeldistance=0.9,
        startangle=startat,
    )
    for t in main_texts:
        t.set_horizontalalignment("center")
        t.set_fontweight("bold")
        t.set_fontsize(24)
        t.set_color("white")
        t.set_bbox(dict(facecolor="grey", alpha=0.7, edgecolor="white", boxstyle="round,pad=0.4", linewidth=3))

    wedges, texts = ax.pie(
        outer_val,
        colors=outer_colors,
        radius=0.8,
        wedgeprops=dict(width=0.3, edgecolor="white", linewidth=2.5),
        startangle=startat,
    )

    left_high, left_low, right_high, right_low = (None, None, None, None)
    margin = 0

    left_top, left_bottom = [], []
    right_top, right_bottom = [], []

    job_mapper = {
        "left": {True: left_top, False: left_bottom},
        "right": {True: right_top, False: right_bottom},
    }
    for i, p in enumerate(wedges):
        bbox_props = dict(fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"), zorder=0, va="center", fontsize=24)

        ang = (p.theta2 - p.theta1) / 2.0 + p.theta1
        y = np.sin(np.deg2rad(ang)) * 0.8
        x = np.cos(np.deg2rad(ang)) * 0.8
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})

        tx, ty = 1.2 * np.sign(x), 1.025 * y

        cat = outer_label[i]
        if horizontalalignment == "left":
            the_text = f"{cat} ({cat2porp[cat]})"
        else:
            the_text = f"({cat2porp[cat]}) {cat}"

        pack = dict(text=the_text, xy=(x, y), xytext=(tx, ty), horizontalalignment=horizontalalignment, weight="bold", **deepcopy(kw))

        job_mapper[horizontalalignment][ty >= 0].append(deepcopy(pack))

    def do_draw(series, up=True):
        sorted_s = sorted(series, key=lambda e: e["xytext"][1], reverse=not up)
        peak = -np.inf if up else np.inf
        raw_delta = 0.161
        delta = raw_delta if up else -1 * raw_delta
        cmp = np.greater_equal if up else np.less_equal

        for job in sorted_s:
            tx, ty = job["xytext"]
            if cmp(ty, peak + delta):
                peak = ty
            else:
                ty = peak + delta
                peak = ty
                job["xytext"] = (tx, ty)
            ax.annotate(**job)

    do_draw(job_mapper["left"][True], True)
    do_draw(job_mapper["right"][True], True)
    do_draw(job_mapper["left"][False], False)
    do_draw(job_mapper["right"][False], False)

    python_img = image.imread("./misc/python.png")
    python_logo = OffsetImage(python_img, zoom=0.13, filterrad=0.001, interpolation="gaussian")
    ab = AnnotationBbox(python_logo, (0, 0), frameon=False)
    ab.set_zorder(-1)
    ax.add_artist(ab)

    plt.tight_layout()
    plt.show()
    # plt.savefig(f"fine-grained-analyze.pdf")
