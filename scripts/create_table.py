from siuba import *
import pandas as pd

import sys

IN_FILE = sys.argv[1]
N_CATEGORIES = 6

cols = ["explore",  "wrangle", "program", "model", "communicate", "workflow", "", "", "notes"]


df = pd.read_csv("curriculum.csv")

anchors = (df
  >> mutate(
      title = '<a class="' + _.category + '">' + _.title + "</a>",
      id = _.index
      )
)


week_min_ids = anchors >> group_by(_.week) >> summarize(id = _.id.min(), n_rows = _.shape[0])


notes = (
  pd.DataFrame({
      "week": [1],
      "category": ["notes"],
      "note": ["""This material is taught in the <a href="https://learn.siuba.org">intro to siuba course</a>."""]
  })
  >> inner_join(_, week_min_ids, on = "week")
  >> transmute(
      _.id,
      td_note = '<td class="note" rowspan="' + _.n_rows.astype(str) + '">' + _["note"] + "</td>"
      )
)


units = (anchors
  >> filter(_.category != "project")
  #>> complete("id", "category")
  >> mutate(
      title = _.title.fillna(""),
      col_num = _.category.apply(cols.index)
      )
  >> arrange(_.id, _.col_num)
  >> left_join(_, notes, "id")
  >> mutate(
      blank_cell = "<td></td>",            # necessary to mult string and int series :/
      td_left = _.blank_cell * _.col_num,
      td_right = _.blank_cell * (N_CATEGORIES - _.col_num - 1),
      td_link = '<td class="syl-unit" colspan="3">' + _["title"] + "</td>",
      td_week = '<td class="syl-week">' + _["week"].astype(int).astype(str) + "</td>",
      td_note = _.td_note.fillna(""),
      tds = _.td_week + _.td_left + _.td_link + _.td_right +  _.td_note,
      )
  >> mutate(
      tr = '<tr>' + _.tds + "</tr>"
      )
)


projects = (anchors
  >> filter(_.category == "project")
  >> mutate(
      td_week = '<td class="syl-week">' + _["week"].astype(int).astype(str) + "</td>",
      td_link = '<td class="syl-unit project" colspan="%s">'%(len(cols)-1) + _["title"] + "</td>",
      )
  >> transmute(
      _.id, _.week,
      tr = '<tr>' + _.td_week + _.td_link + "</tr>"
      )
)


links = (
  pd.concat([units, projects], ignore_index = True)
  >> arrange(_.id)
  >> group_by(_.week)
  >> summarize(tbody = "<tbody>" + _.tr.str.cat(sep = "") + "</tbody>")
)


header = "".join(["<th>%s</th>" %x for x in [""] + cols])

content = "\n".join([
    "<table>",
    "<thead><tr>", header, "</tr></thead>",
    links.tbody.str.cat(sep = "\n"),
    "</table>"
    ])  

from utils import load_template
from pathlib import Path

template = load_template()

out_dir = Path("_website/curriculum")
out_dir.mkdir(exist_ok = True)

(out_dir / "index.html").write_text(template.substitute(content = content))
